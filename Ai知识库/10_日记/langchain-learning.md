# LangChain 学习记录

## 学习进度

- Day 1-3: 基础概念和简单应用
- **Day 4 (2026-02-27): Agent 开发实战** ← 当前

## Day 4 学习目标

### 核心内容
1. **构建基础 Agent** - 使用 create_agent 创建智能代理
2. **工具(Tools)开发** - 创建自定义工具函数
3. **系统提示词(System Prompt)** - 设计 Agent 行为
4. **模型配置** - 设置语言模型参数
5. **结构化输出** - 定义响应格式
6. **对话记忆(Memory)** - 实现多轮对话

### 实战项目
构建一个天气预报 Agent，具备以下能力：
- 获取天气信息
- 识别用户位置
- 生成幽默回复（双关语）
- 记住对话历史

## 学习资源
- 官方文档: https://docs.langchain.com/oss/python/langchain/quickstart
- 代码示例: 见下方

## 代码笔记

### 1. 基础 Agent 结构
```python
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="claude-sonnet-4-5-20250929",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

# 运行 agent
agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)
```

### 2. 高级特性

#### 工具开发
```python
from langchain.tools import tool, ToolRuntime

@tool
def get_weather_for_location(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

# 使用运行时上下文
@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """Retrieve user information based on user ID."""
    user_id = runtime.context.user_id
    return "Florida" if user_id == "1" else "SF"
```

#### 模型配置
```python
from langchain.chat_models import init_chat_model

model = init_chat_model(
    "claude-sonnet-4-5-20250929",
    temperature=0.5,
    timeout=10,
    max_tokens=1000
)
```

#### 结构化输出
```python
from dataclasses import dataclass

@dataclass
class ResponseFormat:
    """Response schema for the agent."""
    punny_response: str  # 必需字段
    weather_conditions: str | None = None  # 可选字段
```

#### 添加记忆
```python
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()

agent = create_agent(
    model=model,
    tools=[...],
    checkpointer=checkpointer  # 启用记忆
)

# 使用 thread_id 维护对话
config = {"configurable": {"thread_id": "1"}}
response = agent.invoke(messages, config=config)
```

## 学习要点

### 关键概念
1. **Agent**: 能够调用工具和模型的智能代理
2. **Tools**: Agent 可以调用的函数
3. **System Prompt**: 定义 Agent 的角色和行为
4. **Runtime Context**: 工具运行时的上下文信息
5. **Checkpointer**: 保存对话状态的组件
6. **Thread ID**: 标识对话的唯一ID

### 最佳实践
- ✅ 工具函数要有清晰的文档字符串
- ✅ System Prompt 要具体且可操作
- ✅ 生产环境使用持久化的 checkpointer
- ✅ 为结构化输出定义明确的 schema
- ✅ 使用 temperature 控制响应的创造性

## 下一步
- [ ] 实践代码示例
- [ ] 尝试不同的工具组合
- [ ] 测试多轮对话
- [ ] 探索更多 LangChain 功能

---
*创建时间: 2026-02-27*
