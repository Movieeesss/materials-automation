from flask import Flask
import threading
from materials import run_materials_broadcast

app = Flask(__name__)

@app.route('/')
def home():
    return "Uniq Designs Bot is Active!"

@app.route('/run-materials')
def trigger_materials():
    # Threading moolama background-la scraper odum
    thread = threading.Thread(target=run_materials_broadcast)
    thread.start()
    
    # CRITICAL FIX: Cron-job error thavirkka chinna response
    return "Scraper Started", 200 

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
