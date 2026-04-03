import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta, timezone

# --- CONFIGURATION ---
TOKEN = "8236985453:AAHKOSEMhu4ATV0MwN4B-VaAmK9wmuWbJwo"
CHAT_ID = "1115358053" 
# Unga Puthiya ScrapingBee API Key
API_KEY = "MKDCNDT9VWVFGX57CQ5NCR9R40F4FZWHDSLF98Z1KEK0NN5F9ZNKOM6GT5UDKD9YB6IO3A7WLNAAEHY0"

def get_ars_live_prices_per_kg():
    target_url = "https://arsgroup.in/tmt-steel-price-today"
    
    # ScrapingBee Parameters - Bypass mode ON
    params = {
        'api_key': API_KEY,
        'url': target_url,
        'render_js': 'true',     # Calculator grid-ah load panna
        'premium_proxy': 'true',  # Blocking-ah thavirkka
        'country_code': 'in',     # Indian pricing local data-kaga
        'wait': '12000'           # 12s wait for calculator rendering
    }
    
    steel_report = []
    try:
        # Hitting ScrapingBee API
        response = requests.get('https://app.scrapingbee.com/api/v1/', params=params, timeout=60)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Target: ARS Price cards from the screenshot
            containers = soup.find_all('div', class_=re.compile('elementor-widget-container|elementor-column-wrap'))
            
            for box in containers:
                text = box.get_text(separator=" ", strip=True)
                
                # Rod price section-ah identify panrom
                if "rod price" in text.lower() and "Per Ton" in text:
                    try:
                        # Extracting Size (8mm, 10mm, etc.)
                        size = text.split("rod price")[0].strip()
                        
                        # SMART FILTER: Look for 5-digit numbers (Price range 50k to 80k)
                        prices = re.findall(r'\b[567]\d{4}\b', text)
                        
                        if prices:
                            ton_p = float(prices[0])
                            kg_p = ton_p / 1000
                            # Per KG Formatting for Uniq Designs
                            steel_report.append(f"🏗️ *{size} Rod*\n💰 *₹{kg_p:.2f} / KG* _(₹{ton_p:,.0f}/T)_")
                    except: continue
        
        # Duplicate results-ah remove panni clean-ah tharum
        return list(dict.fromkeys(steel_report))[:8]
    except Exception as e:
        print(f"Scraper Error: {e}")
        return []

def run_materials_broadcast():
    # Initial status update
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": "🐝 *ScrapingBee Deep Scan: Fetching ARS Steel Prices...*", "parse_mode": "Markdown"})
    
    data = get_ars_live_prices_per_kg()
    
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    header = "🧱 *ARS TMT - TODAY'S LIVE RATES* 🧱\n"
    meta = f"🕒 {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not data:
        body = "⚠️ *Status:* Prices are currently being updated on the ARS site.\n_Please check back in 30 minutes._"
    else:
        body = "\n\n".join(data)
            
    footer = "\n━━━━━━━━━━━━━━━━━━━━\n📊 Source: ARS Official (Live)\n_Bot by Uniq Designs | Unit: Per KG_"
    
    final_msg = header + meta + body + footer
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params={"chat_id": CHAT_ID, "text": final_msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    run_materials_broadcast()
