import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

TOKEN = "8236985453:AAHKOSEMhu4ATV0MwN4B-VaAmK9wmuWbJwo"
CHAT_ID = "1115358053" 
API_KEY = "5a50f090-2bd7-442f-b0c6-3888ee7620c5"

def get_ars_live_prices():
    target_url = "https://arsgroup.in/tmt-steel-price-today"
    # Residential Proxy is MUST for ARS dynamic cards
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={target_url}&proxy=residential&render=true&wait=15000"
    
    steel_report = []
    try:
        response = requests.get(proxy_url, timeout=60)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # ARS Calculator Cards usually have specific classes like 'elementor-column'
            # Namma logic-ah simplify panni numbers-ah mattum focus pannuvom
            containers = soup.find_all('div', class_=['elementor-widget-container', 'elementor-column-wrap'])
            
            for box in containers:
                text = box.get_text(separator=" ", strip=True)
                # Targeting specific rod size blocks
                if "rod price" in text.lower():
                    try:
                        # Extracting Size (e.g., 8mm)
                        size = text.split("rod price")[0].strip()
                        
                        # Extracting Price from the input value or text
                        # Logic: Look for 5-digit numbers starting with 6 or 5 or 7
                        import re
                        prices = re.findall(r'\b[567]\d{4}\b', text)
                        
                        if prices:
                            ton_p = float(prices[0])
                            kg_p = ton_p / 1000
                            steel_report.append(f"🏗️ *{size} Rod*\n💰 *₹{kg_p:.2f} / KG* _(₹{ton_p:,.0f}/T)_")
                    except: continue
        
        return list(dict.fromkeys(steel_report))[:8]
    except: return []

def run_materials_broadcast():
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": "🏗️ *Re-scanning ARS Dynamic Calculator...*", "parse_mode": "Markdown"})
    
    data = get_ars_live_prices()
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    header = "🧱 *ARS TMT - TODAY'S LIVE RATES* 🧱\n"
    meta = f"🕒 {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not data:
        body = "⚠️ *Status:* Data not captured from Calculator.\n_Reason: Site rendering slow. Retrying in next cycle..._"
    else:
        body = "\n\n".join(data)
            
    footer = "\n━━━━━━━━━━━━━━━━━━━━\n📊 Source: ARS Group Official\n_Unit: Price per KG_"
    final_msg = header + meta + body + footer
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params={"chat_id": CHAT_ID, "text": final_msg, "parse_mode": "Markdown"})
