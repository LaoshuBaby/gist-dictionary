# Firefox Tab Counter Debug Extension 🚀

## 🎯 功能特性
- **📊 实时标签页统计**：数量、标题、URL、ID、状态、**最后访问时间**
- **📱 可视化表格**：点击图标弹出美观表格（**多窗口全覆盖**）
- **🔄 实时监听**：自动检测标签页创建/关闭/加载完成
- **⏰ 时间戳**：每个标签页的最后访问时间（中文格式）
- **🎨 现代化 UI**：玻璃态设计，支持自动刷新

## ❓ 多窗口逻辑解答
> **Q: Firefox 3 个窗口各 10 个标签页，总数是多少？**

**答案：30 个** ✅

**MDN 确认** (`browser.tabs.query({})`):
```
- 返回**浏览器所有窗口**的所有标签页
- windowId 参数可选，默认查询**全局所有窗口**
- 每个标签页有独立 ID，即使跨窗口
```

## 📖 使用教程

### 1. **安装（Firefox）**
```
1. 打开 about:debugging#/runtime/this-firefox
2. \"Load Temporary Add-on\" → 选择 manifest.json
3. ✅ 工具栏出现图标
```

### 2. **控制台调试（推荐开发者）**
```
1. 右键扩展图标 → \"Inspect\"
2. DevTools Console 查看实时日志：
   📊 当前标签页: 48 个
   Tab 1 [ID:123] Google | google.com | ⏰ 2024/1/10 10:30 | 📱 complete
   ➕ 新标签 [ID:125] GitHub
   ➖ 标签关闭 [ID:124]
```

### 3. **图形界面（一键表格）**
```
1. 点击工具栏图标
2. 弹出玻璃态窗口：
   ┌─ 总标签页: 48 | 窗口数: 3 | 最近更新: 2024/1/10 10:35 ─┐
   │ ID | 标题 | URL | 最后访问 | 状态                           │
   │ #123 | Google... | google.com | 10:30:45 | 🟢 complete │
   └─ [🔄 刷新] 5秒自动更新 ───────────────────────────────┘
```

### 4. **Chrome 兼容**
```
chrome://extensions/ → 开发者模式 → Load unpacked → 文件夹
```

## 🔧 高级用法
```
实时监听已内置，无需配置
支持隐身窗口（需额外权限）
5秒自动刷新表格
hover 显示完整标题/URL
```

## 📚 MDN 参考
- [tabs.query](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/tabs/query)
- [tabs.onCreated](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/tabs/onCreated)
- [Window 支持](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/windows#getAll)

## 🐛 故障排除
```
❌ 无数据 → 检查 tabs 权限
❌ 无图标 → 重新加载扩展
❌ 时间异常 → 时区设置 (zh-CN)
```

**开源友好 | MIT License | Firefox/Chrome v1.1**