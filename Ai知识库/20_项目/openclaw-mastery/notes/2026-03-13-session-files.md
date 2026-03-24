# 学习笔记：会话文件存储

**日期**: 2026-03-13
**主题**: 理解会话文件的存储格式

---

## 文件位置
```
~/.openclaw/agents/<agentId>/sessions/
```

## 实际文件命名格式
```
0972de53-4fcb-4318-a2e7-c366256db2ce.jsonl
```
- 这是 **UUID 格式**（随机生成的唯一ID）
- 不是描述性名称

## 文件格式
- .jsonl = 每行一个 JSON 对象
- 每行 = 一条消息或事件

## 文件内容结构

**第一行（会话元数据）**：
```json
{"type":"session","version":3,"id":"0972de53-xxx","timestamp":"2026-03-10T01:17:04.663Z","cwd":"/root/.openclaw/workspace"}
```
- `type: "session"` — 会话开始标记
- `version: 3` — 格式版本
- `id` — 会话ID（就是文件名）
- `timestamp` — 创建时间（UTC）
- `cwd` — 工作目录

**后面的行**：
```json
{"type":"message","id":"xxx","timestamp":"...","message":{"role":"user/assistant","content":[...]}}
```
- 每行是一条消息

## 查看会话内容

```bash
# 搜索包含关键词的会话
grep -l "关键词" ~/.openclaw/agents/main/sessions/*.jsonl

# 查看会话元数据
head -1 ~/.openclaw/agents/main/sessions/0972de53-xxx.jsonl

# 查看完整内容
cat ~/.openclaw/agents/main/sessions/0972de53-xxx.jsonl
```

---

*学习时间: 2026-03-13 09:14*
*纠正：文件名只有UUID格式，没有描述性命名*
