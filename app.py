from flask import Flask
import threading
from materials import run_materials_broadcast

app = Flask(__name__)

@app.route('/')
def home():
    return "Uniq Designs Bot is Active!"

@app.route('/run-materials')
def trigger_materials():
    # Background-la scraper odum, so response udane anuppalam
    thread = threading.Thread(target=run_materials_broadcast)
    thread.start()
    
    # CRITICAL: Cron-job error thavirkka chinna response
    return "Success", 200 

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
