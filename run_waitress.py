# run_waitress.py
import logging
logging.basicConfig(level=logging.INFO)
from myapp import app
from waitress import serve

if __name__ == "__main__":
    print("Serving on http://127.0.0.1:8080")
    serve(app, host="127.0.0.1", port=8080)  # Serving the app using Waitress