"""
Main Flask Application Entry Point
"""
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config.app import create_app


if __name__ == '__main__':
    app = create_app()
    
    # Development server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )
