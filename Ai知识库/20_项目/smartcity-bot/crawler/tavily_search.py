"""
Tavily 搜索采集器
================

使用 Tavily API 搜索智慧城市相关技术资料
"""

import os
import requests
from typing import List, Dict
from dataclasses import dataclass
import time


@dataclass
class SearchResult:
    """搜索结果"""
    title: str
    url: str
    content: str
    source: str
    score: float


class TavilySearcher:
    """Tavily 搜索器"""
    
    def __init__(self):
        self.api_key = os.getenv("TAVILY_API_KEY", "")
        self.base_url = "https://api.tavily.com"
        
        # 搜索关键词配置
        self.search_queries = [
            "智慧城市建设方案 技术规范",
            "智能安防系统 设计标准",
            "物联网平台 架构设计",
            "城市大脑 数据中台",
            "智慧交通 信号控制",
            "数字孪生城市 BIM GIS",
            "智慧社区 解决方案",
            "数据中心机房 建设标准",
            "综合布线系统 设计规范",
            "楼宇自控 BAS 系统",
        ]
    
    def search(self, query: str, max_results: int = 10) -> List[SearchResult]:
        """
        搜索
        
        Args:
            query: 搜索关键词
            max_results: 最大结果数
        
        Returns:
            搜索结果列表
        """
        if not self.api_key:
            print("❌ 未配置 TAVILY_API_KEY")
            return []
        
        url = f"{self.base_url}/search"
        
        payload = {
            "api_key": self.api_key,
            "query": query,
            "search_depth": "advanced",
            "include_answer": False,
            "include_raw_content": True,
            "max_results": max_results,
            "include_domains": [],
            "exclude_domains": []
        }
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            result = response.json()
            
            if response.status_code != 200:
                print(f"❌ 搜索失败: {result.get('error', '未知错误')}")
                return []
            
            results = []
            for item in result.get("results", []):
                results.append(SearchResult(
                    title=item.get("title", ""),
                    url=item.get("url", ""),
                    content=item.get("content", item.get("raw_content", "")),
                    source=item.get("url", "").split("/")[2] if "/" in item.get("url", "") else "未知",
                    score=item.get("score", 0)
                ))
            
            return results
            
        except Exception as e:
            print(f"❌ 搜索异常: {e}")
            return []
    
    def search_all(self, max_results_per_query: int = 5) -> List[SearchResult]:
        """
        执行所有搜索
        
        Args:
            max_results_per_query: 每个关键词的最大结果数
        
        Returns:
            所有搜索结果
        """
        all_results = []
        
        print(f"\n🔍 开始 Tavily 搜索...")
        print(f"   关键词数量: {len(self.search_queries)}")
        
        for i, query in enumerate(self.search_queries, 1):
            print(f"\n[{i}/{len(self.search_queries)}] 搜索: {query}")
            
            results = self.search(query, max_results_per_query)
            
            if results:
                print(f"   找到 {len(results)} 条结果")
                for r in results[:3]:
                    print(f"   - {r.title[:50]}...")
                all_results.extend(results)
            else:
                print(f"   未找到结果")
            
            # 礼貌延迟
            time.sleep(1)
        
        # 去重
        seen_urls = set()
        unique_results = []
        for r in all_results:
            if r.url not in seen_urls:
                seen_urls.add(r.url)
                unique_results.append(r)
        
        print(f"\n✅ 搜索完成，共 {len(unique_results)} 条不重复结果")
        return unique_results


def run_tavily_search():
    """运行 Tavily 搜索"""
    from utils.knowledge_base import knowledge_base
    
    # 加载环境变量
    env_file = os.path.join(os.path.dirname(__file__), "..", ".env")
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key] = value
    
    searcher = TavilySearcher()
    results = searcher.search_all(max_results_per_query=5)
    
    print(f"\n📊 搜索结果统计:")
    print(f"   总数: {len(results)}")
    
    # 显示前5条
    for i, r in enumerate(results[:5], 1):
        print(f"\n{i}. {r.title}")
        print(f"   来源: {r.source}")
        print(f"   内容长度: {len(r.content)} 字符")
        print(f"   链接: {r.url}")
    
    return results


if __name__ == "__main__":
    run_tavily_search()
