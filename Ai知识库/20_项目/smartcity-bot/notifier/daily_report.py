"""
日报生成与推送
=============

生成每日知识简报并推送到飞书
"""

import os
import sys
from datetime import datetime
from typing import List, Dict
from collections import Counter

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from utils.feishu_api import feishu_api
from config.schedule_config import schedule_config


class DailyReporter:
    """日报生成器"""
    
    def __init__(self):
        # 优先从配置文件获取，其次从环境变量
        self.chat_id = schedule_config.get_report_chat_id() or os.getenv("REPORT_CHAT_ID", "")
    
    def generate_report(self, results: List[Dict]) -> str:
        """
        生成日报内容
        
        Args:
            results: 分析后的结果列表
        
        Returns:
            日报文本
        """
        if not results:
            return "今日暂无新增资料"
        
        # 统计分类
        categories = [r["category"] for r in results if r.get("category")]
        category_count = Counter(categories)
        
        # 生成报告
        report_lines = [
            "📊 **每日智慧城市资料简报**",
            f"📅 {datetime.now().strftime('%Y年%m月%d日')}",
            "",
            f"今日共收集 **{len(results)}** 条有价值资料",
            ""
        ]
        
        # 分类统计
        if category_count:
            report_lines.append("📋 **分类统计：**")
            for cat, count in category_count.most_common(5):
                report_lines.append(f"  • {cat}: {count}条")
            report_lines.append("")
        
        # 详细列表（按分类）
        report_lines.append("📝 **详细内容：**")
        report_lines.append("")
        
        # 按分类组织
        by_category = {}
        for result in results:
            cat = result.get("category", "其他")
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(result)
        
        # 输出每个分类
        for category, items in by_category.items():
            report_lines.append(f"**{category}** ({len(items)}条)")
            
            for i, item in enumerate(items[:3], 1):  # 每类最多3条
                title = item.get("title", "无标题")[:50]
                summary = item.get("summary", "")[:100]
                url = item.get("url", "")
                tags = item.get("tags", [])
                
                report_lines.append(f"{i}. {title}")
                if summary:
                    report_lines.append(f"   {summary}...")
                if tags:
                    report_lines.append(f"   🏷️ {' '.join(tags[:3])}")
                if url:
                    report_lines.append(f"   🔗 {url}")
                report_lines.append("")
        
        # 底部
        report_lines.extend([
            "---",
            "🤖 由智慧城市助手自动生成",
            f"⏰ {datetime.now().strftime('%H:%M')}"
        ])
        
        return "\n".join(report_lines)
    
    def send_report(self, report: str, chat_id: str = None):
        """
        发送日报到飞书
        
        Args:
            report: 日报内容
            chat_id: 接收者ID（可选）
        """
        target_chat_id = chat_id or self.chat_id
        
        if not target_chat_id:
            print("⚠️ 未配置日报接收者")
            print("\n" + report)
            return False
        
        try:
            result = feishu_api.send_text_message(target_chat_id, report)
            
            if result.get("code") == 0:
                print(f"✅ 日报已发送")
                return True
            else:
                print(f"❌ 发送失败: {result}")
                return False
                
        except Exception as e:
            print(f"❌ 发送异常: {e}")
            return False
    
    def generate_and_send(self, results: List[Dict], chat_id: str = None):
        """
        生成并发送日报
        
        Args:
            results: 分析结果
            chat_id: 接收者
        """
        print("\n📝 生成日报...")
        
        # 生成报告
        report = self.generate_report(results)
        
        # 发送
        self.send_report(report, chat_id)
        
        # 打印预览
        print("\n" + "=" * 60)
        print("📄 日报预览：")
        print("=" * 60)
        print(report[:500] + "..." if len(report) > 500 else report)


# 全局实例
daily_reporter = DailyReporter()


if __name__ == "__main__":
    # 测试日报生成
    reporter = DailyReporter()
    
    # 模拟数据
    test_results = [
        {
            "title": "2026智慧城市白皮书发布",
            "url": "https://example.com/1",
            "summary": "最新报告涵盖AI、物联网等技术趋势",
            "category": "行业报告",
            "tags": ["#白皮书", "#2026"]
        },
        {
            "title": "海康威视发布新一代AI摄像机",
            "url": "https://example.com/2",
            "summary": "支持4K超高清和人脸识别",
            "category": "安防系统",
            "tags": ["#海康", "#AI"]
        }
    ]
    
    # 生成日报
    report = reporter.generate_report(test_results)
    print(report)
