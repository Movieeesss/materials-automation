from flask import Flask
import threading
from materials import run_materials_broadcast

app = Flask(__name__)

@app.route('/')
def home():
    return "Material Bot is Running!"

@app.route('/run-materials')
def trigger_materials():
    # Important: Run in background to prevent Render 30s timeout
    thread = threading.Thread(target=run_materials_broadcast)
    thread.start()
    return "Scraper Started Successfully", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
