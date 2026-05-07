#!/usr/bin/env python3
"""
Deployment verification script for ForgeMind AI
Checks all components before starting the server
"""

import sys
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger()

def check_imports():
    """Verify all critical imports work"""
    logger.info("Checking imports...")
    try:
        import fastapi
        logger.info("✓ fastapi")
    except ImportError as e:
        logger.error(f"✗ fastapi: {e}")
        return False
    
    try:
        import sqlalchemy
        logger.info("✓ sqlalchemy")
    except ImportError as e:
        logger.error(f"✗ sqlalchemy: {e}")
        return False
    
    try:
        import spacy
        logger.info("✓ spacy")
    except ImportError as e:
        logger.error(f"✗ spacy: {e}")
        return False
    
    try:
        import pydantic
        logger.info("✓ pydantic")
    except ImportError as e:
        logger.error(f"✗ pydantic: {e}")
        return False
    
    return True

def check_backend_modules():
    """Verify backend modules can be imported"""
    logger.info("\nChecking backend modules...")
    try:
        from database import db
        logger.info("✓ database module")
    except Exception as e:
        logger.error(f"✗ database module: {e}")
        return False
    
    try:
        from models import models
        logger.info("✓ models module")
    except Exception as e:
        logger.error(f"✗ models module: {e}")
        return False
    
    try:
        from nlp import engine
        logger.info("✓ nlp engine module")
    except Exception as e:
        logger.error(f"✗ nlp engine module: {e}")
        return False
    
    try:
        from routes import chat, orders
        logger.info("✓ routes modules")
    except Exception as e:
        logger.error(f"✗ routes modules: {e}")
        return False
    
    return True

def check_database():
    """Verify database can be initialized"""
    logger.info("\nChecking database...")
    try:
        from database.db import engine, Base
        Base.metadata.create_all(bind=engine)
        
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("✓ Database connection verified")
        return True
    except Exception as e:
        logger.error(f"✗ Database error: {e}")
        return False

def check_nlp():
    """Verify NLP engine loads"""
    logger.info("\nChecking NLP engine...")
    try:
        from nlp.engine import nlp_engine, nlp
        if nlp is not None:
            logger.info("✓ NLP model loaded")
        else:
            logger.warning("⚠ NLP model not loaded (will run in fallback mode)")
        logger.info("✓ NLP engine initialized")
        return True
    except Exception as e:
        logger.error(f"✗ NLP error: {e}")
        return False

if __name__ == "__main__":
    logger.info("=" * 80)
    logger.info("FORGEMIND AI - PRE-DEPLOYMENT VERIFICATION")
    logger.info("=" * 80)
    
    checks = [
        check_imports,
        check_backend_modules,
        check_database,
        check_nlp
    ]
    
    results = []
    for check in checks:
        try:
            results.append(check())
        except Exception as e:
            logger.error(f"Check failed: {e}")
            results.append(False)
    
    logger.info("\n" + "=" * 80)
    if all(results):
        logger.info("✓ ALL CHECKS PASSED - READY FOR DEPLOYMENT")
        logger.info("=" * 80)
        sys.exit(0)
    else:
        logger.error("✗ SOME CHECKS FAILED - DEPLOYMENT NOT SAFE")
        logger.info("=" * 80)
        sys.exit(1)
