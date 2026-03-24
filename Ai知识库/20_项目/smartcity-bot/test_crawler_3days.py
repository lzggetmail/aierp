"""
测试采集 - 近3天
"""

import sys
import os
from datetime import datetime, timedelta

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from crawler.cn_web_search import cn_web_searcher
from utils.content_analyzer import ContentAnalyzer
from utils.knowledge_base import knowledge_base


def test_crawl_3days():
    """测试采集近3天的资料"""
    
    print("\n" + "=" * 60)
    print("🧪 测试采集 - 近3天")
    print("=" * 60)
    
    # 计算3天前的日期
    three_days_ago = datetime.now() - timedelta(days=3)
    print(f"📅 采集时间范围：{three_days_ago.strftime('%Y-%m-%d')} 至今\n")
    
    # 执行采集
    print("🔍 正在采集...")
    results = cn_web_searcher.search_all()
    
    if not results:
        print("⚠️ 未获取到搜索结果")
        return
    
    print(f"✅ 共采集 {len(results)} 条内容\n")
    
    # 分析并存储
    print("📊 正在分析并存储...")
    analyzer = ContentAnalyzer()
    stored_count = 0
    filtered_count = 0
    
    for i, result in enumerate(results[:20], 1):  # 只处理前20条测试
        print(f"\n[{i}/20] {result.title[:50]}...")
        
        # 检查发布时间
        try:
            if hasattr(result, 'date') and result.date:
                pub_date = datetime.strptime(result.date, '%Y-%m-%d')
                
                # 只保留近3天的
                if pub_date < three_days_ago:
                    print(f"   ⏭️  跳过（发布于 {result.date}，超过3天）")
                    filtered_count += 1
                    continue
        except:
            pass
        
        # 分析内容
        analysis = analyzer.analyze(result.snippet)
        
        if analysis.has_value:
            # 存储到知识库
            success = knowledge_base.add_knowledge(
                title=result.title,
                content=result.snippet,
                category=analysis.category,
                subsystem=analysis.subsystem or "",
                tags=analysis.tags,
                source=result.source,
                url=result.url,
                publish_date=result.date if hasattr(result, 'date') else ""
            )
            
            if success:
                stored_count += 1
                print(f"   ✅ 已存储 | 分类: {analysis.category}")
                if hasattr(result, 'date') and result.date:
                    print(f"   📅 发布时间: {result.date}")
            else:
                print(f"   ❌ 存储失败")
        else:
            print(f"   ⏭️  跳过（无价值内容）")
    
    # 统计
    print("\n" + "=" * 60)
    print("📊 测试采集统计")
    print("=" * 60)
    print(f"测试数量: 20 条")
    print(f"时间过滤: {filtered_count} 条（超过3天）")
    print(f"有效内容: {stored_count} 条")
    print(f"跳过内容: {20 - stored_count - filtered_count} 条")
    print("\n✅ 测试采集完成！")
    print(f"\n💡 输入 /kb stats 查看知识库")


if __name__ == "__main__":
    test_crawl_3days()
