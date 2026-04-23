# 天气查询Agent

LangChain实践项目 - 天气查询Agent

## 📁 文件说明

- `weather_agent.py` - 主程序文件

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install langchain langgraph requests
```

### 2. 申请API Key

**OpenAI API Key**（必需）
- 访问：https://platform.openai.com/api-keys
- 创建API Key
- 设置环境变量：
  ```bash
  export OPENAI_API_KEY="your_key_here"
  ```

**OpenWeather API Key**（免费）
- 访问：https://openweathermap.org/api
- 免费注册
- 获取API Key
- 设置环境变量：
  ```bash
  export OPENWEATHER_API_KEY="your_key_here"
  ```

### 3. 运行程序

```bash
python weather_agent.py
```

## 📝 使用示例

```
👤 您：北京天气怎么样？
🤖 Agent：北京今天晴，温度25°C，湿度45%，风速3米/秒

👤 您：上海呢？
🤖 Agent：上海今天多云，温度28°C，湿度60%，风速2米/秒

👤 您：未来3天天气怎么样？
🤖 Agent：北京未来3天天气预报：
2026-03-01：晴，26°C
2026-03-02：多云，24°C
2026-03-03：小雨，22°C
```

## 🧪 测试工具

如果只想测试工具函数（不需要LLM），修改 `weather_agent.py` 最后一行：

```python
if __name__ == "__main__":
    test_tools()  # 测试工具
    # main()      # 运行主程序
```

## 📚 学习要点

这个项目演示了：

1. **工具定义** - `@tool` 装饰器
2. **错误处理** - try/except、友好提示
3. **Agent创建** - create_agent
4. **对话记忆** - InMemorySaver
5. **System Prompt** - 定义Agent行为

## 🔧 常见问题

**Q: 运行报错 "No module named 'langchain'"**
A: 安装依赖：`pip install langchain langgraph`

**Q: 运行报错 "OPENAI_API_KEY not found"**
A: 设置环境变量：`export OPENAI_API_KEY="your_key"`

**Q: 天气查询失败**
A: 检查OPENWEATHER_API_KEY是否正确设置

## 📖 相关文档

- LangChain文档：https://docs.langchain.com
- OpenWeather API：https://openweathermap.org/api

---
*LangChain Day 4-14 实践项目*
*2026-02-28*
