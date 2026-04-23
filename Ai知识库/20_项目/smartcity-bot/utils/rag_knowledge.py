"""
RAG 知识库检索模块
================

支持从飞书多维表格和本地文档进行RAG检索
"""

import os
import sys
import json
from typing import List, Dict, Optional
from dataclasses import dataclass

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.feishu_api import feishu_api


@dataclass
class KnowledgeChunk:
    """知识片段"""
    id: str
    title: str
    content: str
    category: str
    subsystem: str
    source: str
    url: str
    score: float = 0.0


class RAGKnowledgeBase:
    """RAG知识库检索"""
    
    def __init__(self):
        self.app_token = os.getenv("FEISHU_BITABLE_TOKEN", "ZJ80b8lciakBaBss8x0cpCKQnhd")
        self.table_id = os.getenv("FEISHU_TABLE_ID", "tblhv9xQS1kkYJeP")
        self._cache = None
        self._cache_time = 0
    
    def _get_all_records(self, force_refresh: bool = False) -> List[Dict]:
        """获取所有知识库记录（带缓存）"""
        import time
        
        # 缓存5分钟
        if not force_refresh and self._cache and (time.time() - self._cache_time) < 300:
            return self._cache
        
        access_token = feishu_api.get_tenant_access_token()
        if not access_token:
            return []
        
        import requests
        
        all_records = []
        page_token = None
        
        while True:
            url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/records"
            
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
            
            params = {"page_size": 100}
            if page_token:
                params["page_token"] = page_token
            
            try:
                response = requests.get(url, headers=headers, params=params, timeout=10)
                result = response.json()
                
                if result.get("code") == 0:
                    items = result.get("data", {}).get("items", [])
                    all_records.extend(items)
                    
                    has_more = result.get("data", {}).get("has_more", False)
                    if has_more:
                        page_token = result.get("data", {}).get("page_token")
                    else:
                        break
                else:
                    break
            except Exception as e:
                print(f"获取记录失败: {e}")
                break
        
        # 过滤空记录
        valid_records = [r for r in all_records if r.get("fields", {}).get("标题")]
        
        self._cache = valid_records
        self._cache_time = time.time()
        
        return valid_records
    
    def search(self, query: str, limit: int = 10) -> List[KnowledgeChunk]:
        """
        搜索知识库
        
        Args:
            query: 搜索关键词
            limit: 返回数量
        
        Returns:
            匹配的知识片段列表
        """
        records = self._get_all_records()
        results = []
        
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        for record in records:
            fields = record.get("fields", {})
            title = fields.get("标题", "")
            content = fields.get("内容", "")
            category = fields.get("分类", "")
            subsystem = fields.get("子系统", "")
            source = fields.get("来源", "")
            url_data = fields.get("链接", {})
            url = url_data.get("link", "") if isinstance(url_data, dict) else ""
            
            if not title:
                continue
            
            # 计算匹配分数
            score = 0
            
            # 标题匹配（权重高）
            title_lower = title.lower()
            if query_lower in title_lower:
                score += 10
            for word in query_words:
                if word in title_lower:
                    score += 5
            
            # 内容匹配
            content_lower = content.lower() if content else ""
            if query_lower in content_lower:
                score += 5
            for word in query_words:
                if word in content_lower:
                    score += 2
            
            # 分类匹配
            if category and category.lower() in query_lower:
                score += 3
            
            # 子系统匹配
            if subsystem and subsystem.lower() in query_lower:
                score += 3
            
            if score > 0:
                results.append(KnowledgeChunk(
                    id=record.get("record_id", ""),
                    title=title,
                    content=content,
                    category=category,
                    subsystem=subsystem,
                    source=source,
                    url=url,
                    score=score
                ))
        
        # 按分数排序
        results.sort(key=lambda x: x.score, reverse=True)
        
        return results[:limit]
    
    def search_by_domain(self, domain: str, limit: int = 20) -> List[KnowledgeChunk]:
        """
        按领域搜索
        
        Args:
            domain: 智慧领域（如"智慧城市"、"智慧园区"）
            limit: 返回数量
        
        Returns:
            该领域的知识片段列表
        """
        records = self._get_all_records()
        results = []
        
        for record in records:
            fields = record.get("fields", {})
            title = fields.get("标题", "")
            content = fields.get("内容", "")
            category = fields.get("分类", "")
            subsystem = fields.get("子系统", "")
            source = fields.get("来源", "")
            url_data = fields.get("链接", {})
            url = url_data.get("link", "") if isinstance(url_data, dict) else ""
            
            # 检查是否匹配领域
            text = f"{title} {content} {category}".lower()
            if domain.lower() in text:
                results.append(KnowledgeChunk(
                    id=record.get("record_id", ""),
                    title=title,
                    content=content,
                    category=category,
                    subsystem=subsystem,
                    source=source,
                    url=url,
                    score=1.0
                ))
        
        return results[:limit]
    
    def search_by_subsystem(self, subsystem: str, limit: int = 20) -> List[KnowledgeChunk]:
        """
        按子系统搜索
        
        Args:
            subsystem: 子系统名称（如"安防系统"、"机房工程"）
            limit: 返回数量
        
        Returns:
            该子系统的知识片段列表
        """
        records = self._get_all_records()
        results = []
        
        for record in records:
            fields = record.get("fields", {})
            title = fields.get("标题", "")
            content = fields.get("内容", "")
            category = fields.get("分类", "")
            record_subsystem = fields.get("子系统", "")
            source = fields.get("来源", "")
            url_data = fields.get("链接", {})
            url = url_data.get("link", "") if isinstance(url_data, dict) else ""
            
            # 检查是否匹配子系统
            if subsystem.lower() in record_subsystem.lower():
                results.append(KnowledgeChunk(
                    id=record.get("record_id", ""),
                    title=title,
                    content=content,
                    category=category,
                    subsystem=record_subsystem,
                    source=source,
                    url=url,
                    score=1.0
                ))
        
        return results[:limit]
    
    def get_context_for_query(self, query: str, max_length: int = 4000) -> str:
        """
        获取用于RAG的上下文
        
        Args:
            query: 用户问题
            max_length: 最大上下文长度
        
        Returns:
            拼接的上下文文本
        """
        results = self.search(query, limit=5)
        
        if not results:
            return ""
        
        context_parts = []
        total_length = 0
        
        for r in results:
            part = f"【{r.title}】\n{r.content}\n"
            if total_length + len(part) > max_length:
                break
            context_parts.append(part)
            total_length += len(part)
        
        return "\n---\n".join(context_parts)
    
    def get_stats(self) -> Dict:
        """获取知识库统计"""
        records = self._get_all_records()
        
        categories = {}
        subsystems = {}
        
        for record in records:
            fields = record.get("fields", {})
            cat = fields.get("分类", "未分类")
            sub = fields.get("子系统", "通用")
            
            categories[cat] = categories.get(cat, 0) + 1
            subsystems[sub] = subsystems.get(sub, 0) + 1
        
        return {
            "total": len(records),
            "categories": categories,
            "subsystems": subsystems
        }


# 全局实例
rag_kb = RAGKnowledgeBase()


# 测试
if __name__ == "__main__":
    print("🧪 测试 RAG 知识库检索\n")
    
    # 统计
    stats = rag_kb.get_stats()
    print(f"📊 知识库统计：")
    print(f"   总条目: {stats['total']}")
    print(f"   分类数: {len(stats['categories'])}")
    print(f"   子系统数: {len(stats['subsystems'])}")
    
    # 搜索测试
    print("\n🔍 搜索测试：")
    
    test_queries = [
        "智慧园区 安防系统",
        "机房工程 UPS",
        "物联网平台",
    ]
    
    for q in test_queries:
        print(f"\n   查询: {q}")
        results = rag_kb.search(q, limit=3)
        for r in results:
            print(f"   - [{r.score}分] {r.title}")
    
    # RAG上下文测试
    print("\n📝 RAG上下文测试：")
    context = rag_kb.get_context_for_query("智慧城市如何建设安防系统？")
    print(f"   上下文长度: {len(context)} 字符")
    print(f"   预览: {context[:200]}...")
