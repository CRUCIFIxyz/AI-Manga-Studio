"""
热门题材分析引擎
路径：D:\作业\全球数字创业\任务pt.2\mvp\trend_engine.py

功能：利用DeepSeek API分析当前AI漫剧市场趋势：
- 热门题材排行和热度评估
- 流行元素和高频关键词
- 题材组合建议
- 市场饱和度分析

生成结构化趋势报告，供创作参考。
"""

import json
import time
from datetime import datetime

import requests


def _safe_json_parse(raw_text: str, fallback: dict) -> dict:
    """稳健地从LLM响应中提取JSON——处理常见格式瑕疵。"""
    import re
    candidates = []
    code_blocks = re.findall(r"```(?:json)?\s*([\s\S]*?)```", raw_text)
    for block in code_blocks:
        stripped = block.strip()
        if stripped.startswith("{"):
            candidates.append(stripped)
    for match in re.finditer(r"\{", raw_text):
        start = match.start()
        depth = 0
        for i in range(start, len(raw_text)):
            if raw_text[i] == "{": depth += 1
            elif raw_text[i] == "}":
                depth -= 1
                if depth == 0:
                    candidates.append(raw_text[start:i + 1])
                    break
    candidates.sort(key=len, reverse=True)
    for candidate in candidates[:5]:
        try:
            cleaned = _clean_json(candidate)
            return json.loads(cleaned)
        except (json.JSONDecodeError, ValueError):
            continue
    return fallback


def _clean_json(text: str) -> str:
    """清理LLM输出的常见JSON格式错误。"""
    import re
    text = re.sub(r",\s*([}\]])", r"\1", text)   # 尾逗号
    text = re.sub(r"//[^\n]*", "", text)          # 注释
    def fix_nl(m):
        return '"' + m.group(1).replace("\n", "\\n").replace("\r", "") + '"'
    text = re.sub(r'"((?:[^"\\]|\\.)*)"', fix_nl, text)
    text = text.replace("\ufeff", "")
    return text


def _build_trend_system_prompt() -> str:
    """构建趋势分析System Prompt。"""
    return """You are a market analyst specializing in the AI-generated short drama (漫剧) industry in China, 2025-2026.

The market is booming: 168 billion RMB in 2025, projected 243.6 billion in 2026 (+45%).
AIGC short dramas grew 181x in yearly views. Key platforms: Douyin (抖音), Kuaishou (快手), Bilibili.

Your task: analyze current trending themes and provide actionable market intelligence for content creators.

Output in the following JSON format ONLY:

```json
{
  "trending_genres": [
    {
      "genre": "题材名",
      "name_cn": "中文名",
      "heat": <1-10热度>,
      "trend": "rising|stable|declining",
      "audience": "目标受众描述",
      "avg_views": "预估平均播放量级",
      "key_elements": ["核心元素1", "核心元素2"]
    }
  ],
  "hot_keywords": [
    {"keyword": "关键词", "frequency": "high|medium|emerging", "category": "分类"}
  ],
  "genre_combos": [
    {
      "combo": "题材组合名",
      "example": "示例描述",
      "appeal": "受众吸引力说明",
      "difficulty": "easy|medium|hard"
    }
  ],
  "market_insights": {
    "overall_trend": "市场总体趋势概述（100-200字中文）",
    "opportunities": ["机会点1", "机会点2", "机会点3"],
    "warnings": ["风险提示1", "风险提示2"]
  },
  "recommendations": [
    {
      "for_genre": "推荐题材",
      "reason": "推荐理由（50字中文）",
      "target_platform": "推荐发布平台"
    }
  ]
}
```

Base your analysis on general knowledge of the Chinese short drama market trends in 2025-2026. 
Consider these real trends:
- 重生/逆袭 (rebirth/revenge) is the #1 genre by volume
- 甜宠/霸总 (sweet romance/CEO) consistently tops engagement
- 校园+奇幻 (campus+fantasy) crossovers are growing fast
- AI-native production is lowering barriers, increasing competition
- 古风/仙侠 (xianxia) has high production value but also high viewer expectation
- 悬疑/反转 (mystery/twist) short dramas have high completion rates

Be specific, data-informed, and actionable."""


def _build_trend_user_prompt() -> str:
    """构建趋势分析User Prompt。"""
    current_time = datetime.now().strftime("%Y年%m月%d日")
    return f"""Analyze the current AI short drama (AI漫剧) market trends as of {current_time}.

Provide:
1. Top 6-8 trending genres with heat scores
2. 10-15 hot keywords across categories (themes, character types, settings, tropes)
3. 5-7 recommended genre combinations that perform well
4. Market insights: what's hot, what's saturated, what's emerging
5. Actionable recommendations for content creators

Focus on the Chinese market (抖音/快手/B站). Consider both mass-market appeal and niche opportunities.

Output JSON as specified in the system prompt."""


def analyze_trends(api_key: str, api_base: str) -> dict:
    """执行热门题材分析。

    参数:
        api_key: DeepSeek API Key
        api_base: DeepSeek API Base URL

    返回:
        {
            "success": True/False,
            "data": {...},  # 结构化趋势数据
            "report_md": "Markdown趋势报告",
            "updated_at": "ISO时间戳"
        }
    """
    system_prompt = _build_trend_system_prompt()
    user_prompt = _build_trend_user_prompt()

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
        "temperature": 0.7,
        "max_tokens": 4096,
        "stream": False,
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=120)
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]

        # 稳健JSON提取（处理LLM常见格式问题）
        data = _safe_json_parse(content, {
            "error": "无法解析趋势分析结果",
            "raw": content[:500],
        })
        if "error" in data and "raw" not in data:
            data["raw"] = content[:500]

        report_md = _build_trend_report(data)
        return {
            "success": True,
            "data": data,
            "report_md": report_md,
            "updated_at": datetime.now().isoformat(),
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "data": {},
            "report_md": f"# 趋势分析失败\n\n错误: {str(e)}",
            "updated_at": datetime.now().isoformat(),
        }


def _build_trend_report(data: dict) -> str:
    """生成Markdown趋势报告。"""
    lines = [
        "# 📈 AI漫剧市场趋势分析",
        "",
        f"**更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "---",
        "",
        "## 🔥 热门题材排行",
        "",
        "| 排名 | 题材 | 热度 | 趋势 | 目标受众 |",
        "|:---:|------|:---:|:---:|------|",
    ]

    genres = data.get("trending_genres", [])
    for i, g in enumerate(genres[:8], 1):
        heat_bar = "█" * g.get("heat", 5)
        trend_icon = {"rising": "📈", "stable": "📊", "declining": "📉"}.get(g.get("trend", ""), "")
        lines.append(
            f"| {i} | {g.get('name_cn', g.get('genre', ''))} | {heat_bar} {g.get('heat', 0)} | {trend_icon} {g.get('trend', '')} | {g.get('audience', '')} |"
        )

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 🏷️ 热门关键词")
    lines.append("")

    keywords = data.get("hot_keywords", [])
    high_kw = [k for k in keywords if k.get("frequency") == "high"]
    med_kw = [k for k in keywords if k.get("frequency") == "medium"]
    emerging_kw = [k for k in keywords if k.get("frequency") == "emerging"]

    if high_kw:
        lines.append("### 🔴 高频词")
        lines.append(" | ".join(k.get("keyword", "") for k in high_kw))
        lines.append("")
    if med_kw:
        lines.append("### 🟡 中频词")
        lines.append(" | ".join(k.get("keyword", "") for k in med_kw))
        lines.append("")
    if emerging_kw:
        lines.append("### 🟢 新兴词")
        lines.append(" | ".join(k.get("keyword", "") for k in emerging_kw))
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 🎯 推荐题材组合")
    lines.append("")

    combos = data.get("genre_combos", [])
    for c in combos[:5]:
        diff = {"easy": "⭐ 低门槛", "medium": "⭐⭐ 中等", "hard": "⭐⭐⭐ 高难度"}.get(
            c.get("difficulty", ""), ""
        )
        lines.append(f"### {c.get('combo', '')} — {diff}")
        lines.append(f"> 示例: {c.get('example', '')}")
        lines.append(f"> 吸引力: {c.get('appeal', '')}")
        lines.append("")

    lines.append("---")
    lines.append("")

    insights = data.get("market_insights", {})
    if insights:
        lines.append("## 📊 市场洞察")
        lines.append("")
        lines.append(insights.get("overall_trend", ""))

        opportunities = insights.get("opportunities", [])
        if opportunities:
            lines.append("")
            lines.append("### 🟢 机会点")
            for o in opportunities:
                lines.append(f"- {o}")

        warnings_list = insights.get("warnings", [])
        if warnings_list:
            lines.append("")
            lines.append("### 🔴 风险提示")
            for w in warnings_list:
                lines.append(f"- {w}")

    lines.append("")
    lines.append("---")

    recommendations = data.get("recommendations", [])
    if recommendations:
        lines.append("## 💡 创作建议")
        lines.append("")
        for r in recommendations:
            lines.append(f"- **{r.get('for_genre', '')}**: {r.get('reason', '')} → 推荐平台: {r.get('target_platform', '')}")

    lines.append("")
    lines.append("---")
    lines.append("*报告由AI市场分析系统自动生成，数据基于2025-2026年行业趋势*")

    return "\n".join(lines)
