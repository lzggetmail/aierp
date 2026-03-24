# 智慧城市知识管理机器人

智慧城市群知识自动收集、整理、问答机器人

## 🎯 功能特性

### 1. 智能收集
- 自动识别群内有价值的内容
- 提取关键信息（方案、技术、案例）
- 自动分类和打标签

### 2. 知识库管理
- 自动存储到飞书知识库
- 按子系统分类（安防、机房、布线等）
- 支持标签检索

### 3. 智能问答
- @机器人 触发问答
- 基于知识库回答问题
- 提供相关案例参考

## 📁 项目结构

```
smartcity-bot/
├── config/
│   ├── config.py          # 配置文件
│   └── permissions.py     # 权限配置
├── docs/                   # 📄 技术文档存储
│   ├── README.md          # 文档索引
│   ├── 政策标准/          # 国家及地方标准
│   ├── 技术方案/          # 子系统技术方案
│   ├── 行业报告/          # 市场分析报告
│   ├── 城市案例/          # 建设案例
│   └── 新兴技术/          # AI/5G/数字孪生
├── bot/
│   ├── message_handler.py # 消息处理
│   ├── knowledge_bot.py   # 知识管理
│   └── qa_bot.py          # 问答模块
├── crawler/
│   ├── cn_web_search.py   # 国内搜索
│   ├── full_text_fetcher.py # 完整内容抓取
│   ├── pdf_fetcher.py     # PDF提取
│   └── tavily_search.py   # Tavily搜索
├── utils/
│   ├── feishu_api.py      # 飞书API
│   ├── content_analyzer.py# 内容分析
│   └── storage.py         # 存储模块
├── main.py                # 主程序
└── README.md              # 说明文档
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
export FEISHU_APP_ID="your_app_id"
export FEISHU_APP_SECRET="your_app_secret"
export OPENAI_API_KEY="your_openai_key"
```

### 3. 运行机器人

```bash
python main.py
```

## 📚 知识库分类

### 智能化子系统
- 综合布线
- 机房工程
- 安防系统
- 楼宇自控
- 智能交通
- 能源管理
- 更多...

### 自动标签
- 子系统标签：#安防 #机房 #布线
- 设备标签：#摄像头 #服务器
- 品牌标签：#海康 #华为
- 技术标签：#AI #IoT #5G

## 🤖 使用方式

### 自动收集
群内讨论时，机器人自动识别有价值内容并收录

### 智能问答
```
@智慧城市助手 什么是智慧交通？
@智慧城市助手 推荐几个安防方案
```

## 🔧 配置说明

### 飞书配置
1. 创建企业自建应用
2. 配置权限（见 permissions.py）
3. 获取 App ID 和 Secret
4. 配置事件订阅

### 知识库配置
1. 创建飞书知识库
2. 按分类创建文件夹
3. 获取知识库 Token

### 知识星球配置
1. 配置认证信息（见 `.zsxq-config.json`）
2. 在 `config/custom_sources.json` 中添加星球
3. 配置同步策略（见 `config/zsxq_config.json`）
4. 查看 [知识星球集成指南](docs/知识星球集成指南.md)

**已集成的知识星球**:
- 数字化解决方案知识库（德勤、凯捷等报告）
- 智慧城市之智慧交通（免费）
- 数字化转型ABC（数据仓库、大数据）

## 📖 相关文档

- [飞书开放平台](https://open.feishu.cn)
- [LangChain文档](https://docs.langchain.com)

---
*智慧城市知识管理机器人*
*2026-02-28*
