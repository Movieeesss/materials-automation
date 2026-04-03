import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

# --- CONFIGURATION ---
TOKEN = "8236985453:AAHKOSEMhu4ATV0MwN4B-VaAmK9wmuWbJwo"
CHAT_ID = "1115358053" 
API_KEY = "5a50f090-2bd7-442f-b0c6-3888ee7620c5"

def get_ars_live_prices():
    target_url = "https://arsgroup.in/tmt-steel-price-today"
    # JS Render and residential proxy to unlock the calculator cards
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={target_url}&proxy=residential&render=true&wait=10000"
    
    steel_report = []
    try:
        response = requests.get(proxy_url, timeout=50)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # ARS site-la ovvoru rod size-um oru card layout-la irukku
            # Namma '8mm', '10mm' nu irukura headings-ah target pannuvom
            cards = soup.select('.elementor-widget-container') or soup.find_all('div')
            
            for card in cards:
                text = card.get_text(separator=" ", strip=True)
                
                # 'rod price' nu irukura section-ah mattum filter panrom
                if "rod price" in text.lower() and "Price (₹ Per Ton)" in text:
                    try:
                        # Extracting the rod size (e.g., 8mm)
                        size = text.split("rod price")[0].strip() + " Rod"
                        
                        # Price extraction logic: Look for the number after (₹ Per Ton exc. GST)
                        price_part = text.split("GST)")[1].strip().split(" ")[0]
                        clean_price = "".join(filter(str.isdigit, price_part))
                        
                        if clean_price and 40000 < float(clean_price) < 90000:
                            ton_price = float(clean_price)
                            kg_price = ton_price / 1000
                            steel_report.append(f"🏗️ *{size}*\n💰 *₹{kg_price:.2f} / KG* _(₹{ton_price:,.0f}/T)_")
                    except:
                        continue
        
        # Uniq data removal (Duplicate results-ah remove panna)
        return list(dict.fromkeys(steel_report))[:8]
    except Exception as e:
        print(f"Error: {e}")
        return []

def run_materials_broadcast():
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": "🏗️ *Scanning ARS Live Pricing Grid...*\n_Calculating Per KG for all sizes..._", "parse_mode": "Markdown"})
    
    data = get_ars_live_prices()
    
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    header = "🧱 *ARS TMT - TODAY'S LIVE RATES* 🧱\n"
    meta = f"🕒 {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not data:
        body = "⚠️ *Status:* Prices are being updated on the official site.\n_Please check again in 30 minutes._"
    else:
        body = "\n\n".join(data)
            
    footer = "\n━━━━━━━━━━━━━━━━━━━━\n📊 Source: ARS Group Official\n_Unit: Price per KG (Excl. GST)_"
    
    final_msg = header + meta + body + footer
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": final_msg, "parse_mode": "Markdown"})
