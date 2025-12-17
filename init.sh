#!/bin/bash

# 初始化脚本 - 检查并同步项目依赖
# 此脚本将检测Python、uv、pm依赖，并同步项目依赖

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 检查Python是否安装
check_python() {
    log_info "检查Python安装情况..."
    
    if command_exists python3; then
        PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
        log_info "Python已安装: $PYTHON_VERSION"
        return 0
    fi
    
    if command_exists python; then
        PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
        log_info "Python已安装: $PYTHON_VERSION"
        return 0
    fi
    
    log_error "Python未安装，请先安装Python"
    return 1
}

# 检查uv是否安装
check_uv() {
    log_info "检查uv安装情况..."
    
    if command_exists uv; then
        UV_VERSION=$(uv --version)
        log_info "uv已安装: $UV_VERSION"
        return 0
    fi
    
    log_error "uv未安装，请先安装uv"
    return 1
}

# 使用uv同步依赖
sync_dependencies() {
    log_info "使用uv同步项目依赖..."
    
    if ! command_exists uv; then
        log_error "uv未安装，无法同步依赖"
        return 1
    fi
    
    # 检查是否存在uv.lock文件
    if [ ! -f "uv.lock" ]; then
        log_error "未找到uv.lock文件"
        return 1
    fi
    
    uv sync
    if [ $? -ne 0 ]; then
        log_error "依赖同步失败"
        return 1
    fi
    
    log_info "依赖同步成功"
    return 0
}

# 检查包管理器是否安装
check_pm() {
    log_info "检查包管理器安装情况..."
    
    # 检查npm
    if command_exists npm; then
        NPM_VERSION=$(npm --version)
        log_info "npm已安装: $NPM_VERSION"
        return 0
    fi
    
    # 检查yarn
    if command_exists yarn; then
        YARN_VERSION=$(yarn --version)
        log_info "yarn已安装: $YARN_VERSION"
        return 0
    fi
    
    # 检查pnpm
    if command_exists pnpm; then
        PNPM_VERSION=$(pnpm --version)
        log_info "pnpm已安装: $PNPM_VERSION"
        return 0
    fi
    
    log_error "未找到npm、yarn或pnpm，请先安装其中一种包管理器"
    return 1
}

# 在src/web目录下执行npm install
install_web_dependencies() {
    log_info "检查web项目依赖..."
    
    if [ ! -d "src/web" ]; then
        log_error "src/web目录不存在"
        return 1
    fi
    
    if [ ! -f "src/web/package.json" ]; then
        log_error "src/web/package.json不存在"
        return 1
    fi
    
    log_info "进入src/web目录并安装依赖..."
    
    # 进入src/web目录
    cd src/web
    
    # 检查使用哪个包管理器
    if [ -f "yarn.lock" ] && command_exists yarn; then
        log_info "检测到yarn.lock，使用yarn安装依赖..."
        yarn install
    elif [ -f "pnpm-lock.yaml" ] && command_exists pnpm; then
        log_info "检测到pnpm-lock.yaml，使用pnpm安装依赖..."
        pnpm install
    elif command_exists npm; then
        log_info "使用npm安装依赖..."
        npm install
    else
        log_error "没有可用的包管理器(npm/yarn/pnpm)"
        cd - > /dev/null
        return 1
    fi
    
    # 检查安装结果
    if [ $? -eq 0 ]; then
        log_info "web项目依赖安装成功"
        cd - > /dev/null
        return 0
    else
        log_error "web项目依赖安装失败"
        cd - > /dev/null
        return 1
    fi
}

# 主函数
main() {
    log_info "开始初始化项目环境..."
    
    # 1. 检查Python是否安装
    check_python
    if [ $? -ne 0 ]; then
        log_error "Python未安装，初始化中止"
        exit 1
    fi
    
    # 2. 检查uv是否安装
    check_uv
    if [ $? -ne 0 ]; then
        log_error "uv未安装，初始化中止"
        exit 1
    fi
    
    # 3. 使用uv同步依赖
    sync_dependencies
    if [ $? -ne 0 ]; then
        log_error "依赖同步失败，初始化中止"
        exit 1
    fi
    
    # 4. 检查包管理器
    check_pm
    if [ $? -ne 0 ]; then
        log_error "包管理器未安装，初始化中止"
        exit 1
    fi
    
    # 5. 安装web项目依赖
    install_web_dependencies
    if [ $? -ne 0 ]; then
        log_error "web项目依赖安装失败，初始化中止"
        exit 1
    fi
    
    log_info "项目环境初始化完成！"
}

# 执行主函数
main