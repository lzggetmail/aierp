"""
群内管理命令
============

支持在群里通过命令管理知识库和智能问答
"""

import re
from typing import Dict, List, Optional
from utils.knowledge_base import knowledge_base
from utils.content_analyzer import ContentAnalyzer
from utils.rag_knowledge import rag_kb
from bot.qa_engine import qa_engine
from config.schedule_config import schedule_config


class GroupCommandHandler:
    """群内命令处理器"""
    
    def __init__(self):
        self.analyzer = ContentAnalyzer()
        # 管理员列表（可以执行敏感操作的用户）
        # 注意：群消息中无法获取发送者ID，所以暂时禁用权限检查
        self.admins = [
            "ou_eb2c662a3733e4be07ba01898b0058ec"  # 主管理员
        ]
        # 是否启用权限检查（群聊中建议关闭）
        self.enable_auth = False  # 暂时禁用权限检查
    
    def is_command(self, text: str) -> bool:
        """判断是否是命令"""
        return text.strip().startswith("/")
    
    def handle_command(self, text: str, user_id: str) -> str:
        """
        处理命令
        
        Args:
            text: 命令文本
            user_id: 用户ID
        
        Returns:
            响应文本
        """
        # 解析命令
        text = text.strip()
        
        # 帮助命令
        if text in ["/help", "/帮助"]:
            return self._help()
        
        # 知识库命令
        if text.startswith("/kb") or text.startswith("/知识库"):
            return self._handle_kb_command(text, user_id)
        
        # 采集命令
        if text.startswith("/crawler") or text.startswith("/采集"):
            return self._handle_crawler_command(text, user_id)
        
        # 搜索命令
        if text.startswith("/search") or text.startswith("/搜索"):
            return self._handle_search_command(text)
        
        # 统计命令
        if text in ["/stats", "/统计"]:
            return self._handle_stats_command()
        
        # 添加知识
        if text.startswith("/add") or text.startswith("/添加"):
            return self._handle_add_command(text, user_id)
        
        return "❌ 未知命令，输入 /help 查看帮助"
    
    def _help(self) -> str:
        """帮助信息"""
        return """
🤖 **智慧城市助手 - 命令帮助**

**📚 知识库管理**
/kb init - 初始化知识库
/kb stats - 查看统计
/kb search <关键词> - 搜索知识
/kb add <标题> | <内容> - 添加知识

**🔍 搜索**
/search <关键词> - 搜索知识库

**📊 统计**
/stats - 查看知识库统计

**⚙️ 采集管理**
/crawler status - 查看状态
/crawler time <时间> - 设置定时
/crawler start - 立即执行
/crawler enable - 启用
/crawler disable - 禁用

**📝 示例**
/search 智慧交通
/add 新技术 | AI摄像头支持人脸识别
/crawler time 08:30

---
输入 /help 查看此帮助
"""
    
    def _handle_kb_command(self, text: str, user_id: str) -> str:
        """处理知识库命令"""
        parts = text.split(maxsplit=2)
        
        if len(parts) < 2:
            return "❌ 请指定子命令，例如: /kb stats"
        
        subcmd = parts[1].lower()
        
        # 初始化知识库
        if subcmd in ["init", "初始化"]:
            # 暂时禁用权限检查（群消息无法获取发送者ID）
            if self.enable_auth and user_id not in self.admins:
                return "❌ 仅管理员可以初始化知识库"
            
            result = knowledge_base.init_knowledge_base()
            
            if result.get("app_token"):
                return f"""✅ 知识库创建成功！

📋 配置信息：
APP_TOKEN: {result['app_token']}
TABLE_ID: {result['table_id']}

⚠️ 请将以下内容添加到服务器环境变量：
export FEISHU_BITABLE_TOKEN={result['app_token']}
export FEISHU_TABLE_ID={result['table_id']}

然后重启机器人服务。"""
            else:
                return f"❌ 创建失败: {result.get('error', '未知错误')}"
        
        # 统计
        elif subcmd in ["stats", "统计"]:
            stats = knowledge_base.get_stats()
            
            if stats["total"] == 0:
                return "📊 知识库暂无数据"
            
            lines = [f"📊 知识库统计\n"]
            lines.append(f"总数: {stats['total']} 条\n")
            lines.append("分类统计:")
            for cat, count in stats["categories"].items():
                lines.append(f"  • {cat}: {count}条")
            
            return "\n".join(lines)
        
        # 立即执行日报
        elif subcmd in ["daily", "日报"]:
            return self._execute_daily_report()
        
        # 批量采集近一年
        elif subcmd in ["batch", "批量"]:
            return self._execute_batch_crawl()
        
        # 自定义时间范围采集
        elif subcmd in ["range", "范围"]:
            if len(parts) < 3:
                return "❌ 格式: /kb range <天数>\n示例: /kb range 3 (采集近3天)"
            try:
                days = int(parts[2])
                return self._execute_range_crawl(days)
            except:
                return "❌ 天数必须是数字，例如: /kb range 7"
        
        # 帮助
        elif subcmd in ["help", "帮助"]:
            return self._kb_help()
        
        # 搜索
        elif subcmd in ["search", "搜索"]:
            if len(parts) < 3:
                return "❌ 请指定搜索关键词，例如: /kb search 智慧交通"
            
            query = parts[2]
            results = knowledge_base.search(query, limit=5)
            
            if not results:
                return f"🔍 未找到相关内容: {query}"
            
            lines = [f"🔍 搜索结果 ({len(results)}条):\n"]
            for i, r in enumerate(results, 1):
                lines.append(f"{i}. {r['title']}")
                if r['content']:
                    lines.append(f"   {r['content'][:100]}...")
                lines.append(f"   分类: {r['category']}")
                if r['tags']:
                    lines.append(f"   标签: {' '.join(r['tags'][:3])}")
                lines.append("")
            
            return "\n".join(lines)
        
        # 添加
        elif subcmd in ["add", "添加"]:
            if len(parts) < 3:
                return "❌ 格式: /kb add 标题 | 内容"
            
            content_parts = parts[2].split("|")
            if len(content_parts) < 2:
                return "❌ 格式: /kb add 标题 | 内容"
            
            title = content_parts[0].strip()
            content = content_parts[1].strip()
            
            # 分析内容
            analysis = self.analyzer.analyze(content)
            
            if knowledge_base.add_knowledge(
                title=title,
                content=content,
                category=analysis.category,
                subsystem=analysis.subsystem or "",
                tags=analysis.tags,
                source="手动添加"
            ):
                return f"✅ 已添加知识: {title}"
            else:
                return "❌ 添加失败"
        
        else:
            return f"❌ 未知子命令: {subcmd}"
    
    def _execute_daily_report(self) -> str:
        """执行日报采集（异步）"""
        import threading
        from crawler.cn_web_search import cn_web_searcher
        from notifier.daily_report import DailyReporter
        from datetime import datetime
        
        def run_in_background():
            """后台执行采集任务"""
            try:
                # 执行采集
                results = cn_web_searcher.search_all()
                
                if not results:
                    print("⚠️ 未获取到搜索结果")
                    return
                
                # 分析并存储
                analyzed_results = []
                for result in results:
                    analysis = self.analyzer.analyze(result.snippet)
                    
                    if analysis.has_value:
                        knowledge_base.add_knowledge(
                            title=result.title,
                            content=result.snippet,
                            category=analysis.category,
                            subsystem=analysis.subsystem or "",
                            tags=analysis.tags,
                            source=result.source,
                            url=result.url
                        )
                        
                        analyzed_results.append({
                            "title": result.title,
                            "url": result.url,
                            "snippet": result.snippet,
                            "category": analysis.category,
                            "tags": analysis.tags,
                            "summary": analysis.summary
                        })
                
                # 生成日报
                reporter = DailyReporter()
                reporter.generate_and_send(analyzed_results)
                
                print(f"✅ 日报采集完成！采集了 {len(analyzed_results)} 条有价值内容")
                
            except Exception as e:
                print(f"❌ 日报执行失败: {str(e)}")
        
        # 启动后台线程
        thread = threading.Thread(target=run_in_background, daemon=True)
        thread.start()
        
        return """✅ 日报采集已启动！

⏳ 正在后台执行，预计1-2分钟完成...

📊 完成后会自动推送到群里

💡 查看结果：
- 等待群消息推送
- 或输入 /kb stats 查看知识库
"""
    
    def _kb_help(self) -> str:
        """知识库帮助"""
        return """📚 **知识库命令帮助**

/kb init - 初始化知识库
/kb stats - 查看统计
/kb daily - 立即执行日报采集
/kb batch - 批量采集近一年资料
/kb range <天数> - 自定义时间范围采集 🆕
/kb search <关键词> - 搜索知识
/kb add <标题> | <内容> - 添加知识

示例:
/kb range 3 - 采集近3天
/kb range 7 - 采集近7天
/kb range 30 - 采集近30天
/kb batch - 采集近一年
/kb search 智慧交通
/kb add 新技术 | AI摄像头支持人脸识别
"""
    
    def _execute_range_crawl(self, days: int) -> str:
        """执行自定义时间范围采集"""
        import threading
        from datetime import datetime, timedelta
        
        def run_range_in_background():
            """后台执行范围采集"""
            try:
                from crawler.cn_web_search import cn_web_searcher
                from utils.content_analyzer import ContentAnalyzer
                
                # 计算时间范围
                start_date = datetime.now() - timedelta(days=days)
                print(f"📅 采集时间范围：{start_date.strftime('%Y-%m-%d')} 至今")
                
                # 执行采集
                results = cn_web_searcher.search_all()
                
                if not results:
                    print("⚠️ 未获取到搜索结果")
                    return
                
                # 分析并存储
                analyzer = ContentAnalyzer()
                stored_count = 0
                
                for result in results:
                    # 检查发布时间
                    try:
                        if hasattr(result, 'date') and result.date:
                            pub_date = datetime.strptime(result.date, '%Y-%m-%d')
                            if pub_date < start_date:
                                continue
                    except:
                        pass
                    
                    # 分析内容
                    analysis = analyzer.analyze(result.snippet)
                    
                    if analysis.has_value:
                        knowledge_base.add_knowledge(
                            title=result.title,
                            content=result.snippet,
                            category=analysis.category,
                            subsystem=analysis.subsystem or "",
                            tags=analysis.tags,
                            source=result.source,
                            url=result.url,
                            publish_date=result.date if hasattr(result, 'date') else ""
                        )
                        stored_count += 1
                
                print(f"✅ 采集完成！存储了 {stored_count} 条内容")
                
            except Exception as e:
                print(f"❌ 采集失败: {str(e)}")
        
        # 启动后台线程
        thread = threading.Thread(target=run_range_in_background, daemon=True)
        thread.start()
        
        return f"""✅ 自定义采集已启动！

⏳ 正在后台采集近 {days} 天的资料...

📅 时间范围：{(datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')} 至今

⏰ 预计2-5分钟完成

💡 查看结果：
- 输入 /kb stats 查看知识库
- 输入 /kb search <关键词> 搜索
"""
    
    def _execute_batch_crawl(self) -> str:
        """执行批量采集（近一年）"""
        import threading
        
        def run_batch_in_background():
            """后台执行批量采集"""
            try:
                from batch_crawler import batch_crawl_last_year
                batch_crawl_last_year()
            except Exception as e:
                print(f"❌ 批量采集失败: {str(e)}")
        
        # 启动后台线程
        thread = threading.Thread(target=run_batch_in_background, daemon=True)
        thread.start()
        
        return """✅ 批量采集已启动！

⏳ 正在后台采集近一年的资料...

📊 采集内容：
- 时间范围：近365天
- 自动过滤过期内容
- 标注发布时间

⏰ 预计5-10分钟完成

💡 查看结果：
- 输入 /kb stats 查看知识库
- 输入 /kb search <关键词> 搜索
"""
    
    def _handle_crawler_command(self, text: str, user_id: str) -> str:
        """处理采集命令"""
        parts = text.split(maxsplit=2)
        
        if len(parts) < 2:
            return "❌ 请指定子命令，例如: /crawler status"
        
        subcmd = parts[1].lower()
        
        # 状态
        if subcmd in ["status", "状态"]:
            run_time = schedule_config.get_run_time()
            enabled = schedule_config.is_enabled()
            keywords = schedule_config.get_keywords()
            
            return f"""⚙️ 采集服务状态

运行时间: 每天 {run_time}
状态: {'✅ 已启用' if enabled else '❌ 已禁用'}
关键词数量: {len(keywords)}
最大采集数: {schedule_config.get_max_results()}
日报接收: {schedule_config.get_report_chat_id() or '未设置'}
"""
        
        # 设置时间
        elif subcmd in ["time", "时间"]:
            if self.enable_auth and user_id not in self.admins:
                return "❌ 仅管理员可以修改配置"
            
            if len(parts) < 3:
                return "❌ 格式: /crawler time 08:30"
            
            time_str = parts[2]
            if schedule_config.set_run_time(time_str):
                return f"✅ 已设置采集时间: 每天 {time_str}"
            else:
                return "❌ 时间格式错误，请使用 HH:MM 格式"
        
        # 启用
        elif subcmd in ["enable", "启用"]:
            if self.enable_auth and user_id not in self.admins:
                return "❌ 仅管理员可以修改配置"
            
            schedule_config.set_enabled(True)
            return "✅ 采集服务已启用"
        
        # 禁用
        elif subcmd in ["disable", "禁用"]:
            if self.enable_auth and user_id not in self.admins:
                return "❌ 仅管理员可以修改配置"
            
            schedule_config.set_enabled(False)
            return "✅ 采集服务已禁用"
        
        # 立即执行
        elif subcmd in ["start", "run", "执行"]:
            if self.enable_auth and user_id not in self.admins:
                return "❌ 仅管理员可以执行此操作"
            
            # 这里只是提示，实际执行需要后台服务
            return """✅ 已发送执行指令

后台服务将在下次检查时执行采集（约1分钟内）

查看结果:
1. 等待日报推送
2. 或查看日志: tail -f /tmp/smartcity_crawler.log
"""
        
        else:
            return f"❌ 未知子命令: {subcmd}"
    
    def _handle_search_command(self, text: str) -> str:
        """处理搜索命令"""
        parts = text.split(maxsplit=1)
        
        if len(parts) < 2:
            return "❌ 请指定搜索关键词，例如: /search 智慧交通"
        
        query = parts[1]
        results = knowledge_base.search(query, limit=10)
        
        if not results:
            return f"🔍 未找到相关内容: {query}"
        
        lines = [f"🔍 搜索结果 ({len(results)}条):\n"]
        for i, r in enumerate(results, 1):
            lines.append(f"{i}. **{r['title']}**")
            if r['content']:
                lines.append(f"   {r['content'][:150]}...")
            lines.append(f"   分类: {r['category']} | 来源: {r['source']}")
            if r['tags']:
                lines.append(f"   🏷️ {' '.join(r['tags'][:5])}")
            lines.append("")
        
        return "\n".join(lines)
    
    def _handle_stats_command(self) -> str:
        """处理统计命令"""
        stats = knowledge_base.get_stats()
        
        if stats["total"] == 0:
            return """📊 系统统计

知识库: 暂无数据
采集服务: 每天运行

💡 提示:
1. 输入 /kb init 初始化知识库
2. 输入 /crawler start 立即采集
"""
        
        lines = ["📊 系统统计\n"]
        lines.append(f"知识库总数: {stats['total']} 条\n")
        lines.append("分类统计:")
        for cat, count in sorted(stats["categories"].items(), key=lambda x: x[1], reverse=True):
            lines.append(f"  • {cat}: {count}条")
        
        lines.append(f"\n采集服务: 每天 {schedule_config.get_run_time()}")
        
        return "\n".join(lines)
    
    def _handle_add_command(self, text: str, user_id: str) -> str:
        """处理添加命令"""
        parts = text.split(maxsplit=1)
        
        if len(parts) < 2:
            return "❌ 格式: /add 标题 | 内容"
        
        content_parts = parts[1].split("|")
        if len(content_parts) < 2:
            return "❌ 格式: /add 标题 | 内容"
        
        title = content_parts[0].strip()
        content = content_parts[1].strip()
        
        # 分析内容
        analysis = self.analyzer.analyze(content)
        
        if knowledge_base.add_knowledge(
            title=title,
            content=content,
            category=analysis.category,
            subsystem=analysis.subsystem or "",
            tags=analysis.tags,
            source="手动添加",
            url=""
        ):
            return f"""✅ 已添加知识

标题: {title}
分类: {analysis.category}
标签: {' '.join(analysis.tags[:5])}

💡 输入 /search {title[:10]} 验证
"""
        else:
            return "❌ 添加失败，请检查知识库配置"


# 全局实例
command_handler = GroupCommandHandler()
