# 学习笔记：多龙虾（多Agent）

**日期**: 2026-03-13
**主题**: 一台服务器养多只龙虾

---

## 为什么需要多只龙虾？

- 多人共用一台服务器
- 不同用途（工作 vs 生活）
- 不同模型（便宜 vs 强大）
- 不同权限（公开 vs 受限）

---

## 架构

```
Gateway（一个进程）
    │
    ├── main 龙虾（独立工作区、记忆、会话）
    ├── work 龙虾（独立工作区、记忆、会话）
    └── family 龙虾（独立工作区、记忆、会话）
```

---

## 每只龙虾的独立组件

| 组件 | 位置 |
|------|------|
| Workspace | `~/.openclaw/workspace-<agentId>` |
| agentDir | `~/.openclaw/agents/<agentId>/agent` |
| Sessions | `~/.openclaw/agents/<agentId>/sessions` |

---

## 命令

```bash
# 创建新龙虾
openclaw agents add <名字>

# 查看所有龙虾
openclaw agents list

# 查看绑定规则
openclaw agents list --bindings
```

---

## 配置示例

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "workspace": "~/.openclaw/workspace",
        "model": "glmcode/glm-5"
      },
      {
        "id": "work",
        "workspace": "~/.openclaw/workspace-work",
        "model": "anthropic/claude-opus-4"
      }
    ]
  }
}
```

---

## 关键理解

- 龙虾之间**不会串台**
- 每只龙虾的记忆完全独立
- 可以用不同模型（省钱）
- 可以有不同性格

---

*学习时间: 2026-03-13 09:16*
