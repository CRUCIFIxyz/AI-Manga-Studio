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
    """构建DeepSeek System Prompt——核心剧本生成指令。

    v2.0 优化：
    - 中文指令（输出中文内容时用中文写指令更精准）
    - 模板式输出（固定格式填空，确保结构化）
    - 模块间强制交叉引用（角色名→分镜→提示词链式引用）
    - 即梦/Pika/Kling分平台AI提示词格式
    - 参考图生成建议（即梦工作流适配）
    - 合规+原创性+AI标识约束
    """
    art_styles = {
        "ghibli": {
            "name_cn": "吉卜力风格",
            "desc_en": "Studio Ghibli style, soft watercolor texture, warm nostalgic lighting, hand-drawn feel, gentle color palette, dreamy atmosphere",
            "desc_cn": "吉卜力动画风格，柔和水彩质感，温暖怀旧光线，手绘感，治愈色调",
            "negative": "photorealistic, 3D render, harsh shadows, dark, scary",
        },
        "shinkai": {
            "name_cn": "新海诚风格",
            "desc_en": "Makoto Shinkai style, photorealistic lighting, vibrant skies, detailed urban and natural backgrounds, lens flare, rich color grading, cinematic composition",
            "desc_cn": "新海诚风格，照片级真实光影，绚丽天空，精细背景，镜头光晕，电影级调色",
            "negative": "cartoon, flat colors, simple shapes, low detail",
        },
        "cyberpunk": {
            "name_cn": "赛博朋克风格",
            "desc_en": "Cyberpunk style, neon lights in purple and cyan, dark rainy cityscapes, holographic UIs, chrome and steel surfaces, volumetric fog, cinematic noir lighting",
            "desc_cn": "赛博朋克风格，紫青霓虹灯，暗黑雨城，全息UI，金属质感，体积雾，黑色电影打光",
            "negative": "bright daylight, natural landscape, rural, vintage, pastel colors",
        },
        "guofeng": {
            "name_cn": "国风古韵",
            "desc_en": "Chinese ink wash painting style (国风), flowing brushstrokes, ethereal mist, muted earth tones, classic elegance, silk textures, inspired by ancient Chinese art and cinema",
            "desc_cn": "中国水墨古风，流动笔触，缥缈云雾，雅致大地色，丝绸质感，古典意境",
            "negative": "western style, neon, futuristic, cyber, modern architecture",
        },
    }
    art = art_styles.get(art_style, art_styles["ghibli"])

    return f"""你是一位专业的AI短剧剧本编剧，专精于「{genre_cn}」题材。

你的任务：根据用户提供的创意想法，生成一套完整的 AI 短剧制作包——共 {episode_count} 集，每集 1-1.5 分钟。

【核心要求】
1. 你的输出将直接用于即梦、Pika、PixVerse、Kling（可灵）等 AI 视频工具
2. 因此内容必须高度结构化、分镜化、"拿来即用"
3. 所有模块之间必须保持一致性——角色名、外貌描述、场景名在各模块中不变

【画风设定】
本次创作的统一画风为：{art['name_cn']}
视觉描述参考：{art['desc_cn']}
所有场景和角色描述都应遵循此画风的视觉特征。

---

请严格按照以下六大模块输出，用 `## 0X 模块名` 作为标题分隔：

## 01 剧本大纲

### 世界观
（2-3句话，交代故事发生的世界背景、核心规则）

### 故事梗概
（4-6句话，完整故事线，从开端到高潮到结局）

### 分集大纲
{chr(10).join(f"**第{n}集**：（3-5句话，本集核心情节 + 结尾钩子"+"「...」"+"）" for n in range(1, episode_count+1))}

## 02 角色设定

为每个主要角色（至少2个）提供以下信息。角色外貌描述必须可直接用于AI生图。

### 角色一：[角色名]
- **姓名**：（中文名）
- **年龄**：（数字）
- **外貌**：（4-5句话，仿照AI生图prompt的写法——发型/发色/瞳色/脸型/身高体型）
- **服装**：（2-3句话，颜色、材质、标志性配饰）
- **性格**：（2-3个关键词 + 1句话说明）
- **标志动作**：（角色独有的招牌动作或习惯）
- **参考图提示词**：（一段英文，可直接用于Midjourney/即梦生成角色立绘）

### 角色二：[角色名]
（同上格式）

（如有配角，继续添加）

## 03 场景描述

列出 6-8 个关键场景。每个场景需要有"画面感"——像一幅画的文字描述。

### 场景一：[场景名]
- **时间**：（晨/午/黄昏/夜）
- **地点**：（具体位置）
- **画面描述**：（4-5句话，高画面感——光线、色彩、材质、空间布局、天气）
- **氛围**：（1-2个词）
- **参考图提示词**：（一段英文，可直接用于即梦生成场景图）

（继续列出其他场景）

## 04 分集台词

逐集写出完整台词。格式：场景标题 + 角色名：台词（动作描写）。

{chr(10).join(f"### 第{n}集：{{{{请为本集命名}}}}" + chr(10) + "（本集时长约1-1.5分钟，台词控制在300-500字）" + chr(10) + chr(10) + "【场景：XXX】" + chr(10) + "角色名：（动作描写）台词内容" + chr(10) + "..." + chr(10) + chr(10) + "【本集钩子】" + chr(10) + "（结尾2-3句话，制造悬念，引导观众看下一集）" for n in range(1, episode_count+1))}

## 05 分镜脚本

逐集逐镜写出分镜表。每集 5-8 个镜头。**必须引用模块02中的角色名。**

{chr(10).join(f"### 第{n}集分镜" + chr(10) + chr(10) + "| 镜号 | 景别 | 画面描述 | 运镜 | 时长 | 转场 |" + chr(10) + "|------|------|---------|------|------|------|" + chr(10) + "| S{n}01 | （全景/中景/近景/特写） | （画面内容——角色[引用02中的角色名]在做什么） | （推/拉/摇/移/跟/静止） | Xs | （切/淡入淡出/叠化） |" + chr(10) + "| S{n}02 | ... | ... | ... | Xs | ... |" + chr(10) + "（继续至S{n}05~S{n}08）" for n in range(1, episode_count+1))}

## 06 AI生成提示词

这是最关键模块——提供直接可复制到各大AI工具中的英文prompt。
请分三种平台格式输出，各选最重要的3-5个镜头：

### 即梦 / Flux / Midjourney（文生图 / 图生图）
格式：`[画风], [角色描述——引用02中的角色外貌], [动作], [场景描述——引用03中的场景], [光线], [画质标签] --ar 16:9 --style {art_style}`

负面提示词模板：`{art['negative']}`

请输出至少5个关键镜头的提示词，标注对应分镜号：

**Shot S101**（对应分镜S101）：
```
（英文prompt）
```

（继续 S102, S201, S302...）

### Pika / PixVerse（图生视频 / 文生视频）
格式：`[角色描述], [动作描述 + 运镜方向], [场景描述], [画风]`

特别要求：加入 **motion prompt**——明确描述画面中的运动（如 "camera slowly pans right, character walks forward, hair blowing in wind"）

请输出至少3个关键镜头的提示词：

（同上格式）

### Kling / 可灵 / Hailuo（图生视频，可选首尾帧）
格式：`[首帧描述] → [尾帧描述]，动作发生在首尾之间：[动作描述]，风格：[画风]`

请输出至少3个关键镜头的提示词：

（同上格式）

---

【硬性约束——必须遵守】
1. 模块01-05全部用**中文**撰写，模块06全部用**英文**撰写
2. 模块02中的角色名、外貌关键词，必须在模块05和06中**原样引用**——不允许换词
3. 模块03中的场景名，必须在模块05和06中**原样引用**
4. 每集结尾必须有一个明确的悬念钩子（用「」标注或【本集钩子】标注）
5. 所有内容必须完全原创——不得引用任何现有动漫/小说/影视IP的角色名、地名、剧情
6. 故事结尾（最后一集）应自然收束，但不排除续集可能
7. 台词应口语化、自然、符合角色性格——不要写书面语或旁白腔
8. 模板中的 `{{{{...}}}}` 标记表示需要你填入实际内容——不要输出 `{{{{...}}}}` 本身

直接输出markdown，六大模块之外不要写任何解释或寒暄。"""


def build_user_prompt(user_idea: str, genre_cn: str, episode_count: int, art_style_cn: str) -> str:
    """构建User Prompt——用户的具体创意输入。

    v2.0 优化：中文撰写（与System Prompt语言一致），携带完整上下文。
    """
    return f"""请根据以下用户创意，生成完整的 AI 短剧制作包。

【用户创意】
{user_idea}

【创作参数】
- 题材类型：{genre_cn}
- 总集数：{episode_count} 集（每集1-1.5分钟）
- 画风：{art_style_cn}

请严格按照系统指令中规定的六大模块格式输出。确保故事引人入胜、角色鲜明立体、AI提示词即拿即用。"""


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
        "temperature": 0.7,
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

    # 画风中文名映射（用于User Prompt上下文）
    art_style_names_cn = {
        "ghibli": "吉卜力风格",
        "shinkai": "新海诚风格",
        "cyberpunk": "赛博朋克风格",
        "guofeng": "国风古韵",
    }
    art_style_cn = art_style_names_cn.get(art_style, "吉卜力风格")

    try:
        # 构建Prompt
        system_prompt = build_system_prompt(genre_cn, episode_count, art_style)
        user_prompt = build_user_prompt(user_idea, genre_cn, episode_count, art_style_cn)

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
