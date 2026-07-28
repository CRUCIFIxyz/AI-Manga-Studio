"""
多Agent AI脚本审核引擎
路径：D:\作业\全球数字创业\任务pt.2\mvp\review_engine.py

功能：5个专业审查Agent并行运行，从不同维度审查生成的剧本，
聚合产生综合审核报告（评分+具体建议）。

审查维度：
- Plot Agent:     剧情连贯性、节奏、钩子有效性
- Character Agent: 角色一致性、深度、辨识度
- Dialogue Agent:  台词自然度、角色语音一致性
- Format Agent:    Markdown格式、平台prompt合规性
- Safety Agent:    内容安全审查

每个Agent独立调用DeepSeek API，并行执行，汇总为审核报告。
"""

import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

# Agent定义：名称、角色描述、审查维度、权重
REVIEW_AGENTS = [
    {
        "id": "plot",
        "name": "剧情审查",
        "role": "资深短剧编剧顾问，专注故事结构和叙事节奏",
        "focus": [
            "剧情连贯性和因果逻辑",
            "分集节奏是否紧凑（每集1-1.5分钟适配）",
            "悬念钩子是否有效（每集末尾是否制造认知缺口）",
            "故事弧线是否完整（起承转合）",
            "世界观设定是否自洽",
        ],
        "weight": 0.25,
    },
    {
        "id": "character",
        "name": "角色审查",
        "role": "角色设计专家，专注人物塑造和跨模块一致性",
        "focus": [
            "角色外貌描述是否跨模块一致（02→05→06关键词原样使用）",
            "角色性格是否鲜明、有辨识度",
            "角色动机是否合理、行为是否符合设定性格",
            "配角是否有存在价值（非工具人）",
            "角色弧线是否有成长/变化",
        ],
        "weight": 0.25,
    },
    {
        "id": "dialogue",
        "name": "台词审查",
        "role": "对白导演，专注口语化台词和角色语音辨识度",
        "focus": [
            "台词是否口语化、自然（非书面语/旁白腔）",
            "不同角色是否有独特的说话方式",
            "台词长度是否适配短视频节奏",
            "是否有无效对话（纯信息灌输无冲突）",
            "语气词和停顿是否恰当",
        ],
        "weight": 0.20,
    },
    {
        "id": "format",
        "name": "格式审查",
        "role": "技术编辑，专注输出格式和平台适配",
        "focus": [
            "Markdown格式是否正确（表格/标题/代码块）",
            "Module 06 AI提示词是否全英文",
            "平台提示词格式是否严格匹配选中平台",
            "分镜表结构是否完整（镜号/景别/画面/运镜/时长/转场）",
            "文件命名和编码是否符合规范",
        ],
        "weight": 0.15,
    },
    {
        "id": "safety",
        "name": "安全审查",
        "role": "内容安全审核员，专注合规性和适宜性",
        "focus": [
            "是否有色情、暴力、血腥内容",
            "是否有政治敏感表述",
            "是否适合全年龄段（PG-13标准）",
            "是否有歧视性或侮辱性语言",
            "是否引用了现实名人或敏感事件",
        ],
        "weight": 0.15,
    },
]


def _build_review_system_prompt(agent: dict) -> str:
    """构建单个审查Agent的System Prompt。"""
    focus_lines = "\n".join(f"- {f}" for f in agent["focus"])
    return f"""You are a {agent['role']} reviewing an AI-generated manga drama script package.

Your review dimensions:
{focus_lines}

RULES:
1. Give a score from 1-10 (10=perfect) for your review dimension.
2. List at least 2 specific issues found (if score < 10). Use precise references (module name, character name, scene name).
3. Provide at least 2 actionable suggestions for improvement.
4. Be honest and critical — sugarcoating helps no one.
5. Output in the following JSON format ONLY:

```json
{{
  "agent_id": "{agent['id']}",
  "agent_name": "{agent['name']}",
  "score": <1-10>,
  "issues": [
    {{"severity": "high|medium|low", "module": "模块名", "detail": "具体问题描述"}}
  ],
  "suggestions": [
    "具体可执行的改进建议1",
    "具体可执行的改进建议2"
  ],
  "summary": "一句话总结审查结论"
}}
```"""


def _build_review_user_prompt(modules: dict, genre_cn: str, agent: dict) -> str:
    """构建单个审查Agent的User Prompt（含剧本内容）。"""
    # 根据Agent类型选择性提供最相关的模块
    relevant_modules = {
        "plot": ["01_剧本大纲", "04_分集台词"],
        "character": ["02_角色设定", "05_分镜脚本"],
        "dialogue": ["04_分集台词"],
        "format": ["05_分镜脚本", "06_AI提示词"],
        "safety": ["01_剧本大纲", "04_分集台词", "02_角色设定"],
    }

    keys = relevant_modules.get(agent["id"], list(modules.keys())[:4])
    content_parts = []
    for key in keys:
        if key in modules:
            text = modules[key]
            # 截断过长内容（保留前2000字符供审查）
            if len(text) > 2000:
                text = text[:2000] + "\n\n... (内容已截断，共{}字符)".format(len(modules[key]))
            content_parts.append(f"### {key}\n\n{text}")

    script_content = "\n\n---\n\n".join(content_parts) if content_parts else "（无内容）"

    return f"""Review the following AI manga drama script package.

GENRE: {genre_cn}

SCRIPT CONTENT:
{script_content}

Please analyze based on your review dimensions and output the JSON result."""


def _call_single_agent(
    agent: dict,
    modules: dict,
    genre_cn: str,
    api_key: str,
    api_base: str,
) -> dict:
    """调用单个审查Agent，返回审查结果。"""
    system_prompt = _build_review_system_prompt(agent)
    user_prompt = _build_review_user_prompt(modules, genre_cn, agent)

    url = f"{api_base}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "deepseek-v4-pro",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.3,
        "max_tokens": 2048,
        "stream": False,
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=120)
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]

        # 尝试提取JSON
        json_match = __import__("re").search(r"\{[\s\S]*\}", content)
        if json_match:
            result = json.loads(json_match.group())
        else:
            result = {
                "agent_id": agent["id"],
                "agent_name": agent["name"],
                "score": 5,
                "issues": [{"severity": "medium", "module": "系统", "detail": "Agent返回格式异常，无法解析"}],
                "suggestions": ["请手动审查此剧本"],
                "summary": f"自动审查失败（{agent['name']}）",
            }

        result.setdefault("agent_id", agent["id"])
        result.setdefault("agent_name", agent["name"])
        return result

    except Exception as e:
        return {
            "agent_id": agent["id"],
            "agent_name": agent["name"],
            "score": 0,
            "issues": [{"severity": "high", "module": "系统", "detail": f"审查Agent异常: {str(e)}"}],
            "suggestions": ["请手动审查此剧本"],
            "summary": f"审查失败: {str(e)[:100]}",
        }


def run_review(
    modules: dict,
    genre_cn: str,
    api_key: str,
    api_base: str,
    progress_callback=None,
) -> dict:
    """执行多Agent并行审核。

    参数:
        modules: {"01_剧本大纲": "...", "02_角色设定": "...", ...}
        genre_cn: 题材中文名
        api_key: DeepSeek API Key
        api_base: DeepSeek API Base URL
        progress_callback(agent_name, status): 可选，每个Agent完成时回调

    返回:
        {
            "success": True/False,
            "overall_score": 8.2,
            "agents": [...],
            "summary": "综合评估...",
            "report_md": "Markdown审核报告"
        }
    """
    agent_results = []
    errors = []

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {
            executor.submit(
                _call_single_agent,
                agent,
                modules,
                genre_cn,
                api_key,
                api_base,
            ): agent
            for agent in REVIEW_AGENTS
        }

        for future in as_completed(futures):
            agent = futures[future]
            try:
                result = future.result()
                agent_results.append(result)
                if progress_callback:
                    progress_callback(agent["name"], "done" if result.get("score", 0) > 0 else "error")
            except Exception as e:
                errors.append(f"{agent['name']}: {str(e)}")
                if progress_callback:
                    progress_callback(agent["name"], "error")

    if not agent_results and errors:
        return {"success": False, "error": "; ".join(errors)}

    # 按原始顺序排序
    agent_order = {a["id"]: i for i, a in enumerate(REVIEW_AGENTS)}
    agent_results.sort(key=lambda r: agent_order.get(r.get("agent_id", ""), 99))

    # 计算综合得分
    weights = {a["id"]: a["weight"] for a in REVIEW_AGENTS}
    total_weight = 0.0
    weighted_sum = 0.0
    for r in agent_results:
        aid = r.get("agent_id", "")
        w = weights.get(aid, 0.15)
        weighted_sum += r.get("score", 5) * w
        total_weight += w

    overall_score = round(weighted_sum / total_weight, 1) if total_weight > 0 else 5.0

    # 生成Markdown审核报告
    report_md = _build_review_report(agent_results, overall_score, genre_cn)

    # 生成综合摘要
    score_labels = [
        (9.0, "优秀 — 可直接用于生产"),
        (7.0, "良好 — 建议微调后使用"),
        (5.0, "一般 — 需部分重写"),
        (0.0, "较差 — 建议重新生成"),
    ]
    label = next(l for t, l in score_labels if overall_score >= t)

    return {
        "success": True,
        "overall_score": overall_score,
        "score_label": label,
        "agents": agent_results,
        "summary": label,
        "report_md": report_md,
    }


def _build_review_report(agent_results: list, overall_score: float, genre_cn: str) -> str:
    """生成Markdown格式的审核报告。"""
    lines = [
        f"# 🔍 AI剧本审核报告",
        f"",
        f"**题材**: {genre_cn} | **综合评分**: {overall_score}/10",
        f"",
        f"---",
        f"",
        f"## 📊 各维度评分",
        f"",
        f"| 审查维度 | 评分 | 状态 |",
        f"|---------|:---:|:----:|",
    ]

    for r in agent_results:
        score = r.get("score", 0)
        badge = "🟢" if score >= 8 else ("🟡" if score >= 6 else "🔴")
        lines.append(f"| {r.get('agent_name', 'Unknown')} | {score}/10 | {badge} |")

    lines.append("")
    lines.append("---")
    lines.append("")

    for r in agent_results:
        lines.append(f"## {r.get('agent_name', 'Unknown')} — {r.get('score', 0)}/10")
        lines.append("")
        lines.append(f"> {r.get('summary', '无总结')}")
        lines.append("")

        issues = r.get("issues", [])
        if issues:
            lines.append("### ⚠️ 发现的问题")
            lines.append("")
            for issue in issues:
                sev = issue.get("severity", "medium")
                icon = "🔴" if sev == "high" else ("🟡" if sev == "medium" else "🔵")
                lines.append(f"- {icon} **[{sev.upper()}]** {issue.get('module', '')}: {issue.get('detail', '')}")
            lines.append("")

        suggestions = r.get("suggestions", [])
        if suggestions:
            lines.append("### 💡 改进建议")
            lines.append("")
            for s in suggestions:
                lines.append(f"- {s}")
            lines.append("")

    lines.append("---")
    lines.append(f"*报告由AI多Agent审核系统自动生成*")

    return "\n".join(lines)
