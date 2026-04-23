#!/usr/bin/env python3
"""
知识星球快速同步脚本
用于智慧城市助手的内容同步
"""
import sys
import os
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from utils.zsxq_manager import ZsxqManager
import json
from datetime import datetime


def main():
    """主函数"""
    print("=" * 60)
    print("智慧城市助手 - 知识星球内容同步")
    print("=" * 60)
    
    try:
        # 初始化管理器
        manager = ZsxqManager()
        
        # 获取所有星球
        print("\n📡 正在获取星球列表...")
        groups = manager.get_groups()
        print(f"✓ 已加入 {len(groups)} 个星球")
        
        # 显示星球信息
        print("\n星球列表:")
        for i, group in enumerate(groups, 1):
            name = group.get('name', '未知')
            group_id = group.get('group_id')
            members = group.get('statistics', {}).get('members', {}).get('count', 0)
            print(f"  {i}. {name} (成员: {members})")
        
        # 选择要同步的星球
        print("\n请选择要同步的星球:")
        print("  0. 全部同步")
        for i, group in enumerate(groups, 1):
            print(f"  {i}. {group.get('name')}")
        
        choice = input("\n请输入选项 (0-{}): ".format(len(groups)))
        
        if choice == '0':
            # 同步所有星球
            print("\n开始同步所有星球...")
            for group in groups:
                sync_group(manager, group)
        else:
            # 同步指定星球
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(groups):
                    sync_group(manager, groups[idx])
                else:
                    print("❌ 无效的选项")
            except ValueError:
                print("❌ 请输入数字")
        
    except FileNotFoundError as e:
        print(f"\n❌ 配置文件不存在: {e}")
        print("\n请先配置知识星球认证信息:")
        print("1. 访问知识星球网页版并登录")
        print("2. 按 F12 打开开发者工具")
        print("3. 获取 Cookie 等认证信息")
        print("4. 保存到 ~/.openclaw/workspace/.zsxq-config.json")
    except Exception as e:
        print(f"\n❌ 同步失败: {e}")
        import traceback
        traceback.print_exc()


def sync_group(manager: ZsxqManager, group: dict):
    """
    同步单个星球
    
    Args:
        manager: 知识星球管理器
        group: 星球信息
    """
    group_id = group.get('group_id')
    name = group.get('name')
    
    print(f"\n{'=' * 60}")
    print(f"同步星球: {name}")
    print(f"{'=' * 60}")
    
    # 设置输出目录
    output_dir = project_root / "zsxq-downloads" / name
    
    try:
        # 同步内容
        stats = manager.sync_group_content(group_id, str(output_dir))
        
        # 显示统计
        print(f"\n✓ 同步完成!")
        print(f"  主题数: {stats['total_topics']}")
        print(f"  文件数: {stats['files_downloaded']}")
        print(f"  图片数: {stats['images_downloaded']}")
        print(f"  失败数: {stats['failed']}")
        print(f"\n保存位置: {output_dir}")
        
    except Exception as e:
        print(f"\n❌ 同步失败: {e}")


if __name__ == "__main__":
    main()
