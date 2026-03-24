"""
图片分类工具
自动识别图片类型并分类存储
"""
import os
import shutil
from pathlib import Path
from typing import Dict, List
import re


class ImageClassifier:
    """图片分类器"""
    
    # 图片类型关键词映射
    CATEGORY_KEYWORDS = {
        "流程图": [
            "流程", "process", "flow", "workflow", "步骤", "step",
            "决策", "decision", "路径", "path"
        ],
        "架构图": [
            "架构", "architecture", "系统", "system", "技术架构",
            "组织架构", "框架", "framework", "拓扑", "topology"
        ],
        "数据可视化": [
            "图表", "chart", "可视化", "visualization", "仪表盘",
            "dashboard", "数据", "data", "统计", "statistics"
        ],
        "思维导图": [
            "思维导图", "mindmap", "脑图", "知识图谱", "knowledge graph",
            "概念图", "concept", "heptabase", "画布"
        ],
        "信息图表": [
            "信息图", "infographic", "对比", "comparison", "时间线",
            "timeline", "路线图", "roadmap"
        ],
        "UI界面": [
            "界面", "interface", "UI", "原型", "prototype",
            "设计稿", "mockup", "截图", "screenshot"
        ]
    }
    
    def __init__(self, base_dir: str):
        """
        初始化分类器
        
        Args:
            base_dir: 图片素材基础目录
        """
        self.base_dir = Path(base_dir)
        self._ensure_directories()
    
    def _ensure_directories(self):
        """确保分类目录存在"""
        categories = list(self.CATEGORY_KEYWORDS.keys()) + ["其他"]
        for category in categories:
            (self.base_dir / category).mkdir(parents=True, exist_ok=True)
    
    def classify_image(self, filename: str, context: str = "") -> str:
        """
        根据文件名和上下文分类图片
        
        Args:
            filename: 文件名
            context: 上下文信息（主题标题、描述等）
            
        Returns:
            分类名称
        """
        # 合并文件名和上下文
        text = f"{filename} {context}".lower()
        
        # 匹配关键词
        scores = {}
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword.lower() in text)
            if score > 0:
                scores[category] = score
        
        # 返回得分最高的分类
        if scores:
            return max(scores, key=scores.get)
        
        return "其他"
    
    def move_image(self, image_path: str, category: str) -> str:
        """
        移动图片到对应分类目录
        
        Args:
            image_path: 原图片路径
            category: 分类名称
            
        Returns:
            新图片路径
        """
        source = Path(image_path)
        if not source.exists():
            raise FileNotFoundError(f"图片不存在: {image_path}")
        
        # 目标路径
        dest_dir = self.base_dir / category
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / source.name
        
        # 避免重名
        if dest.exists():
            stem = source.stem
            suffix = source.suffix
            counter = 1
            while dest.exists():
                dest = dest_dir / f"{stem}_{counter}{suffix}"
                counter += 1
        
        # 移动文件
        shutil.move(str(source), str(dest))
        return str(dest)
    
    def classify_and_move(self, image_path: str, context: str = "") -> Dict:
        """
        分类并移动图片
        
        Args:
            image_path: 图片路径
            context: 上下文信息
            
        Returns:
            操作结果
        """
        filename = Path(image_path).name
        category = self.classify_image(filename, context)
        new_path = self.move_image(image_path, category)
        
        return {
            "original_path": image_path,
            "category": category,
            "new_path": new_path,
            "filename": filename
        }
    
    def batch_classify(self, image_dir: str, context_func=None) -> List[Dict]:
        """
        批量分类图片
        
        Args:
            image_dir: 图片目录
            context_func: 获取上下文的函数
            
        Returns:
            分类结果列表
        """
        results = []
        image_dir = Path(image_dir)
        
        # 支持的图片格式
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
        
        for image_file in image_dir.rglob('*'):
            if image_file.suffix.lower() in image_extensions:
                # 获取上下文
                context = ""
                if context_func:
                    context = context_func(image_file)
                
                # 分类并移动
                try:
                    result = self.classify_and_move(str(image_file), context)
                    results.append(result)
                    print(f"✓ {result['filename']} -> {result['category']}")
                except Exception as e:
                    print(f"✗ {image_file.name}: {e}")
        
        return results


def main():
    """测试分类器"""
    base_dir = Path("~/.openclaw/workspace/zsxq-downloads/数字化解决方案知识库/图片素材").expanduser()
    
    classifier = ImageClassifier(base_dir)
    
    # 测试分类
    test_cases = [
        ("AI决策流程图.png", "凯捷：走进高管层——人工智能如何悄然重塑高管决策"),
        ("系统架构设计.jpg", "德勤：技术趋势2026"),
        ("数据可视化示例.png", "FT 数据可视化词典"),
        ("Heptabase画布.png", "知识管理工具"),
        ("产品界面截图.jpg", "某产品介绍"),
        ("随机图片.png", "")
    ]
    
    print("图片分类测试:")
    for filename, context in test_cases:
        category = classifier.classify_image(filename, context)
        print(f"  {filename:30s} -> {category}")


if __name__ == "__main__":
    main()
