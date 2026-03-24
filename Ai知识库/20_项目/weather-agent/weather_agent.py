"""
天气查询Agent - LangChain实践项目
================================

这是一个简单的天气查询Agent，演示：
1. 工具定义（@tool装饰器）
2. Agent创建
3. 对话记忆
4. 错误处理

运行前准备：
1. 安装依赖：pip install langchain langgraph requests
2. 设置环境变量：OPENAI_API_KEY=your_key
3. 申请天气API：https://openweathermap.org/api

作者：LangChain学习Day 4-14毕业生
日期：2026-02-28
"""

# ============================================
# 1. 导入依赖
# ============================================
import os
import requests
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver

# ============================================
# 2. 定义工具
# ============================================

@tool
def get_weather(city: str) -> str:
    """
    查询指定城市的当前天气情况
    
    参数:
        city: 城市名称，如"北京"、"上海"、"广州"
    
    返回:
        天气信息，如"北京今天晴，温度25°C"
    
    示例:
        >>> get_weather("北京")
        "北京今天晴，温度25°C"
    """
    try:
        # 注意：这里需要您申请OpenWeather API Key
        # 免费申请地址：https://openweathermap.org/api
        API_KEY = os.getenv("OPENWEATHER_API_KEY", "your_api_key_here")
        
        # 调用OpenWeather API
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric",  # 摄氏度
            "lang": "zh_cn"     # 中文
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        # 错误处理：城市不存在
        if response.status_code == 404:
            return f"未找到城市'{city}'，请检查城市名称是否正确"
        
        # 错误处理：API错误
        if response.status_code != 200:
            return f"查询失败（错误码：{response.status_code}），请稍后重试"
        
        # 解析返回数据
        data = response.json()
        temp = data["main"]["temp"]
        weather = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        
        # 格式化输出
        return f"{city}今天{weather}，温度{temp}°C，湿度{humidity}%，风速{wind_speed}米/秒"
        
    except requests.Timeout:
        return "查询超时，请检查网络连接后重试"
    except requests.RequestException as e:
        return f"网络错误，请稍后重试"
    except Exception as e:
        return f"查询失败：{str(e)}"


@tool
def get_weather_forecast(city: str, days: int = 3) -> str:
    """
    查询指定城市未来几天的天气预报
    
    参数:
        city: 城市名称
        days: 预报天数（1-5天），默认3天
    
    返回:
        天气预报信息
    """
    try:
        API_KEY = os.getenv("OPENWEATHER_API_KEY", "your_api_key_here")
        
        url = "https://api.openweathermap.org/data/2.5/forecast"
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric",
            "lang": "zh_cn",
            "cnt": days * 8  # 每天8个时间点
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 404:
            return f"未找到城市'{city}'"
        
        if response.status_code != 200:
            return f"查询失败，请稍后重试"
        
        data = response.json()
        
        # 简化输出：只返回每天的天气
        forecast_list = []
        for item in data["list"][::8]:  # 每天取一个时间点
            date = item["dt_txt"].split()[0]
            temp = item["main"]["temp"]
            weather = item["weather"][0]["description"]
            forecast_list.append(f"{date}：{weather}，{temp}°C")
        
        return f"{city}未来{days}天天气预报：\n" + "\n".join(forecast_list)
        
    except Exception as e:
        return f"查询失败：{str(e)}"


# ============================================
# 3. System Prompt
# ============================================

SYSTEM_PROMPT = """
# 角色
你是一个专业的天气助手，能够帮助用户查询城市天气。

# 技能
- 查询指定城市的当前天气
- 查询未来几天的天气预报
- 用友好、简洁的方式回答

# 服务方式
- 热情、专业
- 回答简洁明了
- 如果城市名不清楚，礼貌询问

# 工作流程
1. 确认用户想查询的城市
2. 确认是当前天气还是预报
3. 调用相应工具查询
4. 用自然语言回复用户

# 约束
- 只回答天气相关问题
- 不确定的信息不要编造
- 如果查询失败，友好提示用户
"""


# ============================================
# 4. 创建Agent
# ============================================

def create_weather_agent():
    """创建天气查询Agent"""
    
    # 配置LLM（需要设置OPENAI_API_KEY环境变量）
    model = init_chat_model(
        "gpt-4o-mini",  # 使用便宜的模型
        temperature=0.7
    )
    
    # 创建记忆组件
    checkpointer = InMemorySaver()
    
    # 创建Agent
    agent = create_agent(
        model=model,
        tools=[get_weather, get_weather_forecast],
        system_prompt=SYSTEM_PROMPT,
        checkpointer=checkpointer
    )
    
    return agent


# ============================================
# 5. 运行Agent
# ============================================

def chat_with_agent(agent, user_input: str, thread_id: str = "default"):
    """
    与Agent对话
    
    参数:
        agent: Agent实例
        user_input: 用户输入
        thread_id: 对话ID（用于记忆）
    
    返回:
        Agent的回复
    """
    config = {"configurable": {"thread_id": thread_id}}
    
    response = agent.invoke(
        {"messages": [{"role": "user", "content": user_input}]},
        config=config
    )
    
    return response["messages"][-1].content


# ============================================
# 6. 主程序
# ============================================

def main():
    """主程序：交互式天气查询"""
    
    print("=" * 50)
    print("🌤️  天气查询Agent")
    print("=" * 50)
    print("输入城市名查询天气，输入 'quit' 退出")
    print()
    
    # 创建Agent
    try:
        agent = create_weather_agent()
        print("✅ Agent创建成功！")
    except Exception as e:
        print(f"❌ Agent创建失败：{e}")
        print("请检查：")
        print("1. 是否安装了依赖：pip install langchain langgraph")
        print("2. 是否设置了环境变量：OPENAI_API_KEY")
        return
    
    print()
    
    # 交互循环
    while True:
        try:
            user_input = input("👤 您：").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q', '退出']:
                print("👋 再见！")
                break
            
            if not user_input:
                continue
            
            # 调用Agent
            print("🤖 Agent：", end="")
            response = chat_with_agent(agent, user_input)
            print(response)
            print()
            
        except KeyboardInterrupt:
            print("\n👋 再见！")
            break
        except Exception as e:
            print(f"❌ 错误：{e}")
            print()


# ============================================
# 7. 测试函数
# ============================================

def test_tools():
    """测试工具函数（不需要LLM）"""
    
    print("=" * 50)
    print("🧪 测试工具函数")
    print("=" * 50)
    
    # 测试查天气
    print("\n1. 测试 get_weather")
    print("-" * 30)
    result = get_weather("北京")
    print(f"北京天气：{result}")
    
    # 测试错误城市
    print("\n2. 测试错误城市名")
    print("-" * 30)
    result = get_weather("火星")
    print(f"火星天气：{result}")
    
    # 测试预报
    print("\n3. 测试 get_weather_forecast")
    print("-" * 30)
    result = get_weather_forecast("上海", days=2)
    print(result)


# ============================================
# 入口
# ============================================

if __name__ == "__main__":
    # 如果只想测试工具，取消下面这行的注释
    # test_tools()
    
    # 运行主程序
    main()
