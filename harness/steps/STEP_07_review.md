# STEP 07: AI脚本审核 (Review)

> 流水线最后一步。在所有模块生成完成后，对完整剧本包进行多维度质量审核。
> 审核结果作为附加模块保存，不影响已生成的6个核心模块。

---

## Input Variables

| 变量 | 来源 | 类型 | 必填 |
|------|------|------|:--:|
| `{genre_cn}` | 用户选择 | 题材中文名 | ✅ |
| `{all_modules}` | STEP 01-06 | 全部已生成模块 | ✅ |

---

## System Prompt Template

```
You are a senior script quality reviewer. Review the complete 6-module AI manga drama package.

GENRE: {genre_cn}

REVIEW DIMENSIONS:
1. **Plot Coherence**: Story logic, pacing, hook effectiveness
2. **Character Consistency**: Cross-module appearance/name consistency, depth
3. **Dialogue Quality**: Naturalness, character voice distinction
4. **Format Compliance**: Markdown structure, platform prompt correctness
5. **Content Safety**: Age-appropriate, no sensitive content

Give an overall score (1-10) and specific improvement suggestions.
Output in markdown with clear sections per dimension.
```

---

## User Prompt Template

```
Review the complete script package below.

SCRIPT PACKAGE:
{all_modules}

Provide a structured review report with scores and actionable suggestions.
```

---

## Output Format

```markdown
## 07 AI脚本审核报告

### 综合评分: X.X / 10

### 各维度评估

| 维度 | 评分 | 状态 | 关键发现 | 改进建议 |
|------|:---:|:----:|------|------|
| 剧情连贯性 | X | ✅/⚠️/❌ | ... | ... |
| 角色一致性 | X | ✅/⚠️/❌ | ... | ... |
| 台词质量 | X | ✅/⚠️/❌ | ... | ... |
| 格式合规 | X | ✅/⚠️/❌ | ... | ... |
| 内容安全 | X | ✅/⚠️/❌ | ... | ... |

### 总体评价
...

### 优先修改项
1. ...
2. ...

---
*审核报告由Harness流水线Step 07自动生成*
```

---

## Validation Rules

| 规则ID | 检查项 | 条件 | 失败动作 |
|--------|--------|------|---------|
| V07-01 | 输出含综合评分 | 数字存在 | WARN |
| V07-02 | 输出含5个维度的评估 | count ≥ 5 | WARN |
| V07-03 | 内容非空 | 长度 ≥ 200 | RETRY |

> 注意：STEP 07 为可选项，校验失败仅 WARN（不阻塞流水线，不触发重试）。
