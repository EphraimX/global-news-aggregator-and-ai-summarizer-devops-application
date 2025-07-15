#!/bin/bash

# 🚀 Deployment Script for Global News Digest AI
echo "🚀 Deploying Global News Digest AI"
echo "=================================="

# Configuration
BACKEND_DIR="backend"
FRONTEND_DIR="frontend"
DOCKER_IMAGE="global-news-digest-backend"
DOCKER_TAG="latest"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed"
        exit 1
    fi
    
    if ! command -v node &> /dev/null; then
        log_error "Node.js is not installed"
        exit 1
    fi
    
    if ! command -v npm &> /dev/null; then
        log_error "npm is not installed"
        exit 1
    fi
    
    log_info "Prerequisites check passed"
}

# Deploy backend
deploy_backend() {
    log_info "Deploying backend..."
    
    cd $BACKEND_DIR
    
    # Build Docker image
    log_info "Building Docker image..."
    docker build -t $DOCKER_IMAGE:$DOCKER_TAG .
    
    if [ $? -ne 0 ]; then
        log_error "Docker build failed"
        exit 1
    fi
    
    # Stop existing container
    log_info "Stopping existing container..."
    docker stop global-news-backend 2>/dev/null || true
    docker rm global-news-backend 2>/dev/null || true
    
    # Run new container
    log_info "Starting new container..."
    docker run -d \
        --name global-news-backend \
        --restart unless-stopped \
        -p 8000:8000 \
        --env-file .env \
        $DOCKER_IMAGE:$DOCKER_TAG
    
    if [ $? -ne 0 ]; then
        log_error "Failed to start backend container"
        exit 1
    fi
    
    # Wait for backend to be ready
    log_info "Waiting for backend to be ready..."
    for i in {1..30}; do
        if curl -s http://localhost:8000/health > /dev/null; then
            log_info "Backend is ready"
            break
        fi
        sleep 2
    done
    
    cd ..
}

# Deploy frontend
deploy_frontend() {
    log_info "Deploying frontend..."
    
    cd $FRONTEND_DIR
    
    # Install dependencies
    log_info "Installing dependencies..."
    npm ci
    
    # Build application
    log_info "Building application..."
    npm run build
    
    if [ $? -ne 0 ]; then
        log_error "Frontend build failed"
        exit 1
    fi
    
    # Deploy to Vercel (if vercel CLI is available)
    if command -v vercel &> /dev/null; then
        log_info "Deploying to Vercel..."
        vercel --prod
    else
        log_warn "Vercel CLI not found. Please deploy manually or install Vercel CLI"
        log_info "Build files are ready in .next directory"
    fi
    
    cd ..
}

# Health check
health_check() {
    log_info "Performing health check..."
    
    # Check backend
    if curl -s http://localhost:8000/health | grep -q "healthy"; then
        log_info "Backend health check passed"
    else
        log_error "Backend health check failed"
        return 1
    fi
    
    # Check if frontend build exists
    if [ -d "$FRONTEND_DIR/.next" ]; then
        log_info "Frontend build check passed"
    else
        log_error "Frontend build not found"
        return 1
    fi
    
    return 0
}

# Main deployment process
main() {
    log_info "Starting deployment process..."
    
    check_prerequisites
    deploy_backend
    deploy_frontend
    
    if health_check; then
        log_info "🎉 Deployment completed successfully!"
        log_info "Backend: http://localhost:8000"
        log_info "API Docs: http://localhost:8000/docs"
        log_info "Frontend: Check Vercel deployment URL"
    else
        log_error "Deployment completed with errors"
        exit 1
    fi
}

# Handle script arguments
case "$1" in
    backend)
        check_prerequisites
        deploy_backend
        ;;
    frontend)
        check_prerequisites
        deploy_frontend
        ;;
    health)
        health_check
        ;;
    *)
        main
        ;;
esac
