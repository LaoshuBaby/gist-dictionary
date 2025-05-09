# Gist Dictionary

使用GitHub Gist存储多来源数据的词典 | Multi-source dictionary that using GitHub Gist for storage | GitHub Gist でストレージの辞書

## Overview

Gist Dictionary is a tool for collecting and organizing vocabulary from multiple sources. It uses GitHub Gist for storage, allowing you to track changes to your vocabulary lists over time.

## Features

- Store vocabulary from multiple languages (English, Japanese, Korean, etc.)
- Link to online dictionaries for detailed explanations
- Track changes to your vocabulary lists using Git
- Import vocabulary from various sources (browser tabs, Anki decks, screenshots, etc.)

## Installation

### Using Poetry (Recommended)

```bash
# Clone the repository
git clone https://github.com/LaoshuBaby/gist-dictionary.git
cd gist-dictionary

# Install with Poetry
poetry install  # Basic installation

# Install with specific tool dependencies
poetry install --extras "browser_tab_reader"
poetry install --extras "ocr_dictionary"

# Install all tool dependencies
poetry install --extras "all"
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/LaoshuBaby/gist-dictionary.git
cd gist-dictionary

# Install with pip
pip install -e .  # Basic installation
pip install -e ".[browser_tab_reader]"  # With specific tool
pip install -e ".[all]"  # With all tools
```

## Tools

The project includes various tools to help import and manage vocabulary:

| Tool | Description |
|------|-------------|
| [Browser Tab Reader](tools/browser_tab_reader/) | Extract vocabulary from browser tabs |
| [Anki Import](tools/anki_import/) | Convert Anki decks to gist-dictionary format |
| [OCR Dictionary](tools/ocr_dictionary/) | Extract vocabulary from dictionary app screenshots |
| [CSV/Excel Converter](tools/csv_excel_converter/) | Convert CSV/Excel vocabulary lists |

See the [tools directory](tools/) for more information.

## 代码结构

一个FastAPI的后端用于接受和完成请求

提供一个CLI的命令行客户端进行词典查询和添加，同时做一个网页版的方便自己在手机上直接输入网址打开就访问

这算是两个前端。考虑到现在用的手机太慢，打开浏览器需要时间，也考虑如果有能力用AI写一个PWA应用或者原生安卓的前端

## 干嘛用

高中的时候背英语词是用的百词斩，后来曾经用沪江小D背过一段日语，当时还是五十音水平。这两个是不能在浏览器或者网上看的，只有软件内。

后来学的深入了就改为目前用的mojidict、然后现在查更多词和日语解释就用weblio。

但是weblio的单词帐同步功能是要钱的付费的，而且仅限日英，日语词汇是没有的，只有一个固定链接。但是我仅靠浏览器收藏夹去点开查看还是太费力了，我还是希望能聚合一个能管理和同步我记了的所有单词的东西。

我猜有人又要推荐anki，但我并不需要记住它的所有内容，我需要的是一个简单的单词名称和一句话的释义，以及一个引导我到某个在线辞书（moji也好、weblio也好）的超链接让我点开就进去看这个词典内的详细解释。以及我可能会同时管理韩语和英语的单词（因为我也有在学）

那么我觉得与其在anki基础上搞一个同步插件（因为如果要实现自己可以在外部查看的功能，估计还是得开发一个同步服务的后端来接受和处理），不如直接造一个完事了。

毕竟我用Anki还是更少以及我希望能追踪我单词表的变化和扩充情况，那么有历史记录的git做diff的话是更好处理的，而且真实可信。

那么就酱，我的坑挖好了，欢迎好心人帮我来填（不这个肯定是要自己填的）
