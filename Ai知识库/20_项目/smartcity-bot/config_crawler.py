"""
配置管理启动脚本
================

管理定时采集配置
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.schedule_config import interactive_config


def main():
    """主函数"""
    print("=" * 60)
    print("⚙️ 智慧城市采集 - 定时配置管理")
    print("=" * 60)
    
    interactive_config()


if __name__ == "__main__":
    main()
