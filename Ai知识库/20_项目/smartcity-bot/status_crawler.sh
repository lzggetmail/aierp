#!/bin/bash
# 智慧城市采集 - 查看状态

echo "📊 智慧城市采集服务状态"
echo "============================"

if [ -f /tmp/smartcity_crawler.pid ]; then
    pid=$(cat /tmp/smartcity_crawler.pid)
    if ps -p $pid > /dev/null 2>&1; then
        echo "状态: ✅ 运行中"
        echo "PID: $pid"
        echo ""
        echo "进程信息:"
        ps -p $pid -o pid,ppid,cmd,%mem,%cpu,etime
        echo ""
        echo "最近日志:"
        tail -20 /tmp/smartcity_crawler.log
    else
        echo "状态: ❌ 已停止 (进程不存在)"
        rm -f /tmp/smartcity_crawler.pid
    fi
else
    echo "状态: ❌ 未运行"
    echo ""
    echo "启动服务: ./start_crawler.sh"
fi
