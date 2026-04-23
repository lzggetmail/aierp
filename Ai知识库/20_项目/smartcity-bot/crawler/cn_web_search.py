"""
国内可用搜索模块
===============

使用国内可用的数据源：
- RSS订阅源
- 新闻API
- 百度搜索（备选）
"""

import os
import requests
import feedparser
from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime, timedelta
import time


@dataclass
class SearchResult:
    """搜索结果"""
    title: str
    url: str
    snippet: str
    source: str
    date: str
    category: str = ""


class CNWebSearcher:
    """国内可用搜索器"""
    
    def __init__(self):
        # 关键词列表 - 覆盖所有智慧类建设领域
        self.keywords = [
            # 智慧城市整体
            "智慧城市", "智能城市", "城市大脑", "数字城市",
            "智慧城区", "智慧小镇", "新基建",
            
            # 智慧园区
            "智慧园区", "智慧社区", "智慧楼宇", "智慧建筑",
            "园区管理", "社区服务", "智能建筑",
            
            # 智慧医疗
            "智慧医疗", "智慧医院", "远程医疗", "医疗信息化",
            "健康城市", "智慧康养", "医疗AI",
            
            # 智慧交通
            "智慧交通", "智能交通", "智慧停车", "智慧物流",
            "交通大脑", "智能网联", "车路协同",
            
            # 智慧教育
            "智慧教育", "智慧校园", "智慧课堂", "教育信息化",
            
            # 智慧政务
            "智慧政务", "数字政府", "一网通办", "智慧办公",
            
            # 智慧环保
            "智慧环保", "环境监测", "智慧水务", "智慧环卫",
            
            # 智慧能源
            "智慧能源", "能耗监测", "智能电网", "智慧电力",
            
            # 智慧安防
            "智慧安防", "视频监控", "人脸识别", "智能门禁",
            "安防系统", "安全城市",
            
            # 基础设施
            "综合布线", "机房工程", "数据中心", "弱电系统",
            "物联网", "IoT平台", "5G应用",
            
            # 技术应用
            "数字孪生", "BIM", "GIS系统", "大数据平台",
            "人工智能应用", "云计算",
            
            # 项目相关
            "解决方案", "技术方案", "系统设计", "项目案例",
            "工程实施", "运维管理", "标准规范",
            
            # 政策市场
            "数字化转型", "行业报告", "白皮书"
        ]
        
        # News API Key（可选）
        self.news_api_key = os.getenv("NEWS_API_KEY", "")
        
        # RSS源配置 - 聚焦智慧城市建设
        self.rss_sources = [
            # 行业媒体
            {
                "name": "中国智慧城市网",
                "url": "http://www.smartcitychina.cn/rss.xml",
                "category": "行业资讯"
            },
            {
                "name": "智慧城市头条",
                "url": "https://www.smartcity.top/rss",
                "category": "行业资讯"
            },
            
            # 技术媒体
            {
                "name": "CSDN-物联网",
                "url": "https://blog.csdn.net/nav/iot/rss",
                "category": "技术方案"
            },
            {
                "name": "CSDN-人工智能",
                "url": "https://blog.csdn.net/nav/ai/rss",
                "category": "新兴技术"
            },
            
            # 政府和政策
            {
                "name": "中国政府网-政策",
                "url": "http://www.gov.cn/rss/govrss.xml",
                "category": "政策标准"
            },
            
            # 科技媒体（筛选智慧城市相关）
            {
                "name": "36氪-智慧城市",
                "url": "https://36kr.com/feed",
                "category": "科技资讯"
            },
            {
                "name": "InfoQ-架构",
                "url": "https://www.infoq.cn/feed",
                "category": "技术方案"
            }
        ]
        
        # 自定义数据源（用户可添加）
        self.custom_sources = self._load_custom_sources()
    
    def _load_custom_sources(self) -> List[Dict]:
        """加载自定义数据源"""
        config_file = os.path.join(os.path.dirname(__file__), "..", "config", "custom_sources.json")
        
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def add_custom_source(self, name: str, url: str, source_type: str = "rss", category: str = "其他"):
        """
        添加自定义数据源
        
        Args:
            name: 数据源名称
            url: 数据源URL
            source_type: 类型（rss/api/web）
            category: 分类
        """
        source = {
            "name": name,
            "url": url,
            "type": source_type,
            "category": category
        }
        
        self.custom_sources.append(source)
        
        # 保存
        config_file = os.path.join(os.path.dirname(__file__), "..", "config", "custom_sources.json")
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(self.custom_sources, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 已添加数据源: {name}")
    
    def search_custom_sources(self) -> List[SearchResult]:
        """搜索自定义数据源"""
        results = []
        
        for source in self.custom_sources:
            if source.get("type") == "rss":
                try:
                    feed = feedparser.parse(source['url'])
                    
                    for entry in feed.entries[:10]:
                        title = entry.get('title', '')
                        summary = entry.get('summary', '')
                        link = entry.get('link', '')
                        
                        results.append(SearchResult(
                            title=title,
                            url=link,
                            snippet=summary[:200],
                            source=source['name'],
                            date=datetime.now().strftime('%Y-%m-%d'),
                            category=source.get('category', '其他')
                        ))
                except Exception as e:
                    print(f"⚠️ 自定义源 {source['name']} 获取失败: {e}")
        
        return results
        
        # 新闻API配置（如果有）
        self.news_api_key = os.getenv("NEWS_API_KEY", "")
        
        # 搜索关键词（用于过滤）
        self.keywords = [
            "智慧城市", "智能城市", "城市大脑",
            "安防", "摄像头", "监控",
            "机房", "服务器", "数据中心",
            "物联网", "IoT", "传感器",
            "人工智能", "AI", "人脸识别",
            "智能交通", "停车", "信号灯",
            "数字孪生", "3D建模",
            "新能源", "充电桩",
            "白皮书", "研究报告"
        ]
    
    def search_rss(self) -> List[SearchResult]:
        """
        从RSS源获取内容
        
        Returns:
            RSS内容列表
        """
        all_results = []
        
        print(f"\n📡 开始RSS采集...")
        print(f"   RSS源数量: {len(self.rss_sources)}")
        
        for source in self.rss_sources:
            try:
                print(f"   获取: {source['name']}")
                
                # 获取RSS（添加超时）
                import signal
                
                def timeout_handler(signum, frame):
                    raise TimeoutError("RSS获取超时")
                
                # 设置10秒超时
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(10)
                
                try:
                    feed = feedparser.parse(source['url'])
                    signal.alarm(0)  # 取消超时
                except TimeoutError:
                    print(f"      ⚠️ 超时，跳过此源")
                    signal.alarm(0)
                    continue
                
                if feed.bozo:  # 解析错误
                    print(f"      ⚠️ 解析失败: {feed.bozo_exception}")
                    continue
                
                # 处理每篇文章
                for entry in feed.entries[:10]:  # 每个源最多10篇
                    title = entry.get('title', '')
                    summary = entry.get('summary', entry.get('description', ''))
                    link = entry.get('link', '')
                    
                    # 发布时间
                    pub_date = entry.get('published', entry.get('updated', ''))
                    if pub_date:
                        try:
                            dt = datetime(*entry.published_parsed[:6])
                            pub_date = dt.strftime('%Y-%m-%d')
                        except:
                            pub_date = datetime.now().strftime('%Y-%m-%d')
                    else:
                        pub_date = datetime.now().strftime('%Y-%m-%d')
                    
                    # 关键词过滤 - 聚焦智慧类建设
                    text = f"{title} {summary}"
                    matched_keywords = [kw for kw in self.keywords if kw in text]
                    
                    # 优先级：
                    # 1. 标题包含"智慧"相关词汇
                    # 2. 内容包含解决方案、技术方案、系统设计
                    # 3. 至少匹配2个关键词
                    
                    smart_keywords = ["智慧城市", "智慧园区", "智慧医疗", "智慧交通", 
                                     "智慧教育", "智慧政务", "智慧环保", "智慧能源",
                                     "智慧社区", "智慧医院", "智慧校园", "智能城市"]
                    solution_keywords = ["解决方案", "技术方案", "系统设计", "项目案例",
                                        "工程实施", "建设方案", "应用案例"]
                    
                    is_smart = any(kw in title or kw in text for kw in smart_keywords)
                    is_solution = any(kw in text for kw in solution_keywords)
                    has_enough_keywords = len(matched_keywords) >= 2
                    
                    if is_smart or (is_solution and has_enough_keywords):
                        all_results.append(SearchResult(
                            title=title,
                            url=link,
                            snippet=summary[:200],
                            source=source['name'],
                            date=pub_date,
                            category=source['category']
                        ))
                
                print(f"      ✅ 获取 {len(feed.entries)} 篇文章")
                
                # 礼貌延迟
                time.sleep(1)
                
            except Exception as e:
                print(f"      ❌ 错误: {e}")
                continue
        
        print(f"\n✅ RSS采集完成，共 {len(all_results)} 条相关内容")
        
        return all_results
    
    def search_news_api(self, query: str = "智慧城市") -> List[SearchResult]:
        """
        使用新闻API搜索（如果有配置）
        
        Args:
            query: 搜索关键词
        
        Returns:
            新闻列表
        """
        if not self.news_api_key:
            return []
        
        # 可以接入天行数据、聚合数据等国内新闻API
        # 这里是示例结构
        try:
            url = "https://api.tianapi.com/it/index"
            
            params = {
                "key": self.news_api_key,
                "word": query,
                "num": 20
            }
            
            response = requests.get(url, params=params, timeout=10)
            result = response.json()
            
            if result.get("code") != 200:
                return []
            
            results = []
            for item in result.get("newslist", []):
                results.append(SearchResult(
                    title=item.get("title", ""),
                    url=item.get("url", ""),
                    snippet=item.get("description", ""),
                    source=item.get("source", ""),
                    date=item.get("ctime", ""),
                    category="科技新闻"
                ))
            
            return results
            
        except Exception as e:
            print(f"❌ 新闻API错误: {e}")
            return []
    
    def search_all(self) -> List[SearchResult]:
        """
        执行所有搜索
        
        Returns:
            所有搜索结果
        """
        all_results = []
        
        print("\n" + "=" * 60)
        print("🔍 开始全网采集（国内源）")
        print("=" * 60)
        
        # 1. RSS采集
        rss_results = self.search_rss()
        all_results.extend(rss_results)
        
        # 2. 新闻API（如果有）
        if self.news_api_key:
            print("\n📰 使用新闻API...")
            news_results = self.search_news_api()
            all_results.extend(news_results)
        
        # 3. 自定义数据源
        if self.custom_sources:
            print(f"\n📡 搜索自定义数据源 ({len(self.custom_sources)}个)...")
            custom_results = self.search_custom_sources()
            all_results.extend(custom_results)
        
        # 去重（按URL）
        seen_urls = set()
        unique_results = []
        for result in all_results:
            if result.url not in seen_urls:
                seen_urls.add(result.url)
                unique_results.append(result)
        
        print(f"\n" + "=" * 60)
        print(f"✅ 采集完成，共 {len(unique_results)} 条内容")
        print("=" * 60)
        
        return unique_results


# 全局实例
cn_web_searcher = CNWebSearcher()


if __name__ == "__main__":
    # 测试
    searcher = CNWebSearcher()
    
    print("\n🧪 测试国内源采集")
    
    results = searcher.search_all()
    
    print(f"\n📄 获取到 {len(results)} 条结果")
    
    if results:
        print("\n前5条：")
        for i, r in enumerate(results[:5], 1):
            print(f"\n{i}. {r.title}")
            print(f"   来源: {r.source}")
            print(f"   分类: {r.category}")
            print(f"   摘要: {r.snippet[:100]}...")
