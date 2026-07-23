# AI Manga Studio — Pipeline Harness

> 多步流水线总控文档。定义6步生成流程的编排规则、数据流向和校验逻辑。

---

## 流水线架构

```
用户输入 + 配置参数
        │
        ▼
┌──────────────────────────────────────────────────┐
│  STEP 01: 剧本大纲 (outline)                       │
│  输入: genre, idea, episode_count                  │
│  输出: 01_剧本大纲.md                               │
│  校验: ep_count≥1, world≥50chars, each_ep_has_hook │
├──────────────────────────────────────────────────┤
│  STEP 02: 角色设定 (characters)                    │
│  输入: genre, art_style, outline_summary(200chars)  │
│  输出: 02_角色设定.md                               │
│  校验: count≥2, each_has_appearance≥80chars         │
├──────────────────────────────────────────────────┤
│  STEP 03: 场景描述 (scenes)                        │
│  输入: genre, art_style, character_names(List)      │
│  输出: 03_场景描述.md                               │
│  校验: count≥5, each_has_visual≥80chars             │
├──────────────────────────────────────────────────┤
│  STEP 04: 分集台词 (dialogue)                      │
│  输入: outline_episodes, character_names, scene_names│
│  输出: 04_分集台词.md                               │
│  校验: ep_count_match, each_ep_has_hook              │
├──────────────────────────────────────────────────┤
│  STEP 05: 分镜脚本 (storyboard)                    │
│  输入: character_appearances(Map), scene_descs(Map), │
│        dialogue_summary                             │
│  输出: 05_分镜脚本.md                               │
│  校验: char_names_referenced, shot_count≥5_per_ep   │
├──────────────────────────────────────────────────┤
│  STEP 06: AI提示词 (prompts)                       │
│  输入: storyboard_shots(List), img_platform,         │
│        vid_platform, art_style                       │
│  输出: 06_AI提示词.md                               │
│  校验: platform_match, prompt_count≥5               │
└──────────────────────────────────────────────────┘
        │
        ▼
   6模块Markdown → 保存到 输出剧本/{folder}/
```

---

## 步骤间数据传递

| 步骤 | 需要的前置数据 | 传递方式 |
|:---:|---------------|---------|
| 01 | genre, idea, episode_count | 用户输入 |
| 02 | genre, art_style, 01大纲摘要(200字) | STEP 01 输出摘要 |
| 03 | genre, art_style, 02角色名列表 | STEP 02 输出提取 |
| 04 | 01大纲, 02角色名列表, 03场景名列表 | 全部前置输出注入 |
| 05 | 02角色外貌Map, 03场景描述Map, 04台词摘要 | 全部前置输出注入 |
| 06 | 05分镜表, img_platform, vid_platform, art_style | STEP 05输出 + 用户配置 |

---

## 校验与重试

每步完成后执行校验。校验失败时：
1. 记录失败原因
2. 自动重试最多 **2次**（重新调用API）
3. 3次均失败 → 标记该步骤为 `FAILED`，流水线终止，返回错误信息

## 全局约束

所有步骤必须遵守 `CONSTRAINTS.md` 中定义的全局约束。

## 一致性规则

步骤间的数据一致性由 `CONSISTENCY.md` 定义并强制校验。
