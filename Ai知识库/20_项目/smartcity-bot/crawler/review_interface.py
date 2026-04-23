"""
技术资料审核界面
================

提供简单的审核流程：
1. 查看待审核文章
2. 通过/拒绝操作
3. 批量操作
4. 统计报告
"""

import json
from datetime import datetime
from pathlib import Path
from crawler.article_manager import TechArticleManager
from crawler.rss_api_collector import RSSTechCollector


class ArticleReviewer:
    """文章审核器"""
    
    def __init__(self):
        self.manager = TechArticleManager()
        self.collector = RSSTechCollector()
    
    def collect_and_review(self):
        """收集并准备审核"""
        print("=" * 60)
        print("📥 第1步：收集新文章")
        print("=" * 60)
        
        # 收集文章
        articles = self.collector.collect_all()
        
        # 添加到管理系统（自动去重）
        print("\n" + "=" * 60)
        print("💾 第2步：添加到管理系统（去重）")
        print("=" * 60)
        
        stats = self.manager.batch_add_articles([
            {
                "title": a.title,
                "url": a.url,
                "source": a.source,
                "category": a.category,
                "content_type": a.content_type,
                "summary": a.summary,
                "published": a.published,
                "tags": a.tags
            }
            for a in articles
        ])
        
        print(f"\n✓ 新增: {stats['new']} 篇")
        print(f"✓ 重复: {stats['duplicate']} 篇")
        
        # 显示待审核文章
        self.show_pending_articles()
    
    def show_pending_articles(self, limit: int = 20, min_credibility: int = 6):
        """显示待审核文章"""
        print("\n" + "=" * 60)
        print(f"📰 第3步：待审核文章（可信度≥{min_credibility}）")
        print("=" * 60)
        
        pending = self.manager.get_pending_articles(limit=limit, min_credibility=min_credibility)
        
        if not pending:
            print("\n✅ 没有待审核的文章")
            return
        
        print(f"\n共 {len(pending)} 篇待审核:\n")
        
        for i, article in enumerate(pending, 1):
            print(f"\n{'─' * 60}")
            print(f"{i}. {article['title'][:80]}")
            print(f"   📍 来源: {article['source']} ({article['source_type']})")
            print(f"   ⭐ 可信度: {article['credibility_score']}/10")
            print(f"   📂 分类: {article['category']} | 类型: {article['content_type']}")
            print(f"   🔗 链接: {article['url'][:70]}")
            print(f"   📝 摘要: {article['summary'][:100]}...")
            print(f"   🏷️  标签: {', '.join(article['tags'][:5])}")
            print(f"   📅 收集时间: {article['collected_at'][:19]}")
            print(f"   🆔 ID: {article['id']}")
    
    def show_statistics(self):
        """显示统计信息"""
        stats = self.manager.get_statistics()
        
        print("\n" + "=" * 60)
        print("📊 审核统计")
        print("=" * 60)
        
        print(f"\n总数统计:")
        print(f"  总文章数: {stats['total']}")
        print(f"  待审核: {stats['pending']}")
        print(f"  已通过: {stats['approved']}")
        print(f"  已拒绝: {stats['rejected']}")
        print(f"  今日新增: {stats['today_new']}")
        
        if stats['by_source']:
            print(f"\n已通过文章来源TOP5:")
            for i, (source, count) in enumerate(list(stats['by_source'].items())[:5], 1):
                print(f"  {i}. {source}: {count} 篇")
        
        if stats['by_credibility']:
            print(f"\n按可信度分布:")
            for score in sorted(stats['by_credibility'].keys(), reverse=True):
                count = stats['by_credibility'][score]
                bar = "█" * (count // 10)
                print(f"  {score}分: {bar} {count}")
    
    def approve_by_credibility(self, min_score: int = 8):
        """自动通过高可信度文章"""
        print(f"\n" + "=" * 60)
        print(f"✅ 自动通过可信度≥{min_score}的文章")
        print("=" * 60)
        
        pending = self.manager.get_pending_articles(limit=1000, min_credibility=min_score)
        
        approved_count = 0
        for article in pending:
            if article['credibility_score'] >= min_score:
                self.manager.approve_article(article['id'], reviewer="auto-credibility")
                approved_count += 1
        
        print(f"\n✓ 已自动通过 {approved_count} 篇文章")
    
    def export_approved(self):
        """导出已通过的文章"""
        output_file = self.manager.export_approved()
        
        print(f"\n" + "=" * 60)
        print(f"📤 导出已审核通过的文章")
        print("=" * 60)
        print(f"\n✓ 已导出到: {output_file}")
        
        return output_file
    
    def interactive_review(self):
        """交互式审核"""
        print("\n" + "=" * 60)
        print("🔍 交互式审核模式")
        print("=" * 60)
        print("\n命令:")
        print("  y - 通过")
        print("  n - 拒绝")
        print("  s - 跳过")
        print("  q - 退出")
        print("  auto - 自动通过高可信度(≥8)")
        print("  stats - 显示统计")
        
        pending = self.manager.get_pending_articles(limit=50, min_credibility=6)
        
        if not pending:
            print("\n✅ 没有待审核的文章")
            return
        
        reviewed = 0
        
        for article in pending:
            print(f"\n{'=' * 60}")
            print(f"待审核: {reviewed + 1}/{len(pending)}")
            print(f"{'=' * 60}")
            print(f"\n标题: {article['title']}")
            print(f"来源: {article['source']} ({article['source_type']}) | 可信度: {article['credibility_score']}/10")
            print(f"链接: {article['url']}")
            print(f"\n摘要: {article['summary'][:200]}...")
            
            while True:
                cmd = input("\n操作 (y/n/s/q/auto/stats): ").strip().lower()
                
                if cmd == 'y':
                    self.manager.approve_article(article['id'])
                    print("✓ 已通过")
                    reviewed += 1
                    break
                elif cmd == 'n':
                    reason = input("拒绝原因: ").strip()
                    self.manager.reject_article(article['id'], reason)
                    print("✗ 已拒绝")
                    reviewed += 1
                    break
                elif cmd == 's':
                    print("→ 跳过")
                    break
                elif cmd == 'q':
                    print("\n退出审核")
                    return
                elif cmd == 'auto':
                    self.approve_by_credibility(8)
                    return
                elif cmd == 'stats':
                    self.show_statistics()
                else:
                    print("无效命令，请重试")
        
        print(f"\n✅ 审核完成，共审核 {reviewed} 篇文章")


def main():
    """主函数"""
    reviewer = ArticleReviewer()
    
    print("\n" + "=" * 60)
    print("🛠️  技术资料审核系统")
    print("=" * 60)
    
    while True:
        print("\n选项:")
        print("  1. 收集新文章并审核")
        print("  2. 查看待审核文章")
        print("  3. 交互式审核")
        print("  4. 自动通过高可信度(≥8)")
        print("  5. 查看统计")
        print("  6. 导出已通过文章")
        print("  0. 退出")
        
        choice = input("\n请选择 (0-6): ").strip()
        
        if choice == '1':
            reviewer.collect_and_review()
        elif choice == '2':
            reviewer.show_pending_articles()
        elif choice == '3':
            reviewer.interactive_review()
        elif choice == '4':
            reviewer.approve_by_credibility(8)
        elif choice == '5':
            reviewer.show_statistics()
        elif choice == '6':
            reviewer.export_approved()
        elif choice == '0':
            print("\n👋 再见！")
            break
        else:
            print("无效选择，请重试")


if __name__ == "__main__":
    main()
