/**
 * AI漫剧剧本生成器 MVP - 前端交互脚本
 * 路径：D:\作业\全球数字创业\任务pt.2\mvp\static\script.js
 * 功能：语言切换、粒子背景、API调用、进度动画、Tab切换、复制下载
 */

// ===== 国际化字典 =====
const i18n = {
  zh: {
    brand_name: "AI漫剧工坊",
    brand_sub: "剧本生成器 MVP",
    nav_workflow: "创作流程",
    nav_input: "填入创意",
    nav_generating: "AI生成中",
    nav_result: "查看结果",
    nav_history: "历史记录",
    nav_history_btn: "已生成剧本",
    footer_tip: "生成的AI提示词可直接用于即梦、Pika等工具",
    panel_input_title: "开始创作你的AI漫剧",
    panel_input_subtitle: "填入想法，AI自动生成完整剧本包——大纲、人设、台词、分镜、提示词一应俱全",
    card_genre_title: "选择题材",
    card_idea_title: "描述你的创意",
    card_config_title: "生成配置",
    idea_placeholder: "例如：一只会说话的猫在魔法学院里揭开了地下王国的秘密...\n\n输入关键词即可：主题 / 主角特征 / 世界观 / 核心冲突",
    hint1: "🐱 会说话的猫",
    hint2: "🔄 重生逆袭",
    hint3: "⚔️ 机甲末世",
    config_episodes: "集数",
    config_style: "画风偏好",
    btn_generate: "生成剧本",
    gen_title: "AI正在为你创作剧本...",
    gen_status: "正在调用DeepSeek大模型，预计需要30-60秒",
    step_outline: "① 剧本大纲",
    step_characters: "② 角色设定",
    step_scenes: "③ 场景描述",
    step_dialogue: "④ 分集台词",
    step_storyboard: "⑤ 分镜脚本",
    step_prompts: "⑥ AI提示词",
    result_title: "🎉 剧本生成完成",
    result_info: "已保存到输出文件夹",
    btn_copy_all: "复制全部",
    btn_download: "下载Markdown",
    btn_new: "新建剧本",
    tab_outline: "剧本大纲",
    tab_characters: "角色设定",
    tab_scenes: "场景描述",
    tab_dialogue: "分集台词",
    tab_storyboard: "分镜脚本",
    tab_prompts: "AI提示词",
    placeholder_text: "点击上方Tab查看对应模块内容",
    history_title: "📂 已生成剧本",
    btn_back: "返回创作",
    history_empty: "暂无历史记录",
    status_quick_stats: "快捷统计",
    metric_modules: "生成模块",
    metric_format: "输出格式",
    metric_api: "AI模型",
    status_progress: "生成进度",
    status_actions: "快捷操作",
    check_outline: "剧本大纲",
    check_characters: "角色设定",
    check_scenes: "场景描述",
    check_dialogue: "分集台词",
    check_storyboard: "分镜脚本",
    check_prompts: "AI提示词",
    check_review: "AI审核",
    qa_copy_prompts: "复制AI提示词",
    qa_copy_storyboard: "复制分镜脚本",
    qa_copy_outline: "复制剧本大纲",
    toast_copied: "已复制到剪贴板 ✓",
    toast_error: "生成失败，请重试",
    genre_campus: "校园奇幻",
    genre_urban: "都市逆袭",
    genre_xianxia: "古风仙侠",
    genre_scifi: "科幻末世",
    genre_mystery: "悬疑推理",
    genre_romance: "甜宠现言",
    switch_language: "切换语言",
    err_empty: "请输入创意描述",
    err_network: "网络错误，请检查连接后重试",
    err_timeout: "AI服务响应超时，请稍后重试",
    err_server: "服务器错误，请重试",
    config_harness: "严格模式",
    config_harness_off: "快速模式",
    config_harness_desc: "6步流水线校验，质量更高，耗时约3-5分钟",

    // v5.0 审核/趋势/合规
    nav_review: "AI审核",
    nav_trends: "趋势分析",
    review_title: "AI剧本审核",
    review_subtitle: "多Agent并行审查——剧情/角色/台词/格式/安全 5维度评分",
    review_select: "选择要审核的剧本",
    review_empty_hint: "请先生成剧本后再进行审核，或从历史记录中选择",
    review_start_btn: "开始审核",
    review_loading_title: "审查Agent正在并行分析",
    review_loading_sub: "5个Agent同时工作，预计10-20秒",
    review_result_title: "审核结果",
    review_score_label: "/10 综合评分",
    review_btn_compliance: "合规检测",
    review_btn_copy: "复制报告",
    compliance_title: "原创合规检测",
    compliance_subtitle: "IP侵权风险检查——30+知名IP数据库比对",
    compliance_result_title: "检测结果",
    compliance_loading_title: "正在检测原创合规性",
    compliance_loading_sub: "比对已知IP数据库，预计5-10秒",
    compliance_score_label: "/100 原创度",
    compliance_fail: "检测失败",
    trends_title: "市场趋势",
    trends_subtitle: "AI漫剧市场热门趋势分析——助你选题更精准",
    trends_loading_title: "正在分析市场趋势",
    trends_loading_sub: "AI分析中，预计10-20秒",
    trends_result_title: "市场分析",
    trends_prompt_title: "获取最新趋势",
    trends_prompt_desc: "AI将分析2025-2026年中国AI漫剧市场热门题材、关键词和题材组合",
    trends_btn: "分析市场趋势",
    trends_refresh: "刷新分析",
    trends_fail: "趋势分析失败",
    step_review: "AI审核",
    tab_review: "审核报告",
    btn_zip: "ZIP下载",
    btn_review: "AI审核",
    btn_compliance: "合规检测",
    review_no_script: "当前没有可审核的剧本",
    review_current_script: "当前生成的剧本",
    review_modules_count: "个模块",
    review_fail: "审核请求失败",
    compliance_req_fail: "检测请求失败",
    review_no_report: "暂无审核报告",
    copy_fail: "复制失败，请手动复制",
    zip_no_folder: "无法找到剧本文件夹",
    review_load_fail: "加载剧本失败",
  },

  en: {
    brand_name: "AI Manga Studio",
    brand_sub: "Script Generator MVP",
    nav_workflow: "Workflow",
    nav_input: "Enter Idea",
    nav_generating: "Generating",
    nav_result: "View Result",
    nav_history: "History",
    nav_history_btn: "Saved Scripts",
    footer_tip: "Generated AI prompts work directly with Jimeng, Pika, and more",
    panel_input_title: "Create Your AI Manga Drama",
    panel_input_subtitle: "Enter your idea — AI generates a complete script package: outline, characters, dialogue, storyboard, and prompts",
    card_genre_title: "Choose Genre",
    card_idea_title: "Describe Your Idea",
    card_config_title: "Settings",
    idea_placeholder: "Example: A talking cat at a magic academy discovers an underground kingdom...\n\nEnter keywords: theme / character traits / world / conflict",
    hint1: "🐱 Talking Cat",
    hint2: "🔄 Rebirth Revenge",
    hint3: "⚔️ Mecha Apocalypse",
    config_episodes: "Episodes",
    config_style: "Art Style",
    btn_generate: "Generate Script",
    gen_title: "AI is crafting your script...",
    gen_status: "Calling DeepSeek model, estimated 30-60 seconds",
    step_outline: "① Outline",
    step_characters: "② Characters",
    step_scenes: "③ Scenes",
    step_dialogue: "④ Dialogue",
    step_storyboard: "⑤ Storyboard",
    step_prompts: "⑥ AI Prompts",
    result_title: "🎉 Script Generated",
    result_info: "Saved to output folder",
    btn_copy_all: "Copy All",
    btn_download: "Download",
    btn_new: "New Script",
    tab_outline: "Outline",
    tab_characters: "Characters",
    tab_scenes: "Scenes",
    tab_dialogue: "Dialogue",
    tab_storyboard: "Storyboard",
    tab_prompts: "AI Prompts",
    placeholder_text: "Click a tab above to view the content",
    history_title: "📂 Saved Scripts",
    btn_back: "Back to Create",
    history_empty: "No saved scripts yet",
    status_quick_stats: "Quick Stats",
    metric_modules: "Modules",
    metric_format: "Format",
    metric_api: "AI Model",
    status_progress: "Progress",
    status_actions: "Quick Actions",
    check_outline: "Outline",
    check_characters: "Characters",
    check_scenes: "Scenes",
    check_dialogue: "Dialogue",
    check_storyboard: "Storyboard",
    check_prompts: "AI Prompts",
    check_review: "AI Review",
    qa_copy_prompts: "Copy AI Prompts",
    qa_copy_storyboard: "Copy Storyboard",
    qa_copy_outline: "Copy Outline",
    toast_copied: "Copied to clipboard ✓",
    toast_error: "Generation failed, please retry",
    genre_campus: "Campus Fantasy",
    genre_urban: "Urban Revenge",
    genre_xianxia: "Xianxia",
    genre_scifi: "Sci-Fi",
    genre_mystery: "Mystery",
    genre_romance: "Romance",
    switch_language: "Switch Language",
    err_empty: "Please enter your creative idea",
    err_network: "Network error. Check your connection and try again",
    err_timeout: "AI service timed out. Please try again later",
    err_server: "Server error. Please try again",
    config_harness: "Strict Mode",
    config_harness_off: "Fast Mode",
    config_harness_desc: "6-step pipeline with validation, higher quality, ~3-5 min",

    // v5.0 Review / Trends / Compliance
    nav_review: "AI Review",
    nav_trends: "Trends",
    review_title: "AI Script Review",
    review_subtitle: "5-agent parallel review — Plot / Characters / Dialogue / Format / Safety",
    review_select: "Select Script to Review",
    review_empty_hint: "Generate a script first, or select from history",
    review_start_btn: "Start Review",
    review_loading_title: "Review Agents Analyzing",
    review_loading_sub: "5 agents working in parallel, ~10-20s",
    review_result_title: "Review Results",
    review_score_label: "/10 Overall Score",
    review_btn_compliance: "Compliance",
    review_btn_copy: "Copy Report",
    compliance_title: "Copyright Compliance",
    compliance_subtitle: "IP infringement risk check — cross-referencing 30+ known IPs",
    compliance_result_title: "Compliance Results",
    compliance_loading_title: "Checking Originality",
    compliance_loading_sub: "Cross-referencing known IP database, ~5-10s",
    compliance_score_label: "/100 Originality",
    compliance_fail: "Check Failed",
    trends_title: "Market Trends",
    trends_subtitle: "AI manga drama market trend analysis — smarter topic selection",
    trends_loading_title: "Analyzing Market Trends",
    trends_loading_sub: "AI-powered market intelligence, ~10-20s",
    trends_result_title: "Market Analysis",
    trends_prompt_title: "Get Latest Trends",
    trends_prompt_desc: "AI analyzes 2025-2026 Chinese AI manga drama market: trending genres, keywords, and combos",
    trends_btn: "Analyze Trends",
    trends_refresh: "Refresh",
    trends_fail: "Trend analysis failed",
    step_review: "AI Review",
    tab_review: "Review Report",
    btn_zip: "ZIP Download",
    btn_review: "AI Review",
    btn_compliance: "Compliance",
    review_no_script: "No scripts available for review",
    review_current_script: "Current Script",
    review_modules_count: "modules",
    review_fail: "Review request failed",
    compliance_req_fail: "Compliance request failed",
    review_no_report: "No review report available",
    copy_fail: "Copy failed, please copy manually",
    zip_no_folder: "Cannot locate script folder",
    review_load_fail: "Failed to load script",
  }
};

let currentLang = 'zh';
let currentPanel = 'input';
let episodeCount = 5;
let generatedModules = {};
let currentTab = null;
let useHarness = false;  // Harness严格模式开关

// ===== 页面初始化 =====
document.addEventListener('DOMContentLoaded', () => {
  initGenreSelection();
  updateLangUI();
  // 点击其他区域关闭语言菜单
  document.addEventListener('click', (e) => {
    const menu = document.getElementById('langMenu');
    const btn = document.getElementById('langToggle');
    if (menu && !btn.contains(e.target)) {
      menu.classList.remove('open');
    }
  });
});

// ===== 语言切换 =====
function switchLang(lang) {
  currentLang = lang;
  document.querySelectorAll('.lang-option').forEach(opt => opt.classList.remove('active'));
  document.querySelector(`.lang-option[data-lang="${lang}"]`).classList.add('active');
  document.getElementById('langMenu').classList.remove('open');
  updateLangUI();
}

function toggleLangMenu() {
  document.getElementById('langMenu').classList.toggle('open');
}

function updateLangUI() {
  const dict = i18n[currentLang];
  document.getElementById('currentLangLabel').textContent = currentLang === 'zh' ? '简' : 'EN';
  document.documentElement.lang = currentLang === 'zh' ? 'zh-CN' : 'en';

  // 更新所有带有 data-i18n 属性的元素
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (dict[key]) {
      // 如果元素内部只有文本节点，直接替换textContent；否则只更新直接文本
      if (el.children.length === 0 || el.tagName === 'BUTTON') {
        el.textContent = dict[key];
      } else {
        // 有子元素时，只更新第一个文本节点
        for (const node of el.childNodes) {
          if (node.nodeType === Node.TEXT_NODE && node.textContent.trim()) {
            node.textContent = dict[key];
            break;
          }
        }
      }
    }
  });

  // 更新 placeholder
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    const key = el.getAttribute('data-i18n-placeholder');
    if (dict[key]) {
      el.placeholder = dict[key];
    }
  });

  // 更新 logo alt 文本
  document.querySelectorAll('[data-i18n-alt]').forEach(el => {
    const key = el.getAttribute('data-i18n-alt');
    if (dict[key]) {
      el.alt = dict[key];
    }
  });
}

function t(key) {
  return i18n[currentLang][key] || key;
}

// ===== 粒子背景 (Canvas) =====
function initParticles() {
  const canvas = document.getElementById('particleCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let particles = [];
  const maxParticles = 40;

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  resize();
  window.addEventListener('resize', resize);

  class Particle {
    constructor() {
      this.reset();
      this.y = Math.random() * canvas.height;
    }
    reset() {
      this.x = Math.random() * canvas.width;
      this.y = -10;
      this.size = Math.random() * 6 + 2;
      this.speed = Math.random() * 0.4 + 0.1;
      this.opacity = Math.random() * 0.3 + 0.05;
      this.drift = Math.random() * 0.3 - 0.15;
      // 马卡龙色系粒子
      const colors = ['#F598A8', '#FAB8C4', '#EDB8C8', '#FCD5E0', '#A8D8C8'];
      this.color = colors[Math.floor(Math.random() * colors.length)];
    }
    update() {
      this.y += this.speed;
      this.x += this.drift;
      if (this.y > canvas.height + 10) {
        this.reset();
        this.y = -10;
      }
      if (this.x < -10) this.x = canvas.width + 10;
      if (this.x > canvas.width + 10) this.x = -10;
    }
    draw(ctx) {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
      ctx.fillStyle = this.color;
      ctx.globalAlpha = this.opacity;
      ctx.fill();
      ctx.globalAlpha = 1;
    }
  }

  for (let i = 0; i < maxParticles; i++) {
    particles.push(new Particle());
  }

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach(p => { p.update(); p.draw(ctx); });
    requestAnimationFrame(animate);
  }
  animate();
}

// ===== 题材选择 =====
function initGenreSelection() {
  document.querySelectorAll('.genre-chip').forEach(item => {
    item.addEventListener('click', function() {
      document.querySelectorAll('.genre-chip').forEach(i => i.classList.remove('selected'));
      this.classList.add('selected');
      this.querySelector('input[type="radio"]').checked = true;
    });
  });
}

// ===== 下拉面板（平台单选）=====
function toggleDropdown(id) {
  const panel = document.getElementById(id);
  panel.classList.toggle('open');
}

function updateDropdownLabel(id) {
  const panel = document.getElementById(id);
  const label = panel.querySelector('[id$="Label"]');
  const selected = panel.querySelector('input[type="radio"]:checked');
  if (selected) {
    const text = selected.parentElement.textContent.trim();
    label.textContent = text;
  }
  
  // 更新选中样式
  panel.querySelectorAll('.dd-option').forEach(opt => {
    const radio = opt.querySelector('input[type="radio"]');
    opt.classList.toggle('selected', radio.checked);
  });
  
  // 选中后自动关闭下拉
  setTimeout(() => panel.classList.remove('open'), 150);
}

function getSelectedPlatforms() {
  const imgRadio = document.querySelector('#imgPlatformDropdown input[name="imgPlatform"]:checked');
  const vidRadio = document.querySelector('#vidPlatformDropdown input[name="vidPlatform"]:checked');
  return {
    imgPlatform: imgRadio ? imgRadio.value : 'jimeng',
    vidPlatform: vidRadio ? vidRadio.value : 'jimeng_video',
  };
}

// 点击外部关闭下拉
document.addEventListener('click', function(e) {
  if (!e.target.closest('.dropdown-panel')) {
    document.querySelectorAll('.dropdown-panel.open').forEach(p => p.classList.remove('open'));
  }
});
function stepEpisode(delta) {
  episodeCount = Math.max(1, Math.min(10, episodeCount + delta));
  document.getElementById('episodeCount').textContent = episodeCount;
}

// ===== 快速填充 =====
function fillHint(text) {
  document.getElementById('ideaInput').value = text;
  document.getElementById('ideaInput').focus();
}

// ===== 导航切换 =====
function navigateTo(target) {
  currentPanel = target;

  // 更新侧边栏
  document.querySelectorAll('.nav-item').forEach(item => {
    item.classList.toggle('active', item.getAttribute('data-step') === target);
  });

  // 切换面板
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  const panelMap = {
    'input': 'panelInput',
    'generating': 'panelGenerating',
    'result': 'panelResult',
    'history': 'panelHistory',
    'review': 'panelReview',
    'trends': 'panelTrends',
    'compliance': 'panelCompliance',
  };
  const panelId = panelMap[target];
  if (panelId) {
    const panel = document.getElementById(panelId);
    if (panel) panel.classList.add('active');
  }

  // 状态面板
  document.getElementById('statusCardInput').style.display = target === 'input' ? 'block' : 'none';
  document.getElementById('statusCardProgress').style.display = target === 'generating' ? 'block' : 'none';
  document.getElementById('statusCardResult').style.display = target === 'result' ? 'block' : 'none';
}

// ===== 开始生成 =====
async function startGeneration() {
  if (useHarness) {
    return startHarnessGeneration();
  }

  const ideaInput = document.getElementById('ideaInput');
  const idea = ideaInput.value.trim();

  if (!idea) {
    showToast(t('err_empty'), true);
    ideaInput.focus();
    ideaInput.style.borderColor = '#F598A8';
    setTimeout(() => { ideaInput.style.borderColor = ''; }, 2000);
    return;
  }

  // 获取选中题材
  const genreRadio = document.querySelector('input[name="genre"]:checked');
  const genre = genreRadio ? genreRadio.value : 'campus_fantasy';
  const artStyle = document.getElementById('artStyle').value;
  const episodes = episodeCount;

  // 获取选中平台
  const platforms = getSelectedPlatforms();

  // 切换到生成面板
  navigateTo('generating');
  resetProgressUI();

  // 启动进度动画
  startProgressAnimation();

  try {
    const response = await fetch('/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        genre: genre,
        idea: idea,
        episodes: episodes,
        art_style: artStyle,
        img_platform: platforms.imgPlatform,
        vid_platform: platforms.vidPlatform,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || t('err_server'));
    }

    if (data.success) {
      // 快速完成进度条
      completeProgress();
      await sleep(600);

      // 保存结果
      generatedModules = data.modules || {};
      document.getElementById('resultInfo').textContent =
        `${currentLang === 'zh' ? '已保存至' : 'Saved to'} ${data.folder}`;

      // 切换到结果面板
      navigateTo('result');
      switchTab(Object.keys(generatedModules)[0] || '01_剧本大纲');
    }
  } catch (err) {
    navigateTo('input');
    showToast(err.message || t('err_network'), true);
    console.error('Generation error:', err);
  }
}

// ===== Harness 严格模式生成（SSE流式）=====
const STEP_NAME_TO_INDEX = {
  '剧本大纲': 0,
  '角色设定': 1,
  '场景描述': 2,
  '分集台词': 3,
  '分镜脚本': 4,
  'AI提示词': 5,
  'AI审核': 6,
};

async function startHarnessGeneration() {
  const ideaInput = document.getElementById('ideaInput');
  const idea = ideaInput.value.trim();

  if (!idea) {
    showToast(t('err_empty'), true);
    ideaInput.focus();
    ideaInput.style.borderColor = '#F598A8';
    setTimeout(() => { ideaInput.style.borderColor = ''; }, 2000);
    return;
  }

  const genreRadio = document.querySelector('input[name="genre"]:checked');
  const genre = genreRadio ? genreRadio.value : 'campus_fantasy';
  const artStyle = document.getElementById('artStyle').value;
  const episodes = episodeCount;
  const platforms = getSelectedPlatforms();

  navigateTo('generating');
  resetProgressUI();

  // 更新状态文字
  document.getElementById('genStatus').textContent =
    currentLang === 'zh'
      ? 'Harness 6步流水线生成中，预计3-5分钟...'
      : 'Harness 6-step pipeline running, ~3-5 minutes...';

  try {
    const response = await fetch('/generate_harness', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        genre: genre,
        idea: idea,
        episodes: episodes,
        art_style: artStyle,
        img_platform: platforms.imgPlatform,
        vid_platform: platforms.vidPlatform,
        stream: true,
      }),
    });

    if (!response.ok) {
      const errData = await response.json().catch(() => ({}));
      throw new Error(errData.error || t('err_server'));
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop() || '';
      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            const event = JSON.parse(line.slice(6));
            handleHarnessEvent(event);
          } catch (e) { /* 忽略解析错误 */ }
        }
      }
    }
  } catch (err) {
    navigateTo('input');
    showToast(err.message || t('err_network'), true);
    console.error('Harness generation error:', err);
  }
}

function handleHarnessEvent(event) {
  if (event.type === 'progress') {
    const stepIdx = STEP_NAME_TO_INDEX[event.step];
    if (stepIdx === undefined) return;

    if (event.status === 'running') {
      updateStepNode(stepIdx, 'active');
      updateCheckItem(stepIdx, 'active');
      // 确保前面的已完成
      for (let i = 0; i < stepIdx; i++) {
        updateStepNode(i, 'done');
        updateCheckItem(i, 'done');
      }
      const pct = (stepIdx / 7) * 100;
      document.getElementById('progressFill').style.width = pct + '%';
      document.getElementById('progressPercent').textContent = Math.round(pct) + '%';

      const msgs = {
        zh: {
          '剧本大纲': '正在生成剧本大纲...',
          '角色设定': '正在设计角色...',
          '场景描述': '正在构建场景...',
          '分集台词': '正在编写台词...',
          '分镜脚本': '正在绘制分镜...',
          'AI提示词': '正在优化AI提示词...',
          'AI审核': '正在进行AI综合审核...',
        },
        en: {
          '剧本大纲': 'Generating outline...',
          '角色设定': 'Designing characters...',
          '场景描述': 'Building scenes...',
          '分集台词': 'Writing dialogue...',
          '分镜脚本': 'Creating storyboard...',
          'AI提示词': 'Optimizing AI prompts...',
          'AI审核': 'Running AI review...',
        },
      };
      const genStatus = document.getElementById('genStatus');
      genStatus.textContent = msgs[currentLang][event.step] || event.step;

    } else if (event.status === 'done') {
      updateStepNode(stepIdx, 'done');
      updateCheckItem(stepIdx, 'done');
      const pct = ((stepIdx + 1) / 7) * 100;
      document.getElementById('progressFill').style.width = pct + '%';
      document.getElementById('progressPercent').textContent = Math.round(pct) + '%';

    } else if (event.status === 'retry') {
      updateStepNode(stepIdx, 'retry');
      updateCheckItem(stepIdx, 'retry');
      document.getElementById('genStatus').textContent = event.detail || '校验失败，正在重试...';
    }

  } else if (event.type === 'complete') {
    generatedModules = event.modules || {};
    document.getElementById('resultInfo').textContent =
      `${currentLang === 'zh' ? '已保存至' : 'Saved to'} ${event.folder}`;
    completeProgress();
    navigateTo('result');
    switchTab(Object.keys(generatedModules)[0] || '01_剧本大纲');

  } else if (event.type === 'error') {
    navigateTo('input');
    showToast(event.error, true);
  }
}

// ===== Harness 模式切换 =====
function toggleHarnessMode() {
  useHarness = !useHarness;
  const toggle = document.getElementById('harnessToggle');
  if (toggle) {
    toggle.classList.toggle('active', useHarness);
    const label = document.getElementById('harnessToggleLabel');
    if (label) {
      label.innerHTML = useHarness
        ? (currentLang === 'zh' ? '⏳ <span data-i18n="config_harness">严格模式</span>' : '⏳ <span>Strict Mode</span>')
        : (currentLang === 'zh' ? '⚡ <span data-i18n="config_harness_off">快速模式</span>' : '⚡ <span>Fast Mode</span>');
    }
  }
  // 更新状态面板中的AI模型显示
  document.querySelectorAll('.metric').forEach(m => {
    const label = m.querySelector('.metric-label');
    if (label && label.textContent.includes('模型')) {
      const val = m.querySelector('.metric-value');
      if (val) val.textContent = useHarness ? 'DeepSeek×6' : 'DeepSeek';
    }
  });
}

function updateStepNode(index, status) {
  const nodes = document.querySelectorAll('.tl-node');
  if (index < nodes.length) {
    nodes[index].classList.remove('active', 'done', 'retry');
    if (status === 'active') nodes[index].classList.add('active');
    else if (status === 'done') nodes[index].classList.add('done');
    else if (status === 'retry') nodes[index].classList.add('active');
  }
}

function updateCheckItem(index, status) {
  const checks = document.querySelectorAll('.check-item');
  if (index < checks.length) {
    checks[index].classList.remove('active', 'done', 'retry');
    const icon = checks[index].querySelector('.check-icon');
    if (status === 'active') {
      checks[index].classList.add('active');
      icon.textContent = '◉';
    } else if (status === 'done') {
      checks[index].classList.add('done');
      icon.textContent = '✓';
    } else if (status === 'retry') {
      checks[index].classList.add('active');
      icon.textContent = '↻';
    }
  }
}

// ===== 进度动画 =====
let progressInterval = null;

function resetProgressUI() {
  if (progressInterval) clearInterval(progressInterval);
  document.getElementById('progressFill').style.width = '0%';
  document.getElementById('progressPercent').textContent = '0%';
  document.querySelectorAll('.tl-node').forEach(n => n.classList.remove('active', 'done'));
  document.querySelectorAll('.check-item').forEach(n => n.classList.remove('active', 'done'));
  document.querySelectorAll('.check-icon').forEach(n => n.textContent = '○');
}

function startProgressAnimation() {
  let progress = 0;
  const fill = document.getElementById('progressFill');
  const percent = document.getElementById('progressPercent');
  const steps = document.querySelectorAll('.tl-node');
  const checks = document.querySelectorAll('.check-item');
  const genStatus = document.getElementById('genStatus');

  const statusMessages = {
    zh: ['正在调用DeepSeek...', '正在构建世界观...', '正在设计角色...', '正在编写台词...', '正在生成分镜...', '正在优化提示词...'],
    en: ['Calling DeepSeek...', 'Building world...', 'Designing characters...', 'Writing dialogue...', 'Creating storyboard...', 'Optimizing prompts...'],
  };

  progressInterval = setInterval(() => {
    // 模拟进度：前80%较快，后20%较慢
    if (progress < 85) {
      progress += Math.random() * 3 + 0.5;
    } else if (progress < 95) {
      progress += Math.random() * 0.5 + 0.1;
    }
    progress = Math.min(progress, 95);

    fill.style.width = progress + '%';
    percent.textContent = Math.round(progress) + '%';

    // 步骤节点点亮
    const stepIndex = Math.floor(progress / 16.6);
    steps.forEach((step, i) => {
      step.classList.remove('active', 'done');
      if (i < stepIndex) step.classList.add('done');
      else if (i === stepIndex) step.classList.add('active');
    });

    // 右侧checklist同步
    checks.forEach((check, i) => {
      check.classList.remove('active', 'done');
      const icon = check.querySelector('.check-icon');
      if (i < stepIndex) {
        check.classList.add('done');
        icon.textContent = '✓';
      } else if (i === stepIndex) {
        check.classList.add('active');
        icon.textContent = '◉';
      } else {
        icon.textContent = '○';
      }
    });

    // 状态文字
    if (stepIndex < 6) {
      genStatus.textContent = statusMessages[currentLang][stepIndex] || statusMessages[currentLang][5];
    }
  }, 500);
}

function completeProgress() {
  if (progressInterval) clearInterval(progressInterval);
  const fill = document.getElementById('progressFill');
  const percent = document.getElementById('progressPercent');
  fill.style.width = '100%';
  percent.textContent = '100%';

  document.querySelectorAll('.tl-node').forEach(n => { n.classList.remove('active'); n.classList.add('done'); });
  document.querySelectorAll('.check-item').forEach(c => {
    c.classList.remove('active'); c.classList.add('done');
    c.querySelector('.check-icon').textContent = '✓';
  });
}

// ===== Tab切换 =====
function switchTab(moduleKey) {
  currentTab = moduleKey;

  // 更新Tab状态
  document.querySelectorAll('.tab').forEach(tab => {
    tab.classList.toggle('active', tab.getAttribute('data-tab') === moduleKey);
  });

  // 更新Tab指示器
  const activeTab = document.querySelector('.tab.active');
  const indicator = document.getElementById('tabIndicator');
  if (activeTab && indicator) {
    indicator.style.left = activeTab.offsetLeft + 'px';
    indicator.style.width = activeTab.offsetWidth + 'px';
  }

  // 渲染内容
  const placeholder = document.getElementById('contentPlaceholder');
  const render = document.getElementById('contentRender');

  if (generatedModules[moduleKey]) {
    placeholder.style.display = 'none';
    render.style.display = 'block';
    render.innerHTML = simpleMarkdown(generatedModules[moduleKey]);
  } else {
    placeholder.style.display = 'flex';
    render.style.display = 'none';
  }
}

// 简易Markdown渲染器
function simpleMarkdown(text) {
  if (!text) return '';
  let html = text
    // 标题
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^# (.+)$/gm, '<h1>$1</h1>')
    // 粗体/斜体
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    // 行内代码
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    // 列表
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    .replace(/^(\d+)\. (.+)$/gm, '<li>$2</li>')
    // 连续li包裹
    .replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>')
    // 水平线
    .replace(/^---$/gm, '<hr>')
    // 引用
    .replace(/^> (.+)$/gm, '<blockquote>$1</blockquote>')
    // 分隔线前的连续blockquote
    .replace(/<\/blockquote>\n<blockquote>/g, '<br>')
    // 段落（双换行）
    .replace(/\n\n/g, '</p><p>')
    // 单换行
    .replace(/\n/g, '<br>');

  // 包裹段落
  html = '<p>' + html + '</p>';
  // 清理空段落
  html = html.replace(/<p><\/p>/g, '');
  // 清理嵌套问题
  html = html.replace(/<p><(h[123]|ul|blockquote|hr)/g, '<$1');
  html = html.replace(/<\/(h[123]|ul|blockquote|hr)><\/p>/g, '</$1>');

  return html;
}

// ===== 复制功能 =====
function copyModule(moduleKey) {
  if (!generatedModules[moduleKey]) {
    showToast('No content to copy', true);
    return;
  }
  copyToClipboard(generatedModules[moduleKey]);
}

function copyAll() {
  const allText = Object.entries(generatedModules)
    .map(([key, val]) => `# ${key}\n\n${val}`)
    .join('\n\n---\n\n');
  copyToClipboard(allText);
}

function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => {
    showToast(t('toast_copied'));
  }).catch(() => {
    // Fallback
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
    showToast(t('toast_copied'));
  });
}

// ===== 下载功能 =====
function downloadAll() {
  const allText = Object.entries(generatedModules)
    .map(([key, val]) => `# ${key.replace(/_/g, ' ')}\n\n${val}`)
    .join('\n\n---\n\n');

  const blob = new Blob([allText], { type: 'text/markdown;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `script_${Date.now()}.md`;
  a.click();
  URL.revokeObjectURL(url);
  showToast('Download started ✓');
}

// ===== 返回输入页 =====
function resetToInput() {
  generatedModules = {};
  currentTab = null;
  document.getElementById('contentRender').style.display = 'none';
  document.getElementById('contentPlaceholder').style.display = 'flex';
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  navigateTo('input');
}

// ===== 历史记录 =====
async function loadHistory() {
  navigateTo('history');
  try {
    const resp = await fetch('/list');
    const data = await resp.json();
    const list = document.getElementById('historyList');

    if (data.length === 0) {
      list.innerHTML = `<p class="history-empty">${t('history_empty')}</p>`;
      return;
    }

    list.innerHTML = data.map(item => `
      <div class="history-item">
        <div>
          <div class="history-name">${item.name}</div>
          <div class="history-meta">${item.count} files</div>
        </div>
        <span>→</span>
      </div>
    `).join('');
  } catch (err) {
    document.getElementById('historyList').innerHTML =
      `<p class="history-empty">${t('err_network')}</p>`;
  }
}

// ===== Toast =====
function showToast(message, isError = false) {
  const toast = document.getElementById('toast');
  toast.textContent = message;
  toast.style.background = isError ? '#E88595' : '#2D1B23';
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 2500);
}

// ===== v5.0 新增功能 =====

let currentReviewModules = {};
let currentReviewGenre = '';
let lastReviewResult = null;
let lastComplianceResult = null;

function showReviewPanel() {
  navigateTo('review');
  // 如果当前有已生成的模块，自动加载
  if (Object.keys(generatedModules).length > 0) {
    currentReviewModules = generatedModules;
    // 获取题材（从生成上下文推断）
    const genreRadio = document.querySelector('input[name="genre"]:checked');
    currentReviewGenre = genreRadio ? genreRadio.closest('.genre-chip')?.querySelector('span:last-child')?.textContent || '校园奇幻' : '校园奇幻';
    populateReviewScriptList();
  } else {
    loadAvailableScripts();
  }
}

async function loadAvailableScripts() {
  try {
    const resp = await fetch('/list');
    const data = await resp.json();
    const list = document.getElementById('reviewScriptList');
    if (data.length === 0) {
      list.innerHTML = `<p class="tile-meta">${t('review_empty_hint')}</p>`;
      return;
    }
    list.innerHTML = data.slice(0, 10).map((item, idx) => `
      <div class="review-script-option ${idx === 0 ? 'selected' : ''}" 
           data-folder="${item.name}" onclick="selectReviewScript('${item.name}', this)">
        <span class="script-name">${item.name}</span>
        <span class="script-meta">${item.count} files</span>
      </div>
    `).join('');
    if (data.length > 0) {
      document.getElementById('btnStartReview').style.display = 'inline-block';
    }
  } catch (err) {
    console.error('加载剧本列表失败:', err);
  }
}

function selectReviewScript(folderName, el) {
  document.querySelectorAll('.review-script-option').forEach(o => o.classList.remove('selected'));
  el.classList.add('selected');
  // 加载剧本内容
  fetch(`/export_json/${folderName}`)
    .then(r => r.json())
    .then(data => {
      currentReviewModules = data.modules || {};
      document.getElementById('btnStartReview').style.display = 'inline-block';
    })
    .catch(err => {
      showToast(t('review_load_fail') + ': ' + err.message, true);
    });
}

function populateReviewScriptList() {
  const list = document.getElementById('reviewScriptList');
  const moduleKeys = Object.keys(currentReviewModules);
  if (moduleKeys.length === 0) {
    list.innerHTML = `<p class="tile-meta">${t('review_no_script')}</p>`;
    return;
  }
  list.innerHTML = `
    <div class="review-script-option selected">
      <span class="script-name">${t('review_current_script')} (${moduleKeys.length}${t('review_modules_count')})</span>
      <span class="script-meta">${moduleKeys.slice(0,3).join(', ')}...</span>
    </div>
  `;
  document.getElementById('btnStartReview').style.display = 'inline-block';
}

async function startReview() {
  if (Object.keys(currentReviewModules).length === 0) {
    showToast(t('review_no_script'), true);
    return;
  }

  document.getElementById('reviewInputCard').style.display = 'none';
  document.getElementById('reviewLoadingCard').style.display = 'block';
  document.getElementById('reviewResultCard').style.display = 'none';

  try {
    const resp = await fetch('/review', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        modules: currentReviewModules,
        genre_cn: currentReviewGenre,
      }),
    });
    const data = await resp.json();

    document.getElementById('reviewLoadingCard').style.display = 'none';
    document.getElementById('reviewResultCard').style.display = 'block';

    if (data.success) {
      lastReviewResult = data;
      renderReviewResult(data);
      // 如果审核结果在result页面，也更新07 tab
      if (data.report_md) {
        generatedModules['07_审核报告'] = data.report_md;
        document.getElementById('tab07').style.display = '';
      }
    } else {
      document.getElementById('reviewOverall').innerHTML = 
        `<p style="color:var(--tile-pink)">${t('review_fail')}: ${data.error || ''}</p>`;
    }
  } catch (err) {
    document.getElementById('reviewLoadingCard').style.display = 'none';
    document.getElementById('reviewResultCard').style.display = 'block';
    document.getElementById('reviewOverall').innerHTML = 
      `<p style="color:var(--tile-pink)">${t('review_fail')}: ${err.message}</p>`;
  }
}

function renderReviewResult(data) {
  // 总分
  const score = data.overall_score || 0;
  const scoreClass = score >= 8 ? 'score-high' : (score >= 6 ? 'score-mid' : 'score-low');
  document.getElementById('reviewOverall').innerHTML = `
    <div class="review-overall">
      <span class="review-score-big ${scoreClass}">${score}</span>
      <div class="review-score-label">
        <strong>${t('review_score_label')}</strong><br>
        ${data.summary || data.score_label || ''}
      </div>
    </div>
  `;

  // Agent卡片
  const agents = data.agents || [];
  document.getElementById('reviewAgents').innerHTML = agents.map(a => {
    const s = a.score || 0;
    const sc = s >= 8 ? 'score-high' : (s >= 6 ? 'score-mid' : 'score-low');
    const issues = (a.issues || []).map(i => {
      const sv = i.severity || 'low';
      return `<div><span class="sev-${sv === 'high' ? 'high' : (sv === 'medium' ? 'med' : 'low')}">${sv.toUpperCase()}</span> ${i.module || ''}: ${i.detail || ''}</div>`;
    }).join('');
    const suggestions = (a.suggestions || []).map(s => `<div class="agent-suggestion">${s}</div>`).join('');
    return `
      <div class="review-agent-card">
        <div class="agent-header">
          <span class="agent-name">${a.agent_name || ''}</span>
          <span class="agent-score ${sc}">${s}/10</span>
        </div>
        <div class="agent-detail">
          ${issues}
          ${suggestions}
        </div>
      </div>
    `;
  }).join('');

  // Markdown报告
  if (data.report_md) {
    document.getElementById('reviewReportMd').innerHTML =
      '<div class="review-md">' + renderMarkdownRaw(data.report_md) + '</div>';
  }
}

function runReviewFromResult() {
  if (Object.keys(generatedModules).length === 0) {
    showToast('请先生成剧本', true);
    return;
  }
  currentReviewModules = generatedModules;
  const genreRadio = document.querySelector('input[name="genre"]:checked');
  currentReviewGenre = genreRadio ? genreRadio.closest('.genre-chip')?.querySelector('span:last-child')?.textContent || '校园奇幻' : '校园奇幻';
  
  navigateTo('review');
  populateReviewScriptList();
  startReview();
}

async function runComplianceFromResult() {
  if (Object.keys(generatedModules).length === 0) {
    showToast('请先生成剧本', true);
    return;
  }
  await runCompliance(generatedModules);
}

async function runComplianceAfterReview() {
  if (Object.keys(currentReviewModules).length === 0) {
    showToast('请先进行审核', true);
    return;
  }
  await runCompliance(currentReviewModules);
}

async function runCompliance(modules) {
  navigateTo('compliance');
  document.getElementById('complianceLoadingCard').style.display = 'block';
  document.getElementById('complianceResultCard').style.display = 'none';

  try {
    const resp = await fetch('/compliance', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ modules: modules }),
    });
    const data = await resp.json();

    document.getElementById('complianceLoadingCard').style.display = 'none';
    document.getElementById('complianceResultCard').style.display = 'block';
    lastComplianceResult = data;

    if (data.success) {
      renderComplianceResult(data);
    } else {
      document.getElementById('complianceScore').innerHTML = 
        `<p style="color:var(--tile-pink)">${t('compliance_fail')}: ${data.error || ''}</p>`;
    }
  } catch (err) {
    document.getElementById('complianceLoadingCard').style.display = 'none';
    document.getElementById('complianceResultCard').style.display = 'block';
    document.getElementById('complianceScore').innerHTML = 
      `<p style="color:var(--tile-pink)">${t('compliance_req_fail')}: ${err.message}</p>`;
  }
}

function renderComplianceResult(data) {
  const score = data.originality_score || 0;
  const risk = data.risk_level || 'unknown';
  const recClass = data.recommendation === 'pass' ? 'score-pass' : (data.recommendation === 'reject' ? 'score-reject' : 'score-revise');
  
  document.getElementById('complianceScore').innerHTML = `
    <div class="compliance-score-display">
      <span class="compliance-score-num ${recClass}">${score}</span>
      <div>
        <div style="margin-bottom:8px;">
          <span class="compliance-risk-badge ${risk}">${risk.toUpperCase()}</span>
          <span class="compliance-score-meta" style="margin-left:8px;">${t('compliance_score_label')}</span>
        </div>
        <div class="compliance-score-summary">${data.summary || ''}</div>
      </div>
    </div>
  `;

  if (data.report_md) {
    document.getElementById('complianceReportMd').innerHTML =
      '<div class="review-md">' + renderMarkdownRaw(data.report_md) + '</div>';
  }
}

async function loadTrends() {
  navigateTo('trends');
  document.getElementById('trendsPromptCard').style.display = 'none';
  document.getElementById('trendsLoadingCard').style.display = 'block';
  document.getElementById('trendsResultCard').style.display = 'none';

  try {
    const resp = await fetch('/trends');
    const data = await resp.json();

    document.getElementById('trendsLoadingCard').style.display = 'none';
    document.getElementById('trendsResultCard').style.display = 'block';

    if (data.success && data.report_md) {
      document.getElementById('trendsReportMd').innerHTML =
        '<div class="review-md">' + renderMarkdownRaw(data.report_md) + '</div>';
    } else {
      document.getElementById('trendsReportMd').innerHTML = 
        `<p style="color:var(--tile-pink)">${t('trends_fail')}: ${data.error || ''}</p>`;
    }
  } catch (err) {
    document.getElementById('trendsLoadingCard').style.display = 'none';
    document.getElementById('trendsResultCard').style.display = 'block';
    document.getElementById('trendsReportMd').innerHTML = 
      `<p style="color:var(--tile-pink)">${t('trends_fail')}: ${err.message}</p>`;
  }
}

function downloadZip() {
  const resultInfo = document.getElementById('resultInfo').textContent;
  const folderMatch = resultInfo.match(/[^\s:]+\d{8}_\d{6}/);
  if (!folderMatch) {
    showToast(t('zip_no_folder'), true);
    return;
  }
  const folder = folderMatch[0];
  window.open(`/download_zip/${folder}`, '_blank');
}

function copyReviewReport() {
  if (!lastReviewResult || !lastReviewResult.report_md) {
    showToast(t('review_no_report'), true);
    return;
  }
  navigator.clipboard.writeText(lastReviewResult.report_md).then(() => {
    showToast(t('toast_copied'));
  }).catch(() => {
    showToast(t('copy_fail'), true);
  });
}

// Markdown到HTML渲染（纯语义标签，样式由 .review-md CSS类控制）
function renderMarkdownRaw(md) {
  if (!md) return '';
  let html = md
    // 标题
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^# (.+)$/gm, '<h1>$1</h1>')
    // 内联
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    // 列表
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    // 段落
    .replace(/\n\n/g, '</p><p>')
    .replace(/\n/g, '<br>');

  html = '<p>' + html + '</p>';

  // 表格——包裹在 .table-wrap 中以支持横向滚动
  html = html.replace(/\|(.+)\|/g, (match) => {
    const cells = match.split('|').filter(c => c.trim());
    return '<tr>' + cells.map(c => {
      const trimmed = c.trim();
      if (trimmed.match(/^[-:]+$/)) return '';
      // 长文本列使用 long-text 类
      const cls = trimmed.length > 40 ? ' class="long-text"' : '';
      return `<td${cls}>${trimmed}</td>`;
    }).join('') + '</tr>';
  });
  html = html.replace(/(<tr>.*<\/tr>\n?)+/g, '<div class="table-wrap"><table>$&</table></div>');
  return html;
}

// 覆盖resetToInput以清理新面板
const _originalResetToInput = resetToInput;
resetToInput = function() {
  _originalResetToInput();
  // 清理审核和合规面板
  document.getElementById('reviewResultCard').style.display = 'none';
  document.getElementById('reviewInputCard').style.display = 'block';
  document.getElementById('reviewLoadingCard').style.display = 'none';
  document.getElementById('complianceResultCard').style.display = 'none';
  document.getElementById('complianceLoadingCard').style.display = 'none';
  document.getElementById('tab07').style.display = 'none';
  lastReviewResult = null;
  lastComplianceResult = null;
  currentReviewModules = {};
};

// ===== 工具函数 =====
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
