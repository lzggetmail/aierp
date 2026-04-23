"""
GLM-5 工具类
============

封装智谱AI GLM-5 API调用
"""

import os
import json
import requests
from typing import Dict, List, Optional
from config.config import llm_config


class GLMClient:
    """GLM客户端"""
    
    def __init__(self):
        self.api_key = llm_config.api_key
        self.model = llm_config.model
        self.base_url = llm_config.base_url
    
    def chat(self, messages: List[Dict], temperature: float = None) -> str:
        """
        发送对话请求
        
        Args:
            messages: 消息列表 [{"role": "user", "content": "..."}]
            temperature: 温度参数
        
        Returns:
            回复内容
        """
        url = f"{self.base_url}/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature or llm_config.temperature,
            "max_tokens": llm_config.max_tokens
        }
        
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        
        if "error" in result:
            raise Exception(f"GLM API错误: {result['error']}")
        
        return result["choices"][0]["message"]["content"]
    
    def analyze_content(self, text: str) -> Dict:
        """
        分析内容（用于知识提取）
        
        Args:
            text: 待分析文本
        
        Returns:
            分析结果
        """
        prompt = f"""分析以下智慧城市相关的文本，提取关键信息：

{text}

请以JSON格式返回：
{{
    "title": "标题",
    "category": "分类（如：安防系统、机房工程、智能交通等）",
    "summary": "100字以内的摘要",
    "keywords": ["关键词1", "关键词2"],
    "tags": ["标签1", "标签2"],
    "value_score": 1-10的价值评分
}}

只返回JSON，不要其他内容。"""

        messages = [{"role": "user", "content": prompt}]
        
        try:
            result = self.chat(messages, temperature=0.3)
            # 解析JSON
            return json.loads(result)
        except Exception as e:
            print(f"GLM分析失败: {e}")
            return {
                "title": "分析失败",
                "category": "其他",
                "summary": text[:100],
                "keywords": [],
                "tags": [],
                "value_score": 5
            }
    
    def answer_question(self, question: str, context: str = "") -> str:
        """
        回答问题
        
        Args:
            question: 问题
            context: 上下文（知识库内容）
        
        Returns:
            回答
        """
        if context:
            prompt = f"""基于以下知识库内容回答问题。

知识库内容：
{context}

问题：{question}

请提供专业、准确的回答，必要时引用相关知识。"""
        else:
            prompt = f"""你是智慧城市领域的专家助手。

问题：{question}

请提供专业、准确的回答。"""
        
        messages = [{"role": "user", "content": prompt}]
        return self.chat(messages)


# 全局实例
glm_client = GLMClient()


if __name__ == "__main__":
    # 测试GLM连接
    client = GLMClient()
    
    if not client.api_key:
        print("❌ 请设置 GLM_API_KEY 环境变量")
    else:
        print(f"✅ GLM配置：{client.model}")
        
        # 测试对话
        try:
            response = client.chat([{"role": "user", "content": "你好，请用一句话介绍智慧城市"}])
            print(f"\n回答: {response}")
        except Exception as e:
            print(f"❌ 测试失败: {e}")
