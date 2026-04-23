#!/bin/bash
# 智慧城市采集 - 停止服务

echo "🛑 停止智慧城市采集服务..."

if [ -f /tmp/smartcity_crawler.pid ]; then
    pid=$(cat /tmp/smartcity_crawler.pid)
    if ps -p $pid > /dev/null 2>&1; then
        kill $pid
        echo "✅ 服务已停止 (PID: $pid)"
    else
        echo "⚠️ 进程不存在"
    fi
    rm -f /tmp/smartcity_crawler.pid
else
    echo "⚠️ 未找到运行中的服务"
fi
