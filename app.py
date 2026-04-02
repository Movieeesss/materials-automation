from flask import Flask
import threading
import os
import movies
import materials # Import the new file

app = Flask(__name__)

@app.route('/')
def home():
    return "Multi-Tracker is Live!", 200

@app.route('/run-movies')
def trigger_movies():
    thread = threading.Thread(target=movies.run_all)
    thread.start()
    return "Movie Scraper Started", 200

@app.route('/run-materials')
def trigger_materials():
    # Background Thread for IndiaMART
    thread = threading.Thread(target=materials.run_materials)
    thread.start()
    return "Material Scraper Started", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
