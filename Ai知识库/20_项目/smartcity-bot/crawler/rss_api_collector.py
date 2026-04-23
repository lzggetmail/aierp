"""
RSS & API 技术资料收集器
========================

使用官方API和RSS订阅获取技术资料
"""

import json
import time
import feedparser
import requests
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class TechArticle:
    """技术文章"""
    title: str
    url: str
    source: str
    category: str
    summary: str
    published: Optional[str]
    tags: List[str]
    content_type: str  # article, paper, project, news
    created_at: str = datetime.now().isoformat()


class RSSTechCollector:
    """RSS技术资料收集器"""
    
    def __init__(self, config_path: str = "config/rss_api_sources.json"):
        self.config_path = config_path
        self.config = self._load_config()
        self.storage_dir = Path("tech_documents/rss")
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def _load_config(self) -> Dict:
        """加载配置"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载配置失败: {e}")
            return {"rss_feeds": [], "api_sources": []}
    
    def collect_rss_feeds(self) -> List[TechArticle]:
        """收集RSS订阅源"""
        articles = []
        
        print("\n📡 收集RSS订阅...")
        print("=" * 60)
        
        for feed_config in self.config.get("rss_feeds", []):
            if not feed_config.get("enabled", False):
                continue
            
            name = feed_config["name"]
            url = feed_config["url"]
            category = feed_config.get("category", "技术资讯")
            
            print(f"\n📌 {name}")
            
            try:
                # 解析RSS
                feed = feedparser.parse(url)
                
                if feed.bozo:  # RSS解析错误
                    print(f"  ⚠️  RSS解析警告: {feed.bozo_exception}")
                
                count = 0
                for entry in feed.entries[:20]:  # 最多20条
                    title = entry.get("title", "")
                    link = entry.get("link", "")
                    summary = entry.get("summary", entry.get("description", ""))
                    published = entry.get("published", entry.get("updated", ""))
                    
                    if title and link:
                        article = TechArticle(
                            title=title,
                            url=link,
                            source=name,
                            category=category,
                            summary=summary[:500],
                            published=published,
                            tags=feed_config.get("keywords", []),
                            content_type="article"
                        )
                        articles.append(article)
                        count += 1
                
                print(f"  ✓ 收集 {count} 篇文章")
                time.sleep(1)  # 礼貌爬取
                
            except Exception as e:
                print(f"  ✗ 失败: {e}")
        
        return articles
    
    def collect_arxiv_papers(self) -> List[TechArticle]:
        """收集arXiv论文"""
        articles = []
        
        print("\n📚 收集arXiv论文...")
        print("=" * 60)
        
        for source_config in self.config.get("api_sources", []):
            if source_config.get("type") != "arxiv":
                continue
            
            if not source_config.get("enabled", False):
                continue
            
            name = source_config["name"]
            query = source_config["query"]
            max_results = source_config.get("max_results", 20)
            keywords = source_config.get("keywords", [])
            
            print(f"\n📌 {name}")
            
            try:
                # arXiv API
                url = f"http://export.arxiv.org/api/query?search_query={query}&max_results={max_results}"
                
                response = self.session.get(url, timeout=30)
                
                if response.status_code == 200:
                    feed = feedparser.parse(response.text)
                    
                    count = 0
                    for entry in feed.entries:
                        title = entry.get("title", "").strip()
                        link = entry.get("link", "")
                        summary = entry.get("summary", "").strip()
                        published = entry.get("published", "")
                        
                        # 提取作者
                        authors = [author.name for author in entry.get("authors", [])]
                        
                        # 检查关键词匹配
                        text = f"{title} {summary}".lower()
                        if keywords and not any(kw.lower() in text for kw in keywords):
                            continue
                        
                        if title and link:
                            article = TechArticle(
                                title=title,
                                url=link,
                                source="arXiv",
                                category="学术论文",
                                summary=summary[:500],
                                published=published,
                                tags=keywords[:5],
                                content_type="paper"
                            )
                            articles.append(article)
                            count += 1
                    
                    print(f"  ✓ 收集 {count} 篇论文")
                
                time.sleep(3)  # arXiv要求3秒间隔
                
            except Exception as e:
                print(f"  ✗ 失败: {e}")
        
        return articles
    
    def collect_github_projects(self) -> List[TechArticle]:
        """收集GitHub热门项目"""
        articles = []
        
        print("\n💻 收集GitHub热门项目...")
        print("=" * 60)
        
        for source_config in self.config.get("api_sources", []):
            if source_config.get("type") != "github":
                continue
            
            if not source_config.get("enabled", False):
                continue
            
            name = source_config["name"]
            language = source_config.get("language")
            topic = source_config.get("topic")
            since = source_config.get("since", "weekly")
            
            print(f"\n📌 {name}")
            
            try:
                # 使用GitHub Trending API（非官方但可用）
                if topic:
                    url = f"https://api.github.com/search/repositories?q=topic:{topic}&sort=stars&order=desc&per_page=20"
                elif language:
                    url = f"https://api.github.com/search/repositories?q=language:{language}&sort=stars&order=desc&per_page=20"
                else:
                    url = "https://api.github.com/search/repositories?q=stars:>1000&sort=stars&order=desc&per_page=20"
                
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    count = 0
                    for repo in data.get("items", []):
                        title = repo.get("full_name", "")
                        description = repo.get("description", "") or "无描述"
                        html_url = repo.get("html_url", "")
                        stars = repo.get("stargazers_count", 0)
                        language_name = repo.get("language", "")
                        
                        if title and html_url:
                            article = TechArticle(
                                title=f"{title} ⭐ {stars:,}",
                                url=html_url,
                                source="GitHub",
                                category="开源项目",
                                summary=description[:200],
                                published=None,
                                tags=[language_name, "GitHub"] if language_name else ["GitHub"],
                                content_type="project"
                            )
                            articles.append(article)
                            count += 1
                    
                    print(f"  ✓ 收集 {count} 个项目")
                
                time.sleep(2)  # GitHub API限制
                
            except Exception as e:
                print(f"  ✗ 失败: {e}")
        
        return articles
    
    def collect_devto_articles(self) -> List[TechArticle]:
        """收集Dev.to文章"""
        articles = []
        
        print("\n📝 收集Dev.to文章...")
        print("=" * 60)
        
        for source_config in self.config.get("api_sources", []):
            if source_config.get("type") != "devto":
                continue
            
            if not source_config.get("enabled", False):
                continue
            
            name = source_config["name"]
            tag = source_config.get("tag")
            per_page = source_config.get("per_page", 30)
            
            print(f"\n📌 {name}")
            
            try:
                # Dev.to API
                url = f"https://dev.to/api/articles?tag={tag}&per_page={per_page}"
                
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    count = 0
                    for article_data in data:
                        title = article_data.get("title", "")
                        url = article_data.get("url", "")
                        description = article_data.get("description", "")
                        published = article_data.get("published_at", "")
                        tags = article_data.get("tag_list", [])
                        
                        if title and url:
                            article = TechArticle(
                                title=title,
                                url=url,
                                source="Dev.to",
                                category="技术博客",
                                summary=description,
                                published=published,
                                tags=tags[:5],
                                content_type="article"
                            )
                            articles.append(article)
                            count += 1
                    
                    print(f"  ✓ 收集 {count} 篇文章")
                
                time.sleep(1)
                
            except Exception as e:
                print(f"  ✗ 失败: {e}")
        
        return articles
    
    def collect_all(self) -> List[TechArticle]:
        """收集所有数据源"""
        all_articles = []
        
        print("\n" + "=" * 60)
        print("🚀 开始收集技术资料...")
        print("=" * 60)
        
        # RSS订阅
        rss_articles = self.collect_rss_feeds()
        all_articles.extend(rss_articles)
        
        # arXiv论文
        arxiv_articles = self.collect_arxiv_papers()
        all_articles.extend(arxiv_articles)
        
        # GitHub项目
        github_articles = self.collect_github_projects()
        all_articles.extend(github_articles)
        
        # Dev.to文章
        devto_articles = self.collect_devto_articles()
        all_articles.extend(devto_articles)
        
        print("\n" + "=" * 60)
        print(f"✅ 收集完成！总计: {len(all_articles)} 篇")
        print("=" * 60)
        
        # 保存结果
        self._save_articles(all_articles)
        
        # 显示统计
        self._show_statistics(all_articles)
        
        return all_articles
    
    def _save_articles(self, articles: List[TechArticle]):
        """保存文章列表"""
        output = []
        
        for article in articles:
            output.append({
                "title": article.title,
                "url": article.url,
                "source": article.source,
                "category": article.category,
                "summary": article.summary,
                "published": article.published,
                "tags": article.tags,
                "content_type": article.content_type,
                "created_at": article.created_at
            })
        
        # 保存JSON
        output_file = self.storage_dir / f"articles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 已保存到: {output_file}")
    
    def _show_statistics(self, articles: List[TechArticle]):
        """显示统计信息"""
        print("\n📊 统计信息:")
        print(f"  总计: {len(articles)} 篇")
        
        # 按来源统计
        sources = {}
        for article in articles:
            sources[article.source] = sources.get(article.source, 0) + 1
        
        print("\n按来源统计:")
        for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
            print(f"  {source}: {count} 篇")
        
        # 按类型统计
        types = {}
        for article in articles:
            types[article.content_type] = types.get(article.content_type, 0) + 1
        
        print("\n按类型统计:")
        for content_type, count in sorted(types.items(), key=lambda x: x[1], reverse=True):
            print(f"  {content_type}: {count} 篇")


def main():
    """主函数"""
    collector = RSSTechCollector()
    articles = collector.collect_all()
    
    # 显示前10篇
    print("\n📰 最新10篇:")
    print("-" * 60)
    for i, article in enumerate(articles[:10], 1):
        print(f"\n{i}. {article.title}")
        print(f"   来源: {article.source} | 类型: {article.content_type}")
        print(f"   链接: {article.url}")


if __name__ == "__main__":
    main()
