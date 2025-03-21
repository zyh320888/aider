#!/bin/bash

# 设置环境变量
VENV_NAME="aider_env"

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

# 安装核心依赖
print_info "安装Aider核心依赖"
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    print_error "安装核心依赖失败"
    exit 1
fi

# 安装API依赖
print_info "安装API依赖"
pip install -r requirements/requirements-api.txt
if [ $? -ne 0 ]; then
    print_error "安装API依赖失败"
    exit 1
fi

print_success "环境设置完成，依赖安装成功"
print_info "您可以通过执行 'source $VENV_NAME/bin/activate' 手动激活此环境"

# 保持虚拟环境处于激活状态
print_info "虚拟环境已激活并可以使用" 