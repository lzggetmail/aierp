"""
后台守护进程
============

在后台持续运行，定时执行采集任务
"""

import sys
import os
import time
from datetime import datetime

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from scheduler.daily_task import daily_scheduler
from config.schedule_config import schedule_config


def main():
    """主函数"""
    print("=" * 60)
    print("🔍 智慧城市采集 - 后台守护进程")
    print("=" * 60)
    print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 获取配置
    run_time = schedule_config.get_run_time()
    enabled = schedule_config.is_enabled()
    
    print(f"\n📋 配置信息:")
    print(f"   运行时间: 每天 {run_time}")
    print(f"   状态: {'✅ 已启用' if enabled else '❌ 已禁用'}")
    print(f"   关键词数量: {len(schedule_config.get_keywords())}")
    
    if not enabled:
        print("\n⚠️ 定时任务已禁用，等待启用...")
        while not schedule_config.is_enabled():
            time.sleep(60)
            schedule_config._load_config()
        print("✅ 已启用，开始运行...")
    
    # 启动定时任务
    print(f"\n⏰ 启动定时任务...")
    print(f"   按 Ctrl+C 停止")
    print("=" * 60)
    
    try:
        daily_scheduler.start(run_time)
    except KeyboardInterrupt:
        print("\n\n👋 服务已停止")
    except Exception as e:
        print(f"\n❌ 服务异常: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
