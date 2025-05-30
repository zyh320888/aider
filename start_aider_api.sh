#!/bin/bash

# 设置环境变量
VENV_NAME="aider_env"
PORT=23948
WORK_DIR="." # 默认为当前目录
CONFIG_FILE=""
MODEL_METADATA_FILE=""
MODEL_SETTINGS_FILE=""

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

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -d|--dir)
            WORK_DIR="$2"
            shift 2
            ;;
        -p|--port)
            PORT="$2"
            shift 2
            ;;
        -c|--config)
            if [[ -n "$2" && ! "$2" =~ ^- ]]; then
                CONFIG_FILE="$2"
                shift 2
            else
                print_error "配置文件参数缺少值"
                exit 1
            fi
            ;;
        --model-metadata-file)
            if [[ -n "$2" && ! "$2" =~ ^- ]]; then
                MODEL_METADATA_FILE="$2"
                shift 2
            else
                print_error "模型元数据文件参数缺少值"
                exit 1
            fi
            ;;
        --model-settings-file)
            if [[ -n "$2" && ! "$2" =~ ^- ]]; then
                MODEL_SETTINGS_FILE="$2"
                shift 2
            else
                print_error "模型设置文件参数缺少值"
                exit 1
            fi
            ;;
        *)
            print_error "未知参数: $1"
            echo "用法: $0 [-d|--dir 工作目录] [-p|--port 端口号] [-c|--config 配置文件] [--model-metadata-file 模型元数据文件] [--model-settings-file 模型设置文件]"
            exit 1
            ;;
    esac
done

# 显示配置信息
print_info "工作目录: $WORK_DIR"
print_info "端口: $PORT"
if [ -n "$CONFIG_FILE" ]; then
    print_info "配置文件: $CONFIG_FILE"
fi
if [ -n "$MODEL_METADATA_FILE" ]; then
    print_info "模型元数据文件: $MODEL_METADATA_FILE"
fi
if [ -n "$MODEL_SETTINGS_FILE" ]; then
    print_info "模型设置文件: $MODEL_SETTINGS_FILE"
fi

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

# # 检查是否已安装核心依赖
# if ! pip freeze | grep -q "^json5=="; then
#     print_info "安装Aider核心依赖"
#     pip install -r requirements.txt
#     if [ $? -ne 0 ]; then
#         print_error "安装核心依赖失败"
#         exit 1
#     fi
# fi

# # 检查是否已安装API依赖
# if ! pip freeze | grep -q "^fastapi=="; then
#     print_info "安装API依赖"
#     pip install -r requirements/requirements-api.txt
#     if [ $? -ne 0 ]; then
#         print_error "安装API依赖失败"
#         exit 1
#     fi
# fi

# 构建Python命令行参数
PYTHON_ARGS="--port $PORT"

# 添加配置文件参数
if [ -n "$CONFIG_FILE" ]; then
    PYTHON_ARGS+=" --config $CONFIG_FILE"
    print_info "使用配置文件: $CONFIG_FILE"
fi

# 添加模型元数据文件参数
if [ -n "$MODEL_METADATA_FILE" ]; then
    PYTHON_ARGS+=" --model-metadata-file $MODEL_METADATA_FILE"
    print_info "使用模型元数据文件: $MODEL_METADATA_FILE"
fi

# 添加模型设置文件参数
if [ -n "$MODEL_SETTINGS_FILE" ]; then
    PYTHON_ARGS+=" --model-settings-file $MODEL_SETTINGS_FILE"
    print_info "使用模型设置文件: $MODEL_SETTINGS_FILE"
fi

# 启动FastAPI服务
print_info "启动Aider API服务，端口: $PORT，工作目录: $WORK_DIR"
cd "$WORK_DIR" && python3 -m aider.fastapi $PYTHON_ARGS

# 如果服务结束，退出虚拟环境
deactivate

print_success "服务已关闭，已退出虚拟环境" 