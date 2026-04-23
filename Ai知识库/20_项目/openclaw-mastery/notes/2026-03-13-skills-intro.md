# 学习笔记：技能（Skills）

**日期**: 2026-03-13
**主题**: 给龙虾装"技能包"

---

## 什么是技能（Skills）？

**技能 = 能力插件**

给龙虾安装特定的能力，让它能干更多事情。

---

## 技能的类型

| 类型 | 说明 | 例子 |
|------|------|------|
| **内置技能** | OpenClaw 自带 | read, write, exec, browser |
| **安装技能** | 从市场安装 | weather, summarize, notion |
| **自定义技能** | 自己创建 | 针对你的业务场景 |

---

## 技能存储位置

```
~/.openclaw/skills/           # 共享技能
~/.openclaw/workspace/skills/ # 当前龙虾的技能
```

---

## 技能市场

### skillhub（国内优化）

```bash
# 搜索技能
skillhub search <关键词>

# 安装技能
skillhub install <技能名>
```

### clawhub（公共市场）

```bash
# 搜索技能
clawhub search <关键词>

# 安装技能
clawhub install <技能名>
```

---

## 常用技能

| 技能 | 用途 |
|------|------|
| weather | 天气查询 |
| summarize | 总结网页/PDF/视频 |
| notion | Notion 操作 |
| obsidian | Obsidian 笔记操作 |
| github | GitHub 操作 |

---

## 八、志刚的实用场景

### 场景1：天气查询

```bash
skillhub install weather
```

**然后你可以问**：
> "今天东莞天气怎么样？"

---

### 场景2：总结网页

```bash
skillhub install summarize
```

**然后你可以问**：
> "帮我总结这个网页：https://xxx.com"

---

### 场景3：Obsidian 笔记

```bash
skillhub install obsidian
```

**然后你可以问**：
> "帮我创建今天的日记"

---

## 九、总结

| 概念 | 说明 |
|------|------|
| **技能** | 能力插件，扩展龙虾的能力 |
| **市场** | skillhub（国内）、clawhub（公共） |
| **安装** | `skillhub install <技能名>` |
| **存储** | `~/.openclaw/skills/` 或 `workspace/skills/` |

---

## 十、已安装技能

| 技能 | 用途 | 安装时间 |
|------|------|----------|
| notebooklm-skill | 查询 Google NotebookLM 笔记本 | 2026-03-13 |

---

*学习时间: 2026-03-13 10:06*
