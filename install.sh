#!/data/data/com.termux/files/usr/bin/bash

echo "==== Termux 一键部署骰子BOT脚本 ===="

# 1. 更新包管理器
echo "1. 更新包管理器..."
pkg update -y && pkg upgrade -y

# 2. 安装Python3、git、clang及matplotlib依赖
echo "2. 安装Python3、git、clang及matplotlib依赖..."
pkg install -y python git clang freetype libpng libjpeg-turbo
pkg install -y python-pip

# 3. 克隆/更新项目源码
REPO_URL="https://github.com/xiaodu11129/dicebot.git"
DIR_NAME="dicebot"

echo "3. 克隆/更新项目源码..."
if [ -d "$DIR_NAME" ]; then
    cd "$DIR_NAME"
    git pull
else
    git clone "$REPO_URL"
    cd "$DIR_NAME"
fi

# 4. 安装Python依赖（不升级pip）
echo "4. 安装Python依赖..."
pip install --no-cache-dir -r requirements.txt

echo "==== 部署完成！===="
echo "你可以根据 README.md 进一步操作。"
