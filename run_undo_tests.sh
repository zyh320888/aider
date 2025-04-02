#!/bin/bash

# 设置颜色输出函数
print_info() {
    echo -e "\033[1;34m[INFO]\033[0m $1"
}

print_success() {
    echo -e "\033[1;32m[SUCCESS]\033[0m $1"
}

print_error() {
    echo -e "\033[1;31m[ERROR]\033[0m $1"
}

# 设置环境变量
VENV_NAME="aider_env"
TEST_FILE="tests/browser/test_fastapi_undo.py"
TEST_METHOD=""
LOG_FILE="undo_test.log"

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --method=*)
            TEST_METHOD="${1#*=}"
            shift
            ;;
        --debug)
            DEBUG=1
            shift
            ;;
        --log=*)
            LOG_FILE="${1#*=}"
            shift
            ;;
        *)
            print_error "未知参数: $1"
            echo "用法: $0 [--method=测试方法名] [--debug] [--log=日志文件路径]"
            exit 1
            ;;
    esac
done

# 输出运行信息
print_info "将日志输出到文件: $LOG_FILE"
print_info "清空之前的日志文件"
> "$LOG_FILE"

# 检查环境
if [ ! -d "$VENV_NAME" ]; then
    print_error "找不到虚拟环境: $VENV_NAME, 请先运行 setup_aider_env.sh"
    exit 1
fi

# 激活虚拟环境
print_info "激活虚拟环境"
source "$VENV_NAME/bin/activate"
if [ $? -ne 0 ]; then
    print_error "激活虚拟环境失败"
    exit 1
fi

# 确保测试依赖已安装
print_info "检查测试依赖"
pip install pytest fastapi[all] httpx 2>&1 > /dev/null

# 检查测试文件是否存在
if [ ! -f "$TEST_FILE" ]; then
    print_error "测试文件不存在: $TEST_FILE"
    deactivate
    exit 1
fi

# 添加初步日志输出
echo "========== 开始执行撤销功能测试 $(date) ==========" >> "$LOG_FILE"

# 设置测试命令
TEST_CMD="pytest -xvs"
if [ ! -z "$TEST_METHOD" ]; then
    TEST_CMD="$TEST_CMD $TEST_FILE::TestFastAPIUndo::$TEST_METHOD"
    print_info "将只运行测试方法: $TEST_METHOD"
    echo "运行测试方法: $TEST_METHOD" >> "$LOG_FILE"
else
    TEST_CMD="$TEST_CMD $TEST_FILE"
    print_info "将运行所有撤销功能测试方法"
    echo "运行所有撤销功能测试方法" >> "$LOG_FILE"
fi

# 设置环境变量
if [ ! -z "$DEBUG" ]; then
    print_info "启用调试模式"
    export AIDER_LOG_LEVEL=DEBUG
    export PYTEST_LOG_LEVEL=DEBUG
    export PYTHONVERBOSE=1
    export FASTAPI_DEBUG=1
    echo "已开启调试模式" >> "$LOG_FILE"
fi

# 输出环境信息到日志
echo "Python版本: $(python --version 2>&1)" >> "$LOG_FILE"
echo "系统信息: $(uname -a)" >> "$LOG_FILE"
echo "工作目录: $(pwd)" >> "$LOG_FILE"
echo "测试命令: $TEST_CMD" >> "$LOG_FILE"
echo "===========================================\n" >> "$LOG_FILE"

# 运行测试
print_info "开始运行撤销功能测试..."
# 将输出重定向到日志文件和标准输出
$TEST_CMD 2>&1 | tee -a "$LOG_FILE" | grep -E "^(E|ERROR|FAILED)" --color=always
TEST_RESULT=${PIPESTATUS[0]}

# 添加完成日志标记
echo "\n========== 测试完成 $(date) ==========" >> "$LOG_FILE"

# 提取错误信息到单独的错误日志
ERROR_LOG="undo_error_summary.log"
grep -E "^(E|ERROR|FAILED|Exception|Error|Traceback)" "$LOG_FILE" > "$ERROR_LOG"
if [ -s "$ERROR_LOG" ]; then
    print_info "错误摘要已保存到 $ERROR_LOG"
    echo -e "\n关键错误信息:"
    cat "$ERROR_LOG" | head -n 20
    if [ $(wc -l < "$ERROR_LOG") -gt 20 ]; then
        echo "... 更多错误信息请查看 $ERROR_LOG ..."
    fi
fi

# 输出测试结果
if [ $TEST_RESULT -eq 0 ]; then
    print_success "所有测试通过! FastAPI撤销提交功能测试成功"
else
    print_error "测试失败，完整日志请查看 $LOG_FILE"
fi

# 退出虚拟环境
deactivate
print_info "已退出虚拟环境"

exit $TEST_RESULT 