from flask import Flask, request
import threading
from materials import run_materials_broadcast # Import the new function

app = Flask(__name__)

@app.route('/run-materials', methods=['GET'])
def trigger_materials():
    # Run in background to avoid Render timeout
    thread = threading.Thread(target=run_materials_broadcast)
    thread.start()
    return "OK", 200 # Instant response to Cron-job

# ... (Unga existing /webhook and /run-movies routes) ...

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
