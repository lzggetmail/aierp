"""
定时配置管理
============

允许用户自定义定时采集时间
"""

import os
import json
from datetime import datetime
from typing import Optional


class ScheduleConfig:
    """定时配置管理器"""
    
    def __init__(self):
        self.config_file = os.path.join(
            os.path.dirname(__file__), 
            "..", 
            "config", 
            "schedule.json"
        )
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        """加载配置"""
        default_config = {
            "run_time": "09:00",  # 默认每天9点
            "enabled": True,
            "keywords": [
                "智慧城市", "智能城市", "城市大脑",
                "安防", "摄像头", "监控",
                "机房", "服务器", "数据中心",
                "物联网", "IoT", "传感器",
                "人工智能", "AI", "人脸识别",
                "智能交通", "停车", "信号灯",
                "数字孪生", "3D建模",
                "新能源", "充电桩",
                "白皮书", "研究报告"
            ],
            "max_results": 50,  # 每次最大采集数量
            "report_chat_id": ""  # 日报接收者
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    saved = json.load(f)
                    default_config.update(saved)
            except Exception as e:
                print(f"⚠️ 加载配置失败: {e}")
        
        return default_config
    
    def _save_config(self):
        """保存配置"""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            print(f"✅ 配置已保存")
            return True
        except Exception as e:
            print(f"❌ 保存配置失败: {e}")
            return False
    
    def get_run_time(self) -> str:
        """获取运行时间"""
        return self.config.get("run_time", "09:00")
    
    def set_run_time(self, time_str: str) -> bool:
        """
        设置运行时间
        
        Args:
            time_str: 时间字符串，格式 "HH:MM"
        
        Returns:
            是否设置成功
        """
        # 验证时间格式
        try:
            datetime.strptime(time_str, "%H:%M")
        except ValueError:
            print(f"❌ 时间格式错误，请使用 HH:MM 格式，例如: 09:00")
            return False
        
        self.config["run_time"] = time_str
        return self._save_config()
    
    def is_enabled(self) -> bool:
        """是否启用"""
        return self.config.get("enabled", True)
    
    def set_enabled(self, enabled: bool):
        """启用/禁用"""
        self.config["enabled"] = enabled
        self._save_config()
    
    def get_keywords(self) -> list:
        """获取关键词列表"""
        return self.config.get("keywords", [])
    
    def add_keyword(self, keyword: str):
        """添加关键词"""
        keywords = self.get_keywords()
        if keyword not in keywords:
            keywords.append(keyword)
            self.config["keywords"] = keywords
            self._save_config()
            print(f"✅ 已添加关键词: {keyword}")
    
    def remove_keyword(self, keyword: str):
        """删除关键词"""
        keywords = self.get_keywords()
        if keyword in keywords:
            keywords.remove(keyword)
            self.config["keywords"] = keywords
            self._save_config()
            print(f"✅ 已删除关键词: {keyword}")
    
    def get_max_results(self) -> int:
        """获取最大采集数量"""
        return self.config.get("max_results", 50)
    
    def set_max_results(self, max_num: int):
        """设置最大采集数量"""
        self.config["max_results"] = max_num
        self._save_config()
    
    def get_report_chat_id(self) -> str:
        """获取日报接收者ID"""
        return self.config.get("report_chat_id", "")
    
    def set_report_chat_id(self, chat_id: str):
        """设置日报接收者ID"""
        self.config["report_chat_id"] = chat_id
        self._save_config()
    
    def show_config(self):
        """显示当前配置"""
        print("\n" + "=" * 60)
        print("📋 当前定时配置")
        print("=" * 60)
        print(f"⏰ 运行时间: {self.get_run_time()}")
        print(f"🔄 状态: {'✅ 已启用' if self.is_enabled() else '❌ 已禁用'}")
        print(f"📊 最大采集数: {self.get_max_results()}")
        print(f"💬 日报接收: {self.get_report_chat_id() or '未设置'}")
        print(f"\n🏷️ 关键词 ({len(self.get_keywords())}个):")
        for i, kw in enumerate(self.get_keywords()[:10], 1):
            print(f"   {i}. {kw}")
        if len(self.get_keywords()) > 10:
            print(f"   ... 还有 {len(self.get_keywords()) - 10} 个")
        print("=" * 60)


# 全局实例
schedule_config = ScheduleConfig()


def interactive_config():
    """交互式配置界面"""
    config = ScheduleConfig()
    
    while True:
        config.show_config()
        
        print("\n📝 配置选项:")
        print("1. 修改运行时间")
        print("2. 启用/禁用定时任务")
        print("3. 添加关键词")
        print("4. 删除关键词")
        print("5. 设置最大采集数量")
        print("6. 设置日报接收者")
        print("0. 退出")
        
        choice = input("\n请选择 (0-6): ").strip()
        
        if choice == "0":
            print("\n👋 再见！")
            break
        
        elif choice == "1":
            print(f"\n当前运行时间: {config.get_run_time()}")
            new_time = input("请输入新的运行时间 (HH:MM): ").strip()
            if new_time:
                config.set_run_time(new_time)
        
        elif choice == "2":
            current = config.is_enabled()
            print(f"\n当前状态: {'启用' if current else '禁用'}")
            new_status = input("启用定时任务? (y/n): ").strip().lower()
            config.set_enabled(new_status == 'y')
        
        elif choice == "3":
            keyword = input("\n请输入新关键词: ").strip()
            if keyword:
                config.add_keyword(keyword)
        
        elif choice == "4":
            keywords = config.get_keywords()
            print("\n当前关键词:")
            for i, kw in enumerate(keywords, 1):
                print(f"  {i}. {kw}")
            
            idx = input("\n请输入要删除的序号: ").strip()
            try:
                idx = int(idx) - 1
                if 0 <= idx < len(keywords):
                    config.remove_keyword(keywords[idx])
            except:
                print("❌ 无效输入")
        
        elif choice == "5":
            print(f"\n当前最大采集数: {config.get_max_results()}")
            max_num = input("请输入新的最大采集数 (1-100): ").strip()
            try:
                max_num = int(max_num)
                if 1 <= max_num <= 100:
                    config.set_max_results(max_num)
            except:
                print("❌ 无效输入")
        
        elif choice == "6":
            print(f"\n当前日报接收: {config.get_report_chat_id() or '未设置'}")
            chat_id = input("请输入飞书群/用户ID: ").strip()
            if chat_id:
                config.set_report_chat_id(chat_id)
        
        else:
            print("❌ 无效选择")


if __name__ == "__main__":
    interactive_config()
