# AI漫剧工坊 — Demo Script (2-Minute Bilingual)

> **AI Manga Studio** — AI-Powered Short Drama Script Generator MVP
>
> Target: **~2 minutes** | Format: EN + 中文 bilingual | Video generation wait time excluded

---

## Timeline

| # | Section | Time |
|---|---------|:---:|
| 1 | Opening + Product Positioning | 15s |
| 2 | Quick UI Tour | 15s |
| 3 | Generation Demo (core) | 45s |
| 4 | Result Highlight | 25s |
| 5 | Features + Wrap Up | 20s |

---

## ① Opening + Positioning (15s)

### Visual

Browser full-screen at `http://127.0.0.1:5000`. Show the complete homepage. **Don't move the mouse** for 3s.

### Narration

> **EN** &nbsp;&nbsp;| This is AI Manga Studio — an AI script generator for short drama creators. The problem it solves is simple: creators spend hours translating a text script into AI image and video prompts for each shot. We cut out that translation step entirely. You input an idea, and it outputs a complete production package — ready to use in Jimeng, Pika, Midjourney, and more.

> **CN** &nbsp;&nbsp;| 这是AI漫剧工坊——AI短剧剧本生成器。它解决的问题很简单：创作者拿到文字剧本后，需要手工把每个镜头翻译成AI图像和视频工具的提示词。我们把这个翻译工序砍掉了——你输入想法，它直接输出一套完整的制作包。

---

## ② Quick UI Tour (15s)

### Visual

Mouse moves across the three-zone layout — left nav → center input cards → right status panel.

### Narration

> **EN** &nbsp;&nbsp;| The layout has three zones. Left sidebar: workflow navigation — input, generate, view results. Center: your creative workspace. Right: stats panel showing what you'll get — 6 modules, Markdown format, powered by DeepSeek.

> **CN** &nbsp;&nbsp;| 界面分三个区域。左侧是创作流程导航——输入创意、AI生成、查看结果。中间是创作面板。右侧状态面板显示关键信息——6个模块、Markdown格式、DeepSeek驱动。

---

## ③ Generation Demo — Core (45s)

### Visual — Step-by-step with precise mouse actions

**Step 1: Select genre (3s)**
- Click "Campus Fantasy" (校园奇幻)
- Card highlights with pink border

**Step 2: Input idea (5s)**
- Click the textarea
- Type: `A talking cat at a magic academy uncovers an underground kingdom's secret — only to discover it is the guardian spirit sealed away a thousand years ago`
- Or click the quick-fill chip "会说话的猫"

**Step 3: Configure (5s)**
- Set episodes to 2
- Art style: Anime (日系二次元)

**Step 4: Select platforms (5s)**
- Image platform: 即梦 / Flux
- Video platform: HappyHorse

**Step 5: Click Generate (2s)**
- Click the coral button "生成剧本"

### Narration

> **EN** &nbsp;&nbsp;| Pick a genre — Campus Fantasy. Type your idea — a talking cat, a magic academy, an underground kingdom. Set episodes to 2. For image generation, pick Jimeng. For video, HappyHorse. Each platform gets its own prompt format — Jimeng uses `--ar 16:9` with quality tags and a negative prompt; HappyHorse takes a structured layered approach with separate character, background, and props elements plus an interaction definition. Hit generate.

> **CN** &nbsp;&nbsp;| 选题材——校园奇幻。输入创意——会说话的猫、魔法学院、地下王国的秘密。集数调两集。图像平台选即梦，视频平台选HappyHorse。每个平台都有专属的提示词格式——即梦用16:9宽高比+画质标签+负面提示词；HappyHorse采用结构化分层方式，把角色、背景、道具拆成独立元素，再定义交互方式。点击生成。

**Wait phase — show progress bar running (skip time, just narrate over it)**

> **EN** &nbsp;&nbsp;| The progress bar reflects six pipeline steps — outline, characters, scenes, dialogue, storyboard, and the crucial final module: AI generation prompts. Each step lights up as it completes. About one minute, all six modules done.

> **CN** &nbsp;&nbsp;| 进度条对应六个步骤——剧本大纲、角色设定、场景描述、分集台词、分镜脚本，以及最关键的一步：AI提示词。每一步完成自动点亮。大约一分钟，六个模块全部完成。

---

## ④ Result Highlight (25s)

### Visual

Result page opens. **Focus on Tab 6 — AI Prompts (the key deliverable)**.

Click through tabs quickly (2s each), then **dwell on Tab 6 for 12s**:
- Tab 1 "① 大纲" → Tab 2 "② 角色" → Tab 3 "③ 场景" → Tab 4 "④ 台词" → Tab 5 "⑤ 分镜" → **Tab 6 "⑥ AI提示词" (⏸ dwell)**

Mouse points to:
- `SELECTED IMAGE PLATFORM: Jimeng / Flux`
- `--ar 16:9` | `8K, highly detailed, masterpiece`
- `Negative prompt: photorealistic, 3D render, low quality`
- `SELECTED VIDEO PLATFORM: HappyHorse`
- `Element 1 (Character): ...` | `Element 2 (Background): ...`
- `Interaction: character walks left-to-right across scene...`
- `Animation: Full scene motion`

### Narration

> **EN** &nbsp;&nbsp;| Six modules are generated. Outline, characters, scenes, dialogue, storyboard. But the killer feature is Module 6 — AI prompts. Because we selected Jimeng and HappyHorse, every prompt here is formatted specifically for those tools. Jimeng prompts include `--ar 16:9`, quality tags, and a negative prompt. HappyHorse prompts break each shot into layered elements — character, background, props — then define how they interact. **Copy. Paste. Render.** No manual adjustment needed. That's the core value: AI-native format, production-ready.

> **CN** &nbsp;&nbsp;| 六个模块全部生成。大纲、角色、场景、台词、分镜。但最关键的是第六个模块——AI提示词。因为我们选了即梦和HappyHorse，这里的每一条提示词都是为这两个平台专门优化的格式。即梦的加了16:9宽高比、画质标签和负面提示词；HappyHorse的把每个镜头拆成角色、背景、道具三个独立元素，再定义元素间的交互方式和动画类型。**复制、粘贴、渲染。** 不需要任何手动调整。这就是核心价值：AI原生格式，即拿即用。

---

## ⑤ Features + Wrap Up (20s)

### Visual — Quick demos (fast-paced)

- **5s**: Right-click "Copy AI Prompts" → toast "Copied ✓"
- **5s**: Click language toggle 简 → EN → back to 简 (show UI text switching)
- **10s**: Return to homepage, show full layout one last time

### Narration

> **EN** &nbsp;&nbsp;| One-click copy any module. Toggle between Chinese and English UI. That's AI Manga Studio in two minutes — pick a genre, describe your idea, get a production-ready script package. Six modules, platform-specific prompts, zero manual translation. Thank you.

> **CN** &nbsp;&nbsp;| 一键复制任意模块。中英文界面一键切换。以上就是AI漫剧工坊的两分钟演示——选题材、写想法、拿到可直接用于AI视频工具的制作包。六个模块、分平台提示词、零手工翻译。谢谢。

---

## Pre-Shoot Checklist

```
□ Flask running: python app.py → http://127.0.0.1:5000
□ Incognito browser window, 1920×1080 or 1280×720
□ Pre-generate 1 script (for history demo if needed):
   curl -X POST http://127.0.0.1:5000/generate \
     -H "Content-Type: application/json" \
     -d '{"genre":"campus_fantasy","idea":"猫在魔法学院","episodes":1,"art_style":"ghibli","img_platform":"jimeng","vid_platform":"happyhorse_video"}'
□ Creative idea ready (paste in notepad):
   "一只会说话的猫在魔法学院里揭开了地下王国的秘密，
    却发现自己是千年前被封印的守护灵"
□ Microphone tested, environment quiet
□ Screen recorder ready (OBS recommended)
□ All notifications / popups disabled
□ API key valid, balance sufficient
```

---

## Shooting Tips

| Tip | Detail |
|-----|--------|
| Mouse speed | Pause 1-2s on each element, let viewers digest |
| Scroll speed | Slow, steady — especially result tabs |
| Voice | Natural, conversational — like showing a friend |
| Backup plan | Pre-generated result ready in case API is slow |
| Highlight clicks | Enable "show mouse clicks" in OBS |
| Zoom | Zoom in on AI prompt text for the key reveal |

---

*Script optimized for 2-minute delivery. Section ③ (generation) is the core — spend the most time on the Tab 6 AI prompts reveal at ④. Cut or shorten ② and ⑤ if runtime is tight.*
