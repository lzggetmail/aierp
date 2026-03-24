"""
知识星球 API 管理模块
用于智慧城市助手的知识星球内容同步
"""
import json
import os
import time
from pathlib import Path
from typing import Dict, List, Optional
import requests


class ZsxqManager:
    """知识星球管理器"""
    
    def __init__(self, config_path: str = None):
        """
        初始化知识星球管理器
        
        Args:
            config_path: 配置文件路径
        """
        self.config_path = config_path or "~/.openclaw/workspace/.zsxq-config.json"
        self.config = self._load_config()
        self.zsxq_config = self._load_zsxq_config()
        
    def _load_config(self) -> Dict:
        """加载认证配置"""
        config_file = Path(self.config_path).expanduser()
        if not config_file.exists():
            raise FileNotFoundError(f"配置文件不存在: {config_file}")
        
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _load_zsxq_config(self) -> Dict:
        """加载知识星球配置"""
        config_file = Path("~/.openclaw/workspace/projects/smartcity-bot/config/zsxq_config.json").expanduser()
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _get_headers(self) -> Dict[str, str]:
        """构建请求头"""
        return {
            'Cookie': self.config.get('cookie', ''),
            'User-Agent': self.config.get('user_agent', ''),
            'x-request-id': self.config.get('x_request_id', ''),
            'x-signature': self.config.get('x_signature', ''),
            'x-timestamp': self.config.get('x_timestamp', ''),
            'x-version': '2.55.0',
            'x-tzone': 'Asia/Shanghai',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Origin': 'https://wx.zsxq.com',
            'Referer': 'https://wx.zsxq.com/',
        }
    
    def get_groups(self) -> List[Dict]:
        """获取所有加入的星球"""
        url = "https://api.zsxq.com/v2/groups"
        response = requests.get(url, headers=self._get_headers())
        
        if response.status_code == 200:
            data = response.json()
            if data.get('succeeded'):
                return data['resp_data']['groups']
        return []
    
    def get_topics(self, group_id: str, scope: str = 'all', count: int = 20) -> List[Dict]:
        """
        获取星球主题列表
        
        Args:
            group_id: 星球ID
            scope: 范围 (all/digests)
            count: 数量
            
        Returns:
            主题列表
        """
        url = f"https://api.zsxq.com/v2/groups/{group_id}/topics"
        params = {'scope': scope, 'count': count}
        
        response = requests.get(url, headers=self._get_headers(), params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('succeeded'):
                return data['resp_data']['topics']
        return []
    
    def get_all_topics(self, group_id: str) -> List[Dict]:
        """
        获取所有主题（分页加载）
        
        Args:
            group_id: 星球ID
            
        Returns:
            所有主题列表
        """
        all_topics = []
        end_time = None
        count = 20
        
        while True:
            url = f"https://api.zsxq.com/v2/groups/{group_id}/topics"
            params = {'scope': 'all', 'count': count}
            
            if end_time:
                params['end_time'] = end_time
            
            response = requests.get(url, headers=self._get_headers(), params=params)
            
            if response.status_code != 200:
                break
            
            data = response.json()
            if not data.get('succeeded') or not data['resp_data']['topics']:
                break
            
            topics = data['resp_data']['topics']
            all_topics.extend(topics)
            
            # 获取最后一个主题的时间
            if len(topics) < count:
                break
            
            last_topic = topics[-1]
            end_time = last_topic['create_time']
            
            # 避免请求过快
            time.sleep(0.5)
        
        return all_topics
    
    def download_file(self, file_id: str, save_path: str) -> bool:
        """
        下载文件
        
        Args:
            file_id: 文件ID
            save_path: 保存路径
            
        Returns:
            是否成功
        """
        try:
            # 获取下载链接
            url = f"https://api.zsxq.com/v2/files/{file_id}/download"
            response = requests.get(url, headers=self._get_headers())
            
            if response.status_code == 200:
                data = response.json()
                if data.get('succeeded') and data['resp_data'].get('download_url'):
                    download_url = data['resp_data']['download_url']
                    
                    # 下载文件
                    file_response = requests.get(download_url, stream=True)
                    if file_response.status_code == 200:
                        with open(save_path, 'wb') as f:
                            for chunk in file_response.iter_content(chunk_size=8192):
                                f.write(chunk)
                        return True
        except Exception as e:
            print(f"下载文件失败: {e}")
        
        return False
    
    def sync_group_content(self, group_id: str, output_dir: str) -> Dict:
        """
        同步星球内容到本地
        
        Args:
            group_id: 星球ID
            output_dir: 输出目录
            
        Returns:
            同步统计信息
        """
        stats = {
            'total_topics': 0,
            'files_downloaded': 0,
            'images_downloaded': 0,
            'failed': 0
        }
        
        # 获取所有主题
        topics = self.get_all_topics(group_id)
        stats['total_topics'] = len(topics)
        
        # 创建输出目录
        output_path = Path(output_dir).expanduser()
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 保存主题列表
        topics_file = output_path / 'topics.json'
        with open(topics_file, 'w', encoding='utf-8') as f:
            json.dump(topics, f, ensure_ascii=False, indent=2)
        
        # TODO: 实现文件和图片下载逻辑
        
        return stats


if __name__ == "__main__":
    # 测试代码
    manager = ZsxqManager()
    
    # 获取所有星球
    groups = manager.get_groups()
    print(f"已加入 {len(groups)} 个星球:")
    for group in groups:
        print(f"  - {group['name']} (ID: {group['group_id']})")
    
    # 测试获取主题
    if groups:
        group_id = groups[0]['group_id']
        topics = manager.get_topics(group_id, count=5)
        print(f"\n获取到 {len(topics)} 个主题")
