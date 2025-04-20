# run_waitress.py
import logging
logging.basicConfig(level=logging.INFO)
from myapp import app
from waitress import serve

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080)  # Serving the app using Waitress