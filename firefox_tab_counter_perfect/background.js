// 🔥 Firefox Tab Counter - 完美调试版 (AliyunOSS + ChatGPT + 时间戳增强)
// 1. 初始全面统计（带时间戳）
browser.tabs.query({}).then(tabs => {
  console.group(`📊 当前标签页: ${tabs.length} 个`);
  tabs.forEach((tab, index) => {
    const time = new Date(tab.lastAccessed).toLocaleString('zh-CN');  // 打开/最后访问时间
    console.log(`Tab ${index+1} [ID:${tab.id}] ${tab.title?.slice(0,50) || '无标题'} | ${tab.url?.slice(0,60) || 'local'} | ⏰ ${time} | 📱 ${tab.status}`);
  });
  console.groupEnd();
}).catch(err => console.error('初始查询失败:', err));

// 2. 实时监听（ChatGPT 增强）
browser.tabs.onCreated.addListener(tab => {
  console.log(`➕ 新标签 [ID:${tab.id}] ${tab.title || tab.url}`);
});

browser.tabs.onRemoved.addListener((tabId, info) => {
  console.log(`➖ 标签关闭 [ID:${tabId}] ${info.isWindowClosing ? '(窗口关闭)' : '(单个标签)'}`);
});

browser.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab) {
    console.log(`✅ 加载完成 [ID:${tabId}] ${tab.title || tab.url}`);
  }
});

// 3. 周期性刷新统计（可选，每 30s 一次，避免频繁）
setInterval(() => {
  browser.tabs.query({}).then(tabs => {
    if (tabs.length !== gLastTabCount) {  // 只在数量变化时输出
      gLastTabCount = tabs.length;
      console.log(`🔄 标签页数量变化 → 当前: ${tabs.length} 个`);
    }
  });
}, 30000);
let gLastTabCount = 0;
