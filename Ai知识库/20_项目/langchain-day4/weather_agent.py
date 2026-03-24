"""
LangChain Day 4 - 天气预报 Agent 实战示例
功能：构建一个能记住对话、调用工具、生成幽默回复的智能 Agent
"""

from dataclasses import dataclass
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool, ToolRuntime
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.structured_output import ToolStrategy


# ============================================
# 1. 定义系统提示词
# ============================================
SYSTEM_PROMPT = """You are an expert weather forecaster, who speaks in puns.

You have access to two tools:

- get_weather_for_location: use this to get the weather for a specific location
- get_user_location: use this to get the user's location

If a user asks you for the weather, make sure you know the location. If you can tell from the question that they mean wherever they are, use the get_user_location tool to find their location."""


# ============================================
# 2. 定义上下文 Schema
# ============================================
@dataclass
class Context:
    """自定义运行时上下文"""
    user_id: str


# ============================================
# 3. 创建工具函数
# ============================================
@tool
def get_weather_for_location(city: str) -> str:
    """Get weather for a given city."""
    # 这里可以接入真实的天气 API
    return f"It's always sunny in {city}!"


@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """Retrieve user information based on user ID."""
    # 从运行时上下文中获取用户信息
    user_id = runtime.context.user_id
    # 模拟根据用户ID返回位置
    return "Florida" if user_id == "1" else "SF"


# ============================================
# 4. 配置模型
# ============================================
model = init_chat_model(
    "claude-sonnet-4-5-20250929",
    temperature=0,  # 0 = 更确定的输出
    timeout=10,
    max_tokens=1000
)


# ============================================
# 5. 定义响应格式
# ============================================
@dataclass
class ResponseFormat:
    """Agent 响应的结构化格式"""
    punny_response: str  # 幽默的双关语回复（必需）
    weather_conditions: str | None = None  # 天气信息（可选）


# ============================================
# 6. 设置记忆系统
# ============================================
checkpointer = InMemorySaver()  # 生产环境应使用持久化存储


# ============================================
# 7. 创建并运行 Agent
# ============================================
def create_weather_agent():
    """创建天气 Agent"""
    agent = create_agent(
        model=model,
        system_prompt=SYSTEM_PROMPT,
        tools=[get_user_location, get_weather_for_location],
        context_schema=Context,
        response_format=ToolStrategy(ResponseFormat),
        checkpointer=checkpointer
    )
    return agent


def main():
    """主函数 - 演示 Agent 的使用"""
    agent = create_weather_agent()
    
    # thread_id 用于标识对话，同一个 ID 会保持上下文
    config = {"configurable": {"thread_id": "conversation-1"}}
    
    print("=" * 60)
    print("🌤️  LangChain 天气 Agent 启动")
    print("=" * 60)
    
    # 第一次对话
    print("\n[第1轮对话]")
    print("用户: what is the weather outside?")
    
    response1 = agent.invoke(
        {"messages": [{"role": "user", "content": "what is the weather outside?"}]},
        config=config,
        context=Context(user_id="1")
    )
    
    print(f"Agent: {response1['structured_response'].punny_response}")
    if response1['structured_response'].weather_conditions:
        print(f"天气: {response1['structured_response'].weather_conditions}")
    
    # 继续对话（Agent 会记住之前的上下文）
    print("\n[第2轮对话]")
    print("用户: thank you!")
    
    response2 = agent.invoke(
        {"messages": [{"role": "user", "content": "thank you!"}]},
        config=config,
        context=Context(user_id="1")
    )
    
    print(f"Agent: {response2['structured_response'].punny_response}")
    
    print("\n" + "=" * 60)
    print("✅ 演示完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
