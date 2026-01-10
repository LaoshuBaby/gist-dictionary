// Firefox Tab Counter Popup v1.7 - 语法完整修复版
if (typeof browser === 'undefined' && typeof chrome === 'undefined') {
  document.addEventListener('DOMContentLoaded', () => {
    document.body.innerHTML = `
      <div style=\"padding:20px;text-align:center;color:#ff4444;background:#ffe6e6;border-radius:12px;margin:20px;font-family:sans-serif\">
        <h2>❌ 需要浏览器扩展环境</h2>
        <p>请按以下步骤安装:</p>
        <ol style=\"text-align:left;max-width:350px;margin:0 auto\">
          <li><strong>Firefox:</strong> about:debugging → Load Temporary Add-on → manifest.json</li>
          <li><strong>Chrome:</strong> chrome://extensions/ → Load unpacked → 整个文件夹</li>
          <li>点击工具栏图标</li>
        </ol>
      </div>
    `;
  });
} else {
  let tabData = []; 
  let lastUpdate = 0;

  async function loadTabs() {
    try {
      console.log('🔄 加载标签页数据...');
      
      const tabsApi = (typeof browser !== 'undefined') ? browser.tabs : chrome.tabs;
      const windowsApi = (typeof browser !== 'undefined') ? browser.windows : chrome.windows;
      
      const tabs = await tabsApi.query({});
      const windows = await windowsApi.getAll({ populate: true });
      
      tabData = tabs.map(tab => ({
        id: tab.id,
        title: tab.title || '无标题',
        url: tab.url || 'about:blank',
        lastAccessed: new Date(tab.lastAccessed).toISOString(),
        lastAccessedCN: new Date(tab.lastAccessed).toLocaleString('zh-CN'),
        status: tab.status || 'unknown',
        windowId: tab.windowId,
        windowIndex: tab.index,
        faviconUrl: tab.favIconUrl || ''
      }));

      console.log(`✅ ${tabs.length}标签/${windows.length}窗口`);

      const totalEl = document.getElementById('total-count');
      const windowEl = document.getElementById('window-count');
      const updateEl = document.getElementById('last-update');
      
      if (totalEl) totalEl.textContent = tabs.length;
      if (windowEl) windowEl.textContent = windows.length;
      if (updateEl) {
        lastUpdate = Date.now();
        updateEl.textContent = new Date().toLocaleString('zh-CN');
      }

      const tbody = document.getElementById('tab-table');
      if (!tbody) return;
      
      tbody.innerHTML = '';

      if (tabs.length === 0) {
        tbody.innerHTML = '<tr><td colspan=\"6\" class=\"empty\">暂无标签页</td></tr>';
        return;
      }

      tabData.forEach(tab => {
        const row = document.createElement('tr');
        const statusClass = tab.status === 'complete' ? 'complete' : 'loading';
        
        row.innerHTML = `
          <td class=\"id\">#${tab.id}</td>
          <td title=\"${tab.title}\">${tab.title.slice(0,25)}${tab.title.length>25?'...':''}</td>
          <td title=\"${tab.url}\">${tab.url.split('/')[2]||tab.url.slice(0,25)||'local'}${tab.url.length>25?'...':''}</td>
          <td class=\"time\">${tab.lastAccessedCN}</td>
          <td><span class=\"status ${statusClass}\">${tab.status}</span></td>
          <td>W${tab.windowId}:${tab.windowIndex}</td>
        `;
        tbody.appendChild(row);
      });

    } catch (error) {
      console.error('❌ 错误:', error);
      const tbody = document.getElementById('tab-table');
      if (tbody) tbody.innerHTML = '<tr><td colspan=\"6\" class=\"empty\">错误: ' + error.message + '</td></tr>';
    }
  }

  function exportJSON() {
    if (!tabData.length) return alert('请先刷新！');
    
    const json = JSON.stringify(tabData, null, 2);
    const blob = new Blob([json], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `tabs-${new Date(lastUpdate).toISOString().slice(0,10)}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  document.addEventListener('DOMContentLoaded', function() {
    const refreshBtn = document.getElementById('refresh-btn');
    const exportBtn = document.getElementById('export-btn');
    
    if (refreshBtn) refreshBtn.addEventListener('click', loadTabs);
    if (exportBtn) exportBtn.addEventListener('click', exportJSON);
    
    console.log('✅ 按钮事件绑定完成');
    loadTabs();
  });

  setInterval(loadTabs, 5000);
}