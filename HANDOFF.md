# HANDOFF.md — 项目交接文档

> 写给下一个接手此项目的会话/开发者。本文档包含完整上下文，无需查阅历史聊天记录即可继续工作。

---

## 一、项目概览

### 这是什么

**AI漫剧工坊 (AI Manga Studio)** — 一个 AI 驱动的短剧剧本生成平台 MVP。

用户选择题材+画风+目标AI工具平台 → 输入创意 → 自动生成6模块标准化剧本包（大纲/角色/场景/台词/分镜/AI提示词）→ 内容可直接复制到即梦/Pika/Midjourney等工具中制作AI漫剧视频。

### 项目背景

- **课程**：对外经济贸易大学「全球数字创业」2026暑期学校
- **选题**：AI漫剧标准化剧本服务平台
- **阶段**：第二阶段 — MVP开发
- **负责人**：李翰霆（负责价值主张UVP + MVP开发）
- **GitHub**：https://github.com/CRUCIFIxyz/AI-Manga-Studio

### 源文件位置

```
D:\作业\全球数字创业\
├── 源文件pt.1/          # 第一阶段资料（选题/精益画布/价值主张）
├── 源文件pt.2/          # 第二阶段资料（UVP讲稿/痛点分析/解决方案PPT）
├── 任务pt.1/            # 第一阶段输出（图表/PPT内容）
└── 任务pt.2/mvp/        # ← 当前工作目录（MVP代码）
```

---

## 二、当前项目状态

### 分支结构

| 分支 | 状态 | 说明 |
|------|:--:|------|
| `master` | 稳定 | 基线版本，含完整UI+单次API调用模式 |
| `pt.2-MVP_1.1` | **活跃** | Harness流水线版本，含9个MD约束文档+6步引擎+SSE实时进度+设计系统优化 |

### 当前工作分支：`pt.2-MVP_1.1`

最新提交：`dbd421d` — "Harness强化审查：9文档全面升级 + 引擎阈值对齐 + README同步"

### 文件清单

```
D:\作业\全球数字创业\任务pt.2\mvp\
├── .env                              # API密钥（不提交git，需手动创建）
├── .gitignore                        # 排除.env、输出剧本/、__pycache__
├── requirements.txt                  # flask, python-dotenv, requests
├── app.py                            # Flask后端（~740行）
├── harness_engine.py                 # Harness流水线引擎（~400行）
├── DEVELOPMENT_SPEC.md               # 开发规范文档
├── README.md                         # 项目README
│
├── templates/
│   └── index.html                    # 前端页面（三栏Dashboard）
│
├── static/
│   ├── style.css                     # 马卡龙色系样式
│   └── script.js                     # 前端交互逻辑
│
├── harness/                          # ← v3.3 新增
│   ├── PIPELINE.md                   # 6步流水线架构总控
│   ├── CONSTRAINTS.md                # 7条全局约束
│   ├── CONSISTENCY.md                # 6条跨模块一致性规则
│   └── steps/
│       ├── STEP_01_outline.md        # 大纲生成规范
│       ├── STEP_02_characters.md     # 角色设定规范
│       ├── STEP_03_scenes.md         # 场景描述规范
│       ├── STEP_04_dialogue.md       # 分集台词规范
│       ├── STEP_05_storyboard.md     # 分镜脚本规范
│       └── STEP_06_prompts.md        # AI提示词规范
│
└── 输出剧本/                         # 生成内容存档（不提交git）
    └── {题材}_{关键词}_{时间戳}/
        ├── 01_剧本大纲.md
        ├── 02_角色设定.md
        ├── 03_场景描述.md
        ├── 04_分集台词.md
        ├── 05_分镜脚本.md
        └── 06_AI提示词.md
```

---

## 三、已完成功能

### 前端（templates/index.html + static/）

- [x] 三栏Dashboard布局（侧边栏+主内容+状态面板）
- [x] 马卡龙粉色系UI（#F598A8草莓/#FAB8C4蜜桃/#FCD5E0樱花/#A8D8C8薄荷）
- [x] 6题材选择（校园奇幻/都市逆袭/古风仙侠/科幻末世/悬疑推理/甜宠现言）
- [x] 10种画风下拉选择
- [x] 1图像平台+1视频平台单选（下拉滑动面板）
- [x] 右上角中英文语言切换
- [x] Canvas粒子背景动画
- [x] 流光进度条 + 6步骤节点依次点亮动画
- [x] 生成结果6个Tab展示 + Markdown渲染
- [x] 复制全部/下载Markdown/分模块复制 快捷操作
- [x] 历史记录查看

### 后端 — 单次模式（app.py: `/generate`）

- [x] DeepSeek Chat API 调用（temperature=0.8, max_tokens=8192）
- [x] 单次System Prompt生成全部6模块
- [x] 分平台提示词格式（10种画风 × 4图像平台 × 6视频平台）
- [x] 正则解析Markdown按 `## 0X` 拆分为6模块
- [x] 模块保存为UTF-8 Markdown文件
- [x] 参数校验（题材白名单、集数1-10、创意非空）
- [x] 错误处理（超时504、API异常502、内部错误500）

### 后端 — Harness模式（app.py: `/generate_harness`）

- [x] 6步顺序流水线引擎（harness_engine.py）
- [x] 每步独立API调用 + SSE实时进度推送
- [x] 前端Harness模式开关（快速/严格模式切换）
- [x] 前置步骤数据强制注入后续prompt
  - STEP 01大纲 → 注入STEP 02角色生成
  - STEP 02角色名 → 注入STEP 04/05/06
  - STEP 03场景名 → 注入STEP 04/05/06
  - STEP 02角色外貌 → 注入STEP 05分镜
- [x] 每步完成后运行校验（36条规则），失败自动重试最多2次
- [x] 角色名一致性强制检查（V05-06：新角色名=0 → RETRY）
- [x] 平台匹配检查（V06-01/V06-02/V06-08）

### 约束文档体系

- [x] PIPELINE.md — 6步架构 + 数据传递定义 + 三层校验体系
- [x] CONSTRAINTS.md — 7条全局约束（语言/原创/钩子/时长/格式/角色完整性/安全）+ 适用矩阵
- [x] CONSISTENCY.md — 6条跨模块一致性规则 + 自动化覆盖率表
- [x] STEP_01~06 — 每步含 Input/SystemPrompt/Output/Validation + 反例示范

---

## 四、如何运行

### 环境

- Python 3.11+（Windows 10）
- bash (git-bash / MSYS)

### 启动步骤

```bash
cd D:\作业\全球数字创业\任务pt.2\mvp

# 1. 安装依赖（首次）
pip install -r requirements.txt

# 2. 确认 .env 文件存在且API Key有效
# .env 内容：
# DEEPSEEK_API_KEY=sk-你的密钥
# DEEPSEEK_API_BASE=https://api.deepseek.com/v1

# 3. 启动
python app.py
# → http://127.0.0.1:5000

# 4. 测试单次模式
curl -X POST http://127.0.0.1:5000/generate \
  -H "Content-Type: application/json" \
  -d '{"genre":"campus_fantasy","idea":"猫在魔法学院","episodes":1,"art_style":"ghibli","img_platform":"jimeng","vid_platform":"pika"}'

# 5. 测试Harness模式
curl -X POST http://127.0.0.1:5000/generate_harness \
  -H "Content-Type: application/json" \
  -d '{"genre":"campus_fantasy","idea":"猫在魔法学院","episodes":1,"art_style":"ghibli","img_platform":"midjourney","vid_platform":"pika"}'
```

### Git操作

```bash
# 查看分支
git branch -a

# 切换到稳定版
git checkout master

# 切换到Harness版
git checkout pt.2-MVP_1.1

# 拉取最新
git pull origin pt.2-MVP_1.1

# 回滚到基线
git checkout a1d7564
```

---

## 五、当前问题与踩过的坑

### 🔴 已知问题

| # | 问题 | 影响 | 建议 |
|---|------|------|------|
| 1 | **Harness模式耗时较长** | 6次API调用约3-5分钟 vs 单次约60秒 | 前端进度条需要适配Harness的6步节奏；后续可考虑STEP 02+03并行（互不依赖） |
| 2 | **CONSISTENCY.md 的 R2/R3/R6 未完全自动化** | 外貌关键词/场景名/钩子跨步骤一致性目前靠prompt注入软约束，未做代码级硬校验 | 后续完善 `harness_engine.py` 中的 `_validate_step()` |
| 3 | **GitHub SSH连接在代理环境下超时** | 全局git config有 `url.git@github.com:.insteadof=https://github.com/`，导致每次push用SSH | 已改用HTTPS remote；如再超时用 `gh` CLI |
| 4 | **Flask debug模式热重载可能不一致** | 修改app.py后第一次请求可能跑旧代码 | 改代码后手动重启Flask确保加载最新版本 |
| 5 | **温度参数有两套** | `/generate` 用0.8，Harness引擎用0.7 | 统一到0.7或做成可配置参数 |

### 💀 踩过的坑

1. **git-filter-repo清除了BUSINESS_FLOW.md和DEMO_SCRIPT.md**
   - 原因：用git-filter-repo清除历史中的API Key时，filter-repo重写了全部commit hash，导致部分文件丢失
   - 解决：用 `git checkout <old-commit> -- <file>` 手动恢复
   - 教训：filter-repo前确保所有文件都已commit，操作后立即验证文件完整性

2. **f-string内嵌 `chr(10).join()` 导致语法错误**
   - Python 3.11不允许f-string表达式内含反斜杠
   - 解决：将join值预计算为变量，f-string中只引用变量

3. **System Prompt英→中→英反复切换**
   - 第一版用英文，Phase 1改成中文（认为中文输出应该用中文指令），结果用户要求保留英文
   - 最终方案：System Prompt用英文（当前 `build_system_prompt` 保持英文），Harness各步骤prompt用中文（因为01-05输出中文）

4. **前端平台选择从checkbox改为radio时JS未同步更新**
   - `getSelectedPlatforms()` 返回的key从 `imgPlatforms[]` 变成 `imgPlatform`（单值），后端/api需同步修改

5. **GitHub Secret Scanning拦截推送**
   - DEVELOPMENT_SPEC.md 中写了真实的API Key示例
   - 解决：用git-filter-repo清除全部历史 → 重新推送

---

## 六、下一步计划

### 🔥 高优先级

| 任务 | 说明 |
|------|------|
|| **Harness前端适配** | ~~index.html 中的进度条目前假设单次API调用（均匀6段），需适配Harness的实际6步节奏（每步完成一次跳跃）~~ ✅ 已完成：SSE流式推送 + 前端实时消费 |
| **STEP 02+03并行化** | 角色设定和场景描述互不依赖，可并行调用API，缩短总耗时约40% |
| **V06-08完善** | 当前仅检查Midjourney/Pika，需扩展到全部10个平台的交叉排除逻辑 |
| **流式输出** | DeepSeek支持stream=True，可实现打字机效果逐模块展示 |

### 🟡 中优先级

| 任务 | 说明 |
|------|------|
| **一致性R2/R3/R6硬校验** | 提取颜色词/场景名进行跨步骤强制对比 |
| **温度参数统一** | `/generate` 和 `/generate_harness` 统一到0.7 |
| **前端Harness模式开关** | 在UI上加一个"Harness严格模式"切换按钮 |
| **输出格式校验增强** | STEP_05表格格式检查、STEP_06代码块检查 |

### 🟢 低优先级

| 任务 | 说明 |
|------|------|
| **用户系统** | 历史记录持久化到SQLite |
| **配音集成** | 调用ElevenLabs/Minimax TTS API |
| **多集并行** | 多集剧本用多个API并行生成 |
| **Docker部署** | 方便非Python用户使用 |

---

## 七、关键API参数速查

### DeepSeek API

```
POST https://api.deepseek.com/v1/chat/completions
Authorization: Bearer {DEEPSEEK_API_KEY}
{
  "model": "deepseek-chat",
  "messages": [...],
  "temperature": 0.7 (Harness) / 0.8 (单次),
  "max_tokens": 4096 (Harness单步) / 8192 (单次),
  "stream": false
}
```

### 前端 → 后端参数

```json
{
  "genre": "campus_fantasy",        // 题材key
  "idea": "猫在魔法学院",            // 用户创意
  "episodes": 2,                     // 集数 1-10
  "art_style": "ghibli",            // 画风key
  "img_platform": "midjourney",     // 图像平台key
  "vid_platform": "pika"            // 视频平台key
}
```

### 平台key对照表

**图像平台**：`jimeng`, `midjourney`, `happyhorse`, `stablediffusion`
**视频平台**：`jimeng_video`, `pika`, `kling`, `hailuo`, `happyhorse_video`, `runway`
**画风**：`ghibli`, `shinkai`, `anime`, `webtoon`, `disney`, `cinematic`, `cyberpunk`, `guofeng`, `picturebook`, `pixel`

---

## 八、重要文件索引

| 文件 | 行数 | 用途 |
|------|:--:|------|
| `app.py` | ~740 | Flask主程序，两个路由 `/generate` 和 `/generate_harness` |
| `harness_engine.py` | ~400 | Harness流水线引擎，`run_pipeline()` 入口 |
| `harness/PIPELINE.md` | ~100 | 流水线架构总控 |
| `harness/CONSTRAINTS.md` | ~80 | 7条全局约束 + 适用矩阵 |
| `harness/CONSISTENCY.md` | ~90 | 6条跨模块规则 + 自动化覆盖率 |
| `harness/steps/STEP_01~06.md` | 各~100 | 每步的详细规范 |
| `templates/index.html` | ~410 | 前端单页面 |
| `static/script.js` | ~690 | 前端全部交互逻辑 |
| `static/style.css` | ~1100 | 全部样式 |

---

## 九、Git提交历史（精简）

```
dbd421d  Harness强化审查：9文档全面升级 + 引擎阈值对齐 + README同步
9c92444  Harness多步流水线体系：9个MD文档约束 + 6步引擎 + 每步校验+重试
2271da8  做了一些适当调整
b73a2a2  README：移除课程信息段落和Built with标签
ca22d2e  清理：移除 BUSINESS_FLOW.md 和 DEMO_SCRIPT.md
ff2c920  文档：README.md
6f2760c  文档：演示视频拍摄脚本
d0cfb51  文档：完整业务流程梳理
6a9bae5  v3.2: 单选平台 + 强力约束prompt
c79568b  v3.1: 扩充画风10种 + 下拉面板UI
edd8441  v3.0: 分平台提示词优化
3ef419f  Phase 2: 负面提示词强制输出
1fa0ce8  Phase 1: System Prompt重构 v2.0
a1d7564  初始化MVP（基线版本）
```

---

*本文档写给下一个无上下文的会话。如需更详细的技术细节，请阅读 `DEVELOPMENT_SPEC.md` 和各 `harness/` 下的MD文档。*
