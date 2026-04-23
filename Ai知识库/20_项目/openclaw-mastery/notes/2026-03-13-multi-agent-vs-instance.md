# 学习笔记：多 Agent vs 多实例

**日期**: 2026-03-13
**主题**: 澄清"多龙虾"的概念

---

## 两种"多龙虾"方案

### 方案A：多 Agent（推荐）

```
一个 OpenClaw 安装
    │
    └── 一个 Gateway 进程
            │
            ├── main 龙虾（独立工作区）
            ├── work 龙虾（独立工作区）
            └── family 龙虾（独立工作区）
```

**特点**：
- 只安装一次 OpenClaw
- 通过配置文件创建多只龙虾
- 共享 Gateway 进程

---

### 方案B：多实例

```
OpenClaw 实例1（服务器A）
OpenClaw 实例2（服务器B）
```

**特点**：
- 安装多次 OpenClaw
- 完全物理隔离

---

## 纠正之前的说法

| 之前说的 | 正确的说法 |
|----------|-----------|
| "每只龙虾需要不同的 openclaw 实体" | ❌ 不准确 |
| "每只龙虾需要不同的工作区" | ✅ 正确 |

---

## 关键

**多 Agent = 不同的 workspace**

```json
{
  "agents": {
    "list": [
      { "id": "main", "workspace": "~/.openclaw/workspace" },
      { "id": "work", "workspace": "~/.openclaw/workspace-work" }
    ]
  }
}
```

---

*学习时间: 2026-03-13 09:29*
