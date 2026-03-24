"""
文章同步器
==========

将审核通过的文章同步到docs/目录结构
"""

import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import sqlite3
import sys
sys.path.insert(0, '.')
from crawler.article_manager import TechArticleManager


class ArticleSynchronizer:
    """文章同步器"""
    
    def __init__(self, 
                 db_path: str = "tech_documents/articles.db",
                 docs_root: str = "docs"):
        self.db_path = db_path
        self.docs_root = Path(docs_root)
        self.manager = TechArticleManager(db_path)
        
        # 确保目录存在
        self._ensure_directories()
    
    def _ensure_directories(self):
        """确保必要的目录存在"""
        # 智慧类领域
        domains = [
            "智慧城市", "智慧交通", "智慧医疗", "智慧教育",
            "智慧园区", "智慧社区", "智慧应急", "智慧环保",
            "AI应用", "大数据", "云计算", "物联网", "数字孪生"
        ]
        
        for domain in domains:
            (self.docs_root / "智慧类领域" / domain).mkdir(parents=True, exist_ok=True)
        
        # 智能化子系统
        subsystems = [
            "安防系统", "机房工程", "综合布线", "楼宇自控",
            "智能交通", "能源管理", "数据中心", "网络通信"
        ]
        
        for subsystem in subsystems:
            (self.docs_root / "智能化子系统" / subsystem).mkdir(parents=True, exist_ok=True)
        
        # 新技术
        (self.docs_root / "新兴技术").mkdir(parents=True, exist_ok=True)
        
        # 行业报告
        (self.docs_root / "行业报告").mkdir(parents=True, exist_ok=True)
    
    def _determine_category_path(self, article: Dict) -> Path:
        """根据文章内容确定存储路径"""
        title = article.get('title', '').lower()
        summary = article.get('summary', '').lower()
        tags = [tag.lower() for tag in article.get('tags', [])]
        source = article.get('source', '').lower()
        
        text = f"{title} {summary} {' '.join(tags)}"
        
        # 智慧类领域映射
        domain_mapping = {
            "智慧城市": ["智慧城市", "城市大脑", "一网统管", "数字政府"],
            "智慧交通": ["交通", "停车", "信号", "自动驾驶", "车联网"],
            "智慧医疗": ["医疗", "医院", "健康", "诊断"],
            "智慧教育": ["教育", "学校", "教学"],
            "智慧园区": ["园区", "产业园"],
            "智慧社区": ["社区", "小区"],
            "智慧应急": ["应急", "消防", "救灾"],
            "智慧环保": ["环保", "环境", "监测"],
            "AI应用": ["ai", "人工智能", "机器学习", "深度学习", "gpt", "llm"],
            "大数据": ["大数据", "数据分析", "数据仓库", "etl"],
            "云计算": ["云", "kubernetes", "docker", "微服务", "devops"],
            "物联网": ["iot", "物联网", "传感器", "边缘计算"],
            "数字孪生": ["数字孪生", "3d", "仿真", "建模"]
        }
        
        # 匹配领域
        for domain, keywords in domain_mapping.items():
            if any(kw in text for kw in keywords):
                return self.docs_root / "智慧类领域" / domain
        
        # 根据来源分类
        if any(s in source for s in ["arxiv", "ieee", "acm"]):
            return self.docs_root / "新兴技术"
        
        if any(s in source for s in ["infoq", "csdn", "dev.to", "github"]):
            return self.docs_root / "新兴技术"
        
        # 默认分类
        content_type = article.get('content_type', '')
        if content_type == 'paper':
            return self.docs_root / "新兴技术"
        elif content_type == 'project':
            return self.docs_root / "新兴技术"
        else:
            return self.docs_root / "行业报告"
    
    def _generate_markdown(self, article: Dict) -> str:
        """生成Markdown文件内容"""
        title = article.get('title', '无标题')
        url = article.get('url', '')
        source = article.get('source', '')
        summary = article.get('summary', '')
        tags = article.get('tags', [])
        published = article.get('published', '')
        credibility = article.get('credibility_score', 0)
        collected_at = article.get('collected_at', '')[:10]
        
        md_content = f"""# {title}

## 📌 基本信息

- **来源**: {source}
- **可信度**: {credibility}/10
- **链接**: [{url}]({url})
- **收集时间**: {collected_at}
"""
        
        if published:
            md_content += f"- **发布时间**: {published[:10]}\n"
        
        if tags:
            md_content += f"\n## 🏷️ 标签\n\n"
            md_content += " | ".join([f"`{tag}`" for tag in tags[:10]])
            md_content += "\n"
        
        if summary:
            md_content += f"\n## 📝 摘要\n\n{summary}\n"
        
        md_content += f"""
## 📚 相关资料

- 原文链接: [{url}]({url})

---
*收集时间: {collected_at}*
*可信度评分: {credibility}/10*
"""
        
        return md_content
    
    def sync_approved_articles(self, limit: int = 100) -> Dict[str, int]:
        """
        同步审核通过的文章到docs目录
        
        Returns:
            统计信息
        """
        print("\n" + "=" * 60)
        print("📂 同步审核通过的文章到docs目录")
        print("=" * 60)
        
        # 获取审核通过的文章
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM articles 
            WHERE status = 'approved'
            ORDER BY credibility_score DESC, reviewed_at DESC
            LIMIT ?
        ''', (limit,))
        
        columns = [description[0] for description in cursor.description]
        articles = []
        
        for row in cursor.fetchall():
            article = dict(zip(columns, row))
            article['tags'] = json.loads(article['tags']) if article['tags'] else []
            articles.append(article)
        
        conn.close()
        
        stats = {
            "total": len(articles),
            "synced": 0,
            "skipped": 0,
            "by_category": {}
        }
        
        for article in articles:
            try:
                # 确定分类路径
                category_path = self._determine_category_path(article)
                
                # 生成文件名（安全的文件名）
                safe_title = "".join(c for c in article['title'][:50] if c.isalnum() or c in (' ', '-', '_'))
                filename = f"{safe_title}.md"
                
                # 完整文件路径
                file_path = category_path / filename
                
                # 检查是否已存在
                if file_path.exists():
                    stats["skipped"] += 1
                    continue
                
                # 生成Markdown内容
                md_content = self._generate_markdown(article)
                
                # 写入文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(md_content)
                
                stats["synced"] += 1
                
                # 统计分类
                category_name = category_path.name
                stats["by_category"][category_name] = stats["by_category"].get(category_name, 0) + 1
                
                print(f"✓ {article['title'][:50]}")
                print(f"  → {category_path.relative_to(self.docs_root)}")
                
            except Exception as e:
                print(f"✗ 失败: {article['title'][:30]} - {e}")
                stats["skipped"] += 1
        
        # 更新README索引
        self._update_readme_index(stats["by_category"])
        
        return stats
    
    def _update_readme_index(self, by_category: Dict[str, int]):
        """更新README索引"""
        readme_path = self.docs_root / "README.md"
        
        # 读取现有内容
        if readme_path.exists():
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            content = "# 智慧城市知识库\n\n"
        
        # 添加技术资料索引
        index_content = "\n\n## 📚 技术资料索引\n\n"
        index_content += f"更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        
        index_content += "### 按分类统计\n\n"
        for category, count in sorted(by_category.items(), key=lambda x: x[1], reverse=True):
            index_content += f"- **{category}**: {count} 篇\n"
        
        # 检查是否已有索引部分
        if "## 📚 技术资料索引" in content:
            # 替换现有索引
            parts = content.split("## 📚 技术资料索引")
            content = parts[0] + index_content
        else:
            content += index_content
        
        # 写入文件
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def auto_approve_and_sync(self, min_credibility: int = 8):
        """自动通过高可信度文章并同步"""
        print("\n" + "=" * 60)
        print(f"🤖 自动审核并同步（可信度≥{min_credibility}）")
        print("=" * 60)
        
        # 获取待审核的高可信度文章
        pending = self.manager.get_pending_articles(limit=1000, min_credibility=min_credibility)
        
        # 自动通过
        approved_count = 0
        for article in pending:
            if article['credibility_score'] >= min_credibility:
                self.manager.approve_article(article['id'], reviewer="auto-sync")
                approved_count += 1
        
        print(f"\n✓ 自动通过: {approved_count} 篇")
        
        # 同步到docs
        if approved_count > 0:
            stats = self.sync_approved_articles()
            
            print("\n" + "=" * 60)
            print("📊 同步统计")
            print("=" * 60)
            print(f"  总数: {stats['total']}")
            print(f"  已同步: {stats['synced']}")
            print(f"  已跳过: {stats['skipped']}")
            
            print("\n按分类统计:")
            for category, count in sorted(stats['by_category'].items(), key=lambda x: x[1], reverse=True):
                print(f"  {category}: {count} 篇")


def main():
    """测试"""
    syncer = ArticleSynchronizer()
    
    # 自动审核并同步高可信度文章
    syncer.auto_approve_and_sync(min_credibility=8)


if __name__ == "__main__":
    main()
