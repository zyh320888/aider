#!/bin/bash

# 设置工作目录
WORK_DIR="/docker/codeserver/project/test/aider"
cd $WORK_DIR

# 设置环境变量
export AIDER_LOG_LEVEL="INFO"

# 设置LD_LIBRARY_PATH
# 这将帮助可执行文件找到Python共享库
export LD_LIBRARY_PATH="/usr/lib:$LD_LIBRARY_PATH"

# 启动服务
./dist/aider-api --port 8000 