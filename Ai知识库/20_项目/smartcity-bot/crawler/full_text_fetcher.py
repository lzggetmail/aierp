"""
完整内容抓取器
=============

从RSS摘要链接抓取完整的文章内容
"""

import re
import time
import feedparser
import requests
from bs4 import BeautifulSoup
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class Article:
    """文章数据"""
    title: str
    url: str
    content: str
    source: str
    date: str
    category: str


class FullTextFetcher:
    """完整内容抓取器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.timeout = 20
        
        # RSS源配置
        self.rss_sources = [
            {"name": "CSDN-物联网", "url": "https://blog.csdn.net/nav/iot/rss", "category": "技术方案"},
            {"name": "CSDN-人工智能", "url": "https://blog.csdn.net/nav/ai/rss", "category": "新兴技术"},
            {"name": "InfoQ", "url": "https://www.infoq.cn/feed", "category": "技术方案"},
            {"name": "36氪", "url": "https://36kr.com/feed", "category": "科技资讯"},
        ]
        
        # 关键词过滤
        self.keywords = [
            "智慧城市", "智能城市", "城市大脑", "物联网", "IoT",
            "人工智能", "AI", "数字孪生", "智慧交通", "智慧社区",
            "安防", "监控", "传感器", "5G", "大数据"
        ]
    
    def fetch_page_content(self, url: str) -> Optional[str]:
        """抓取网页完整内容"""
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.encoding = response.apparent_encoding or 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 移除脚本和样式
            for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
                tag.decompose()
            
            # 尝试找到主要内容区域
            content_selectors = [
                'article',
                '.article-content',
                '.post-content',
                '.content',
                '#content',
                'main'
            ]
            
            content_area = None
            for selector in content_selectors:
                if selector.startswith('.'):
                    content_area = soup.find(class_=selector[1:])
                elif selector.startswith('#'):
                    content_area = soup.find(id=selector[1:])
                else:
                    content_area = soup.find(selector)
                
                if content_area:
                    break
            
            if not content_area:
                # 使用body
                content_area = soup.find('body')
            
            if content_area:
                text = content_area.get_text(separator='\n', strip=True)
                # 清理文本
                text = self._clean_text(text)
                return text
            
            return None
            
        except Exception as e:
            print(f"      抓取失败: {e}")
            return None
    
    def _clean_text(self, text: str) -> str:
        """清理文本"""
        # 移除多余空白
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r' {2,}', ' ', text)
        # 移除行首行尾空格
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        return '\n'.join(lines)
    
    def search(self, keywords: List[str] = None, max_results: int = 10) -> List[Article]:
        """
        从RSS源搜索并抓取完整内容
        
        Args:
            keywords: 过滤关键词
            max_results: 最大结果数
        
        Returns:
            文章列表（包含完整内容）
        """
        if keywords is None:
            keywords = self.keywords
        
        all_articles = []
        
        for source in self.rss_sources:
            print(f"\n📡 采集: {source['name']}")
            
            try:
                feed = feedparser.parse(source['url'])
                
                if not feed.entries:
                    print(f"   未获取到内容")
                    continue
                
                print(f"   获取到 {len(feed.entries)} 篇文章")
                
                for entry in feed.entries[:10]:
                    title = entry.get('title', '')
                    link = entry.get('link', '')
                    summary = entry.get('summary', entry.get('description', ''))
                    
                    # 获取发布时间
                    pub_date = ''
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        pub_date = time.strftime('%Y-%m-%d', entry.published_parsed)
                    elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                        pub_date = time.strftime('%Y-%m-%d', entry.updated_parsed)
                    
                    # 关键词过滤
                    text = f"{title} {summary}"
                    matched = [kw for kw in keywords if kw in text]
                    
                    if not matched:
                        continue
                    
                    print(f"   匹配: {title[:40]}...")
                    
                    # 抓取完整内容
                    print(f"      抓取完整内容...")
                    full_content = self.fetch_page_content(link)
                    
                    if full_content and len(full_content) > 200:
                        article = Article(
                            title=title,
                            url=link,
                            content=full_content[:5000],  # 限制长度
                            source=source['name'],
                            date=pub_date,
                            category=source['category']
                        )
                        all_articles.append(article)
                        print(f"      ✅ 内容长度: {len(full_content)} 字符")
                    else:
                        # 使用摘要
                        article = Article(
                            title=title,
                            url=link,
                            content=summary[:1000] if summary else "无内容",
                            source=source['name'],
                            date=pub_date,
                            category=source['category']
                        )
                        all_articles.append(article)
                        print(f"      ⚠️ 使用摘要: {len(summary)} 字符")
                    
                    # 礼貌延迟
                    time.sleep(1)
                    
                    if len(all_articles) >= max_results:
                        break
                        
            except Exception as e:
                print(f"   ❌ 错误: {e}")
                continue
            
            if len(all_articles) >= max_results:
                break
        
        print(f"\n✅ 采集完成，共 {len(all_articles)} 篇文章")
        return all_articles


# 测试
if __name__ == "__main__":
    fetcher = FullTextFetcher()
    articles = fetcher.search(max_results=5)
    
    for i, article in enumerate(articles, 1):
        print(f"\n{'='*50}")
        print(f"文章 {i}: {article.title}")
        print(f"来源: {article.source}")
        print(f"日期: {article.date}")
        print(f"分类: {article.category}")
        print(f"链接: {article.url}")
        print(f"内容长度: {len(article.content)} 字符")
        print(f"内容预览:\n{article.content[:500]}...")
