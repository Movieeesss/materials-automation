import os
from flask import Flask
import threading
import materials # Materials file mattum import pandrom

app = Flask(__name__)

@app.route('/')
def home():
    return "Materials Tracker is Live!", 200

@app.route('/run-materials')
def trigger_materials():
    # Background-la scraper run aagum
    thread = threading.Thread(target=materials.run_materials)
    thread.start()
    return "Material Scraper Started in Background", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
