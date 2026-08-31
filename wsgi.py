"""
WSGI entry point for Render deployment.
This file allows Render to properly start the Flask application.
"""

from app.app import app

if __name__ == "__main__":
    app.run()
