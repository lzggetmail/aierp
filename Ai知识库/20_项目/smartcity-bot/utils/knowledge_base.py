"""
飞书多维表格知识库
================

使用飞书多维表格作为知识库存储
支持自动存储、检索、RAG问答
"""

import os
import json
from typing import List, Dict, Optional
from datetime import datetime
import requests

# 添加项目根目录到路径
import sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from utils.feishu_api import feishu_api


class FeishuKnowledgeBase:
    """飞书多维表格知识库"""
    
    def __init__(self):
        # 从 .env 文件读取配置
        self._load_env()
        
        self.app_token = os.getenv("FEISHU_BITABLE_TOKEN", "")
        self.table_id = os.getenv("FEISHU_TABLE_ID", "")
        
        # 如果没有配置，需要创建
        if not self.app_token:
            print("⚠️ 知识库未配置，需要初始化")
    
    def _load_env(self):
        """从 .env 文件加载环境变量"""
        env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
        if os.path.exists(env_file):
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
    
    def init_knowledge_base(self, name: str = "智慧城市知识库") -> Dict:
        """
        初始化知识库（创建多维表格）
        
        Args:
            name: 知识库名称
        
        Returns:
            创建结果 {app_token, table_id}
        """
        print(f"\n🏗️ 创建知识库: {name}")
        
        # 获取access token
        access_token = feishu_api.get_tenant_access_token()
        if not access_token:
            return {"error": "获取token失败"}
        
        url = "https://open.feishu.cn/open-apis/bitable/v1/apps"
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "name": name
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            result = response.json()
            
            if result.get("code") == 0:
                app_token = result["data"]["app"]["app_token"]
                print(f"✅ 知识库创建成功: {app_token}")
                
                # 创建默认表格
                table_result = self._create_default_table(app_token)
                
                return {
                    "app_token": app_token,
                    "table_id": table_result.get("table_id", ""),
                    "name": name
                }
            else:
                print(f"❌ 创建失败: {result.get('msg')}")
                return {"error": result.get('msg')}
                
        except Exception as e:
            print(f"❌ 创建异常: {e}")
            return {"error": str(e)}
    
    def _create_default_table(self, app_token: str) -> Dict:
        """创建默认表格"""
        access_token = feishu_api.get_tenant_access_token()
        
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables"
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "table": {
                "name": "知识库",
                "default_view_name": "所有知识"
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            result = response.json()
            
            if result.get("code") == 0:
                table_id = result["data"]["table_id"]
                print(f"✅ 表格创建成功: {table_id}")
                
                # 创建字段
                self._create_fields(app_token, table_id)
                
                return {"table_id": table_id}
            else:
                print(f"❌ 表格创建失败: {result.get('msg')}")
                print(f"   完整响应: {result}")
                
                # 如果创建失败，尝试获取已存在的表格
                print(f"   尝试获取已存在的表格...")
                existing_tables = self._get_existing_tables(app_token)
                if existing_tables:
                    table_id = existing_tables[0]["table_id"]
                    print(f"   ✅ 找到已存在的表格: {table_id}")
                    return {"table_id": table_id}
                
                return {"error": result.get('msg'), "table_id": ""}
                
        except Exception as e:
            print(f"❌ 表格创建异常: {e}")
            return {"error": str(e), "table_id": ""}
    
    def _get_existing_tables(self, app_token: str) -> List[Dict]:
        """获取已存在的表格列表"""
        access_token = feishu_api.get_tenant_access_token()
        
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables"
        
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            result = response.json()
            
            if result.get("code") == 0:
                return result["data"]["items"]
            else:
                return []
        except:
            return []
    
    def _create_fields(self, app_token: str, table_id: str):
        """创建字段"""
        access_token = feishu_api.get_tenant_access_token()
        
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields"
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        # 定义字段
        fields = [
            {"field_name": "标题", "type": 1},  # 文本
            {"field_name": "内容", "type": 1},  # 文本
            {"field_name": "分类", "type": 3, "property": {  # 单选
                "options": [
                    {"name": "基础设施"},
                    {"name": "建筑智能化"},
                    {"name": "通信系统"},
                    {"name": "城市管理"},
                    {"name": "能源管理"},
                    {"name": "公共服务"},
                    {"name": "新兴技术"},
                    {"name": "方案设计"},
                    {"name": "技术方案"},
                    {"name": "城市案例"},
                    {"name": "行业报告"},
                    {"name": "政策标准"}
                ]
            }},
            {"field_name": "子系统", "type": 1},  # 文本
            {"field_name": "标签", "type": 4},  # 多选
            {"field_name": "来源", "type": 1},  # 文本
            {"field_name": "链接", "type": 15, "property": {}},  # URL
            {"field_name": "收藏时间", "type": 5}  # 日期
        ]
        
        for field in fields:
            try:
                requests.post(url, headers=headers, json=field, timeout=5)
            except:
                pass
        
        print(f"✅ 字段创建完成")
    
    def add_knowledge(self, title: str, content: str, category: str, 
                      subsystem: str = "", tags: List[str] = None,
                      source: str = "", url: str = "", publish_date: str = "") -> bool:
        """
        添加知识到知识库
        
        Args:
            title: 标题
            content: 内容
            category: 分类
            subsystem: 子系统
            tags: 标签
            source: 来源
            url: 链接
            publish_date: 发布时间（原始文章时间）
        
        Returns:
            是否成功
        """
        if not self.app_token or not self.table_id:
            print("⚠️ 知识库未配置")
            return False
        
        access_token = feishu_api.get_tenant_access_token()
        
        url_api = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/records"
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        # 构建字段数据
        fields_data = {
            "标题": title,
            "内容": content,
            "分类": category,
            "子系统": subsystem,
            "来源": source,
            "收藏时间": int(datetime.now().timestamp() * 1000)
        }
        
        # 添加发布时间（原始文章时间）
        if publish_date:
            try:
                # 支持多种日期格式
                if isinstance(publish_date, str):
                    # 尝试解析日期字符串
                    for fmt in ['%Y-%m-%d', '%Y/%m/%d', '%Y年%m月%d日']:
                        try:
                            dt = datetime.strptime(publish_date, fmt)
                            fields_data["发布时间"] = int(dt.timestamp() * 1000)
                            break
                        except:
                            pass
            except:
                pass
        
        # 添加发布时间（原始文章时间）
        if publish_date:
            try:
                # 支持多种日期格式
                if isinstance(publish_date, str):
                    for fmt in ['%Y-%m-%d', '%Y/%m/%d', '%Y年%m月%d日']:
                        try:
                            dt = datetime.strptime(publish_date, fmt)
                            fields_data["发布时间"] = int(dt.timestamp() * 1000)
                            break
                        except:
                            pass
            except:
                pass
        
        if tags:
            fields_data["标签"] = tags
        
        if url:
            fields_data["链接"] = {"text": "查看原文", "link": url}
        
        data = {
            "fields": fields_data
        }
        
        try:
            response = requests.post(url_api, headers=headers, json=data, timeout=10)
            result = response.json()
            
            if result.get("code") == 0:
                print(f"✅ 知识已添加: {title[:30]}")
                return True
            else:
                print(f"❌ 添加失败: {result.get('msg')}")
                return False
                
        except Exception as e:
            print(f"❌ 添加异常: {e}")
            return False
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """
        搜索知识库
        
        Args:
            query: 搜索关键词
            limit: 返回数量
        
        Returns:
            搜索结果列表
        """
        if not self.app_token or not self.table_id:
            return []
        
        access_token = feishu_api.get_tenant_access_token()
        
        # 使用飞书搜索API
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/records/search"
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "view_id": "",
            "field_names": ["标题", "内容", "标签"],
            "search": [{"field_name": "标题", "search_value": query}],
            "sort": [{"field_name": "收藏时间", "desc": True}],
            "limit": limit
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            result = response.json()
            
            if result.get("code") == 0:
                items = result.get("data", {}).get("items", [])
                return [self._format_record(item) for item in items]
            else:
                return []
                
        except Exception as e:
            print(f"❌ 搜索异常: {e}")
            return []
    
    def _format_record(self, item: Dict) -> Dict:
        """格式化记录"""
        fields = item.get("fields", {})
        return {
            "id": item.get("record_id"),
            "title": fields.get("标题", ""),
            "content": fields.get("内容", ""),
            "category": fields.get("分类", ""),
            "subsystem": fields.get("子系统", ""),
            "tags": fields.get("标签", []),
            "source": fields.get("来源", ""),
            "url": fields.get("链接", {}).get("link", ""),
            "date": fields.get("收藏时间", "")
        }
    
    def get_stats(self) -> Dict:
        """获取知识库统计"""
        if not self.app_token or not self.table_id:
            return {"total": 0, "categories": {}}
        
        access_token = feishu_api.get_tenant_access_token()
        
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/records"
        
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            result = response.json()
            
            if result.get("code") == 0:
                items = result.get("data", {}).get("items", [])
                
                # 统计分类
                categories = {}
                for item in items:
                    cat = item.get("fields", {}).get("分类", "未分类")
                    categories[cat] = categories.get(cat, 0) + 1
                
                return {
                    "total": len(items),
                    "categories": categories
                }
            else:
                return {"total": 0, "categories": {}}
                
        except Exception as e:
            return {"total": 0, "categories": {}}


# 全局实例
knowledge_base = FeishuKnowledgeBase()


if __name__ == "__main__":
    # 测试创建知识库
    kb = FeishuKnowledgeBase()
    
    if not kb.app_token:
        print("\n🧪 测试创建知识库")
        result = kb.init_knowledge_base()
        
        if result.get("app_token"):
            print(f"\n✅ 知识库配置信息:")
            print(f"   APP_TOKEN: {result['app_token']}")
            print(f"   TABLE_ID: {result['table_id']}")
            print(f"\n📝 请将以下内容添加到 .env 文件:")
            print(f"   FEISHU_BITABLE_TOKEN={result['app_token']}")
            print(f"   FEISHU_TABLE_ID={result['table_id']}")
    else:
        print("\n🧪 测试添加知识")
        kb.add_knowledge(
            title="测试知识",
            content="这是一条测试知识",
            category="新兴技术",
            tags=["测试", "AI"]
        )
        
        print("\n🧪 测试搜索")
        results = kb.search("测试")
        print(f"找到 {len(results)} 条记录")
