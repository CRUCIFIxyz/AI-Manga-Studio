# STEP 06: AI生成提示词 (Prompts)

> 流水线最后一步。根据分镜表和平台选择，生成可直接复制使用的英文AI提示词。
> **核心约束：只生成用户选中平台的提示词，不生成未选中平台的格式。**

---

## Input Variables

| 变量 | 来源 | 类型 | 必填 |
|------|------|------|:--:|
| `{art_desc}` | 用户画风 | 画风英文描述 | ✅ |
| `{art_negative}` | 用户画风 | 负面提示词 | ✅ |
| `{character_appearances}` | STEP 02 | 角色外貌Map | ✅ |
| `{scene_descriptions}` | STEP 03 | 场景描述Map | ✅ |
| `{storyboard_full}` | STEP 05 | 分镜全文 | ✅ |
| `{img_platform}` | 用户选择 | 图像平台ID | ✅ |
| `{vid_platform}` | 用户选择 | 视频平台ID | ✅ |

---

## System Prompt Template

```
You are an AI prompt engineer. Generate platform-specific prompts.

**CRITICAL RULE**: ONLY generate prompts for the EXACT platforms specified below.
DO NOT generate prompts for platforms the user did NOT select.

ART STYLE: {art_desc}
NEGATIVE PROMPT: {art_negative}

CHARACTERS (copy exact appearance keywords):
{character_appearances}

SCENES (copy exact scene names):
{scene_descriptions}

STORYBOARD (reference these shot numbers):
{storyboard_full}

SELECTED IMAGE PLATFORM: {img_platform}
SELECTED VIDEO PLATFORM: {vid_platform}

Generate prompts labeled by shot number. ALL prompts in English.
Image prompts: ≥5. Video prompts: ≥3.
```

---

## Platform-Specific Output Formats

### 图像平台（仅生成 {img_platform} 的格式）

#### 即梦/Flux (jimeng)
```
### Image Prompts for Jimeng / Flux

**Shot SXXX**:
```
[Art style: {art_desc}], [Character appearance from above], [Action from storyboard], [Scene from above], [Lighting], [Quality: 8K, highly detailed, masterpiece] --ar 16:9

Negative prompt: {art_negative}
```
```

#### Midjourney (midjourney)
```
### Image Prompts for Midjourney

**Shot SXXX**:
```
[Character] in [Scene], [Action], {art_desc}, [Lighting] --ar 16:9 --style expressive --niji 6

--no {art_negative}
```
```

#### HappyHorse (happyhorse)
```
### Image Prompts for HappyHorse

**Shot SXXX**:
```
Scene: [Scene name]
Character: [Appearance keywords]
Action: [Description]
Style: {art_desc}
Mood: [Atmosphere]
Camera: [wide / medium / close-up]
```
```

#### Stable Diffusion (stablediffusion)
```
### Image Prompts for Stable Diffusion

**Shot SXXX**:
```
({art_desc}), [Character], [Action], [Scene], [Lighting], masterpiece, best quality, 8K

Negative prompt: {art_negative}, lowres, bad anatomy, bad hands, text, error, cropped, worst quality, low quality, jpeg artifacts, signature, watermark, blurry
```
```

### 视频平台（仅生成 {vid_platform} 的格式）

#### 即梦视频 (jimeng_video)
```
### Video Prompts for Jimeng

**Shot SXXX**:
```
Reference: [Character ref] + [Scene ref]
Action: [Detailed motion]
Camera: [Pan/Zoom/Static]
Style: {art_desc}, cinematic, 8K
Motion strength: [1-10, recommend 5-7]
Duration: 6s
```
```

#### Pika/PixVerse (pika)
```
### Video Prompts for Pika / PixVerse

**Shot SXXX**:
```
[Character], [Motion: EXACT camera movement + character action], [Scene], {art_desc}, cinematic, 8K
Motion intensity: [low / medium / high]
Duration: 10s
```
```

#### Kling/可灵 (kling)
```
### Video Prompts for Kling

**Shot SXXX**:
```
START FRAME: [Character] in [Scene], [initial pose], {art_desc}
END FRAME: [Character] in [Scene], [different final pose], {art_desc}
ACTION: [Precise transition description]
Style: {art_desc}, cinematic, 8K
Duration: 5-8s
```
```

#### Hailuo/海螺 (hailuo)
```
### Video Prompts for Hailuo

**Shot SXXX**:
```
[Scene] with [Character], [Action+motion], {art_desc}, smooth camera, film grain, cinematic grade, 8K
Camera: [static / pan / zoom / tracking]
Duration: 10s
```
```

#### HappyHorse视频 (happyhorse_video)
```
### Video Prompts for HappyHorse

**Shot SXXX**:
```
Element 1 (Character): [Character ref]
Element 2 (Background): [Scene ref]
Element 3+: [Props/FX]
Interaction: [How elements interact]
Style: {art_desc}, cohesive lighting, 8K
Animation: [Full / Character only / Camera only / Parallax]
Duration: 8s
```
```

#### Runway Gen-3 (runway)
```
### Video Prompts for Runway Gen-3

**Shot SXXX**:
```
Base: [Character] in [Scene], [Action], {art_desc}, cinematic, film grain, 24fps
Motion Brush:
- Region 1 (head/face): [micro-movements]
- Region 2 (body): [natural motion]
- Region 3 (bg): [environmental motion]
Camera: [Static / Slow pan / Gentle zoom]
Style Preset: Cinematic
Duration: 5-8s
```
```

---

## Validation Rules

| 规则ID | 检查项 | 条件 | 失败动作 |
|--------|--------|------|---------|
| V06-01 | 输出中图像平台名与 `{img_platform}` 一致 | 字符串匹配 | RETRY |
| V06-02 | 输出中视频平台名与 `{vid_platform}` 一致 | 字符串匹配 | RETRY |
| V06-03 | 图像prompt数 ≥ 5 | count ≥ 5 | RETRY |
| V06-04 | 视频prompt数 ≥ 3 | count ≥ 3 | RETRY |
| V06-05 | prompt标注了分镜号（S\d{3}） | 正则匹配 | WARN |
| V06-06 | 全文无中文字符（C1强制执行） | 中文字符=0 | RETRY |
| V06-07 | 含 "Negative prompt" 或 "negative" 关键字 | 字符串包含 | RETRY |
| V06-08 | 未生成未选中平台的格式（如选Midjourney不应含Kling格式） | 反向检查 | RETRY |

---

## Pass Output

```json
{
  "image_prompts": [{"shot": "S101", "prompt": "...", "negative": "..."}, ...],
  "video_prompts": [{"shot": "S101", "prompt": "...", ...}, ...],
  "raw_content": "完整Markdown文本"
}
```
