#!/usr/bin/env python3
"""
Build and deployment helper script for ForgeMind AI
"""

import os
import sys
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger()

def run_command(cmd, cwd=None):
    """Run a shell command"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=False)
        return result.returncode == 0
    except Exception as e:
        logger.error(f"Command failed: {e}")
        return False

def main():
    logger.info("=" * 80)
    logger.info("FORGEMIND AI - BUILD & DEPLOYMENT HELPER")
    logger.info("=" * 80)
    
    root_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(root_dir, "backend")
    frontend_dir = os.path.join(root_dir, "frontend")
    
    if len(sys.argv) < 2:
        logger.info("\nUsage: python deploy.py [command]")
        logger.info("\nCommands:")
        logger.info("  verify         - Verify deployment readiness")
        logger.info("  build-frontend - Build React frontend")
        logger.info("  build-backend  - Verify backend dependencies")
        logger.info("  build-all      - Build entire project")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "verify":
        logger.info("\nVerifying deployment readiness...")
        if run_command(f"python verify_deployment.py", cwd=backend_dir):
            logger.info("\n✓ Deployment verification passed!")
        else:
            logger.error("\n✗ Deployment verification failed!")
            sys.exit(1)
    
    elif command == "build-frontend":
        logger.info("\nBuilding frontend...")
        if run_command("npm install", cwd=frontend_dir):
            if run_command("npm run build", cwd=frontend_dir):
                logger.info("\n✓ Frontend build successful!")
            else:
                logger.error("\n✗ Frontend build failed!")
                sys.exit(1)
        else:
            logger.error("\n✗ npm install failed!")
            sys.exit(1)
    
    elif command == "build-backend":
        logger.info("\nVerifying backend dependencies...")
        if run_command(f"pip install -r requirements.txt", cwd=backend_dir):
            logger.info("\n✓ Backend dependencies installed!")
        else:
            logger.error("\n✗ Backend dependency installation failed!")
            sys.exit(1)
    
    elif command == "build-all":
        logger.info("\nBuilding complete project...")
        
        logger.info("\n1. Building frontend...")
        if not run_command("npm install", cwd=frontend_dir):
            logger.error("✗ npm install failed!")
            sys.exit(1)
        if not run_command("npm run build", cwd=frontend_dir):
            logger.error("✗ Frontend build failed!")
            sys.exit(1)
        logger.info("✓ Frontend build successful!")
        
        logger.info("\n2. Setting up backend...")
        if not run_command(f"pip install -r requirements.txt", cwd=backend_dir):
            logger.error("✗ Backend dependency installation failed!")
            sys.exit(1)
        logger.info("✓ Backend dependencies installed!")
        
        logger.info("\n3. Verifying deployment...")
        if not run_command(f"python verify_deployment.py", cwd=backend_dir):
            logger.error("✗ Deployment verification failed!")
            sys.exit(1)
        logger.info("✓ Deployment verification passed!")
        
        logger.info("\n" + "=" * 80)
        logger.info("✓ BUILD COMPLETE - PROJECT READY FOR DEPLOYMENT")
        logger.info("=" * 80)
    
    else:
        logger.error(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
