#!/bin/bash

# 设置环境变量
VENV_NAME="aider_env"
PORT=23947

# 打印彩色输出的函数
print_info() {
    echo -e "\033[1;34m[INFO]\033[0m $1"
}

print_success() {
    echo -e "\033[1;32m[SUCCESS]\033[0m $1"
}

print_error() {
    echo -e "\033[1;31m[ERROR]\033[0m $1"
}

# 检查Python3是否安装
if ! command -v python3 &> /dev/null; then
    print_error "Python3未找到，请先安装Python3"
    exit 1
fi

# 创建虚拟环境（如果不存在）
if [ ! -d "$VENV_NAME" ]; then
    print_info "创建虚拟环境: $VENV_NAME"
    python3 -m venv "$VENV_NAME"
    if [ $? -ne 0 ]; then
        print_error "创建虚拟环境失败"
        exit 1
    fi
else
    print_info "使用已存在的虚拟环境: $VENV_NAME"
fi

# 激活虚拟环境
print_info "激活虚拟环境"
source "$VENV_NAME/bin/activate"
if [ $? -ne 0 ]; then
    print_error "激活虚拟环境失败"
    exit 1
fi

# 检查是否已安装依赖
if [ ! -f "$VENV_NAME/lib/python3.*/site-packages/fastapi/__init__.py" ]; then
    print_info "安装API依赖"
    pip install -r requirements/requirements-api.txt
    if [ $? -ne 0 ]; then
        print_error "安装依赖失败"
        exit 1
    fi
fi

# 启动FastAPI服务
print_info "启动Aider API服务，端口: $PORT"
python3 -m aider.fastapi --port $PORT

# 如果服务结束，退出虚拟环境
deactivate

print_success "服务已关闭，已退出虚拟环境" 