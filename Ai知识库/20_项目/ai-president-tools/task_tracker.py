#!/usr/bin/env python3
"""
AI总裁项目 - 任务追踪工具
自动统计推荐官完成情况
"""

import json
from datetime import datetime, timedelta
from typing import List, Dict

class TaskTracker:
    """任务追踪器"""
    
    def __init__(self):
        self.target_enterprises = 1000  # 目标企业数
        self.target_days = 10  # 目标天数
        self.total_recommenders = 280  # 推荐官总数
        
    def calculate_daily_target(self) -> Dict:
        """计算每日目标"""
        daily_target = self.target_enterprises / self.target_days
        per_recommender = self.target_enterprises / self.total_recommenders
        
        return {
            "每日需注册企业": f"{daily_target:.0f}家",
            "每个推荐官需完成": f"{per_recommender:.1f}家",
            "推荐官总数": self.total_recommenders,
            "总目标": f"{self.target_enterprises}家"
        }
    
    def track_progress(self, current_registrations: int, days_passed: int) -> Dict:
        """追踪进度"""
        progress_rate = (current_registrations / self.target_enterprises) * 100
        daily_avg = current_registrations / days_passed if days_passed > 0 else 0
        remaining = self.target_enterprises - current_registrations
        remaining_days = self.target_days - days_passed
        required_daily = remaining / remaining_days if remaining_days > 0 else 0
        
        status = "✅ 超前" if daily_avg > required_daily else "⚠️ 落后"
        
        return {
            "当前进度": f"{current_registrations}/{self.target_enterprises}家",
            "完成率": f"{progress_rate:.1f}%",
            "日均完成": f"{daily_avg:.1f}家",
            "剩余任务": f"{remaining}家",
            "剩余天数": f"{remaining_days}天",
            "需要日均": f"{required_daily:.1f}家",
            "状态": status
        }
    
    def generate_report(self, data: Dict) -> str:
        """生成报告"""
        report = f"""
# AI总裁项目进度报告
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 核心指标
- 目标: {self.target_enterprises}家企业注册
- 周期: {self.target_days}天
- 推荐官: {self.total_recommenders}人

## ✅ 当前状态
- 完成率: {data['完成率']}
- 日均: {data['日均完成']}
- 状态: {data['状态']}

## 🎯 需要行动
- 每日需完成: {data['需要日均']}
- 剩余{data['剩余天数']}天需注册{data['剩余任务']}家
"""
        return report


# 使用示例
if __name__ == "__main__":
    tracker = TaskTracker()
    
    # 计算目标
    print("=== 目标分解 ===")
    print(json.dumps(tracker.calculate_daily_target(), indent=2, ensure_ascii=False))
    
    # 模拟进度追踪
    print("\n=== 进度追踪 (假设第3天,已注册350家) ===")
    progress = tracker.track_progress(current_registrations=350, days_passed=3)
    print(json.dumps(progress, indent=2, ensure_ascii=False))
    
    # 生成报告
    print("\n=== 完整报告 ===")
    print(tracker.generate_report(progress))
