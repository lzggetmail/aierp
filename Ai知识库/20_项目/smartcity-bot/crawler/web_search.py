"""
全网搜索模块
============

使用搜索API自动搜索智慧城市相关资料

支持的搜索源：
- Google Custom Search API
- Bing Search API
"""

import os
import requests
from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime


@dataclass
class SearchResult:
    """搜索结果"""
    title: str           # 标题
    url: str             # 链接
    snippet: str         # 摘要
    source: str          # 来源
    date: str            # 日期
    category: str = ""   # 分类


class WebSearcher:
    """全网搜索器"""
    
    def __init__(self):
        # Google Custom Search API配置
        self.google_api_key = os.getenv("GOOGLE_API_KEY", "")
        self.google_cx = os.getenv("GOOGLE_CX", "")  # 自定义搜索引擎ID
        
        # Bing Search API配置（备用）
        self.bing_api_key = os.getenv("BING_API_KEY", "")
        
        # 搜索关键词配置
        self.search_queries = [
            # 新闻类
            "智慧城市 新闻 2026",
            "智慧城市 发布 新品",
            "智慧城市 政策 标准",
            
            # 技术类
            "安防系统 新技术",
            "机房工程 方案",
            "智能交通 解决方案",
            "物联网 智慧城市",
            
            # 报告类
            "智慧城市 白皮书",
            "智慧城市 研究报告",
            "智慧城市 行业分析"
        ]
    
    def search_google(self, query: str, num_results: int = 10) -> List[SearchResult]:
        """
        使用Google Custom Search API搜索
        
        Args:
            query: 搜索关键词
            num_results: 返回结果数量
        
        Returns:
            搜索结果列表
        """
        if not self.google_api_key or not self.google_cx:
            print("⚠️ Google API未配置，使用模拟数据")
            return self._get_mock_results(query)
        
        url = "https://www.googleapis.com/customsearch/v1"
        
        params = {
            "key": self.google_api_key,
            "cx": self.google_cx,
            "q": query,
            "num": num_results,
            "dateRestrict": "d7"  # 限制最近7天
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            result = response.json()
            
            if "error" in result:
                print(f"❌ Google搜索失败: {result['error']}")
                return []
            
            results = []
            for item in result.get("items", []):
                results.append(SearchResult(
                    title=item.get("title", ""),
                    url=item.get("link", ""),
                    snippet=item.get("snippet", ""),
                    source="Google",
                    date=datetime.now().strftime("%Y-%m-%d")
                ))
            
            return results
            
        except Exception as e:
            print(f"❌ 搜索异常: {e}")
            return []
    
    def search_bing(self, query: str, num_results: int = 10) -> List[SearchResult]:
        """
        使用Bing Search API搜索（备用）
        """
        if not self.bing_api_key:
            return []
        
        url = "https://api.bing.microsoft.com/v7.0/search"
        
        headers = {
            "Ocp-Apim-Subscription-Key": self.bing_api_key
        }
        
        params = {
            "q": query,
            "count": num_results,
            "freshness": "Week"  # 最近一周
        }
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            result = response.json()
            
            results = []
            for item in result.get("webPages", {}).get("value", []):
                results.append(SearchResult(
                    title=item.get("name", ""),
                    url=item.get("url", ""),
                    snippet=item.get("snippet", ""),
                    source="Bing",
                    date=datetime.now().strftime("%Y-%m-%d")
                ))
            
            return results
            
        except Exception as e:
            print(f"❌ Bing搜索异常: {e}")
            return []
    
    def search_all(self) -> List[SearchResult]:
        """
        执行所有关键词搜索
        
        Returns:
            所有搜索结果
        """
        all_results = []
        
        print(f"\n🔍 开始全网搜索...")
        print(f"   关键词数量: {len(self.search_queries)}")
        
        for i, query in enumerate(self.search_queries, 1):
            print(f"   [{i}/{len(self.search_queries)}] 搜索: {query}")
            
            # 优先使用Google
            results = self.search_google(query)
            
            # 如果Google失败，尝试Bing
            if not results:
                results = self.search_bing(query)
            
            all_results.extend(results)
        
        print(f"\n✅ 搜索完成，共获取 {len(all_results)} 条结果")
        
        return all_results
    
    def _get_mock_results(self, query: str) -> List[SearchResult]:
        """
        获取模拟搜索结果（用于测试）
        """
        mock_data = [
            {
                "title": "2026智慧城市发展白皮书发布",
                "url": "https://example.com/whitepaper-2026",
                "snippet": "最新智慧城市发展报告，涵盖AI、物联网、数字孪生等技术趋势...",
                "source": "模拟数据",
                "date": "2026-02-28"
            },
            {
                "title": "海康威视发布新一代AI摄像机",
                "url": "https://example.com/hikvision-ai",
                "snippet": "支持4K超高清、人脸识别、行为分析等AI功能...",
                "source": "模拟数据",
                "date": "2026-02-28"
            }
        ]
        
        return [SearchResult(**data) for data in mock_data]


# 全局实例
web_searcher = WebSearcher()


if __name__ == "__main__":
    # 测试搜索
    searcher = WebSearcher()
    
    print("=" * 50)
    print("🔍 测试全网搜索")
    print("=" * 50)
    
    results = searcher.search_all()
    
    print("\n📄 搜索结果:")
    for i, result in enumerate(results[:5], 1):
        print(f"\n{i}. {result.title}")
        print(f"   {result.snippet[:100]}...")
        print(f"   🔗 {result.url}")
