#!/bin/bash
# 智慧城市采集 - 后台启动脚本

cd /root/.openclaw/workspace/projects/smartcity-bot

echo "🚀 启动智慧城市采集服务..."

# 检查是否已经在运行
if [ -f /tmp/smartcity_crawler.pid ]; then
    pid=$(cat /tmp/smartcity_crawler.pid)
    if ps -p $pid > /dev/null 2>&1; then
        echo "⚠️ 服务已在运行 (PID: $pid)"
        echo "如需重启，请先运行: ./stop_crawler.sh"
        exit 1
    fi
fi

# 后台启动
nohup python3 run_crawler_daemon.py > /tmp/smartcity_crawler.log 2>&1 &
pid=$!

# 保存PID
echo $pid > /tmp/smartcity_crawler.pid

echo "✅ 服务已启动 (PID: $pid)"
echo "📝 日志文件: /tmp/smartcity_crawler.log"
echo ""
echo "管理命令:"
echo "  查看状态: ./status_crawler.sh"
echo "  查看日志: tail -f /tmp/smartcity_crawler.log"
echo "  停止服务: ./stop_crawler.sh"
