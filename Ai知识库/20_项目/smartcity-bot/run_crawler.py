"""
全网采集启动脚本
================

启动每日自动采集任务
"""

import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from scheduler.daily_task import daily_scheduler
from config.schedule_config import schedule_config


def main():
    """主函数"""
    print("=" * 60)
    print("🔍 智慧城市全网采集系统")
    print("=" * 60)
    
    # 检查配置
    print("\n📋 配置检查：")
    
    google_key = os.getenv("GOOGLE_API_KEY", "")
    google_cx = os.getenv("GOOGLE_CX", "")
    
    if google_key and google_cx:
        print("  ✅ Google搜索API已配置")
    else:
        print("  ⚠️ 使用国内RSS源（无需API）")
    
    report_chat = os.getenv("REPORT_CHAT_ID", "")
    if report_chat:
        print(f"  ✅ 日报接收者: {report_chat}")
    else:
        print("  ⚠️ 日报接收者未配置")
    
    # 显示当前定时配置
    print(f"\n⏰ 当前定时: 每天 {schedule_config.get_run_time()}")
    
    print("\n" + "=" * 60)
    print("选择运行模式：")
    print("=" * 60)
    print("1. 立即执行一次采集")
    print("2. 启动定时任务")
    print("3. 修改定时配置")
    print("4. 查看当前配置")
    print("=" * 60)
    
    choice = input("\n请选择 (1-4): ").strip()
    
    if choice == "1":
        # 立即执行
        print("\n🚀 立即执行采集任务...")
        daily_scheduler.run_once()
        
    elif choice == "2":
        # 定时执行（使用配置文件中的时间）
        run_time = schedule_config.get_run_time()
        print(f"\n⏰ 启动定时任务，每天 {run_time} 执行")
        print("按 Ctrl+C 停止")
        daily_scheduler.start(run_time)
        
    elif choice == "3":
        # 修改配置
        from config.schedule_config import interactive_config
        interactive_config()
        
    elif choice == "4":
        # 查看配置
        schedule_config.show_config()
        
    else:
        print("❌ 无效选择")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 已停止")
        daily_scheduler.stop()
