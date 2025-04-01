#!/bin/bash

# 进入网站目录
cd aider/website_cn

# 检查是否安装了Ruby和Bundle
if ! command -v ruby &> /dev/null; then
    echo "Ruby未安装，请先安装Ruby"
    exit 1
fi

if ! command -v bundle &> /dev/null; then
    echo "Bundler未安装，尝试安装中..."
    gem install bundler
fi

# 安装依赖
echo "安装Jekyll和依赖..."
bundle install

# 启动本地服务器
echo "启动website_cn服务器，网站将在http://localhost:23952可访问"
bundle exec jekyll serve --host 0.0.0.0 --port 23952

# 如果出错，提供一些建议
if [ $? -ne 0 ]; then
    echo "启动失败。可能的解决方案："
    echo "1. 确保Ruby版本 >= 2.5.0"
    echo "2. 尝试执行: bundle update"
    echo "3. 如果是权限问题，尝试: sudo bundle exec jekyll serve --host 0.0.0.0"
fi 