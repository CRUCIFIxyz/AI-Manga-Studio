# 🎬 AI Manga Studio — AI漫剧工坊

> **AI短剧剧本界的Canva** — 选题材、写想法、拿成品。一键生成6模块标准化剧本包，直接用于即梦/Pika/Midjourney等主流AI视频工具。

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![DeepSeek](https://img.shields.io/badge/AI-DeepSeek-purple.svg)](https://deepseek.com/)
[![License](https://img.shields.io/badge/License-Apache%202.0-orange.svg)](LICENSE)

---

## 📖 目录

- [项目简介](#项目简介)
- [为什么需要这个产品](#为什么需要这个产品)
- [核心功能](#核心功能)
- [三大壁垒](#三大壁垒)
- [技术架构](#技术架构)
- [快速开始](#快速开始)
- [使用指南](#使用指南)
- [项目结构](#项目结构)
- [支持的平台](#支持的平台)
- [输出格式](#输出格式)
- [Harness流水线约束体系](#harness流水线约束体系)
- [开发历史](#开发历史)

---

## 项目简介

**AI漫剧工坊** 是一个 AI 驱动的短剧剧本生成平台。用户只需选择题材、输入创意想法，AI 自动生成一整套标准化的剧本制作包——包含剧本大纲、角色设定、场景描述、分集台词、分镜脚本，以及最关键的——**可直接复制到即梦/Pika/Midjourney/Kling等AI工具中使用的英文提示词**。

---

## 为什么需要这个产品

### 市场背景（数据来源：DataEye《2025年漫剧数据报告》）

| 指标 | 数据 |
|------|------|
| 2025年漫剧市场规模 | **168亿人民币** |
| 2026年预估市场规模 | **243.6亿人民币**（+45%） |
| AIGC漫剧全年播放增长 | **181倍** |
| AI工具降本 | 生产成本↓70%，效率↑80% |

### 创作者痛点

1. **个人创作者水平参差** — 缺乏专业影视知识（如开头吸引力、分镜设计）
2. **从剧本到AI工具的"翻译"工序繁琐** — 拿到文字稿 → 手工拆镜头 → 定画风 → 写提示词 → 才能渲染
3. **效率瓶颈** — 外聘编剧一周出一套，产能无法规模化
4. **版权风险** — 从不明来源购买的剧本可能涉及IP侵权

### 我们的解决方案

> **把"翻译"工序砍掉。** 用户输入想法 → 拿到一个文件 → 打开即梦/Pika → 直接渲染。

---

## 核心功能

### 🎭 6题材 × 10画风 × 10平台 = 自由组合

- **6种题材**：校园奇幻、都市逆袭、古风仙侠、科幻末世、悬疑推理、甜宠现言
- **10种画风**：吉卜力、新海诚、日系二次元、韩系漫画、美式卡通、写实电影感、赛博朋克、国风古韵、治愈绘本、像素复古
- **单选平台**：1个图像平台（即梦/Midjourney/HappyHorse/Stable Diffusion）× 1个视频平台（即梦/Pika/Kling/Hailuo/HappyHorse/Runway）

### 📦 一键生成6模块剧本包

| 模块 | 内容 | 语言 |
|------|------|:--:|
| ① 剧本大纲 | 世界观 + 故事梗概 + 分集大纲（每集含悬念钩子）| 中文 |
| ② 角色设定 | 外貌/服装/性格/标志动作 + 生图参考prompt | 中文 |
| ③ 场景描述 | 6-8个关键场景的时间/地点/画面/氛围 + 场景图prompt | 中文 |
| ④ 分集台词 | 逐集完整对话（300-500字/集）+ 结尾钩子 | 中文 |
| ⑤ 分镜脚本 | 逐镜表格（镜号/景别/画面/运镜/时长/转场）| 中文 |
| ⑥ AI提示词 | **选中平台的专属英文prompt——直接复制即用** | **英文** |

### 🌐 双语界面

右上角一键切换中文/英文UI，不影响生成内容。

### 📁 本地文件保存

每个剧本自动保存为6个Markdown文件，UTF-8编码，无乱码。

---

## 三大壁垒

| 壁垒 | 说明 |
|------|------|
| **AI原生格式** | 不是文字稿，是6模块结构化制作包。角色设定→分镜→提示词链式引用，同一角色外貌跨模块完全一致 |
| **工业化产出** | 一次API调用，~60秒，6模块全部完成。理论日产5-10套 |
| **版权保障** | System Prompt硬性约束：100%原创，不引用任何现有IP |

---

## 技术架构

```
用户浏览器 (HTML/CSS/JS)
        │
        ▼
   Flask 后端 (Python)
        │
        ├── 参数校验 + Prompt构建
        ├── _build_platform_formats()  ← 分平台格式生成器
        │
        ▼
   DeepSeek Chat API
        │  temperature=0.8
        │  max_tokens=8192
        │
        ▼
   Markdown 解析 → 拆分为6模块 → 保存文件 → 返回JSON
```

### 技术栈

| 层 | 技术 |
|----|------|
| 前端 | HTML5 + CSS3 (马卡龙色系) + Vanilla JS |
| 后端 | Python Flask 3.0+ |
| AI模型 | DeepSeek Chat (`deepseek-chat`) |
| 模板引擎 | Jinja2 |
| 输出格式 | Markdown (UTF-8) |

### 设计特点

- **Dashboard三栏布局**：侧边栏导航 + 主内容区 + 状态面板
- **马卡龙粉色系**：`#F598A8` 草莓 / `#FAB8C4` 蜜桃 / `#FCD5E0` 樱花 / `#A8D8C8` 薄荷
- **高级动画**：Canvas粒子背景、流光进度条、6步骤节点依次点亮、卡片淡入动画
- **响应式**：桌面三栏 → 平板两栏 → 手机单栏

---

## 快速开始

### 环境要求

- Python 3.11+
- Git

### 1. 克隆仓库

```bash
git clone git@github.com:CRUCIFIxyz/AI-Manga-Studio.git
cd AI-Manga-Studio
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置API密钥

创建 `.env` 文件（已通过 `.gitignore` 排除，不会上传到GitHub）：

```env
DEEPSEEK_API_KEY=你的DeepSeek_API_Key
DEEPSEEK_API_BASE=https://api.deepseek.com/v1
```

### 4. 启动服务

```bash
python app.py
```

浏览器打开 **http://127.0.0.1:5000**

### 5. 开始创作

1. 选择题材
2. 输入创意（例如：`一只会说话的猫在魔法学院揭开地下王国的秘密`）
3. 配置集数 + 画风
4. 选择目标平台（图像+视频各一个）
5. 点击「✨ 生成剧本」
6. 等待约60秒 → 查看6模块结果
7. 复制AI提示词 → 粘贴到即梦/Pika → 开始制作

---

## 使用指南

### 平台选择策略

| 如果你想... | 推荐图像平台 | 推荐视频平台 |
|-----------|------------|------------|
| 追求画质 | Midjourney | Runway Gen-3 |
| 追求速度 | 即梦/Flux | 即梦（图生视频） |
| 元素自由组合 | HappyHorse | HappyHorse（视频） |
| 开源免费 | Stable Diffusion | — |
| 国内使用 | 即梦/Flux | Kling/可灵 |
| 精确运镜控制 | — | Pika/PixVerse |

### 画风选择建议

| 适合题材 | 推荐画风 |
|---------|---------|
| 校园/日常 | 吉卜力、日系二次元、治愈绘本 |
| 恋爱/甜宠 | 韩系漫画、新海诚 |
| 科幻/战斗 | 赛博朋克、写实电影感 |
| 古装/仙侠 | 国风古韵 |
| 搞笑/轻松 | 美式卡通、像素复古 |

### 查看历史记录

生成的剧本保存在 `输出剧本/` 目录下。也可点击左侧「📂 已生成剧本」在页面内浏览。

---

## 项目结构

```
AI-Manga-Studio/
├── app.py                    # Flask后端（路由 + API调用 + 文件保存）
├── requirements.txt          # Python依赖
├── .env                      # API密钥（不提交git）
├── .gitignore                # Git排除规则
│
├── templates/
│   └── index.html            # 前端页面（三栏Dashboard布局）
│
├── static/
│   ├── style.css             # 马卡龙色系样式 + 响应式 + 动画
│   └── script.js             # 前端交互 + 语言切换 + 进度动画
│
├── 输出剧本/                  # 生成内容存档（不提交git）
│   └── {题材}_{关键词}_{时间戳}/
│       ├── 01_剧本大纲.md
│       ├── 02_角色设定.md
│       ├── 03_场景描述.md
│       ├── 04_分集台词.md
│       ├── 05_分镜脚本.md
│       └── 06_AI提示词.md
│
├── harness/                   # Harness流水线约束体系
│   ├── PIPELINE.md            # 6步架构 + 数据传递定义
│   ├── CONSTRAINTS.md         # 7条全局约束
│   ├── CONSISTENCY.md         # 6条跨模块一致性规则
│   └── steps/
│       ├── STEP_01_outline.md
│       ├── STEP_02_characters.md
│       ├── STEP_03_scenes.md
│       ├── STEP_04_dialogue.md
│       ├── STEP_05_storyboard.md
│       └── STEP_06_prompts.md
│
├── harness_engine.py          # 流水线引擎（~400行）
├── DEVELOPMENT_SPEC.md        # 开发规范文档
```

---

## 支持的平台

### 图像生成平台（4选1）

| 平台 | 专属Prompt格式特色 |
|------|-------------------|
| 🖼️ 即梦 / Flux | `--ar 16:9` + Negative prompt |
| 🎨 Midjourney | `--niji 6 --style expressive` + `--no` |
| 🐴 HappyHorse | 结构化字段（Scene/Character/Action/Style/Mood/Camera）|
| 🎯 Stable Diffusion | 括号包裹 + 标准负面提示词模板 |

### 视频生成平台（6选1）

| 平台 | 核心技术参数 |
|------|------------|
| 🎬 即梦（图生视频） | Motion strength (1-10)，推荐5-7 |
| 🎥 Pika / PixVerse | Motion intensity + 显式运镜方向 |
| 🎞️ Kling / 可灵 | START FRAME → END FRAME + ACTION |
| 🌊 Hailuo / 海螺 | Camera类型枚举（7种） |
| 🐴 HappyHorse（视频） | Element1+2+3 分层 + Animation type |
| 🚀 Runway Gen-3 | Motion Brush 分区域（3+ Region） |

---

## 输出格式

### 生成的AI提示词示例（选中Midjourney + Pika时）

```
### SELECTED IMAGE PLATFORM: Midjourney
[Character from 02] in [Scene from 03], walking forward, 
Studio Ghibli style, morning sunlight, --ar 16:9 --style expressive --niji 6
--no photorealistic, 3D render, low quality

### SELECTED VIDEO PLATFORM: Pika / PixVerse
[Character from 02], Motion: camera slowly pans right while 
character walks forward, hair blowing gently in breeze, 
[Scene from 03], cinematic lighting, 8K
Motion intensity: medium
Duration: 10 seconds
```

> ⚡ 这些提示词可以直接复制粘贴到对应工具中使用——**无需任何手动调整**。

---

## Harness流水线约束体系

> v3.3 新增。通过9个MD文档 + 6步顺序引擎，对剧本生成全流程进行规范化约束。

### 为什么需要Harness

单次API调用（`/generate`）的问题是：6个模块在一个prompt中生成，AI注意力分散，容易出现模块间角色名不一致、分镜引用错误、平台格式混乱。Harness将生成拆为6步流水线，**每一步的输出数据强制注入后续步骤的prompt**，从根本上消除一致性风险。

### 架构

```
STEP 01 大纲 ──→ STEP 02 角色 ──→ STEP 03 场景 ──→ STEP 04 台词 ──→ STEP 05 分镜 ──→ STEP 06 提示词
    │               │               │               │               │               │
    └── 提取大纲 ──→ 注入角色名 ──→ 注入场景名 ──→ 注入外貌Map ──→ 注入分镜表 ──→ 注入平台选择
```

### 约束文档体系

| 文档 | 内容 | 约束数 |
|------|------|:--:|
| `harness/PIPELINE.md` | 6步架构 + 数据传递 + 三层校验体系 | — |
| `harness/CONSTRAINTS.md` | 7条全局约束（语言/原创/钩子/时长/格式/角色完整性/安全） | 7 |
| `harness/CONSISTENCY.md` | 6条跨模块一致性规则（角色名/外貌/场景名/集数/平台/钩子） | 6 |
| `harness/steps/STEP_01~06.md` | 每步的Input/SystemPrompt/Output/Validation | 36条校验规则 |

### 两种模式

| | `/generate`（原有） | `/generate_harness`（新增） |
|:---|:---:|:---:|
| API调用 | 1次 | 6次 |
| 一致性保障 | prompt约束 | 前置数据强制注入 ✅ |
| 每步校验 | 无 | 最多重试2次 ✅ |
| 约束文档 | 代码内嵌 | 9个MD独立管理 ✅ |

### 使用方式

```bash
# Harness流水线（推荐）
curl -X POST http://127.0.0.1:5000/generate_harness \
  -H "Content-Type: application/json" \
  -d '{"genre":"campus_fantasy","idea":"猫在魔法学院","episodes":2,"art_style":"ghibli","img_platform":"midjourney","vid_platform":"pika"}'
```

---

## 开发历史

| 版本 | 提交 | 内容 |
|:---:|------|------|
| v1.0 | `a1d7564` | MVP基线：Flask后端 + HTML前端 + 6模块生成 |
| v1.1 | `1fa0ce8` | Phase 1: System Prompt重构（中文指令） |
| v1.2 | `3ef419f` | Phase 2: 负面提示词强制输出 |
| v2.0 | `edd8441` | Phase 3: 分平台提示词 + 前端平台选择 |
| v3.0 | `6a9bae5` | 扩充：10种画风 + 6个视频平台 + 下拉面板UI |
| v3.2 | `6f2760c` | 单选平台 + CRITICAL/EXACTLY/KEY RULES三重约束 |
| v3.3 | `9c92444` | **Harness流水线**：9个MD约束文档 + 6步引擎 + 每步校验+重试 |

### Git分支

- `master` — 稳定版本
- `pt.2-MVP_1.1` — 实验分支

```bash
# 回滚到基线版本
git checkout a1d7564

# 查看完整历史
git log --oneline
```

---
