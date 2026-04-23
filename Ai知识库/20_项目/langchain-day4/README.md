# LangChain Day 4 学习材料

## 📚 学习目标

今天我们将学习如何构建一个**完整的 AI Agent**，掌握以下核心技能：

1. ✅ **Agent 架构** - 理解 LangChain Agent 的工作原理
2. ✅ **工具开发** - 创建自定义工具函数
3. ✅ **系统提示词** - 设计 Agent 的行为和角色
4. ✅ **结构化输出** - 定义规范的响应格式
5. ✅ **对话记忆** - 实现多轮对话的上下文管理

## 🚀 快速开始

### 环境准备

```bash
# 安装 LangChain
pip install langchain langgraph

# 设置 API Key
export ANTHROPIC_API_KEY="your-api-key-here"
```

### 运行示例

```bash
cd /root/.openclaw/workspace/projects/langchain-day4
python weather_agent.py
```

## 📖 核心概念详解

### 1. Agent 是什么？

**Agent = LLM + Tools + Memory**

- **LLM**: 大语言模型（如 Claude、GPT）
- **Tools**: 可以调用的函数/工具
- **Memory**: 记住对话历史的能力

### 2. 创建工具 (Tools)

```python
from langchain.tools import tool

@tool
def my_custom_tool(param: str) -> str:
    """工具的描述很重要，会被 LLM 看到"""
    # 你的逻辑
    return "result"
```

**关键点**：
- 使用 `@tool` 装饰器
- 写清晰的文档字符串
- 定义明确的参数类型

### 3. 系统提示词 (System Prompt)

```python
SYSTEM_PROMPT = """You are a helpful assistant.

You have access to these tools:
- tool1: 用于...
- tool2: 用于...

When to use which tool:
- 如果用户问...，使用 tool1
- 如果用户需要...，使用 tool2
"""
```

**最佳实践**：
- ✅ 明确 Agent 的角色
- ✅ 列出可用工具
- ✅ 说明何时使用哪个工具
- ✅ 提供具体的行为指导

### 4. 结构化输出

```python
from dataclasses import dataclass

@dataclass
class ResponseFormat:
    """定义响应的结构"""
    answer: str  # 必需字段
    confidence: float | None = None  # 可选字段
```

**好处**：
- 🎯 响应格式一致
- 📊 易于解析和处理
- 🔍 类型安全

### 5. 对话记忆

```python
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()

agent = create_agent(
    ...,
    checkpointer=checkpointer  # 启用记忆
)

# 使用 thread_id 维护对话
config = {"configurable": {"thread_id": "user-123"}}
agent.invoke(messages, config=config)
```

**注意**：
- `InMemorySaver` 适合开发测试
- 生产环境应使用数据库持久化
- `thread_id` 标识唯一的对话

## 🎯 实战练习

### 练习 1: 添加新工具

在 `weather_agent.py` 中添加一个新工具：

```python
@tool
def get_temperature(city: str) -> str:
    """Get temperature for a given city in Celsius."""
    # 实现你的逻辑
    return f"Temperature in {city} is 25°C"
```

### 练习 2: 修改系统提示词

让 Agent 用不同的风格回复（比如：海盗风格、诗人风格）

### 练习 3: 扩展响应格式

添加更多字段到 `ResponseFormat`：

```python
@dataclass
class ResponseFormat:
    punny_response: str
    weather_conditions: str | None = None
    temperature: str | None = None  # 新增
    recommendation: str | None = None  # 新增
```

## 🔍 深入理解

### Agent 工作流程

```
用户输入
   ↓
System Prompt + 用户消息
   ↓
LLM 决定是否调用工具
   ↓
如果需要 → 调用工具 → 获取结果
   ↓
LLM 生成最终回复
   ↓
结构化输出
   ↓
保存到记忆（如果启用）
```

### Runtime Context

```python
@tool
def my_tool(runtime: ToolRuntime[Context]) -> str:
    """可以访问运行时上下文的工具"""
    user_id = runtime.context.user_id
    # 使用上下文信息
    return f"Processing for user {user_id}"
```

**用途**：
- 访问用户信息
- 获取会话数据
- 传递配置参数

## 📝 学习检查清单

完成以下任务，确保掌握 Day 4 内容：

- [ ] 理解 Agent 的三个核心组件
- [ ] 能创建自定义工具函数
- [ ] 能编写有效的系统提示词
- [ ] 理解结构化输出的作用
- [ ] 能实现对话记忆功能
- [ ] 运行 weather_agent.py 成功
- [ ] 完成 3 个练习任务

## 🐛 常见问题

### Q1: Agent 不调用工具？
**A**: 检查系统提示词是否清晰说明了工具的用途

### Q2: 响应格式不对？
**A**: 确保使用了 `ToolStrategy(ResponseFormat)`

### Q3: Agent 不记得之前的对话？
**A**: 确保使用了相同的 `thread_id` 和 `checkpointer`

## 📚 延伸阅读

- [LangChain 官方文档](https://docs.langchain.com)
- [LangGraph 文档](https://langchain-ai.github.io/langgraph/)
- [Tool 开发指南](https://python.langchain.com/docs/modules/tools/)

## 🎉 完成后

完成今天的学习后，你应该能够：

1. ✅ 独立创建一个完整的 LangChain Agent
2. ✅ 为 Agent 添加自定义工具
3. ✅ 控制 Agent 的行为和输出
4. ✅ 实现多轮对话功能

**准备好开始了吗？** 运行 `python weather_agent.py` 开始实践！

---
*创建时间: 2026-02-27*
*LangChain Day 4 学习材料*
