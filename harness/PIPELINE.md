# AI Manga Studio — Pipeline Harness

> 多步流水线总控文档。定义6步生成流程的编排规则、数据流向和校验逻辑。

---

## 执行顺序（严格串行）

```
STEP 01 ──→ STEP 02 ──→ STEP 03 ──→ STEP 04 ──→ STEP 05 ──→ STEP 06
  │            │            │            │            │            │
  ▼            ▼            ▼            ▼            ▼            ▼
 大纲        角色设定      场景描述      分集台词      分镜脚本      AI提示词
```

**不允许跳过或并行**——每一步依赖前一步的输出数据。

---

## 流水线架构

```
用户输入 + 配置参数
        │
        ▼
┌──────────────────────────────────────────────────────────┐
│  STEP 01: 剧本大纲 (outline)                               │
│  输入: genre, idea, episode_count                          │
│  输出: 01_剧本大纲.md                                       │
│  校验: V01-01~V01-05（共5条）                               │
├──────────────────────────────────────────────────────────┤
│  STEP 02: 角色设定 (characters)                            │
│  输入: genre, art_style, outline_summary(前300字)           │
│  输出: 02_角色设定.md                                       │
│  校验: V02-01~V02-05（共5条）                               │
│  提取: character_names[], character_appearances{}          │
├──────────────────────────────────────────────────────────┤
│  STEP 03: 场景描述 (scenes)                                │
│  输入: genre, art_style, character_names[]                 │
│  输出: 03_场景描述.md                                       │
│  校验: V03-01~V03-05（共5条）                               │
│  提取: scene_names[], scene_descriptions{}                 │
├──────────────────────────────────────────────────────────┤
│  STEP 04: 分集台词 (dialogue)                              │
│  输入: outline全文, character_names[], scene_names[]        │
│  输出: 04_分集台词.md                                       │
│  校验: V04-01~V04-06（共6条）                               │
│  【约束4生效——每集字数300-500】                              │
├──────────────────────────────────────────────────────────┤
│  STEP 05: 分镜脚本 (storyboard)                            │
│  输入: character_appearances{}, scene_descriptions{},       │
│        dialogue_summary                                    │
│  输出: 05_分镜脚本.md                                       │
│  校验: V05-01~V05-07（共7条）                               │
│  【一致性R1——强制引用STEP02角色名，不允许新角色名出现】       │
├──────────────────────────────────────────────────────────┤
│  STEP 06: AI提示词 (prompts)                               │
│  输入: character_appearances{}, scene_descriptions{},       │
│        storyboard全文, img_platform, vid_platform           │
│  输出: 06_AI提示词.md                                       │
│  校验: V06-01~V06-08（共8条）                               │
│  【一致性R5——输出平台必须与用户选择一致】                     │
│  【关键约束——只生成选中平台的prompt，不生成未选中平台格式】    │
└──────────────────────────────────────────────────────────┘
        │
        ▼
   6模块Markdown → 保存到 输出剧本/{folder}/
```

---

## 步骤间数据传递

| 步骤 | 需要的前置数据 | 传递方式 | 约束文档 |
|:---:|---------------|---------|:------:|
| 01 | genre, idea, episode_count | 用户输入 | — |
| 02 | genre, art_style, 01全文 | STEP 01 原始输出 | STEP_02 |
| 03 | genre, art_style, 02角色名列表 | STEP 02 提取 | STEP_03 |
| 04 | 01全文, 02角色名列表, 03场景名列表 | 全部前置数据注入 | STEP_04 |
| 05 | 02角色外貌Map, 03场景描述Map, 04台词摘要 | 结构化提取后注入 | STEP_05, CONSISTENCY R1-R3 |
| 06 | 02外貌, 03场景, 05分镜全文, img/vid_platform | 结构化 + 原始输出 | STEP_06, CONSISTENCY R5 |

---

## 校验体系（三层）

| 层级 | 文档 | 自动化状态 | 说明 |
|:---:|------|:--:|------|
| **步骤内校验** | 各 STEP_0X.md Validation Rules | ✅ 引擎实现 | 该步骤输出自身的格式/内容检查 |
| **全局约束** | CONSTRAINTS.md | ⚠️ 注入System Prompt | 通过注入prompt让AI自约束；V04-03字数检查由引擎实现 |
| **跨模块一致性** | CONSISTENCY.md | ⚠️ 部分引擎实现 | R1(角色名)、R5(平台匹配)已实现；R2-R4,R6需后续完善 |

---

## 校验与重试

每步完成后执行校验。校验失败时：
1. 记录失败原因到日志
2. 自动重试最多 **2次**（重新调用API，注入失败原因到user prompt）
3. 3次均失败 → 标记为 `FAILED`，流水线终止，返回 `{"success":false, "step":"STEP_0X", "reason":"..."}`

---

## 全局约束引用

所有步骤的 System Prompt 自动注入 `CONSTRAINTS.md` 全文作为前缀。

## 一致性规则引用

步骤间数据一致性参照 `CONSISTENCY.md`，由引擎在关键步骤完成后执行交叉校验。
