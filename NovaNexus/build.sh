#!/bin/bash
# ForgeMind AI - Build and Deploy Script (Unix/Linux/Mac)

set -e  # Exit on first error

echo "=================================="
echo "ForgeMind AI - Build & Deploy"
echo "=================================="

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$PROJECT_ROOT/backend"
FRONTEND_DIR="$PROJECT_ROOT/frontend"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓ $2${NC}"
    else
        echo -e "${RED}✗ $2${NC}"
        exit 1
    fi
}

print_section() {
    echo -e "\n${YELLOW}>>> $1${NC}"
}

# Main build command
case "${1:-all}" in
    "verify")
        print_section "Verifying Deployment"
        cd "$BACKEND_DIR"
        python3 verify_deployment.py
        print_status $? "Verification passed"
        ;;
    
    "build-frontend")
        print_section "Building Frontend"
        cd "$FRONTEND_DIR"
        npm install
        print_status $? "npm install"
        npm run build
        print_status $? "Frontend build"
        ;;
    
    "build-backend")
        print_section "Installing Backend Dependencies"
        cd "$BACKEND_DIR"
        pip install -r requirements.txt
        print_status $? "Backend dependencies"
        ;;
    
    "build-all"|"all")
        print_section "Building Frontend"
        cd "$FRONTEND_DIR"
        npm install
        print_status $? "npm install"
        npm run build
        print_status $? "Frontend build"
        
        print_section "Installing Backend Dependencies"
        cd "$BACKEND_DIR"
        pip install -r requirements.txt
        print_status $? "Backend dependencies"
        
        print_section "Verifying Deployment"
        python3 verify_deployment.py
        print_status $? "Verification"
        
        echo -e "\n${GREEN}=================================="
        echo "✓ BUILD COMPLETE"
        echo "Ready for deployment!"
        echo "==================================${NC}"
        ;;
    
    *)
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  verify         - Verify deployment readiness"
        echo "  build-frontend - Build React frontend"
        echo "  build-backend  - Install backend dependencies"
        echo "  build-all      - Build complete project (default)"
        exit 1
        ;;
esac
