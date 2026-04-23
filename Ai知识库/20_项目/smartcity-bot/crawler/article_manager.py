"""
技术资料审核与管理系统
=====================

包含：
1. 去重机制（防止重复收集）
2. 审核机制（人工删减）
3. 来源可信度（防虚假资料）
4. 历史记录（追溯管理）
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Set
from dataclasses import dataclass, asdict
import sqlite3


@dataclass
class ArticleRecord:
    """文章记录"""
    id: str  # 唯一ID（URL的hash）
    title: str
    url: str
    source: str
    source_type: str  # official, community, blog, social
    credibility_score: int  # 可信度评分 1-10
    category: str
    content_type: str
    summary: str
    published: Optional[str]
    tags: List[str]
    
    # 状态管理
    status: str  # pending, approved, rejected, archived
    reviewed_at: Optional[str]
    reviewed_by: Optional[str]
    reject_reason: Optional[str]
    
    # 时间戳
    collected_at: str
    updated_at: str
    
    # 元数据
    duplicate_count: int = 0  # 重复次数
    last_seen_at: Optional[str] = None


class SourceCredibility:
    """来源可信度管理"""
    
    # 官方来源（可信度最高）
    OFFICIAL_SOURCES = {
        # 政府机构
        "gov.cn": 10,
        "ndrc.gov.cn": 10,
        "miit.gov.cn": 10,
        "mohurd.gov.cn": 10,
        
        # 知名厂商
        "huawei.com": 9,
        "aliyun.com": 9,
        "cloud.tencent.com": 9,
        "aws.amazon.com": 9,
        "azure.microsoft.com": 9,
        
        # 学术机构
        "arxiv.org": 9,
        "ieee.org": 9,
        "acm.org": 9,
        
        # 知名咨询
        "deloitte.com": 8,
        "mckinsey.com": 8,
        "accenture.com": 8,
        "pwc.com": 8,
        "ibm.com": 8,
    }
    
    # 社区来源（可信度中等）
    COMMUNITY_SOURCES = {
        "infoq.cn": 7,
        "csdn.net": 6,
        "juejin.cn": 6,
        "segmentfault.com": 6,
        "oschina.net": 7,
        "github.com": 8,
        "dev.to": 7,
        "medium.com": 6,
    }
    
    # 科技媒体（可信度中等）
    MEDIA_SOURCES = {
        "36kr.com": 6,
        "geekpark.net": 6,
        "ifanr.com": 5,
        "ithome.com": 5,
    }
    
    @classmethod
    def get_credibility(cls, url: str) -> int:
        """根据URL判断可信度"""
        url_lower = url.lower()
        
        # 检查官方来源
        for domain, score in cls.OFFICIAL_SOURCES.items():
            if domain in url_lower:
                return score
        
        # 检查社区来源
        for domain, score in cls.COMMUNITY_SOURCES.items():
            if domain in url_lower:
                return score
        
        # 检查媒体来源
        for domain, score in cls.MEDIA_SOURCES.items():
            if domain in url_lower:
                return score
        
        # 未知来源
        return 3
    
    @classmethod
    def get_source_type(cls, url: str) -> str:
        """判断来源类型"""
        url_lower = url.lower()
        
        for domain in cls.OFFICIAL_SOURCES:
            if domain in url_lower:
                return "official"
        
        for domain in cls.COMMUNITY_SOURCES:
            if domain in url_lower:
                return "community"
        
        for domain in cls.MEDIA_SOURCES:
            if domain in url_lower:
                return "media"
        
        return "unknown"


class TechArticleManager:
    """技术文章管理器"""
    
    def __init__(self, db_path: str = "tech_documents/articles.db"):
        self.db_path = db_path
        self.storage_dir = Path(db_path).parent
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化数据库
        self._init_database()
        
        # 加载已审核的ID集合
        self.seen_ids: Set[str] = self._load_seen_ids()
    
    def _init_database(self):
        """初始化SQLite数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建文章表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                source TEXT,
                source_type TEXT,
                credibility_score INTEGER,
                category TEXT,
                content_type TEXT,
                summary TEXT,
                published TEXT,
                tags TEXT,
                status TEXT DEFAULT 'pending',
                reviewed_at TEXT,
                reviewed_by TEXT,
                reject_reason TEXT,
                collected_at TEXT,
                updated_at TEXT,
                duplicate_count INTEGER DEFAULT 0,
                last_seen_at TEXT
            )
        ''')
        
        # 创建索引
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_status ON articles(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_source ON articles(source)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_credibility ON articles(credibility_score)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_collected_at ON articles(collected_at)')
        
        conn.commit()
        conn.close()
    
    def _load_seen_ids(self) -> Set[str]:
        """加载已存在的文章ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM articles')
        ids = {row[0] for row in cursor.fetchall()}
        
        conn.close()
        return ids
    
    def _generate_id(self, url: str) -> str:
        """生成文章唯一ID（基于URL的hash）"""
        return hashlib.md5(url.encode()).hexdigest()
    
    def add_article(self, article_data: Dict) -> Optional[str]:
        """
        添加文章（自动去重）
        
        Returns:
            文章ID（如果是新文章），None（如果是重复文章）
        """
        url = article_data.get("url", "")
        if not url:
            return None
        
        # 生成ID
        article_id = self._generate_id(url)
        
        # 检查是否已存在
        if article_id in self.seen_ids:
            # 更新重复计数
            self._update_duplicate_count(article_id)
            return None
        
        # 获取可信度
        credibility = SourceCredibility.get_credibility(url)
        source_type = SourceCredibility.get_source_type(url)
        
        # 创建记录
        record = ArticleRecord(
            id=article_id,
            title=article_data.get("title", ""),
            url=url,
            source=article_data.get("source", ""),
            source_type=source_type,
            credibility_score=credibility,
            category=article_data.get("category", ""),
            content_type=article_data.get("content_type", ""),
            summary=article_data.get("summary", ""),
            published=article_data.get("published"),
            tags=article_data.get("tags", []),
            status="pending",
            reviewed_at=None,
            reviewed_by=None,
            reject_reason=None,
            collected_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            duplicate_count=0,
            last_seen_at=None
        )
        
        # 保存到数据库
        self._save_article(record)
        
        # 添加到已见集合
        self.seen_ids.add(article_id)
        
        return article_id
    
    def _save_article(self, record: ArticleRecord):
        """保存文章到数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO articles 
            (id, title, url, source, source_type, credibility_score, category, 
             content_type, summary, published, tags, status, reviewed_at, 
             reviewed_by, reject_reason, collected_at, updated_at, 
             duplicate_count, last_seen_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            record.id,
            record.title,
            record.url,
            record.source,
            record.source_type,
            record.credibility_score,
            record.category,
            record.content_type,
            record.summary,
            record.published,
            json.dumps(record.tags, ensure_ascii=False),
            record.status,
            record.reviewed_at,
            record.reviewed_by,
            record.reject_reason,
            record.collected_at,
            record.updated_at,
            record.duplicate_count,
            record.last_seen_at
        ))
        
        conn.commit()
        conn.close()
    
    def _update_duplicate_count(self, article_id: str):
        """更新重复计数"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE articles 
            SET duplicate_count = duplicate_count + 1,
                last_seen_at = ?,
                updated_at = ?
            WHERE id = ?
        ''', (datetime.now().isoformat(), datetime.now().isoformat(), article_id))
        
        conn.commit()
        conn.close()
    
    def batch_add_articles(self, articles: List[Dict]) -> Dict[str, int]:
        """
        批量添加文章
        
        Returns:
            统计信息: {"new": 新增数, "duplicate": 重复数}
        """
        stats = {"new": 0, "duplicate": 0}
        
        for article in articles:
            article_id = self.add_article(article)
            if article_id:
                stats["new"] += 1
            else:
                stats["duplicate"] += 1
        
        return stats
    
    def approve_article(self, article_id: str, reviewer: str = "user"):
        """审核通过"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE articles 
            SET status = 'approved',
                reviewed_at = ?,
                reviewed_by = ?,
                updated_at = ?
            WHERE id = ?
        ''', (datetime.now().isoformat(), reviewer, datetime.now().isoformat(), article_id))
        
        conn.commit()
        conn.close()
    
    def reject_article(self, article_id: str, reason: str, reviewer: str = "user"):
        """审核拒绝"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE articles 
            SET status = 'rejected',
                reviewed_at = ?,
                reviewed_by = ?,
                reject_reason = ?,
                updated_at = ?
            WHERE id = ?
        ''', (datetime.now().isoformat(), reviewer, reason, datetime.now().isoformat(), article_id))
        
        conn.commit()
        conn.close()
    
    def get_pending_articles(self, limit: int = 50, min_credibility: int = 5) -> List[Dict]:
        """获取待审核文章（按可信度排序）"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM articles 
            WHERE status = 'pending' AND credibility_score >= ?
            ORDER BY credibility_score DESC, collected_at DESC
            LIMIT ?
        ''', (min_credibility, limit))
        
        columns = [description[0] for description in cursor.description]
        articles = []
        
        for row in cursor.fetchall():
            article = dict(zip(columns, row))
            article['tags'] = json.loads(article['tags']) if article['tags'] else []
            articles.append(article)
        
        conn.close()
        return articles
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # 总体统计
        cursor.execute('SELECT COUNT(*) FROM articles')
        stats['total'] = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM articles WHERE status = "pending"')
        stats['pending'] = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM articles WHERE status = "approved"')
        stats['approved'] = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM articles WHERE status = "rejected"')
        stats['rejected'] = cursor.fetchone()[0]
        
        # 按来源统计
        cursor.execute('''
            SELECT source, COUNT(*) as count 
            FROM articles 
            WHERE status = 'approved'
            GROUP BY source 
            ORDER BY count DESC 
            LIMIT 10
        ''')
        stats['by_source'] = dict(cursor.fetchall())
        
        # 按可信度统计
        cursor.execute('''
            SELECT credibility_score, COUNT(*) as count 
            FROM articles 
            GROUP BY credibility_score 
            ORDER BY credibility_score DESC
        ''')
        stats['by_credibility'] = dict(cursor.fetchall())
        
        # 今日新增
        today = datetime.now().date().isoformat()
        cursor.execute('''
            SELECT COUNT(*) FROM articles 
            WHERE DATE(collected_at) = ?
        ''', (today,))
        stats['today_new'] = cursor.fetchone()[0]
        
        conn.close()
        return stats
    
    def export_approved(self, output_file: str = None) -> str:
        """导出已审核通过的文章"""
        if not output_file:
            output_file = self.storage_dir / f"approved_{datetime.now().strftime('%Y%m%d')}.json"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM articles 
            WHERE status = 'approved'
            ORDER BY credibility_score DESC, reviewed_at DESC
        ''')
        
        columns = [description[0] for description in cursor.description]
        articles = []
        
        for row in cursor.fetchall():
            article = dict(zip(columns, row))
            article['tags'] = json.loads(article['tags']) if article['tags'] else []
            articles.append(article)
        
        conn.close()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        
        return str(output_file)


def main():
    """测试"""
    manager = TechArticleManager()
    
    print("=" * 60)
    print("技术文章管理系统")
    print("=" * 60)
    
    # 获取统计
    stats = manager.get_statistics()
    
    print("\n📊 统计信息:")
    print(f"  总文章数: {stats['total']}")
    print(f"  待审核: {stats['pending']}")
    print(f"  已通过: {stats['approved']}")
    print(f"  已拒绝: {stats['rejected']}")
    print(f"  今日新增: {stats['today_new']}")
    
    print("\n按来源统计（已通过）:")
    for source, count in stats['by_source'].items():
        print(f"  {source}: {count} 篇")
    
    print("\n按可信度统计:")
    for score, count in sorted(stats['by_credibility'].items(), reverse=True):
        print(f"  {score}分: {count} 篇")
    
    # 获取待审核文章
    pending = manager.get_pending_articles(limit=10, min_credibility=6)
    
    if pending:
        print("\n" + "=" * 60)
        print(f"📰 待审核文章（前10篇，可信度≥6）")
        print("=" * 60)
        
        for i, article in enumerate(pending, 1):
            print(f"\n{i}. {article['title'][:60]}")
            print(f"   来源: {article['source']} | 可信度: {article['credibility_score']}/10")
            print(f"   类型: {article['source_type']} | 分类: {article['category']}")
            print(f"   ID: {article['id']}")
    else:
        print("\n✅ 没有待审核的文章")


if __name__ == "__main__":
    main()
