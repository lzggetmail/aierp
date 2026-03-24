"""
智慧城市知识管理机器人 - 主程序
==============================

启动入口，处理消息事件
"""

import os
import json
import logging
from flask import Flask, request, jsonify

from config.config import (
    feishu_config, 
    llm_config, 
    bot_config,
    validate_config
)
from utils.feishu_api import feishu_api
from utils.content_analyzer import content_analyzer

# 导入命令处理器
from bot.commands import command_handler

# 导入GLM客户端（可选）
try:
    from utils.glm_client import glm_client
    GLM_AVAILABLE = True
except ImportError:
    GLM_AVAILABLE = False
    glm_client = None

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建Flask应用
app = Flask(__name__)


class SmartCityBot:
    """智慧城市知识管理机器人"""
    
    def __init__(self):
        self.name = bot_config.name
        self.trigger_keywords = bot_config.trigger_keywords
    
    def handle_message(self, event: dict) -> dict:
        """
        处理消息事件
        
        Args:
            event: 飞书事件数据
        
        Returns:
            响应结果
        """
        try:
            # 解析消息 - 兼容新旧格式
            event_data = event.get("event", {})
            message = event_data.get("message", {})
            
            message_type = message.get("message_type")
            content = message.get("content")
            chat_id = message.get("chat_id")
            
            # 获取发送者信息（新版格式）
            sender = event_data.get("sender", {})
            if not sender:
                sender = message.get("sender", {})
            
            logger.info(f"收到消息 - 类型: {message_type}, 聊天ID: {chat_id}, 发送者: {sender}")
            
            # 解析消息内容
            if message_type == "text":
                text_content = json.loads(content).get("text", "")
            else:
                # 暂时只处理文本消息
                return {"code": 0, "msg": "success"}
            
            # 获取用户ID
            user_id = sender.get("open_id", "") or sender.get("id", "")
            
            logger.info(f"用户ID: {user_id}, 消息内容: {text_content[:50]}")
            
            # 1. 检查是否是命令
            if command_handler.is_command(text_content):
                response = command_handler.handle_command(text_content, user_id)
                self._send_message(chat_id, response)
                return {"code": 0, "msg": "success"}
            
            # 2. 检查是否是问答触发
            if self._is_triggered(text_content):
                # 问答模式
                answer = self._handle_question(text_content, chat_id)
                self._send_message(chat_id, answer)
                return {"code": 0, "msg": "success"}
            
            # 3. 智能收集模式
            analysis = content_analyzer.analyze(text_content)
            
            if analysis.has_value:
                # 有价值内容，收集存储
                self._collect_knowledge(text_content, analysis, chat_id)
                
                # 通知群
                notification = f"✅ 已收录到知识库\n📚 分类: {analysis.category}\n🏷️ 标签: {', '.join(analysis.tags)}"
                self._send_message(chat_id, notification)
            
            return {"code": 0, "msg": "success"}
            
        except Exception as e:
            logger.error(f"处理消息失败: {e}", exc_info=True)
            return {"code": -1, "msg": str(e)}
    
    def _is_triggered(self, text: str) -> bool:
        """检查是否触发问答"""
        for keyword in self.trigger_keywords:
            if keyword in text:
                return True
        return False
    
    def _handle_question(self, text: str, chat_id: str) -> str:
        """
        处理问答 - 使用RAG检索知识库
        
        Args:
            text: 问题文本
            chat_id: 聊天ID
        
        Returns:
            回答
        """
        # 移除触发词
        question = text
        for keyword in self.trigger_keywords:
            question = question.replace(keyword, "").strip()
        
        # 使用RAG问答引擎
        try:
            from bot.qa_engine import qa_engine
            result = qa_engine.answer(question, use_rag=True)
            
            # 格式化回答（包含来源）
            return qa_engine.format_answer(result, show_sources=True)
            
        except Exception as e:
            logger.error(f"RAG问答失败: {e}")
            return f"抱歉，处理您的问题时出现错误。请稍后重试。"
    
    def _collect_knowledge(self, text: str, analysis, chat_id: str):
        """
        收集知识到知识库
        
        Args:
            text: 原始文本
            analysis: 分析结果
            chat_id: 聊天ID
        """
        # 使用GLM进行深度分析
        try:
            from utils.glm_client import glm_client
            glm_result = glm_client.analyze_content(text)
            
            # 合并分析结果
            logger.info(f"收集知识 - 标题: {glm_result.get('title', analysis.title)}")
            logger.info(f"  分类: {glm_result.get('category', analysis.category)}")
            logger.info(f"  摘要: {glm_result.get('summary', '')[:50]}...")
            logger.info(f"  标签: {glm_result.get('tags', analysis.tags)}")
            logger.info(f"  价值评分: {glm_result.get('value_score', 'N/A')}/10")
            
            # TODO: 调用飞书API存储到知识库
            # feishu_api.create_wiki_node(...)
            
        except Exception as e:
            logger.error(f"GLM分析失败: {e}")
            # 降级使用基础分析
            logger.info(f"收集知识 - 标题: {analysis.title}")
            logger.info(f"  分类: {analysis.category}")
            logger.info(f"  标签: {analysis.tags}")
    
    def _send_message(self, chat_id: str, text: str):
        """
        发送消息
        
        Args:
            chat_id: 聊天ID
            text: 消息内容
        """
        try:
            result = feishu_api.send_text_message(chat_id, text)
            if result.get("code") == 0:
                logger.info(f"消息发送成功: {chat_id}")
            else:
                logger.error(f"消息发送失败: {result}")
        except Exception as e:
            logger.error(f"发送消息异常: {e}")


# 全局机器人实例
bot = SmartCityBot()


@app.route('/webhook', methods=['POST'])
def webhook():
    """
    飞书事件回调接口
    """
    data = request.json
    logger.info(f"收到webhook请求: {json.dumps(data, ensure_ascii=False)[:500]}")
    
    # URL验证
    if data.get("type") == "url_verification":
        challenge = data.get("challenge", "")
        logger.info(f"URL验证请求: {challenge}")
        return jsonify({"challenge": challenge})
    
    # 飞书新版本事件格式
    header = data.get("header", {})
    event_type = header.get("event_type", "")
    
    logger.info(f"事件类型: {event_type}")
    
    # 处理消息接收事件
    if event_type == "im.message.receive_v1":
        try:
            # 提取消息内容
            event = data.get("event", {})
            message = event.get("message", {})
            
            # 构造统一格式
            formatted_data = {
                "event": {
                    "message": message
                }
            }
            
            result = bot.handle_message(formatted_data)
            return jsonify(result)
        except Exception as e:
            logger.error(f"处理消息失败: {e}", exc_info=True)
            return jsonify({"code": -1, "msg": str(e)})
    
    # 旧版本事件格式
    if data.get("type") == "event_callback":
        event = data.get("event", {})
        old_event_type = event.get("type")
        
        if old_event_type == "message.receive":
            try:
                result = bot.handle_message(data)
                return jsonify(result)
            except Exception as e:
                logger.error(f"处理消息失败: {e}", exc_info=True)
                return jsonify({"code": -1, "msg": str(e)})
    
    return jsonify({"code": 0})


@app.route('/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({"status": "ok", "bot": bot_config.name})


def main():
    """主函数"""
    print("=" * 60)
    print(f"🏙️  {bot_config.name}")
    print("=" * 60)
    
    # 验证配置
    if not validate_config():
        print("\n❌ 配置不完整，请设置环境变量")
        return
    
    print("\n✅ 配置验证通过")
    print(f"  App ID: {feishu_config.app_id[:15]}...")
    print(f"  LLM: {llm_config.model} (智谱AI)")
    print(f"  GLM可用: {'是' if GLM_AVAILABLE else '否'}")
    
    # 测试飞书连接
    try:
        token = feishu_api.get_access_token()
        print(f"\n✅ 飞书连接成功")
    except Exception as e:
        print(f"\n❌ 飞书连接失败: {e}")
        return
    
    # 启动服务
    port = int(os.getenv("PORT", 8080))
    print(f"\n🚀 启动Web服务，端口: {port}")
    print(f"  Webhook: http://localhost:{port}/webhook")
    print(f"  Health: http://localhost:{port}/health")
    print("\n按 Ctrl+C 停止服务\n")
    
    app.run(host='0.0.0.0', port=port)


if __name__ == "__main__":
    main()
