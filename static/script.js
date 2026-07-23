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
  }
};

let currentLang = 'zh';
let currentPanel = 'input';
let episodeCount = 5;
let generatedModules = {};
let currentTab = null;

// ===== 页面初始化 =====
document.addEventListener('DOMContentLoaded', () => {
  initParticles();
  initGenreSelection();
  initPlatformChips();
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
      el.textContent = dict[key];
    }
  });

  // 更新 placeholder
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    const key = el.getAttribute('data-i18n-placeholder');
    if (dict[key]) {
      el.placeholder = dict[key];
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
  document.querySelectorAll('.genre-item').forEach(item => {
    item.addEventListener('click', function() {
      document.querySelectorAll('.genre-item').forEach(i => i.classList.remove('selected'));
      this.classList.add('selected');
      this.querySelector('input[type="radio"]').checked = true;
    });
  });
}

// ===== 平台选择 =====
function initPlatformChips() {
  document.querySelectorAll('.platform-chips .chip').forEach(chip => {
    chip.addEventListener('click', function(e) {
      e.preventDefault();
      this.classList.toggle('selected');
      const checkbox = this.querySelector('input[type="checkbox"]');
      checkbox.checked = this.classList.contains('selected');
    });
  });
}

function getSelectedPlatforms() {
  const imgPlatforms = [];
  document.querySelectorAll('#imgPlatforms .chip.selected input').forEach(cb => {
    imgPlatforms.push(cb.value);
  });
  const vidPlatforms = [];
  document.querySelectorAll('#vidPlatforms .chip.selected input').forEach(cb => {
    vidPlatforms.push(cb.value);
  });
  return { imgPlatforms, vidPlatforms };
}
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
        img_platforms: platforms.imgPlatforms,
        vid_platforms: platforms.vidPlatforms,
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

// ===== 进度动画 =====
let progressInterval = null;

function resetProgressUI() {
  if (progressInterval) clearInterval(progressInterval);
  document.getElementById('progressFill').style.width = '0%';
  document.getElementById('progressPercent').textContent = '0%';
  document.querySelectorAll('.step-node').forEach(n => n.classList.remove('active', 'done'));
  document.querySelectorAll('.check-item').forEach(n => n.classList.remove('active', 'done'));
  document.querySelectorAll('.check-icon').forEach(n => n.textContent = '○');
}

function startProgressAnimation() {
  let progress = 0;
  const fill = document.getElementById('progressFill');
  const percent = document.getElementById('progressPercent');
  const steps = document.querySelectorAll('.step-node');
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

  document.querySelectorAll('.step-node').forEach(n => { n.classList.remove('active'); n.classList.add('done'); });
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

// ===== 工具函数 =====
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
