#!/bin/bash

# 开发服务器运行脚本
# 此脚本将同时启动后端(uvicorn)和前端(npm run dev)开发服务器

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_backend() {
    echo -e "${BLUE}[BACKEND]${NC} $1"
}

log_frontend() {
    echo -e "${YELLOW}[FRONTEND]${NC} $1"
}

# 添加缺失的log_warn函数
log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# 检查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 清理函数
cleanup() {
    log_info "正在停止所有服务..."
    
    # 杀死所有子进程
    jobs -p | xargs -r kill
    
    log_info "所有服务已停止"
    exit 0
}

# 设置信号处理 (移除可能不支持的信号)
trap cleanup INT TERM

# 激活虚拟环境
activate_venv() {
    if [ -f ".venv/bin/activate" ]; then
        log_info "激活Python虚拟环境..."
        # 修改source为.以提高兼容性
        . .venv/bin/activate
        return 0
    elif [ -f "venv/bin/activate" ]; then
        log_info "激活Python虚拟环境..."
        # 修改source为.以提高兼容性
        . venv/bin/activate
        return 0
    else
        log_warn "未找到虚拟环境，尝试使用系统Python环境..."
        return 1
    fi
}

# 检查必要命令
log_info "检查必要命令..."

# 激活虚拟环境
activate_venv

# 检查uvicorn是否在虚拟环境中可用
if ! python -c "import uvicorn" 2>/dev/null; then
    log_error "uvicorn未安装，请先安装uvicorn: pip install uvicorn"
    exit 1
fi

if ! command_exists npm; then
    log_error "npm未安装，请先安装npm"
    exit 1
fi

# 检查目录和文件
if [ ! -d "src/service" ]; then
    log_error "src/service目录不存在"
    exit 1
fi

if [ ! -f "src/service/main.py" ]; then
    log_error "src/service/main.py不存在"
    exit 1
fi

if [ ! -d "src/web" ]; then
    log_error "src/web目录不存在"
    exit 1
fi

if [ ! -f "src/web/package.json" ]; then
    log_error "src/web/package.json不存在"
    exit 1
fi

# 检查.env文件
if [ ! -f ".env" ]; then
    log_error ".env文件不存在，请先创建.env文件"
    exit 1
fi

log_info "开始启动开发服务器..."

# 启动后端服务器
log_backend "启动后端服务器..."
(
    cd src/service
    python -m uvicorn main:app --reload
) &
BACKEND_PID=$!

# 启动前端服务器
log_frontend "启动前端服务器..."
(
    cd src/web
    npm run start
) &
FRONTEND_PID=$!

log_info "开发服务器已启动"
log_info "后端PID: $BACKEND_PID"
log_info "前端PID: $FRONTEND_PID"
log_info "按 Ctrl+C 停止所有服务"

# 等待所有后台进程
wait