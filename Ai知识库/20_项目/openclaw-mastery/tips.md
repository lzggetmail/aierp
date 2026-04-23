# 🦞 OpenClaw 实战技巧合集

> 持续更新的技巧库，每学到一个就记录一个

---

## 基础技巧

### 技巧1：查看龙虾状态
```bash
openclaw status
openclaw gateway status
```

### 技巧2：查看渠道连接
```bash
openclaw channels status --probe
```

### 技巧3：重启龙虾
```bash
openclaw gateway restart
```

---

## 配置技巧

### 技巧4：配置文件位置
```
~/.openclaw/openclaw.json
```

### 技巧5：查看当前配置
```bash
cat ~/.openclaw/openclaw.json
```

---

## 会话技巧

### 技巧6：会话存储位置
```
~/.openclaw/agents/<agentId>/sessions/
```

### 技巧7：会话命名规则
```
agent:<agentId>:<mainKey>
例如：agent:main:feishu:direct:ou_xxx
```

---

## 记忆技巧

### 技巧8：长期记忆文件
```
~/.openclaw/workspace/MEMORY.md
```

### 技巧9：每日记录
```
~/.openclaw/workspace/memory/YYYY-MM-DD.md
```

### 技巧10：让AI记住东西
直接说："记录下来" 或 "帮我保存到MEMORY.md"

### 技巧11：查看会话文件
```bash
# 会话文件位置
~/.openclaw/agents/<agentId>/sessions/

# 文件命名规则
agent_<agentId>_<channel>_<type>_<userId>_<timestamp>.jsonl

# 查看文件内容
cat 文件名.jsonl

# 搜索内容
grep "关键词" *.jsonl
```

---

## 多龙虾技巧

### 技巧11：添加新龙虾
```bash
openclaw agents add <龙虾名字>
```

### 技巧12：查看所有龙虾
```bash
openclaw agents list --bindings
```

### 技巧13：绑定渠道到龙虾
在 `openclaw.json` 中配置 `bindings`

---

## 高级技巧

### 技巧14：心跳机制
让龙虾定期主动检查任务，而不是等消息

### 技巧15：子代理
派一只小龙虾去干复杂任务，完成后汇报

### 技巧16：技能安装
```bash
clawhub search <关键词>
clawhub install <技能名>
```

---

*持续更新中...*
