"""
智慧城市知识管理机器人 - 配置文件
================================

配置飞书、OpenAI等服务参数

注意：敏感信息使用环境变量，不要硬编码！
"""

import os
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class FeishuConfig:
    """飞书配置"""
    # 从环境变量读取，确保安全
    app_id: str = os.getenv("FEISHU_APP_ID", "")
    app_secret: str = os.getenv("FEISHU_APP_SECRET", "")
    
    # 飞书API地址
    base_url: str = "https://open.feishu.cn/open-apis"
    
    # 知识库配置
    wiki_space_id: str = os.getenv("FEISHU_WIKU_SPACE_ID", "")  # 知识空间ID


@dataclass
class LLMConfig:
    """LLM配置"""
    # GLM-5配置（智谱AI）
    api_key: str = os.getenv("GLM_API_KEY", "")
    model: str = "glm-5"  # GLM-5
    base_url: str = "https://open.bigmodel.cn/api/anthropic"
    temperature: float = 0.7
    max_tokens: int = 2000


@dataclass
class KnowledgeConfig:
    """知识库配置"""
    
    # 知识分类
    categories: Dict[str, str] = None
    
    def __post_init__(self):
        self.categories = {
            "01": "基础设施",
            "02": "建筑智能化",
            "03": "通信系统",
            "04": "城市管理",
            "05": "能源管理",
            "06": "公共服务",
            "07": "新兴技术",
            "08": "方案设计",
            "09": "技术方案",
            "10": "城市案例",
            "11": "行业报告",
            "12": "政策标准"
        }
    
    # 子系统关键词
    subsystem_keywords: Dict[str, List[str]] = None
    
    def load_keywords(self):
        self.subsystem_keywords = {
            "综合布线": ["光纤", "网线", "配线架", "桥架"],
            "机房工程": ["服务器", "机柜", "UPS", "精密空调", "存储"],
            "安防系统": ["摄像头", "NVR", "门禁", "报警", "监控"],
            "楼宇自控": ["BAS", "空调", "照明", "电梯", "DDC"],
            "智能交通": ["停车", "信号", "电子警察", "诱导"],
            "能源管理": ["电力", "能耗", "充电桩", "节能"],
            "AI应用": ["人脸识别", "行为分析", "智能识别"],
            "物联网": ["传感器", "网关", "IoT"],
            "大数据": ["数据分析", "可视化", "中台"],
            "数字孪生": ["3D建模", "仿真", "虚拟"]
        }


@dataclass
class BotConfig:
    """机器人配置"""
    # 机器人名称
    name: str = "智慧城市助手"
    
    # 触发关键词
    trigger_keywords: List[str] = None
    
    def __post_init__(self):
        self.trigger_keywords = [
            "@智慧城市助手",
            "@智慧城市",
            "@助手"
        ]
    
    # 收集关键词（触发自动收集）
    collect_keywords: List[str] = None
    
    def load_collect_keywords(self):
        self.collect_keywords = [
            # 报告类
            "白皮书", "研究报告", "市场分析", "行业报告",
            # 政策类
            "政策", "标准", "规范", "指南", "通知",
            # 技术类
            "发布", "推出", "突破", "创新", "新技术",
            # 案例类
            "案例", "实践", "落地", "应用", "获奖",
            # 产品类
            "新品", "升级", "版本", "功能"
        ]


# 全局配置实例
feishu_config = FeishuConfig()
llm_config = LLMConfig()
knowledge_config = KnowledgeConfig()
bot_config = BotConfig()


def validate_config():
    """验证配置是否完整"""
    errors = []
    
    if not feishu_config.app_id:
        errors.append("缺少 FEISHU_APP_ID")
    
    if not feishu_config.app_secret:
        errors.append("缺少 FEISHU_APP_SECRET")
    
    if not llm_config.api_key:
        errors.append("缺少 GLM_API_KEY（智谱AI的API Key）")
    
    if errors:
        print("⚠️ 配置错误：")
        for error in errors:
            print(f"  - {error}")
        return False
    
    return True


if __name__ == "__main__":
    # 测试配置
    print("📋 当前配置：")
    print(f"  App ID: {feishu_config.app_id[:10]}..." if feishu_config.app_id else "  App ID: 未配置")
    print(f"  Secret: {'*' * 20}" if feishu_config.app_secret else "  Secret: 未配置")
    print(f"  GLM Key: {'*' * 20}" if llm_config.api_key else "  GLM Key: 未配置")
    print(f"  模型: {llm_config.model}")
    
    if validate_config():
        print("\n✅ 配置完整")
    else:
        print("\n❌ 配置不完整，请设置环境变量")
