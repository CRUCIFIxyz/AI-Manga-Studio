"""
Harness Pipeline Engine — 多步流水线引擎
路径：D:\作业\全球数字创业\任务pt.2\mvp\harness_engine.py

读取 harness/ 目录下的MD文档，按PIPELINE.md定义的流程，
依次执行6步API调用，每步完成后运行校验规则，
将前置步骤的数据注入后续步骤的prompt中。
"""

import re
import json
import time
from pathlib import Path
from typing import Any

import requests

HARNESS_DIR = Path(__file__).parent / "harness"
STEPS_DIR = HARNESS_DIR / "steps"
GLOBAL_CONSTRAINTS = (HARNESS_DIR / "CONSTRAINTS.md").read_text(encoding="utf-8")

MAX_RETRIES = 2  # 每步最多重试次数


def _call_api(system_prompt: str, user_prompt: str, api_key: str, api_base: str) -> str:
    """封装DeepSeek API调用。"""
    url = f"{api_base}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.7,
        "max_tokens": 4096,
        "stream": False,
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=180)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def _extract_char_names(content: str) -> list:
    """从STEP 02输出中提取角色名列表。"""
    names = re.findall(r"###\s*角色[一二三四五六七八九十]?[：:]\s*(.+?)$", content, re.MULTILINE)
    return [n.strip() for n in names if n.strip()]


def _extract_scene_names(content: str) -> list:
    """从STEP 03输出中提取场景名列表。"""
    names = re.findall(r"###\s*场景[一二三四五六七八九十]?[：:]\s*(.+?)$", content, re.MULTILINE)
    return [n.strip() for n in names if n.strip()]


def _build_appearance_map(step02_content: str) -> str:
    """从STEP 02输出构建角色外貌摘要（用于注入后续prompt）。"""
    # 提取每个角色块的"外貌"行
    blocks = re.split(r"###\s*角色", step02_content)
    result = []
    for block in blocks[1:]:  # 跳过第一个空块
        name_match = re.match(r"[一二三四五六七八九十]?[：:]\s*(.+)", block)
        name = name_match.group(1).strip() if name_match else "Unknown"
        appear_match = re.search(r"外貌[：:]\s*(.+?)(?:\n|$)", block)
        appear = appear_match.group(1).strip()[:100] if appear_match else ""
        result.append(f"- {name}: {appear}")
    return "\n".join(result) if result else step02_content[:500]


def _build_scene_map(step03_content: str) -> str:
    """从STEP 03输出构建场景摘要（用于注入后续prompt）。"""
    blocks = re.split(r"###\s*场景", step03_content)
    result = []
    for block in blocks[1:]:
        name_match = re.match(r"[一二三四五六七八九十]?[：:]\s*(.+)", block)
        name = name_match.group(1).strip() if name_match else "Unknown"
        visual_match = re.search(r"画面描述[：:]\s*(.+?)(?:\n|$)", block)
        visual = visual_match.group(1).strip()[:80] if visual_match else ""
        result.append(f"- {name}: {visual}")
    return "\n".join(result) if result else step03_content[:500]


def run_pipeline(
    genre_cn: str,
    idea: str,
    episode_count: int,
    art_style: str,
    art_data: dict,
    img_platform: str,
    vid_platform: str,
    api_key: str,
    api_base: str,
    progress_callback=None,
) -> dict:
    """执行完整6步流水线。

    参数:
        progress_callback(step_name, status, detail): 进度回调

    返回:
        {"success": True, "modules": {"01_...": "...", ...}} 或 {"success": False, "error": "..."}
    """
    state = {
        "genre_cn": genre_cn,
        "idea": idea,
        "episode_count": episode_count,
        "art_desc": art_data["desc"],
        "art_negative": art_data["negative"],
        "img_platform": img_platform,
        "vid_platform": vid_platform,
    }

    steps = [
        {
            "id": "01_outline",
            "name": "剧本大纲",
            "file": "STEP_01_outline.md",
            "requires": [],
        },
        {
            "id": "02_characters",
            "name": "角色设定",
            "file": "STEP_02_characters.md",
            "requires": ["01_outline"],
        },
        {
            "id": "03_scenes",
            "name": "场景描述",
            "file": "STEP_03_scenes.md",
            "requires": ["02_characters"],
        },
        {
            "id": "04_dialogue",
            "name": "分集台词",
            "file": "STEP_04_dialogue.md",
            "requires": ["01_outline", "02_characters", "03_scenes"],
        },
        {
            "id": "05_storyboard",
            "name": "分镜脚本",
            "file": "STEP_05_storyboard.md",
            "requires": ["02_characters", "03_scenes", "04_dialogue"],
        },
        {
            "id": "06_prompts",
            "name": "AI提示词",
            "file": "STEP_06_prompts.md",
            "requires": ["02_characters", "03_scenes", "05_storyboard"],
        },
    ]

    modules = {}
    extracted = {}  # 从各步骤提取的结构化数据

    for step in steps:
        step_id = step["id"]
        step_name = step["name"]

        if progress_callback:
            progress_callback(step_name, "running", "正在生成...")

        # 构建此步骤的 prompt
        system_prompt, user_prompt = _build_step_prompts(
            step["file"], state, modules, extracted
        )

        content = None
        for attempt in range(MAX_RETRIES + 1):
            try:
                content = _call_api(system_prompt, user_prompt, api_key, api_base)
                # 校验
                valid, reason = _validate_step(step_id, content, state, modules, extracted)
                if valid:
                    break
                if progress_callback and attempt < MAX_RETRIES:
                    progress_callback(step_name, "retry", f"校验失败({reason})，重试 {attempt+1}/{MAX_RETRIES}")
            except Exception as e:
                if attempt < MAX_RETRIES:
                    if progress_callback:
                        progress_callback(step_name, "retry", f"API异常({e})，重试 {attempt+1}/{MAX_RETRIES}")
                    time.sleep(2)
                else:
                    return {"success": False, "error": f"Step {step_name} 失败(重试{MAX_RETRIES}次): {e}"}

        if content is None:
            return {"success": False, "error": f"Step {step_name} 生成失败"}

        modules[step_id] = content
        # 提取结构化数据
        _extract_step_data(step_id, content, extracted)

        if progress_callback:
            progress_callback(step_name, "done", "✓")

    # 映射为前端期望的模块名
    module_map = {
        "01_outline": "01_剧本大纲",
        "02_characters": "02_角色设定",
        "03_scenes": "03_场景描述",
        "04_dialogue": "04_分集台词",
        "05_storyboard": "05_分镜脚本",
        "06_prompts": "06_AI提示词",
    }
    result_modules = {module_map[k]: v for k, v in modules.items()}

    # 同时按文件名保存到state（用于旧版save_modules兼容）
    state["modules"] = result_modules

    return {"success": True, "modules": result_modules, "state": state}


def _build_step_prompts(step_file: str, state: dict, modules: dict, extracted: dict) -> tuple:
    """根据步骤MD文档构建 system/user prompt。

    返回: (system_prompt, user_prompt)
    """
    template = (STEPS_DIR / step_file).read_text(encoding="utf-8")

    # 提取模板中的变量并替换
    user_prompt = _build_user_prompt_for_step(step_file, state, modules, extracted)
    system_prompt = GLOBAL_CONSTRAINTS + "\n\n" + template

    return system_prompt, user_prompt


def _build_user_prompt_for_step(step_file: str, state: dict, modules: dict, extracted: dict) -> str:
    """根据步骤类型构建用户提示。"""
    genre = state["genre_cn"]
    ep = state["episode_count"]
    art_desc = state["art_desc"]
    art_neg = state["art_negative"]

    if "outline" in step_file:
        return f"【题材】{genre}\n【集数】{ep}集\n【创意】{state['idea']}\n\n请生成剧本大纲。"

    if "characters" in step_file:
        summary = modules.get("01_outline", "")[:300]
        return f"【题材】{genre}\n【画风】{art_desc}\n【大纲摘要】\n{summary}\n\n请设计主要角色。"

    if "scenes" in step_file:
        char_names = extracted.get("char_names", [])
        names_str = "、".join(char_names) if char_names else "（从大纲推断）"
        return f"【题材】{genre}\n【画风】{art_desc}\n【角色列表】{names_str}\n\n请设计关键场景。"

    if "dialogue" in step_file:
        outlines = modules.get("01_outline", "")[:500]
        char_names = extracted.get("char_names", [])
        scene_names = extracted.get("scene_names", [])
        return (
            f"【题材】{genre}\n【集数】{ep}集\n"
            f"【分集大纲】\n{outlines}\n\n"
            f"【角色（必须使用以下名称）】{', '.join(char_names)}\n"
            f"【场景（必须使用以下名称）】{', '.join(scene_names)}\n\n"
            f"请写出完整分集台词。"
        )

    if "storyboard" in step_file:
        appearances = _build_appearance_map(modules.get("02_characters", ""))
        scenes = _build_scene_map(modules.get("03_scenes", ""))
        dialogue = modules.get("04_dialogue", "")[:400]
        return (
            f"【题材】{genre}\n【集数】{ep}集\n"
            f"【角色外貌——分镜中必须原样使用】\n{appearances}\n\n"
            f"【场景描述——分镜中必须原样使用】\n{scenes}\n\n"
            f"【台词摘要】\n{dialogue}\n\n"
            f"请写出逐镜分镜表。"
        )

    if "prompts" in step_file:
        appearances = _build_appearance_map(modules.get("02_characters", ""))
        scenes = _build_scene_map(modules.get("03_scenes", ""))
        storyboard = modules.get("05_storyboard", "")[:500]
        img_p = state["img_platform"]
        vid_p = state["vid_platform"]
        return (
            f"ART STYLE: {art_desc}\nNEGATIVE: {art_neg}\n\n"
            f"CHARACTERS:\n{appearances}\n\n"
            f"SCENES:\n{scenes}\n\n"
            f"STORYBOARD:\n{storyboard}\n\n"
            f"IMAGE PLATFORM: {img_p}\nVIDEO PLATFORM: {vid_p}\n\n"
            f"Generate platform-specific AI prompts for the above shots."
        )

    return "Generate the output as specified in the system prompt."


def _validate_step(step_id: str, content: str, state: dict, modules: dict, extracted: dict) -> tuple:
    """校验步骤输出。返回 (is_valid, reason)。"""
    ep = state["episode_count"]

    if step_id == "01_outline":
        ep_count = len(re.findall(r"\*\*第\d+集\*\*", content))
        if ep_count != ep:
            return False, f"集数不匹配: 期望{ep}，实际{ep_count}"
        if len(content) < 200:
            return False, "内容过短"
        if "[HOOK]" not in content and "「" not in content:
            return False, "缺少钩子标记"
        return True, ""

    if step_id == "02_characters":
        char_count = len(re.findall(r"###\s*角色", content))
        if char_count < 2:
            return False, f"角色数不足: {char_count}"
        if len(content) < 400:
            return False, "内容过短"
        appear_count = len(re.findall(r"外貌[：:]", content))
        if appear_count < char_count:
            return False, f"外貌描述不足: {appear_count}/{char_count}"
        # 检查每个角色外貌是否 ≥ 100 字符
        appear_blocks = re.findall(r"外貌[：:]\s*(.+?)(?=\n-|\n\n|\Z)", content, re.DOTALL)
        for i, block in enumerate(appear_blocks):
            if len(block.strip()) < 100:
                return False, f"角色{i+1}外貌描述过短({len(block.strip())}字,需≥100)"
        return True, ""

    if step_id == "03_scenes":
        scene_count = len(re.findall(r"###\s*场景", content))
        if scene_count < 6:
            return False, f"场景数不足: {scene_count}（需≥6）"
        if len(content) < 600:
            return False, "内容过短"
        return True, ""

    if step_id == "04_dialogue":
        ep_count = len(re.findall(r"###\s*第\d+集", content))
        if ep_count != ep:
            return False, f"集数不匹配: 期望{ep}，实际{ep_count}"
        if "【本集钩子】" not in content and "[HOOK]" not in content:
            return False, "缺少钩子"
        return True, ""

    if step_id == "05_storyboard":
        ep_count = len(re.findall(r"###\s*第\d+集分镜", content))
        if ep_count != ep:
            return False, f"集数不匹配: 期望{ep}，实际{ep_count}"
        if len(content) < 400:
            return False, "内容过短"
        # 检查角色名引用
        char_names = extracted.get("char_names", [])
        if char_names:
            refs = sum(1 for n in char_names if n in content)
            if refs < len(char_names):
                missing = [n for n in char_names if n not in content]
                return False, f"分镜未引用角色: {missing}"
        return True, ""

    if step_id == "06_prompts":
        if len(content) < 500:
            return False, "内容过短"
        if not any(c.isascii() and c.isalpha() for c in content[:200]):
            return False, "提示词应为英文"
        # 检查平台匹配
        img_p = state["img_platform"]
        vid_p = state["vid_platform"]
        if img_p == "midjourney" and "Midjourney" not in content:
            return False, "未包含Midjourney格式"
        if vid_p == "pika" and "Pika" not in content:
            return False, "未包含Pika格式"
        return True, ""

    return True, ""


def _extract_step_data(step_id: str, content: str, extracted: dict):
    """从步骤输出中提取结构化数据。"""
    if step_id == "02_characters":
        extracted["char_names"] = _extract_char_names(content)

    if step_id == "03_scenes":
        extracted["scene_names"] = _extract_scene_names(content)
