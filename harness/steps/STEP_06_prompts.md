# STEP 06: AI生成提示词 (Prompts)

> 流水线最后一步。根据分镜表和平台选择，生成可直接复制使用的英文AI提示词。
> **这是产品核心价值所在**——分平台专属格式，拿来即用。

---

## Input Variables

| 变量 | 来源 | 类型 | 必填 |
|------|------|------|:--:|
| `{art_desc}` | 用户画风选择 | 画风英文描述 | ✅ |
| `{art_negative}` | 用户画风选择 | 负面提示词 | ✅ |
| `{character_appearances}` | STEP 02 输出 | 角色外貌Map | ✅ |
| `{scene_descriptions}` | STEP 03 输出 | 场景描述Map | ✅ |
| `{storyboard_shots}` | STEP 05 输出 | 分镜列表 | ✅ |
| `{img_platform}` | 用户选择 | 图像平台ID | ✅ |
| `{vid_platform}` | 用户选择 | 视频平台ID | ✅ |

---

## System Prompt Template

```
You are an AI prompt engineer specializing in AI video production tools.

Generate platform-specific prompts based on the following materials.

ART STYLE: {art_desc}
NEGATIVE PROMPT: {art_negative}

CHARACTERS:
{character_appearances}

SCENES:
{scene_descriptions}

STORYBOARD SHOTS (reference these shot numbers):
{storyboard_shots}

TARGET IMAGE PLATFORM: {img_platform}
TARGET VIDEO PLATFORM: {vid_platform}
```

---

## Platform-Specific Output Formats

### 图像平台

#### 即梦/Flux (jimeng)
```
**Shot SXXX** (reference storyboard shot SXXX):
```
[Art style: {art_desc}], [Character description from characters above], [Action from storyboard], [Scene from scenes above], [Lighting], [Quality tags: 8K, highly detailed, masterpiece] --ar 16:9

Negative prompt: {art_negative}
```
```

#### Midjourney (midjourney)
```
**Shot SXXX**:
```
[Character] in [Scene], [Action], {art_desc}, [Lighting details] --ar 16:9 --style expressive --niji 6

--no {art_negative}
```
```

#### HappyHorse (happyhorse)
```
**Shot SXXX**:
```
Scene: [Scene name]
Character: [Appearance keywords]
Action: [What character is doing]
Style: {art_desc}
Mood: [Atmosphere keyword]
Camera: [wide / medium / close-up]
```
```

#### Stable Diffusion (stablediffusion)
```
**Shot SXXX**:
```
({art_desc}), [Character], [Action], [Scene], [Lighting], masterpiece, best quality, 8K, highly detailed

Negative prompt: {art_negative}, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry
```
```

### 视频平台

#### 即梦视频 (jimeng_video)
```
**Shot SXXX**:
```
Reference image: [Character reference] + [Scene reference]
Action: [Detailed motion description]
Camera: [Pan left / Pan right / Zoom in / Zoom out / Static]
Style: {art_desc}, cinematic lighting, smooth motion, 8K
Motion strength: [1-10, recommend 5-7]
Duration: 6 seconds
```
```

#### Pika/PixVerse (pika)
```
**Shot SXXX**:
```
[Character], [Motion: EXACT camera movement + character action], [Scene], {art_desc}, cinematic lighting, 8K

Motion intensity: [low / medium / high]
Duration: 10 seconds
```
```

#### Kling/可灵 (kling)
```
**Shot SXXX**:
```
START FRAME: [Character] in [Scene], [exact initial pose], {art_desc}
END FRAME: [Character] in [Scene], [exact final pose - must differ], {art_desc}
ACTION DURING TRANSITION: [Precise description]
Style: {art_desc}, cinematic, 8K
Duration: 5-8 seconds
```
```

#### Hailuo/海螺 (hailuo)
```
**Shot SXXX**:
```
[Scene] with [Character], [Detailed action + motion], {art_desc}, smooth camera movement, film grain, cinematic color grade, 8K

Camera: [static / pan left / pan right / zoom in / zoom out / tracking shot]
Duration: 10 seconds
```
```

#### HappyHorse视频 (happyhorse_video)
```
**Shot SXXX**:
```
Element 1 (Character): [Character reference]
Element 2 (Background): [Scene reference]
Element 3+ (Props/FX): [Any additional elements]
Interaction: [How elements interact]
Style: {art_desc}, cohesive lighting, 8K
Animation: [Full scene motion / Character only / Camera only / Parallax layers]
Duration: 8 seconds
```
```

#### Runway Gen-3 (runway)
```
**Shot SXXX**:
```
Base prompt: [Character] in [Scene], [Action], {art_desc}, cinematic lighting, film grain, 24fps

Motion Brush regions:
- Region 1 (head/face): [subtle micro-movements]
- Region 2 (body/clothing): [natural movement]
- Region 3 (background): [environmental motion]

Camera: [Static / Slow pan / Gentle zoom]
Style Preset: Cinematic
Duration: 5-8 seconds
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
| V06-05 | 每个prompt标注了对应分镜号 | S\d{3} 格式 | WARN |
| V06-06 | prompt使用英文撰写 | 中文字符=0 | RETRY |
| V06-07 | 包含负面提示词 | "negative" 关键字 | RETRY |

---

## Pass Output

```json
{
  "image_prompts": [{"shot": "S101", "prompt": "...", "negative": "..."}, ...],
  "video_prompts": [{"shot": "S101", "prompt": "...", ...}, ...],
  "raw_content": "完整Markdown文本"
}
```
