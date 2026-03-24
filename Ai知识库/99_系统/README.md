# AI 知识库

> 李志刚的 AI 学习与创业知识库

---

## 📖 关于本仓库

这是我的个人 AI 知识库，记录了：

- AI 创业思维模型
- OpenClaw 学习笔记
- LangChain 学习记录
- 项目讨论与分析
- Agent 配置备份

---

## 📁 目录结构

```
├── MEMORY.md              # 长期记忆（核心内容）
├── USER.md                # 个人信息
├── SOUL.md                # AI 助手人设
├── AGENTS.md              # 工作区规则
├── HEARTBEAT.md           # 心跳任务配置
│
├── memory/                # 记忆文件
│   ├── 2026-03-15.md      # 每日记录
│   ├── AI创业思维模型.md   # 创业思维框架
│   ├── AI总裁项目记录.md   # 项目会议纪要
│   └── langchain-course-record.md
│
├── projects/              # 项目文件
│   ├── ai-entrepreneurship-policy/  # AI 创业政策
│   ├── ai-growth-journal/           # AI 成长日志
│   ├── openclaw-mastery/            # OpenClaw 学习
│   ├── smartcity-bot/               # 智慧城市机器人
│   └── weather-agent/               # 天气 Agent
│
├── skills/                # 技能文件
│   ├── github/            # GitHub 技能
│   ├── notion/            # Notion 技能
│   ├── obsidian/          # Obsidian 技能
│   └── ...
│
├── config/                # 配置备份
│   ├── openclaw.json      # OpenClaw 主配置（模型、渠道、绑定等）
│   └── agents/            # Agent 配置
│       ├── main/          # 主 Agent
│       │   ├── agent/auth.json      # 认证配置
│       │   ├── agent/models.json    # 模型配置
│       │   └── sessions/sessions.json  # 会话列表
│       └── work-assistant/          # 工作助手
│           ├── SOUL.md              # 人设
│           ├── IDENTITY.md          # 身份
│           └── README.md            # 说明
│
└── scripts/               # 脚本
    └── auto-backup.sh     # 自动备份脚本
```

---

## 🔧 功能

### 自动备份

每 6 小时自动备份到 GitHub：
- 0:00, 6:00, 12:00, 18:00

### 备份内容

| 类型 | 说明 |
|------|------|
| 记忆文件 | 所有学习和讨论记录 |
| 项目文件 | 各项目的分析、计划、笔记 |
| 配置文件 | OpenClaw 和 Agent 配置 |
| 技能文件 | 安装的技能包 |

### 配置文件说明

#### openclaw.json（OpenClaw 主配置）

**原始位置**: `/root/.openclaw/openclaw.json`
**备份位置**: `config/openclaw.json`

**主要作用**:
- 模型配置（使用哪个 LLM）
- 渠道绑定（飞书/Telegram/微信等）
- Agent 设置
- 系统参数

**为什么重要**: 这是 OpenClaw 的核心配置文件，丢失后需要重新配置所有绑定和模型。

#### agents/（Agent 配置）

**原始位置**: `/root/.openclaw/agents/`
**备份位置**: `config/agents/`

**包含内容**:
- `main/` - 主 Agent 的认证和模型配置
- `work-assistant/` - 工作助手的人设和身份配置

---

## 📚 核心内容

### AI 创业思维模型

- 普通人创业哲学
- 最小化验证思维
- 海星模式组织架构
- Agent 时代企业信息化

### OpenClaw 学习

- 多 Agent 系统设计
- 界面结构分析
- 技能包开发

### 项目记录

- AI 总裁项目分析
- 知识中台验证方案
- 智慧城市机器人

---

## 🔗 相关链接

- **OpenClaw 官网**: https://openclaw.ai
- **OpenClaw 文档**: https://docs.openclaw.ai
- **ClawHub 技能市场**: https://clawhub.com

---

## 📝 更新日志

| 日期 | 更新内容 |
|------|----------|
| 2026-03-15 | 初始化仓库，添加自动备份 |
| 2026-03-15 | 添加 Agent 配置备份 |
| 2026-03-15 | 添加 README 文档 |

---

## 👤 关于作者

**李志刚**
- 复合型人才（技术 × 传统 × 沟通）
- IT 背景 + 传统行业经验
- AI 坚定支持者和学习者

---

*本仓库由 OpenClaw 自动备份维护*
