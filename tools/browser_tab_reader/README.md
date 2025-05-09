# Browser Tab Reader
# 浏览器标签页阅读器

A tool to extract and process vocabulary from your browser tabs. This tool reads Firefox's existing tabs, sorts them by their actual tab order, retrieves their creation/visiting time, and identifies tabs from dictionary sites.

一个从浏览器标签页中提取和处理词汇的工具。该工具读取Firefox的现有标签页，按照它们的实际标签顺序排序，检索它们的创建/访问时间，并识别来自词典网站的标签页。

## Features
## 功能特点

- Read Firefox's existing tabs from session files
- Sort tabs by their actual tab order (window and tab index)
- Get tab creation and last accessed time
- Identify tabs from dictionary sites
- Extract search terms from dictionary URLs
- Export dictionary site data for gist-dictionary

- 从会话文件中读取Firefox的现有标签页
- 按照实际标签顺序（窗口和标签索引）排序标签页
- 获取标签页创建和最后访问时间
- 识别来自词典网站的标签页
- 从词典URL中提取搜索词
- 为gist-dictionary导出词典网站数据

## Requirements
## 要求

- Python 3.6 or higher
- Firefox browser with an active profile

- Python 3.6或更高版本
- 带有活跃配置文件的Firefox浏览器

## Installation
## 安装

### Manual Installation (Recommended)
### 手动安装（推荐）

No special installation is required. Just make sure you have Python 3.6+ installed. The browser tab reader has no external dependencies.

不需要特殊安装。只需确保已安装Python 3.6+。浏览器标签页阅读器没有外部依赖项。

### Using pip (Optional)
### 使用pip（可选）

If you want to install the tool as a package:

如果你想将该工具作为包安装：

```bash
pip install -e ".[browser_tab_reader]"
```

### Using Poetry (Optional)
### 使用Poetry（可选）

Poetry is a dependency management tool. If you prefer to use it:

Poetry是一个依赖管理工具。如果你喜欢使用它：

```bash
# Install with Poetry
poetry install --extras "browser_tab_reader"

# Or install all tools
poetry install --extras "all"
```

## How to Run
## 如何运行

### Step 1: Clone the Repository
### 步骤1：克隆仓库

First, clone the gist-dictionary repository if you haven't already:

首先，如果你还没有克隆gist-dictionary仓库，请先克隆：

```bash
git clone https://github.com/LaoshuBaby/gist-dictionary.git
cd gist-dictionary
```

### Step 2: Install Dependencies
### 步骤2：安装依赖

Choose one of the installation methods described above. For example, using Poetry:

选择上述安装方法之一。例如，使用Poetry：

```bash
# Install Poetry if you don't have it
pip install poetry

# Install the browser_tab_reader tool
poetry install --extras "browser_tab_reader"
```

### Step 3: Run the Tool
### 步骤3：运行工具

You can run the tool in several ways:

你可以通过几种方式运行该工具：

#### Using Poetry
#### 使用Poetry

```bash
poetry run browser-tab-reader
```

#### Using Python directly
#### 直接使用Python

```bash
# From the repository root
python -m tools.browser_tab_reader.browser_tab_reader

# Or navigate to the tool directory
cd tools/browser_tab_reader
python browser_tab_reader.py
```

### Step 4: View the Results
### 步骤4：查看结果

The tool will output the dictionary tabs it found to the console. You can also specify an output file:

该工具将在控制台输出它找到的词典标签页。你也可以指定一个输出文件：

```bash
python browser_tab_reader.py --output my_dictionary_tabs.json
```

## Usage
## 使用方法

### Basic Usage
### 基本用法

```bash
python browser_tab_reader.py
```

This will automatically find your Firefox profile and use a default list of dictionary sites.

这将自动查找你的Firefox配置文件并使用默认的词典网站列表。

### Advanced Usage
### 高级用法

```bash
python browser_tab_reader.py --profile-path /path/to/firefox/profile --dict-sites-file dictionary_sites.txt --output dictionary_tabs.json
```

### Parameters
### 参数

- `--profile-path`: Path to Firefox profile directory (optional, will auto-detect if not specified)
- `--dict-sites-file`: File containing dictionary site domains, one per line (optional, will use default list if not specified)
- `--output`: Output file for dictionary tabs in JSON format (optional, will print to console if not specified)

- `--profile-path`：Firefox配置文件目录的路径（可选，如果未指定将自动检测）
- `--dict-sites-file`：包含词典网站域名的文件，每行一个（可选，如果未指定将使用默认列表）
- `--output`：以JSON格式输出词典标签页的文件（可选，如果未指定将打印到控制台）

## Dictionary Sites File Format
## 词典网站文件格式

The dictionary sites file should contain one domain per line. For example:

词典网站文件应该每行包含一个域名。例如：

```
dictionary.com
merriam-webster.com
vocabulary.com
thefreedictionary.com
dictionary.cambridge.org
```

## Sample Usage
## 示例用法

A sample usage script is provided to demonstrate how the browser tab reader works:

提供了一个示例用法脚本，用于演示浏览器标签页阅读器的工作原理：

```bash
python sample_usage.py
```

This script creates a sample Firefox profile with some tabs, including dictionary sites, and shows how the browser tab reader processes them.

该脚本创建一个带有一些标签页的示例Firefox配置文件，包括词典网站，并展示浏览器标签页阅读器如何处理它们。

## How It Works
## 工作原理

1. The tool locates Firefox profile directories on your system
2. It reads session data from `sessionstore.js` or `sessionstore-backups/recovery.js`
3. It extracts tab information including URL, title, creation time, and last accessed time
4. It checks if each tab is from a dictionary site
5. For dictionary sites, it attempts to extract the search term from the URL
6. It outputs the results to the console or a JSON file

1. 该工具在你的系统上定位Firefox配置文件目录
2. 它从`sessionstore.js`或`sessionstore-backups/recovery.js`读取会话数据
3. 它提取标签页信息，包括URL、标题、创建时间和最后访问时间
4. 它检查每个标签页是否来自词典网站
5. 对于词典网站，它尝试从URL中提取搜索词
6. 它将结果输出到控制台或JSON文件

## Limitations
## 局限性

- The tool can only read Firefox tabs, not other browsers
- It relies on Firefox's session files, which might change format in future Firefox versions
- It can only extract search terms from known dictionary site URL patterns
- It cannot access the actual content of the tabs, only the URL and metadata

- 该工具只能读取Firefox标签页，不能读取其他浏览器
- 它依赖于Firefox的会话文件，这些文件的格式可能在未来的Firefox版本中发生变化
- 它只能从已知的词典网站URL模式中提取搜索词
- 它不能访问标签页的实际内容，只能访问URL和元数据

## Integration with gist-dictionary
## 与gist-dictionary的集成

The output of this tool can be used to populate your gist-dictionary with words you've looked up in online dictionaries. The JSON output includes the search term, URL, and timestamp information that can be imported into gist-dictionary.

该工具的输出可用于将你在在线词典中查找的单词填充到你的gist-dictionary中。JSON输出包括可以导入到gist-dictionary的搜索词、URL和时间戳信息。

## Troubleshooting
## 故障排除

If the tool cannot find your Firefox profile:
1. Use `--profile-path` to specify the path manually
2. Check if Firefox is installed and has been run at least once
3. Look for the profile directory in:
   - Linux: `~/.mozilla/firefox/`
   - macOS: `~/Library/Application Support/Firefox/Profiles/`
   - Windows: `%APPDATA%\Mozilla\Firefox\Profiles\`

如果该工具找不到你的Firefox配置文件：
1. 使用`--profile-path`手动指定路径
2. 检查是否已安装Firefox并至少运行过一次
3. 在以下位置查找配置文件目录：
   - Linux：`~/.mozilla/firefox/`
   - macOS：`~/Library/Application Support/Firefox/Profiles/`
   - Windows：`%APPDATA%\Mozilla\Firefox\Profiles\`