"""
飞书API封装
==========

封装飞书开放平台API，包括：
- 获取access_token
- 发送消息
- 接收消息
- 知识库操作
"""

import os
import requests
import time
from typing import Dict, List, Optional
from config.config import feishu_config


class FeishuAPI:
    """飞书API封装类"""
    
    def __init__(self):
        # 从 .env 文件加载配置
        self._load_env()
        
        self.app_id = os.getenv("FEISHU_APP_ID", "")
        self.app_secret = os.getenv("FEISHU_APP_SECRET", "")
        self.base_url = "https://open.feishu.cn/open-apis"
        self.access_token = None
        self.token_expire_time = 0
    
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
    
    def get_access_token(self) -> str:
        """
        获取访问令牌

        Returns:
            access_token字符串
        """
        # 如果token未过期，直接返回
        if self.access_token and time.time() < self.token_expire_time:
            return self.access_token

        url = f"{self.base_url}/auth/v3/tenant_access_token/internal"

        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }

        response = requests.post(url, json=data)
        result = response.json()

        if result.get("code") == 0:
            self.access_token = result["tenant_access_token"]
            # 提前5分钟过期
            self.token_expire_time = time.time() + result["expire"] - 300
            return self.access_token
        else:
            raise Exception(f"获取access_token失败: {result}")

    def get_tenant_access_token(self) -> str:
        """
        获取租户访问令牌（别名方法）

        Returns:
            tenant_access_token字符串
        """
        return self.get_access_token()
    
    def get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        token = self.get_access_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    # ==================== 消息相关 ====================
    
    def send_text_message(self, receive_id: str, text: str, receive_id_type: str = "chat_id") -> Dict:
        """
        发送文本消息
        
        Args:
            receive_id: 接收者ID
            text: 文本内容
            receive_id_type: 接收者类型 (open_id, user_id, union_id, email, chat_id)
        
        Returns:
            响应结果
        """
        url = f"{self.base_url}/im/v1/messages"
        
        params = {
            "receive_id_type": receive_id_type
        }
        
        import json
        
        # 正确的JSON格式
        data = {
            "receive_id": receive_id,
            "msg_type": "text",
            "content": json.dumps({"text": text})  # 使用json.dumps确保正确格式
        }
        
        response = requests.post(url, headers=self.get_headers(), params=params, json=data)
        return response.json()
    
    def send_card_message(self, receive_id: str, card: Dict, receive_id_type: str = "chat_id") -> Dict:
        """
        发送卡片消息
        
        Args:
            receive_id: 接收者ID
            card: 卡片内容
            receive_id_type: 接收者类型
        
        Returns:
            响应结果
        """
        url = f"{self.base_url}/im/v1/messages"
        
        params = {
            "receive_id_type": receive_id_type
        }
        
        import json
        data = {
            "receive_id": receive_id,
            "msg_type": "interactive",
            "content": json.dumps(card)
        }
        
        response = requests.post(url, headers=self.get_headers(), params=params, json=data)
        return response.json()
    
    def get_message(self, message_id: str) -> Dict:
        """
        获取消息详情
        
        Args:
            message_id: 消息ID
        
        Returns:
            消息详情
        """
        url = f"{self.base_url}/im/v1/messages/{message_id}"
        
        response = requests.get(url, headers=self.get_headers())
        return response.json()
    
    # ==================== 群组相关 ====================
    
    def get_chat_list(self, page_size: int = 50) -> Dict:
        """
        获取群组列表
        
        Args:
            page_size: 每页数量
        
        Returns:
            群组列表
        """
        url = f"{self.base_url}/im/v1/chats"
        
        params = {
            "page_size": page_size
        }
        
        response = requests.get(url, headers=self.get_headers(), params=params)
        return response.json()
    
    def get_chat_info(self, chat_id: str) -> Dict:
        """
        获取群组信息
        
        Args:
            chat_id: 群组ID
        
        Returns:
            群组信息
        """
        url = f"{self.base_url}/im/v1/chats/{chat_id}"
        
        response = requests.get(url, headers=self.get_headers())
        return response.json()
    
    # ==================== 知识库相关 ====================
    
    def get_wiki_space_list(self) -> Dict:
        """
        获取知识空间列表
        
        Returns:
            知识空间列表
        """
        url = f"{self.base_url}/wiki/v2/spaces"
        
        params = {
            "page_size": 50
        }
        
        response = requests.get(url, headers=self.get_headers(), params=params)
        return response.json()
    
    def get_wiki_node_list(self, space_id: str) -> Dict:
        """
        获取知识节点列表
        
        Args:
            space_id: 知识空间ID
        
        Returns:
            节点列表
        """
        url = f"{self.base_url}/wiki/v2/spaces/{space_id}/nodes"
        
        params = {
            "page_size": 50
        }
        
        response = requests.get(url, headers=self.get_headers(), params=params)
        return response.json()
    
    def create_wiki_node(self, space_id: str, title: str, obj_type: str = "docx") -> Dict:
        """
        创建知识节点
        
        Args:
            space_id: 知识空间ID
            title: 节点标题
            obj_type: 对象类型 (doc, docx, sheet, bitable)
        
        Returns:
            创建结果
        """
        url = f"{self.base_url}/wiki/v2/spaces/{space_id}/nodes/create"
        
        data = {
            "obj_type": obj_type,
            "title": title
        }
        
        response = requests.post(url, headers=self.get_headers(), json=data)
        return response.json()
    
    # ==================== 文档相关 ====================
    
    def create_doc(self, title: str, content: str = "") -> Dict:
        """
        创建文档
        
        Args:
            title: 文档标题
            content: 文档内容
        
        Returns:
            创建结果
        """
        url = f"{self.base_url}/docx/v1/documents"
        
        data = {
            "title": title
        }
        
        response = requests.post(url, headers=self.get_headers(), json=data)
        return response.json()


# 全局实例
feishu_api = FeishuAPI()


if __name__ == "__main__":
    # 测试API连接
    api = FeishuAPI()
    
    try:
        token = api.get_access_token()
        print(f"✅ 获取access_token成功: {token[:20]}...")
        
        # 获取群组列表
        chats = api.get_chat_list()
        print(f"✅ 获取群组列表成功，共 {len(chats.get('data', {}).get('items', []))} 个群")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
