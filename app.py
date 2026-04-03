from flask import Flask
import threading
# Importing the standardized function name
from materials import run_materials_broadcast

app = Flask(__name__)

@app.route('/')
def home():
    return "Uniq Designs - Material Bot is Live!"

@app.route('/run-materials')
def trigger_materials():
    # Background threading for stability
    thread = threading.Thread(target=run_materials_broadcast)
    thread.start()
    return "Trichy Scraper Started Successfully", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
