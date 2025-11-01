"""
Production server script using Waitress (Windows-compatible)
For Linux/Mac, use Gunicorn instead
"""

from waitress import serve
from app import app

if __name__ == "__main__":
    print("🚀 Starting Samarth Q&A Production Server...")
    print("📡 Server running at http://0.0.0.0:5000")
    print("🔒 Production mode enabled")
    serve(app, host="0.0.0.0", port=5000, threads=4)

