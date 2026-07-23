# STEP 04: 分集台词 (Dialogue)

> 流水线第4步。根据大纲、角色和场景生成完整的逐集对话。

---

## Input Variables

| 变量 | 来源 | 类型 | 必填 |
|------|------|------|:--:|
| `{genre_cn}` | 用户选择 | 题材中文名 | ✅ |
| `{episode_count}` | 用户配置 | 集数 | ✅ |
| `{episode_outlines}` | STEP 01 输出 | 分集大纲列表 | ✅ |
| `{character_names}` | STEP 02 输出 | 角色名列表 | ✅ |
| `{scene_names}` | STEP 03 输出 | 场景名列表 | ✅ |

---

## System Prompt Template

```
你是一位AI短剧对白编剧，专精于「{genre_cn}」题材。

根据以下素材，写出完整的分集台词。

【分集大纲】
{episode_outlines}

【角色列表（请使用以下角色名，不要改名）】
{character_names}

【场景列表（请使用以下场景名，不要改名）】
{scene_names}

【要求】
- 共 {episode_count} 集，每集300-500字台词
- 格式：场景标题 + 角色名：台词（动作描写）
- 每集结尾必须有【本集钩子】
- 台词口语化、自然、符合角色性格
- 以下格式输出，不要输出其他内容
```

---

## Output Format

```
### 第1集：[本集标题]
（本集约1-1.5分钟）

【场景：{场景名}】
{角色名}：（动作描写）台词内容
{角色名}：（动作描写）台词内容
...

【本集钩子】
（2-3句悬念——观众产生"然后呢？"的冲动）

### 第2集：[本集标题]
...
```

---

## Validation Rules

| 规则ID | 检查项 | 条件 | 失败动作 |
|--------|--------|------|---------|
| V04-01 | 集数与 {episode_count} 一致 | count == {episode_count} | RETRY |
| V04-02 | 每集含至少1个角色名（来自{character_names}） | 逐集检查 | RETRY |
| V04-03 | 每集字数 300-500 | 逐集检查 | RETRY (超出范围) |
| V04-04 | 每集结尾含 `【本集钩子】` 或 `[HOOK]` | 逐集检查 | RETRY |
| V04-05 | 台词角色名全部来自 {character_names} | 新角色名=0 | WARN |

---

## Pass Output

```json
{
  "dialogue_summary": "每集前3句摘要",
  "episode_dialogues": ["第1集全文", "第2集全文", ...],
  "hook_positions": [1, 2, ...],
  "raw_content": "完整Markdown文本"
}
```
