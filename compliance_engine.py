"""
原创合规检测引擎
路径：D:\作业\全球数字创业\任务pt.2\mvp\compliance_engine.py

功能：对生成的AI漫剧剧本进行原创性检测：
- 角色名vs已知IP角色名比对
- 剧情相似度评估
- 标志性桥段/台词检查
- 风险评估（低/中/高/极高）
- 生成合规报告

使用DeepSeek API进行智能比对分析。
"""

import json
import re
from datetime import datetime

import requests


def _safe_json_parse(raw_text: str, fallback: dict) -> dict:
    """稳健地从LLM响应中提取JSON——处理常见格式瑕疵。"""
    import re as _re
    candidates = []
    code_blocks = _re.findall(r"```(?:json)?\s*([\s\S]*?)```", raw_text)
    for block in code_blocks:
        stripped = block.strip()
        if stripped.startswith("{"):
            candidates.append(stripped)
    for match in _re.finditer(r"\{", raw_text):
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
    import re as _re
    text = _re.sub(r",\s*([}\]])", r"\1", text)
    text = _re.sub(r"//[^\n]*", "", text)
    def fix_nl(m):
        return '"' + m.group(1).replace("\n", "\\n").replace("\r", "") + '"'
    text = _re.sub(r'"((?:[^"\\]|\\.)*)"', fix_nl, text)
    text = text.replace("\ufeff", "")
    return text


# 已知知名IP参考列表（用于比对提示）
KNOWN_IP_DATABASE = """
著名动漫/漫画IP（角色名和标志性元素——比对时参考，非完整列表）：
- 火影忍者: 漩涡鸣人, 宇智波佐助, 春野樱, 卡卡西, 木叶村, 查克拉, 尾兽, 写轮眼
- 海贼王: 路飞, 索隆, 娜美, 恶魔果实, 伟大航路, 霸气
- 鬼灭之刃: 炭治郎, 祢豆子, 日之呼吸, 鬼杀队, 十二鬼月
- 咒术回战: 虎杖悠仁, 五条悟, 两面宿傩, 咒力, 领域展开
- 进击的巨人: 艾伦, 三笠, 调查兵团, 巨人化, 墙壁
- 全职猎人: 小杰, 奇犽, 念能力, 猎人执照
- 死神: 黑崎一护, 朽木露琪亚, 斩魄刀, 卍解, 死神代理
- 名侦探柯南: 工藤新一, 毛利兰, 黑衣组织, APTX4869
- 哆啦A梦: 大雄, 静香, 任意门, 时光机, 四次元口袋
- 龙珠: 孙悟空, 贝吉塔, 超级赛亚人, 龙珠, 龟派气功

著名小说IP:
- 斗罗大陆: 唐三, 小舞, 魂环, 武魂, 史莱克七怪
- 斗破苍穹: 萧炎, 药老, 异火, 斗气
- 凡人修仙传: 韩立, 掌天瓶
- 完美世界: 石昊, 至尊骨

著名影视IP:
- 哈利波特: 哈利, 赫敏, 罗恩, 霍格沃茨, 魔法石, 伏地魔
- 漫威: 钢铁侠, 美国队长, 雷神, 无限宝石, 复仇者联盟
"""


def _build_compliance_system_prompt() -> str:
    """构建合规检测System Prompt。"""
    return f"""You are a copyright and originality compliance auditor for AI-generated content (AI漫剧).

Your task: check the provided script against known intellectual property to detect potential infringement.

REFERENCE DATABASE of known IPs:
{KNOWN_IP_DATABASE}

DETECTION RULES:
1. **Character Name Check**: Any character name that is identical or highly similar to a known IP character → HIGH RISK FLAG
2. **Plot Similarity**: Story arcs that closely mirror specific known works → MEDIUM-HIGH RISK
3. **Setting/Trope Overlap**: Generic genre tropes (e.g., "magic school") are OK; specific world mechanics identical to known IP are NOT
4. **Catchphrase/Technique**: Signature moves, spells, or catchphrases from known IP → HIGH RISK FLAG
5. **Composite Risk**: Multiple medium-level similarities can compound to HIGH

NOTE: Using a broad genre convention (e.g., "cultivation system", "magic academy") is NOT infringement. 
Only specific, identifiable elements from known works are flags.

Output in the following JSON format ONLY:

```json
{{
  "originality_score": <0-100, 100=completely original>,
  "risk_level": "low|medium|high|critical",
  "flags": [
    {{
      "type": "character_name|plot_similarity|setting_overlap|catchphrase|composite",
      "severity": "low|medium|high|critical",
      "detail": "具体发现",
      "matched_ip": "匹配到的已知IP（如无则填null）",
      "suggestion": "修改建议"
    }}
  ],
  "similar_ip_check": [
    {{
      "ip_name": "最相似的已知IP名",
      "similarity": <0-100相似度>,
      "overlap_description": "相似之处描述"
    }}
  ],
  "summary": "综合原创性评估（50-100字中文）",
  "recommendation": "pass|revise|reject"
}}
```

IMPORTANT: 
- Be precise but not overly strict. Genre conventions are NOT infringement.
- Score of 90+ means essentially original with only unavoidable genre overlap.
- Score of 70-89 means some concerning similarities that should be reviewed.
- Score below 70 means potential infringement — recommend significant revision."""


def _build_compliance_user_prompt(modules: dict) -> str:
    """构建合规检测User Prompt（含剧本内容）。"""
    content_parts = []

    # 优先包含角色设定和剧本大纲（最关键的两个模块）
    priority_keys = ["02_角色设定", "01_剧本大纲", "04_分集台词"]
    other_keys = [k for k in modules if k not in priority_keys]

    for key in priority_keys + other_keys:
        if key in modules:
            text = modules[key]
            if len(text) > 1500:
                text = text[:1500] + "\n\n... (截断)"
            content_parts.append(f"### {key}\n\n{text}")

    script_content = "\n\n---\n\n".join(content_parts[:4])  # 最多4个模块

    return f"""Analyze the following AI-generated manga drama script for originality and IP compliance:

{script_content}

Check against the known IP database and report any flags. Output JSON as specified."""


def check_compliance(
    modules: dict,
    api_key: str,
    api_base: str,
) -> dict:
    """执行原创合规检测。

    参数:
        modules: {"01_剧本大纲": "...", "02_角色设定": "...", ...}
        api_key: DeepSeek API Key
        api_base: DeepSeek API Base URL

    返回:
        {
            "success": True/False,
            "originality_score": 95,
            "risk_level": "low",
            "flags": [...],
            "recommendation": "pass|revise|reject",
            "report_md": "Markdown合规报告"
        }
    """
    system_prompt = _build_compliance_system_prompt()
    user_prompt = _build_compliance_user_prompt(modules)

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
        "max_tokens": 3072,
        "stream": False,
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=120)
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]

        # 稳健JSON提取（处理LLM常见格式问题）
        data = _safe_json_parse(content, {
            "originality_score": 0,
            "risk_level": "unknown",
            "flags": [],
            "summary": "无法解析检测结果",
            "recommendation": "revise",
        })

        report_md = _build_compliance_report(data)
        return {
            "success": True,
            "originality_score": data.get("originality_score", 0),
            "risk_level": data.get("risk_level", "unknown"),
            "flags": data.get("flags", []),
            "similar_ip_check": data.get("similar_ip_check", []),
            "summary": data.get("summary", ""),
            "recommendation": data.get("recommendation", "revise"),
            "report_md": report_md,
            "checked_at": datetime.now().isoformat(),
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "originality_score": 0,
            "risk_level": "unknown",
            "flags": [],
            "report_md": f"# 合规检测失败\n\n错误: {str(e)}",
            "checked_at": datetime.now().isoformat(),
        }


def _build_compliance_report(data: dict) -> str:
    """生成Markdown合规报告。"""
    score = data.get("originality_score", 0)
    risk = data.get("risk_level", "unknown")
    recommendation = data.get("recommendation", "revise")

    risk_colors = {
        "low": "🟢",
        "medium": "🟡",
        "high": "🟠",
        "critical": "🔴",
        "unknown": "⚪",
    }
    risk_icon = risk_colors.get(risk, "⚪")

    rec_labels = {
        "pass": "✅ 通过 — 原创度达标，可直接使用",
        "revise": "⚠️ 需修改 — 存在需调整的内容",
        "reject": "🚫 不通过 — 存在严重IP侵权风险，建议重新生成",
    }

    lines = [
        f"# 🛡️ 原创合规检测报告",
        f"",
        f"| 指标 | 结果 |",
        f"|------|------|",
        f"| 原创度评分 | **{score}/100** |",
        f"| 风险等级 | {risk_icon} **{risk.upper()}** |",
        f"| 建议 | {rec_labels.get(recommendation, recommendation)} |",
        f"",
        f"---",
        f"",
        f"## 📋 检测摘要",
        f"",
        f"{data.get('summary', '无摘要')}",
        f"",
    ]

    flags = data.get("flags", [])
    if flags:
        lines.append("## ⚠️ 发现的问题")
        lines.append("")
        lines.append("| 类型 | 严重度 | 详情 | 匹配IP | 建议 |")
        lines.append("|------|:---:|------|------|------|")
        for f in flags:
            sev_icon = {"low": "🟢", "medium": "🟡", "high": "🟠", "critical": "🔴"}.get(
                f.get("severity", ""), "⚪"
            )
            lines.append(
                f"| {f.get('type', '')} | {sev_icon} {f.get('severity', '')} | {f.get('detail', '')[:60]} | {f.get('matched_ip', '-') or '-'} | {f.get('suggestion', '')[:60]} |"
            )

    lines.append("")
    lines.append("---")

    similar = data.get("similar_ip_check", [])
    if similar:
        lines.append("## 🔍 相似IP比对")
        lines.append("")
        for s in similar:
            sim_bar = "█" * min(int(s.get("similarity", 0) / 10), 10)
            lines.append(f"- **{s.get('ip_name', '')}**: 相似度 {s.get('similarity', 0)}% {sim_bar}")
            lines.append(f"  - {s.get('overlap_description', '')}")
        lines.append("")

    lines.append("---")
    lines.append(f"*检测时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    lines.append("")
    lines.append("*本报告由AI自动生成，仅供参考。对于高风险项目，建议人工复核。*")

    return "\n".join(lines)
