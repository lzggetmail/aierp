# HEARTBEAT.md

# 心跳检查任务

> 此文件定义心跳触发时要做什么。
> 晨间简报已改为定时任务（每天 8:30）

---

## 心跳任务

### 1. OpenClaw 动态追踪

**检查内容**：
- 检查 OpenClaw GitHub 最新 Release
- 对比 `projects/openclaw-tracker/README.md` 中记录的版本
- 如有新版本，提取重要更新并推送

**关键词过滤**：browser, MCP, agent, skill, cron, memory, feishu

**推送格式**：
```
🦞 OpenClaw 更新提醒
新版本：vX.X.X
重要更新：
- xxx
- xxx
```

### 2. 钉钉悟空动态追踪

**检查内容**：
- 搜索钉钉悟空平台最新动态
- 关键词：悟空、开放政策、入驻条件、分成模式、Skill开发

**触发条件**：
- 有新的开放政策发布
- Q2正式上线
- 开发者入驻条件变化

**推送格式**：
```
🦈 钉钉悟空更新提醒
更新内容：
- xxx
- xxx
```

---

## 无需提醒时

回复：`HEARTBEAT_OK`

---

*创建时间: 2026-03-13*
*更新时间: 2026-03-17*
