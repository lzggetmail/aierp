"""
内容分析器
=========

智能分析群消息内容：
- 判断内容价值
- 提取关键信息
- 自动分类打标签
"""

import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from config.config import knowledge_config, bot_config


@dataclass
class ContentInfo:
    """内容信息"""
    has_value: bool           # 是否有价值
    category: str             # 分类
    title: str                # 标题
    summary: str              # 摘要
    keywords: List[str]       # 关键词
    tags: List[str]           # 标签
    subsystem: Optional[str]  # 子系统
    content_type: str         # 内容类型


class ContentAnalyzer:
    """内容分析器"""
    
    def __init__(self):
        # 加载配置
        knowledge_config.load_keywords()
        bot_config.load_collect_keywords()
        
        self.subsystem_keywords = knowledge_config.subsystem_keywords
        self.collect_keywords = bot_config.collect_keywords
    
    def analyze(self, text: str) -> ContentInfo:
        """
        分析文本内容
        
        Args:
            text: 文本内容
        
        Returns:
            ContentInfo对象
        """
        # 1. 判断是否有价值
        has_value = self._check_value(text)
        
        if not has_value:
            return ContentInfo(
                has_value=False,
                category="",
                title="",
                summary="",
                keywords=[],
                tags=[],
                subsystem=None,
                content_type=""
            )
        
        # 2. 提取关键信息
        title = self._extract_title(text)
        summary = self._extract_summary(text)
        keywords = self._extract_keywords(text)
        
        # 3. 分类和标签
        category, subsystem = self._classify(text)
        tags = self._generate_tags(text, subsystem)
        content_type = self._detect_content_type(text)
        
        return ContentInfo(
            has_value=True,
            category=category,
            title=title,
            summary=summary,
            keywords=keywords,
            tags=tags,
            subsystem=subsystem,
            content_type=content_type
        )
    
    def _check_value(self, text: str) -> bool:
        """判断内容是否有价值"""
        # 检查是否包含收集关键词
        text_lower = text.lower()
        
        for keyword in self.collect_keywords:
            if keyword in text_lower:
                return True
        
        # 检查是否包含子系统关键词
        for subsystem, keywords in self.subsystem_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    return True
        
        # 检查是否包含链接（可能有价值）
        if "http://" in text or "https://" in text:
            return True
        
        return False
    
    def _extract_title(self, text: str) -> str:
        """提取标题"""
        # 取第一行作为标题
        lines = text.strip().split("\n")
        if lines:
            title = lines[0][:100]  # 限制100字符
            return title
        return "无标题"
    
    def _extract_summary(self, text: str) -> str:
        """提取摘要"""
        # 取前200字符作为摘要
        summary = text.strip()[:200]
        if len(text) > 200:
            summary += "..."
        return summary
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        keywords = []
        
        # 从子系统关键词中匹配
        for subsystem, kws in self.subsystem_keywords.items():
            for kw in kws:
                if kw in text and kw not in keywords:
                    keywords.append(kw)
        
        return keywords[:10]  # 最多10个
    
    def _classify(self, text: str) -> Tuple[str, Optional[str]]:
        """分类"""
        # 匹配子系统
        matched_subsystem = None
        max_matches = 0
        
        for subsystem, keywords in self.subsystem_keywords.items():
            matches = sum(1 for kw in keywords if kw in text)
            if matches > max_matches:
                max_matches = matches
                matched_subsystem = subsystem
        
        # 确定分类
        if matched_subsystem:
            # 根据子系统确定分类
            category_mapping = {
                "综合布线": "01-基础设施",
                "机房工程": "01-基础设施",
                "安防系统": "02-建筑智能化",
                "楼宇自控": "02-建筑智能化",
                "智能交通": "04-城市管理",
                "能源管理": "05-能源管理",
                "AI应用": "07-新兴技术",
                "物联网": "07-新兴技术",
                "大数据": "07-新兴技术",
                "数字孪生": "07-新兴技术"
            }
            category = category_mapping.get(matched_subsystem, "08-方案设计")
        else:
            category = "08-方案设计"
        
        return category, matched_subsystem
    
    def _generate_tags(self, text: str, subsystem: Optional[str]) -> List[str]:
        """生成标签"""
        tags = []
        
        # 子系统标签
        if subsystem:
            tags.append(f"#{subsystem}")
        
        # 技术标签
        tech_keywords = ["AI", "IoT", "5G", "大数据", "云计算", "数字孪生", "人工智能"]
        for tech in tech_keywords:
            if tech in text:
                tags.append(f"#{tech}")
        
        # 品牌标签
        brands = ["海康", "大华", "华为", "华三", "思科", "戴尔", "惠普"]
        for brand in brands:
            if brand in text:
                tags.append(f"#{brand}")
        
        return tags[:5]  # 最多5个标签
    
    def _detect_content_type(self, text: str) -> str:
        """检测内容类型"""
        # 报告类
        if any(kw in text for kw in ["白皮书", "研究报告", "市场分析"]):
            return "报告"
        
        # 政策类
        if any(kw in text for kw in ["政策", "标准", "规范", "指南"]):
            return "政策"
        
        # 案例类
        if any(kw in text for kw in ["案例", "实践", "落地", "应用"]):
            return "案例"
        
        # 技术类
        if any(kw in text for kw in ["发布", "推出", "新技术", "创新"]):
            return "技术"
        
        # 产品类
        if any(kw in text for kw in ["新品", "产品", "功能"]):
            return "产品"
        
        return "其他"


# 全局实例
content_analyzer = ContentAnalyzer()


if __name__ == "__main__":
    # 测试分析器
    analyzer = ContentAnalyzer()
    
    # 测试用例
    test_cases = [
        "【新品发布】海康威视发布新一代AI摄像机，支持4K超高清",
        "深圳市智慧城市建设白皮书2026发布",
        "今天天气不错，大家周末愉快！",
        "机房工程方案：UPS选型建议采用华为品牌",
        "国家发布新型智慧城市评价指标体系"
    ]
    
    for text in test_cases:
        print(f"\n测试文本: {text}")
        print("-" * 50)
        
        result = analyzer.analyze(text)
        
        print(f"有价值: {result.has_value}")
        if result.has_value:
            print(f"分类: {result.category}")
            print(f"子系统: {result.subsystem}")
            print(f"类型: {result.content_type}")
            print(f"标签: {', '.join(result.tags)}")
