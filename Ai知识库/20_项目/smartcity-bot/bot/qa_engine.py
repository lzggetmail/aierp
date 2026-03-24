"""
智能问答模块
============

基于RAG的智能问答，从知识库检索相关内容后生成回答
"""

import os
import sys
import json
import requests
from typing import Optional, Dict, List
from dataclasses import dataclass

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.rag_knowledge import rag_kb, KnowledgeChunk
from utils.feishu_api import feishu_api


@dataclass
class AnswerResult:
    """回答结果"""
    question: str
    answer: str
    sources: List[KnowledgeChunk]
    has_knowledge: bool


class QAEngine:
    """问答引擎"""
    
    def __init__(self):
        self.glm_api_key = os.getenv("GLM_API_KEY", "")
        self.glm_model = os.getenv("GLM_MODEL", "glm-5")
        self.glm_base_url = "https://open.bigmodel.cn/api/anthropic"
        
        # 系统提示词
        self.system_prompt = """你是智慧城市助手，专注于智慧城市、智能化系统、物联网、AI等领域。

你的职责：
1. 基于提供的知识库内容回答用户问题
2. 如果知识库中有相关内容，优先使用知识库信息
3. 如果知识库中没有相关内容，可以基于你的专业知识回答，但要说明"以上是基于通用知识的回答"
4. 回答要专业、准确、简洁

回答格式：
- 直接回答问题，不要说"根据知识库"之类的开场白
- 如果有多个要点，用序号列表
- 如果知识库有相关案例或标准，可以引用"""

    def answer(self, question: str, use_rag: bool = True) -> AnswerResult:
        """
        回答问题
        
        Args:
            question: 用户问题
            use_rag: 是否使用RAG检索
        
        Returns:
            回答结果
        """
        # 1. 从知识库检索相关内容
        sources = []
        context = ""
        
        if use_rag:
            sources = rag_kb.search(question, limit=5)
            if sources:
                context = self._build_context(sources)
        
        # 2. 构建提示词
        if context:
            prompt = f"""参考知识：
{context}

用户问题：{question}

请基于以上知识回答问题，如果知识库内容不足以完全回答，可以补充你的专业知识。"""
        else:
            prompt = f"""用户问题：{question}

请基于你的专业知识回答。注意：知识库中暂无相关内容，以上是基于通用知识的回答。"""
        
        # 3. 调用大模型
        answer = self._call_llm(prompt)
        
        return AnswerResult(
            question=question,
            answer=answer,
            sources=sources,
            has_knowledge=len(sources) > 0
        )
    
    def _build_context(self, sources: List[KnowledgeChunk], max_length: int = 3000) -> str:
        """构建上下文"""
        parts = []
        total_length = 0
        
        for s in sources:
            part = f"【{s.title}】\n{s.content}\n"
            if total_length + len(part) > max_length:
                break
            parts.append(part)
            total_length += len(part)
        
        return "\n---\n".join(parts)
    
    def _call_llm(self, prompt: str) -> str:
        """调用大模型"""
        if not self.glm_api_key:
            return "⚠️ 未配置GLM API Key，无法生成回答"
        
        try:
            # 使用 Anthropic 兼容接口
            headers = {
                "Content-Type": "application/json",
                "x-api-key": self.glm_api_key,
                "anthropic-version": "2023-06-01"
            }
            
            data = {
                "model": "claude-3-5-sonnet-20241022",
                "max_tokens": 2000,
                "system": self.system_prompt,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
            
            response = requests.post(
                f"{self.glm_base_url}/v1/messages",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("content", [{}])[0].get("text", "生成回答失败")
            else:
                # 尝试原生GLM接口
                return self._call_glm_native(prompt)
                
        except Exception as e:
            return self._call_glm_native(prompt)
    
    def _call_glm_native(self, prompt: str) -> str:
        """调用原生GLM接口"""
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.glm_api_key}"
            }
            
            data = {
                "model": "glm-4-flash",
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 2000
            }
            
            response = requests.post(
                "https://open.bigmodel.cn/api/paas/v4/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("choices", [{}])[0].get("message", {}).get("content", "生成回答失败")
            else:
                return f"⚠️ 调用大模型失败: {response.status_code}"
                
        except Exception as e:
            return f"⚠️ 调用大模型异常: {str(e)}"
    
    def format_answer(self, result: AnswerResult, show_sources: bool = False) -> str:
        """
        格式化回答
        
        Args:
            result: 回答结果
            show_sources: 是否显示来源
        
        Returns:
            格式化的回答文本
        """
        lines = [result.answer]
        
        if show_sources and result.sources:
            lines.append("\n---")
            lines.append("📚 参考来源：")
            for s in result.sources[:3]:
                lines.append(f"• {s.title}" + (f" ({s.subsystem})" if s.subsystem else ""))
        
        return "\n".join(lines)


# 全局实例
qa_engine = QAEngine()


# 测试
if __name__ == "__main__":
    print("🧪 测试智能问答\n")
    
    test_questions = [
        "智慧园区的安防系统应该怎么设计？",
        "机房工程需要配置哪些设备？",
        "什么是城市信息模型CIM？",
    ]
    
    for q in test_questions:
        print(f"❓ 问题: {q}")
        result = qa_engine.answer(q)
        
        print(f"💡 回答:")
        print(result.answer)
        
        if result.sources:
            print(f"\n📚 参考来源 ({len(result.sources)}条):")
            for s in result.sources[:2]:
                print(f"   • {s.title}")
        
        print("\n" + "="*60 + "\n")
