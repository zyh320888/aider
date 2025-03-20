#!/bin/bash

# 激活虚拟环境（如果有的话）
# source aider_env/bin/activate

# 设置工作目录
WORK_DIR="/docker/codeserver/project/test/aider"
cd $WORK_DIR

# 清理之前的构建文件
rm -rf build/ dist/

# 使用PyInstaller打包
# --onefile：创建单个可执行文件
# --add-binary：添加额外的二进制文件
# --hidden-import：添加隐藏的导入模块
# --collect-all：收集所有相关模块
pyinstaller --onefile \
  --add-data "aider/:aider/" \
  --hidden-import=fastapi \
  --hidden-import=uvicorn \
  --hidden-import=pydantic \
  --hidden-import=loguru \
  --hidden-import=aider.coders \
  --hidden-import=aider.coders.architect_coder \
  --hidden-import=aider.coders.ask_coder \
  --hidden-import=aider.coders.base_coder \
  --hidden-import=aider.models \
  --hidden-import=aider.prompts \
  --hidden-import=aider.urls \
  --hidden-import=aider.utils \
  --collect-all=aider \
  --collect-all=fastapi \
  --collect-all=uvicorn \
  --collect-all=pydantic \
  --collect-all=loguru \
  --runtime-tmpdir . \
  aider/fastapi.py \
  --name aider-api

echo "打包完成，可执行文件位于: dist/aider-api" 