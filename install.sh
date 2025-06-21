#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "==== Termux 一键部署骰子BOT脚本 ===="
echo "1. 更新包管理器..."
pkg update -y && pkg upgrade -y

echo "2. 安装Python3、git、clang及matplotlib依赖..."
pkg install python git clang -y
pkg install libjpeg-turbo freetype libpng -y

echo "3. 克隆/更新项目源码..."
REPO_URL="https://github.com/xiaodu11129/dicebot.git
"
DIR_NAME="dicebot"

if [ -d "$DIR_NAME" ]; then
    echo "已有$DIR_NAME目录，尝试更新..."
    cd "$DIR_NAME"
    git pull
else
    git clone "$REPO_URL"
    cd "$DIR_NAME"
fi

echo "4. 升级pip并安装Python依赖..."
pip install --upgrade pip
pip install -r requirements.txt

echo "5. 初始化数据库及超级管理员..."
python migrate.py || { echo "数据库初始化失败"; exit 1; }
python init_admin.py || { echo "管理员初始化失败"; exit 1; }

echo "6. 部署完成！"
echo "请手动编辑 config.py 填写你的Telegram Bot Token和管理员ID等信息。"
echo "启动机器人: python bot.py"
echo "启动WEB后台: python admin_web.py"
