"""
每日任务调度
============

定时执行全网采集任务
"""

import schedule
import time
import threading
from datetime import datetime
from typing import Callable
import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from crawler.cn_web_search import cn_web_searcher
from utils.content_analyzer import ContentAnalyzer
from utils.knowledge_base import knowledge_base
from notifier.daily_report import DailyReporter


class DailyScheduler:
    """每日任务调度器"""
    
    def __init__(self):
        # 使用国内可用搜索器
        self.searcher = cn_web_searcher
        self.analyzer = ContentAnalyzer()
        self.reporter = DailyReporter()
        
        self.is_running = False
        self.last_run_time = None
    
    def daily_task(self):
        """
        每日任务：搜索→分析→报告
        """
        print("\n" + "=" * 60)
        print(f"📅 开始每日任务 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        try:
            # 1. 全网搜索
            print("\n🔍 步骤1：全网搜索")
            results = self.searcher.search_all()
            
            if not results:
                print("⚠️ 未获取到搜索结果")
                return
            
            # 2. 分析内容
            print("\n📊 步骤2：分析内容")
            analyzed_results = []
            
            for i, result in enumerate(results, 1):
                print(f"   分析 {i}/{len(results)}: {result.title[:30]}...")
                
                analysis = self.analyzer.analyze(result.snippet)
                
                if analysis.has_value:
                    # 存储到知识库
                    knowledge_base.add_knowledge(
                        title=result.title,
                        content=result.snippet,
                        category=analysis.category,
                        subsystem=analysis.subsystem or "",
                        tags=analysis.tags,
                        source=result.source,
                        url=result.url
                    )
                    
                    analyzed_results.append({
                        "title": result.title,
                        "url": result.url,
                        "snippet": result.snippet,
                        "category": analysis.category,
                        "tags": analysis.tags,
                        "summary": analysis.summary
                    })
            
            print(f"\n✅ 筛选出 {len(analyzed_results)} 条有价值内容")
            
            # 3. 生成日报
            print("\n📝 步骤3：生成日报")
            self.reporter.generate_and_send(analyzed_results)
            
            # 记录运行时间
            self.last_run_time = datetime.now()
            
            print("\n" + "=" * 60)
            print(f"✅ 每日任务完成 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n❌ 任务执行失败: {e}")
    
    def start(self, run_time: str = "09:00"):
        """
        启动定时任务
        
        Args:
            run_time: 每天运行时间，格式 "HH:MM"
        """
        print(f"\n⏰ 定时任务已设置")
        print(f"   运行时间: 每天 {run_time}")
        print(f"   按 Ctrl+C 停止")
        
        # 设置定时任务
        schedule.every().day.at(run_time).do(self.daily_task)
        
        # 启动调度循环
        self.is_running = True
        
        while self.is_running:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次
    
    def start_in_background(self, run_time: str = "09:00"):
        """
        后台启动定时任务
        
        Args:
            run_time: 每天运行时间
        """
        def run_scheduler():
            self.start(run_time)
        
        thread = threading.Thread(target=run_scheduler, daemon=True)
        thread.start()
        
        print(f"✅ 后台定时任务已启动")
    
    def stop(self):
        """停止定时任务"""
        self.is_running = False
        print("⏹️ 定时任务已停止")
    
    def run_once(self):
        """立即执行一次任务"""
        print("\n🚀 立即执行任务...")
        self.daily_task()


# 全局实例
daily_scheduler = DailyScheduler()


if __name__ == "__main__":
    import sys
    
    scheduler = DailyScheduler()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--now":
        # 立即执行
        scheduler.run_once()
    else:
        # 定时执行（默认9:00）
        run_time = sys.argv[1] if len(sys.argv) > 1 else "09:00"
        scheduler.start(run_time)
