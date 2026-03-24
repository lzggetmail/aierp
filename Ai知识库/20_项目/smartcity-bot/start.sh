#!/bin/bash
export FEISHU_APP_ID=cli_a9284311cd785cc7
export FEISHU_APP_SECRET=EbmPJXvUitNLGqdN37iUEg2fcOKn8oHA
export GLM_API_KEY=04e29f652a3a475f8d30532fb53853ef.0wglUj4b3rdHbnZt
export REPORT_CHAT_ID=oc_6272f02a3d023d6146fc4b6971bda455
export FEISHU_BITABLE_TOKEN=TPlmbOupGaN5Qtsb1plcfeoonDd
export FEISHU_TABLE_ID=tblqfaWzwt5IRDRT

cd /root/.openclaw/workspace/projects/smartcity-bot
nohup python3 main.py > logs/bot.log 2>&1 &
echo $! > logs/bot.pid
echo "机器人已启动，PID: $(cat logs/bot.pid)"
