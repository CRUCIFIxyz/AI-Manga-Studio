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

# Harness引擎
from harness_engine import run_pipeline

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


def build_system_prompt(
    genre_cn: str, episode_count: int, art_style: str,
    img_platform: str, vid_platform: str,
) -> str:
    """构建DeepSeek System Prompt——核心剧本生成指令。

    v3.2 优化：
    - 单选平台——只有一个图像平台+一个视频平台
    - 强力约束：ALL prompts必须严格适配选中平台格式
    """
    art_styles = {
        "ghibli": {
            "name_cn": "吉卜力",
            "desc": "Studio Ghibli style, soft watercolor texture, warm nostalgic lighting, hand-drawn feel, gentle colors, dreamy atmosphere",
            "negative": "photorealistic, 3D render, harsh shadows, dark, scary, low quality",
        },
        "shinkai": {
            "name_cn": "新海诚",
            "desc": "Makoto Shinkai style, photorealistic lighting, vibrant skies, detailed backgrounds, lens flare, cinematic color grading",
            "negative": "cartoon, flat colors, simple shapes, low detail, blurry",
        },
        "cyberpunk": {
            "name_cn": "赛博朋克",
            "desc": "Cyberpunk style, neon purple and cyan lights, dark rainy cityscapes, holographic UIs, chrome surfaces, volumetric fog, noir lighting",
            "negative": "bright daylight, natural landscape, rural, vintage, pastel, low contrast",
        },
        "guofeng": {
            "name_cn": "国风古韵",
            "desc": "Chinese ink wash painting (国风), flowing brushstrokes, ethereal mist, muted earth tones, classic elegance, silk textures",
            "negative": "western style, neon, futuristic, cyber, modern architecture, 3D render",
        },
        "anime": {
            "name_cn": "日系二次元",
            "desc": "Japanese anime style, clean cel-shading, vibrant saturated colors, large expressive eyes, dynamic poses, speed lines, screen tones, 2D animation aesthetic",
            "negative": "realistic, 3D, photograph, blurry, western cartoon style, low saturation",
        },
        "webtoon": {
            "name_cn": "韩系漫画",
            "desc": "Korean webtoon/manhwa style, tall slender proportions, soft gradient coloring, glossy hair, fashionable outfits, romantic atmosphere, digital painting finish",
            "negative": "chibi, cartoon, 3D, rough sketch, traditional media, low detail",
        },
        "disney": {
            "name_cn": "美式卡通",
            "desc": "Disney/Pixar 3D animation style, exaggerated expressions, smooth rounded forms, vibrant colors, squash-and-stretch motion, family-friendly appeal, high-quality CG render",
            "negative": "anime, flat 2D, realistic, horror, gritty, dark shadows, cel-shading",
        },
        "cinematic": {
            "name_cn": "写实电影感",
            "desc": "Cinematic realism, photorealistic textures, dramatic lighting with strong shadows, film grain, anamorphic lens flares, shallow depth of field, Hollywood blockbuster look",
            "negative": "cartoon, anime, flat, low poly, low quality, oversaturated, painting",
        },
        "pixel": {
            "name_cn": "像素复古",
            "desc": "Pixel art game style, crisp defined pixels, limited color palette, retro 8-bit/16-bit aesthetic, dithering, nostalgic video game feel, chunky character sprites",
            "negative": "smooth, realistic, photorealistic, high resolution, blurry, gradient, vector",
        },
        "picturebook": {
            "name_cn": "治愈绘本",
            "desc": "Children's picture book illustration style, soft pastel colors, gentle rounded shapes, cozy warm lighting, storybook charm, crayon or watercolor texture, whimsical details",
            "negative": "dark, scary, realistic, sharp angles, neon, cyberpunk, photorealistic, harsh shadows",
        },
    }
    art = art_styles.get(art_style, art_styles["ghibli"])

    # 预计算（避免f-string内嵌表达式含反斜杠）
    nl = chr(10)
    ep_outlines = nl.join(
        f"**Episode {n}** (3-5 sentences summarizing key plot + end with a suspense hook marked [HOOK]: ...)"
        for n in range(1, episode_count + 1)
    )
    ep_scripts = nl.join(
        f"### Episode {n}: [NAME THIS EPISODE]"
        + nl + "(~1-1.5 min, ~300-500 words of dialogue)"
        + nl + "[SCENE: XXX]"
        + nl + "Character Name: (action) dialogue text"
        + nl + "..."
        + nl + "**END HOOK** (at least 2 suspense lines)"
        for n in range(1, episode_count + 1)
    )
    ep_storyboards = nl.join(
        f"### Episode {n} Storyboard"
        + nl + nl
        + "| Shot | Type | Visual Description | Camera Move | Dur | Transition |"
        + nl
        + "|------|------|-------------------|-------------|-----|------------|"
        + nl
        + f"| S{n}01 | Wide/Medium/CU | [Character from 02] in [Scene from 03], doing [action] | Pan/Tilt/Dolly/Zoom/Static | Xs | Cut/Fade/Dissolve |"
        + nl
        + "| ... | ... | ... | ... | Xs | ... |"
        + nl
        + f"(continue S{n}05-S{n}08)"
        for n in range(1, episode_count + 1)
    )

    # 平台提示词格式定义（单选：各一个平台）
    platform_formats = _build_platform_formats(img_platform, vid_platform, art)

    return f"""You are a professional AI short drama scriptwriter specializing in "{genre_cn}" genre.

Generate a COMPLETE production package for a {episode_count}-episode AI short drama. Each episode: 1-1.5 minutes.
The output MUST be directly usable with AI image/video generation tools.

ART STYLE (apply to all visual descriptions):
{art['desc']}

===

OUTPUT THE FOLLOWING SIX MODULES. Use `## 0X Title` as section headers.

## 01 Script Outline

### World Setting
(2-3 sentences describing the story world and its core rules)

### Story Synopsis
(4-6 sentences covering the full arc: setup -> conflict -> climax -> resolution)

### Episode Outlines
{ep_outlines}

## 02 Character Profiles

For EACH main character (at least 2), provide:

### [Character Name]
- **Name**: (Chinese name)
- **Age**:
- **Appearance**: (4-5 sentences in AI-image-prompt style - hair/eyes/face/build/distinctive features - REUSE these exact keywords in Modules 05 and 06)
- **Outfit**: (2-3 sentences - colors, materials, signature accessories)
- **Personality**: (2-3 keywords + one-sentence description)
- **Signature Gesture**: (unique habit or mannerism)
- **Reference Image Prompt** - for Jimeng/Midjourney: (1 English sentence, ready to paste)

[Repeat for each character; add supporting characters as needed]

## 03 Scene Descriptions

List 6-8 key scenes. Each scene must read like a painting description.

### [Scene Name]
- **Time**: (morning/noon/dusk/night)
- **Location**: (specific place)
- **Visual Description**: (4-5 highly visual sentences - light, color, materials, space, weather)
- **Atmosphere**: (1-2 words)
- **Reference Image Prompt** - for Jimeng/Flux: (1 English sentence, ready to paste)

[Continue for all scenes]

## 04 Episode Scripts

Full dialogue for each episode. Format: scene heading + character: dialogue (action).

{ep_scripts}

## 05 Storyboard

Shot-by-shot table for each episode. 5-8 shots per episode.
**MUST reference character names from Module 02 and scene names from Module 03.**

{ep_storyboards}

## 06 AI Generation Prompts

This is the CRITICAL module. Generate platform-specific prompts ready to copy-paste.

{platform_formats}

===

HARD CONSTRAINTS - MUST FOLLOW:
1. Modules 01-05 in **Chinese**. Module 06 in **English**.
2. **Cross-reference consistency**: Character names and appearance keywords from Module 02 MUST appear verbatim in Modules 05 and 06. Scene names from Module 03 MUST appear verbatim in Modules 05 and 06.
3. **Consistency constraint**: The same character must have the same hair color, eye color, outfit, and build across ALL modules. Do not "re-describe" - copy the exact keywords.
4. **Hook density**: Every episode MUST end with at least 1 explicit suspense line (marked [HOOK] or [...]).
5. **Originality**: All content MUST be 100% original. Do NOT reference any existing anime/manga/novel/film IP - no character names, place names, or plot points from known works.
6. **Dialogue naturalness**: Spoken, colloquial, character-appropriate. No narration-style prose in dialogue.
7. Output markdown directly. No meta-commentary outside the six modules."""


def _build_platform_formats(img_platform: str, vid_platform: str, art: dict) -> str:
    """根据用户单选平台构建强力约束的提示词格式指令。

    仅生成选中平台的专属格式——ALL prompts必须严格遵循。
    """
    sections = []
    art_desc = art['desc']
    neg = art['negative']

    # 图像平台（单选）
    img_formats = {
        "jimeng": f"""### SELECTED IMAGE PLATFORM: Jimeng / Flux

**CRITICAL: ALL image prompts MUST follow this exact format. No exceptions.**

For EVERY key shot, output EXACTLY:
```
[Art style: {art_desc}], [Character description from Module 02], [Action], [Scene from Module 03], [Lighting], [Quality tags: 8K, highly detailed, masterpiece] --ar 16:9

Negative prompt: {neg}
```

Output at least 8 prompts, each labeled by shot number (S101, S102, ...).""",

        "midjourney": f"""### SELECTED IMAGE PLATFORM: Midjourney

**CRITICAL: ALL image prompts MUST follow this exact format. No exceptions.**

For EVERY key shot, output EXACTLY:
```
[Character from 02] in [Scene from 03], [Action], {art_desc}, [Lighting details] --ar 16:9 --style expressive --niji 6

--no {neg}
```

Output at least 8 prompts, each labeled by shot number.""",

        "happyhorse": f"""### SELECTED IMAGE PLATFORM: HappyHorse

**CRITICAL: ALL image prompts MUST follow this exact format. No exceptions.**

For EVERY key shot, output EXACTLY:
```
Scene: [Scene from 03]
Character: [Appearance from Module 02 -- copy exact keywords]
Action: [What the character is doing]
Style: {art_desc}
Mood: [Atmosphere keyword from Module 03]
Camera: [wide / medium / close-up]

Reference images to prepare: generate character sheet from Module 02 Reference Image Prompts first, then scene backgrounds from Module 03 Reference Image Prompts.
```

Output at least 8 prompts, each labeled by shot number.""",

        "stablediffusion": f"""### SELECTED IMAGE PLATFORM: Stable Diffusion

**CRITICAL: ALL image prompts MUST follow this exact format. No exceptions.**

For EVERY key shot, output EXACTLY:
```
({art_desc}), [Character from 02], [Action], [Scene from 03], [Lighting], masterpiece, best quality, 8K, highly detailed

Negative prompt: {neg}, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry
```

Output at least 8 prompts, each labeled by shot number.""",
    }

    if img_platform in img_formats:
        sections.append(img_formats[img_platform])

    # 视频平台（单选）
    vid_formats = {
        "jimeng_video": f"""### SELECTED VIDEO PLATFORM: Jimeng / 即梦 (Image-to-Video)

**CRITICAL: ALL video prompts MUST follow this exact format. No exceptions.**

Jimeng works by uploading reference images + defining motion. For EVERY shot, output EXACTLY:
```
Reference image: [Character reference from Module 02] + [Scene reference from Module 03]
Action: [Detailed motion description -- character walks, turns, gestures, objects move]
Camera: [Pan left / Pan right / Zoom in / Zoom out / Static]
Style: {art_desc}, cinematic lighting, smooth motion, 8K
Motion strength: [1-10, where 5=natural, 8=dynamic -- recommend 5-7]
Duration: 6 seconds
```

KEY RULES:
- Always reference specific images from Module 02/03 Reference Image Prompts
- Motion strength MUST be specified as a number
- Keep duration 4-8 seconds per shot
- Avoid extreme motion that causes visual distortion

Output at least 5 prompts labeled by shot number.""",

        "pika": f"""### SELECTED VIDEO PLATFORM: Pika / PixVerse

**CRITICAL: ALL video prompts MUST follow this exact format. No exceptions.**

Pika needs explicit motion direction. For EVERY shot, output EXACTLY:
```
[Character from 02], [Motion: describe EXACT camera movement AND character action -- e.g., "camera slowly pans right while character walks forward, hair blowing gently in breeze"], [Scene from 03], {art_desc}, cinematic lighting, 8K

Motion intensity: [low / medium / high]
Duration: 10 seconds
```

KEY RULES:
- Camera movement MUST be explicitly stated (pan/tilt/zoom/tracking/dolly)
- Character motion MUST be explicit (walks/runs/turns/gestures/reaches)
- Never use vague terms like "some movement" -- be precise
- Motion intensity MUST be set per shot

Output at least 5 prompts labeled by shot number.""",

        "kling": f"""### SELECTED VIDEO PLATFORM: Kling / 可灵

**CRITICAL: ALL video prompts MUST follow this exact format. No exceptions.**

Kling requires start/end frame descriptions. For EVERY shot, output EXACTLY:
```
START FRAME: [Character from 02] in [Scene from 03], [exact initial pose], {art_desc}
END FRAME: [Character from 02] in [Scene from 03], [exact final pose -- must differ from start], {art_desc}
ACTION DURING TRANSITION: [Precise description of what happens between frames]
Style: {art_desc}, cinematic, 8K
Duration: 5-8 seconds
```

KEY RULES:
- Start and end frames MUST describe different poses/positions
- The action between frames MUST be clearly described
- Every frame description must include the character and scene names

Output at least 5 prompts labeled by shot number.""",

        "hailuo": f"""### SELECTED VIDEO PLATFORM: Hailuo / 海螺

**CRITICAL: ALL video prompts MUST follow this exact format. No exceptions.**

For EVERY shot, output EXACTLY:
```
[Scene from 03] with [Character from 02], [Detailed action + motion], {art_desc}, smooth camera movement, film grain, cinematic color grade, 8K

Camera: [static / pan left / pan right / zoom in / zoom out / tracking shot]
Duration: 10 seconds
```

KEY RULES:
- Camera type MUST be explicitly chosen from the list above
- Motion must be described in concrete visual terms

Output at least 5 prompts labeled by shot number.""",

        "happyhorse_video": f"""### SELECTED VIDEO PLATFORM: HappyHorse (Video)

**CRITICAL: ALL video prompts MUST follow this exact format. No exceptions.**

HappyHorse composites elements with defined interactions. For EVERY shot, output EXACTLY:
```
Element 1 (Character): [Image reference from Module 02]
Element 2 (Background): [Image reference from Module 03]
Element 3+ (Props/FX): [Any additional elements]
Interaction: [How elements interact -- e.g., "character walks left-to-right across scene, fabric moves, background parallax scrolls slowly"]
Style: {art_desc}, cohesive lighting, 8K
Animation: [Full scene motion / Character only / Camera only / Parallax layers]
Duration: 8 seconds
```

KEY RULES:
- List ALL elements with their Module references
- Define which elements move and which are static
- HappyHorse excels at layered compositing -- use this strength

Output at least 5 prompts labeled by shot number.""",

        "runway": f"""### SELECTED VIDEO PLATFORM: Runway Gen-3

**CRITICAL: ALL video prompts MUST follow this exact format. No exceptions.**

Runway's Motion Brush allows per-region animation. For EVERY shot, output EXACTLY:
```
Base prompt: [Character from 02] in [Scene from 03], [Action], {art_desc}, cinematic lighting, film grain, 24fps

Motion Brush regions:
- Region 1 (head/face): [subtle micro-movements -- eye blink, hair sway]
- Region 2 (body/clothing): [natural movement -- breathing, fabric shift]
- Region 3 (background): [environmental motion -- clouds drift, leaves fall, light flicker]

Camera: [Static / Slow pan / Gentle zoom]
Style Preset: Cinematic
Duration: 5-8 seconds
```

KEY RULES:
- At least 3 Motion Brush regions per shot
- Each region must have a specific movement description
- Camera choice must match the scene mood

Output at least 5 prompts labeled by shot number.""",
    }

    if vid_platform in vid_formats:
        sections.append(vid_formats[vid_platform])

    if not sections:
        sections.append(f"""### Generic AI Prompts
```
[Art style: {art_desc}], [Character from 02], [Action], [Scene from 03], [Lighting], [Quality: 8K] --ar 16:9
Negative: {neg}
```
Output at least 8 prompts labeled by shot number.""")

    return "\n\n".join(sections)


def build_user_prompt(user_idea: str, genre_cn: str, episode_count: int) -> str:
    """构建User Prompt——用户的具体创意输入（v3.0：英文，携带上下文）。"""
    return f"""Generate a complete AI short drama script package based on the following:

CREATIVE IDEA: {user_idea}

PARAMETERS:
- Genre: {genre_cn}
- Episodes: {episode_count} (1-1.5 minutes each)

Follow the system prompt's six-module format exactly. Ensure the story is engaging, characters are distinct, and ALL platform-specific AI prompts in Module 06 are production-ready — directly copy-pasteable into the target tools."""


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

    # 获取平台选择（单选：各一个平台）
    img_platform = data.get("img_platform", "jimeng")
    vid_platform = data.get("vid_platform", "jimeng_video")

    try:
        # 构建Prompt
        system_prompt = build_system_prompt(genre_cn, episode_count, art_style, img_platform, vid_platform)
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


@app.route("/generate_harness", methods=["POST"])
def generate_harness():
    """Harness流水线路由：6步顺序生成，每步有校验和重试。"""
    data = request.get_json()

    genre_key = data.get("genre", "campus_fantasy")
    user_idea = data.get("idea", "").strip()
    episode_count = int(data.get("episodes", 5))
    art_style = data.get("art_style", "ghibli")
    img_platform = data.get("img_platform", "jimeng")
    vid_platform = data.get("vid_platform", "jimeng_video")

    if not user_idea:
        return jsonify({"error": "创意描述不能为空"}), 400
    if genre_key not in GENRE_MAP:
        return jsonify({"error": f"无效的主题类型: {genre_key}"}), 400
    if episode_count < 1 or episode_count > 10:
        return jsonify({"error": "集数必须在1-10之间"}), 400

    genre_cn = GENRE_MAP[genre_key]

    # 获取画风数据
    art_styles = {
        "ghibli": {"desc": "Studio Ghibli style, soft watercolor, warm nostalgic lighting, hand-drawn feel", "negative": "photorealistic, 3D render, harsh shadows, dark, scary"},
        "shinkai": {"desc": "Makoto Shinkai style, photorealistic lighting, vibrant skies, detailed backgrounds, lens flare", "negative": "cartoon, flat colors, simple shapes, low detail, blurry"},
        "cyberpunk": {"desc": "Cyberpunk style, neon purple and cyan lights, dark rainy cityscapes, holographic UIs", "negative": "bright daylight, natural landscape, rural, vintage, pastel"},
        "guofeng": {"desc": "Chinese ink wash painting, flowing brushstrokes, ethereal mist, classic elegance", "negative": "western style, neon, futuristic, modern architecture, 3D render"},
        "anime": {"desc": "Japanese anime style, cel-shading, vibrant colors, large eyes, dynamic poses", "negative": "realistic, 3D, photograph, blurry, western cartoon"},
        "webtoon": {"desc": "Korean webtoon style, tall proportions, soft gradients, glossy hair, digital painting", "negative": "chibi, cartoon, 3D, rough sketch, traditional media"},
        "disney": {"desc": "Disney/Pixar 3D animation, exaggerated expressions, smooth forms, vibrant colors", "negative": "anime, flat 2D, realistic, horror, gritty, dark shadows"},
        "cinematic": {"desc": "Cinematic realism, photorealistic textures, dramatic lighting, film grain, lens flares", "negative": "cartoon, anime, flat, low poly, low quality, painting"},
        "pixel": {"desc": "Pixel art style, crisp pixels, limited palette, retro 8-bit/16-bit, dithering", "negative": "smooth, realistic, photorealistic, high resolution, blurry"},
        "picturebook": {"desc": "Picture book illustration, soft pastels, gentle shapes, cozy lighting, watercolor texture", "negative": "dark, scary, realistic, sharp angles, neon, cyberpunk"},
    }
    art_data = art_styles.get(art_style, art_styles["ghibli"])

    try:
        result = run_pipeline(
            genre_cn=genre_cn,
            idea=user_idea,
            episode_count=episode_count,
            art_style=art_style,
            art_data=art_data,
            img_platform=img_platform,
            vid_platform=vid_platform,
            api_key=DEEPSEEK_API_KEY,
            api_base=DEEPSEEK_API_BASE,
        )

        if not result.get("success"):
            return jsonify({"error": result.get("error", "流水线执行失败")}), 500

        modules = result["modules"]

        # 保存文件
        keyword = user_idea[:20].replace(" ", "_").replace("/", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_name = f"{genre_cn}_{keyword}_{timestamp}"
        save_path = save_modules(modules, folder_name)

        return jsonify({
            "success": True,
            "folder": folder_name,
            "path": save_path,
            "modules": modules,
            "pipeline": "harness",
        })

    except Exception as e:
        return jsonify({"error": f"Harness流水线错误: {str(e)}"}), 500


if __name__ == "__main__":
    print("=" * 60)
    print("  AI漫剧剧本生成器 MVP")
    print(f"  API Base: {DEEPSEEK_API_BASE}")
    print(f"  Output:   {OUTPUT_DIR}")
    print(f"  URL:      http://127.0.0.1:5000")
    print("=" * 60)
    app.run(debug=True, host="127.0.0.1", port=5000)
