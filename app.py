"""
AI漫剧剧本生成器 MVP - Flask后端
路径：D:\作业\全球数字创业\任务pt.2\mvp\app.py
功能：接收用户输入 → 调用DeepSeek API → 生成6模块剧本 → 保存Markdown → 返回结果
"""

import os
import re
import json
import time
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import requests

# 加载环境变量
load_dotenv()

app = Flask(__name__)

# 配置
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "输出剧本"
OUTPUT_DIR.mkdir(exist_ok=True)

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_BASE = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com/v1")

if not DEEPSEEK_API_KEY:
    raise RuntimeError("DEEPSEEK_API_KEY not found in .env file")

# 主题类型
GENRE_MAP = {
    "campus_fantasy": "校园奇幻",
    "urban_revenge": "都市逆袭",
    "xianxia": "古风仙侠",
    "sci_fi": "科幻末世",
    "mystery": "悬疑推理",
    "romance": "甜宠现言",
}


def build_system_prompt(genre_cn: str, episode_count: int, art_style: str) -> str:
    """构建DeepSeek System Prompt——核心剧本生成指令。"""
    art_styles = {
        "ghibli": "Studio Ghibli style, soft watercolor, warm nostalgic lighting, hand-drawn feel",
        "shinkai": "Makoto Shinkai style, photorealistic lighting, vibrant skies, detailed backgrounds, lens flare",
        "cyberpunk": "Cyberpunk style, neon lights, dark cityscapes, holographic UIs, rain-slicked streets",
        "guofeng": "Chinese ink wash style (国风), flowing brushstrokes, ethereal mist, muted earth tones, classic elegance",
    }
    art_desc = art_styles.get(art_style, art_styles["ghibli"])

    return f"""You are a professional AI short drama scriptwriter specializing in {genre_cn} (Chinese short drama genre).

Generate a COMPLETE production package for a {episode_count}-episode AI short drama. Each episode should be 1-1.5 minutes long.
The script MUST be directly usable with AI video tools like Jimeng (即梦), Pika, PixVerse, Kling (可灵), and Hailuo (海螺).

Output the following SIX modules in markdown format. Use `##` for module titles and `###` for sub-sections.

## 01 Script Outline / 剧本大纲
- World setting (2-3 sentences)
- Story synopsis (4-6 sentences)
- Episode-by-episode outline, each with a cliffhanger "hook" at the end
- Each episode outline: 3-5 sentences covering the key plot point

## 02 Character Profiles / 角色设定
For each main character (at least 2), provide:
- Name / Age / Appearance / Outfit / Personality / Signature gesture
- Add a visual reference description suitable for AI image generation
- Format example: "A cheerful girl with short blue hair, wearing a white school uniform with navy trim, bright amber eyes, always carries a vintage camera"

## 03 Scene Descriptions / 场景描述
List 5-8 key scenes. For each scene:
- Scene name + Time of day + Location
- Visual description (3-5 sentences, highly visual, like a painting description)
- Atmosphere / Mood
- Format example: "Rainy classroom at dusk — desks arranged neatly, raindrops streak down tall windows, the golden hour light pierces through storm clouds casting long shadows, a single open notebook on the teacher's desk, chalk dust floating in the air"

## 04 Episode Scripts / 分集台词
For each episode, provide:
- Episode title
- Scene heading
- Character dialogue with (action descriptions in parentheses)
- Keep each episode to 300-500 words of dialogue
- End each episode with a hook line

## 05 Storyboard / 分镜脚本
For each episode, provide a shot-by-shot storyboard (5-8 shots per episode):
- Shot number / Shot type (Wide/Medium/Close-up/Extreme Close-up)
- Visual description of what the camera sees
- Camera movement (Pan/Tilt/Dolly/Zoom/Static)
- Duration in seconds
- Transition to next shot
- Format example: "Shot 01 | Wide | Classroom interior, morning light streaming in | Slow pan right | 8s | Dissolve to Shot 02"

## 06 AI Generation Prompts / AI提示词
For each key shot from the storyboard, provide English prompts ready to copy-paste into Jimeng (即梦), Pika, PixVerse, Flux, or Midjourney.

Each prompt must follow this format:
"Anime style, {{art_desc}}, {{character description}}, {{action}}, {{scene description}}, {{lighting}}, {{quality tags}} --ar 16:9"

Provide at least 8 prompts covering the most visually important shots. Label each prompt with the shot number it corresponds to.

IMPORTANT RULES:
- Write the ENTIRE script in CHINESE for modules 01-05
- Module 06 (AI Generation Prompts) MUST be in ENGLISH
- Keep the tone appropriate for the genre: {genre_cn}
- Each episode must end with a hook/suspense moment
- All content must be original — do not reference existing IPs or copyrighted works
- The art style for visual descriptions should follow: {art_desc}

Output directly in markdown. Do not include any meta-commentary or explanations outside the six modules."""


def build_user_prompt(user_idea: str, genre_cn: str, episode_count: int) -> str:
    """构建User Prompt——用户的具体创意输入。"""
    return f"""Please generate a complete AI short drama script package based on the following user input:

GENRE: {genre_cn}
EPISODES: {episode_count} (1-1.5 minutes each)
USER'S CREATIVE IDEA: {user_idea}

Generate all six modules as specified in the system prompt. Make sure the story is engaging, the characters are distinct, and the AI prompts in Module 06 are production-ready."""


def call_deepseek_api(system_prompt: str, user_prompt: str) -> str:
    """调用DeepSeek Chat API，返回生成的文本内容。"""
    url = f"{DEEPSEEK_API_BASE}/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.8,
        "max_tokens": 8192,
        "stream": False,
    }

    response = requests.post(url, headers=headers, json=payload, timeout=180)
    response.raise_for_status()

    data = response.json()
    content = data["choices"][0]["message"]["content"]
    return content


def parse_modules(content: str) -> dict:
    """将DeepSeek返回的markdown文本按6个模块拆分。

    返回 dict: { "01_剧本大纲": "...", "02_角色设定": "...", ... }
    使用正则按 '## 0X' 标题拆分，兼容中英文模块标题。
    """
    modules = {}
    pattern = r"##\s*(0\d)\s*[^#\n]+"
    splits = re.split(pattern, content)

    # splits[0] 是第一个 ## 之前的内容（可忽略）
    for i in range(1, len(splits), 2):
        if i + 1 < len(splits):
            num = splits[i].strip()
            text = splits[i + 1].strip()

            # 根据编号映射文件名
            module_names = {
                "01": "01_剧本大纲",
                "02": "02_角色设定",
                "03": "03_场景描述",
                "04": "04_分集台词",
                "05": "05_分镜脚本",
                "06": "06_AI提示词",
            }
            key = module_names.get(num)
            if key:
                modules[key] = text

    return modules


def save_modules(modules: dict, folder_name: str) -> str:
    """将各个模块保存为独立的Markdown文件。

    参数:
        modules: {filename_stem: content} 字典
        folder_name: 剧本文件夹名

    返回: 保存路径
    """
    folder_path = OUTPUT_DIR / folder_name
    folder_path.mkdir(parents=True, exist_ok=True)

    saved_files = []
    for filename, content in modules.items():
        filepath = folder_path / f"{filename}.md"
        # 添加模块标题（因为拆分时去掉了标题）
        full_content = f"# {filename.replace('_', ' ').replace('01', '①').replace('02', '②').replace('03', '③').replace('04', '④').replace('05', '⑤').replace('06', '⑥')}\n\n{content}"
        filepath.write_text(full_content, encoding="utf-8")
        saved_files.append(str(filepath.relative_to(BASE_DIR)))

    return str(folder_path)


# 路由

@app.route("/")
def index():
    """首页——展示剧本生成表单。"""
    return render_template("index.html", genres=GENRE_MAP)


@app.route("/generate", methods=["POST"])
def generate():
    """接收用户输入，调用AI生成剧本，保存并返回结果。"""
    data = request.get_json()

    genre_key = data.get("genre", "campus_fantasy")
    user_idea = data.get("idea", "").strip()
    episode_count = int(data.get("episodes", 5))
    art_style = data.get("art_style", "ghibli")

    # 参数校验
    if not user_idea:
        return jsonify({"error": "创意描述不能为空"}), 400
    if genre_key not in GENRE_MAP:
        return jsonify({"error": f"无效的主题类型: {genre_key}"}), 400
    if episode_count < 1 or episode_count > 10:
        return jsonify({"error": "集数必须在1-10之间"}), 400

    genre_cn = GENRE_MAP[genre_key]

    try:
        # 构建Prompt
        system_prompt = build_system_prompt(genre_cn, episode_count, art_style)
        user_prompt = build_user_prompt(user_idea, genre_cn, episode_count)

        # 调用DeepSeek API
        content = call_deepseek_api(system_prompt, user_prompt)

        # 拆分模块
        modules = parse_modules(content)

        if len(modules) < 4:
            # 如果正则拆分不理想，回退——将整个content作为"完整剧本"
            # 同时尝试按常见分隔符手动拆
            # 回退策略：至少保证大纲和人设能拆出来
            fallback_modules = {}
            # 按常见的分隔拆分
            markers = [
                ("剧本大纲", "01_剧本大纲"),
                ("角色设定", "02_角色设定"),
                ("场景描述", "03_场景描述"),
                ("分集台词", "04_分集台词"),
                ("分镜脚本", "05_分镜脚本"),
                ("AI提示词", "06_AI提示词"),
            ]
            for marker, key in markers:
                idx = content.find(marker)
                if idx > 0:
                    # 从该marker开始，到下一个marker或结尾
                    start = idx
                    # 找下一个marker
                    end = len(content)
                    for m2, _ in markers:
                        i2 = content.find(m2, start + len(marker))
                        if 0 < i2 < end:
                            end = i2
                    fallback_modules[key] = content[start:end].strip()
            modules = fallback_modules if fallback_modules else {"00_完整剧本": content}

        # 生成文件夹名：主题_创意关键词_时间戳
        keyword = user_idea[:20].replace(" ", "_").replace("/", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_name = f"{genre_cn}_{keyword}_{timestamp}"

        # 保存文件
        save_path = save_modules(modules, folder_name)

        # 返回结果
        result = {
            "success": True,
            "folder": folder_name,
            "path": save_path,
            "modules": {},
        }
        # 按顺序返回模块内容
        ordered_keys = [
            "01_剧本大纲", "02_角色设定", "03_场景描述",
            "04_分集台词", "05_分镜脚本", "06_AI提示词"
        ]
        for key in ordered_keys:
            if key in modules:
                result["modules"][key] = modules[key]
        for key in modules:
            if key not in result["modules"]:
                result["modules"][key] = modules[key]

        return jsonify(result)

    except requests.exceptions.Timeout:
        return jsonify({"error": "AI服务响应超时，请稍后重试"}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"API调用失败: {str(e)}"}), 502
    except Exception as e:
        return jsonify({"error": f"服务器内部错误: {str(e)}"}), 500


@app.route("/list")
def list_scripts():
    """列出已生成的剧本文件夹。"""
    folders = []
    if OUTPUT_DIR.exists():
        for f in sorted(OUTPUT_DIR.iterdir(), reverse=True):
            if f.is_dir():
                files = [sf.name for sf in f.iterdir() if sf.is_file()]
                folders.append({
                    "name": f.name,
                    "files": files,
                    "count": len(files),
                })
    return jsonify(folders)


if __name__ == "__main__":
    print("=" * 60)
    print("  AI漫剧剧本生成器 MVP")
    print(f"  API Base: {DEEPSEEK_API_BASE}")
    print(f"  Output:   {OUTPUT_DIR}")
    print(f"  URL:      http://127.0.0.1:5000")
    print("=" * 60)
    app.run(debug=True, host="127.0.0.1", port=5000)
