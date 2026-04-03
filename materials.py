import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

# --- CONFIGURATION ---
TOKEN = "8236985453:AAHKOSEMhu4ATV0MwN4B-VaAmK9wmuWbJwo"
CHAT_ID = "1115358053" 
API_KEY = "5a50f090-2bd7-442f-b0c6-3888ee7620c5"

def get_ars_per_kg_final():
    target_url = "https://arsgroup.in/tmt-steel-price-today"
    # Wait time increased to 10s for full rendering
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={target_url}&render=true&wait=10000"
    
    kg_results = []
    try:
        response = requests.get(proxy_url, timeout=45)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # ARS site-la prices usually <strong> tags or specific table cells-la irukkum
            # Ellaa bold elements-aiyum check pannuvom
            elements = soup.find_all(['strong', 'b', 'td', 'span'])
            
            for el in elements:
                text = el.get_text(strip=True)
                # Looking for price pattern: Rs. followed by numbers
                if "Rs." in text and "/" in text:
                    clean_p = "".join(filter(str.isdigit, text))
                    
                    if clean_p and len(clean_p) >= 4:
                        ton_price = float(clean_p)
                        # CALCULATION: Price per KG
                        per_kg = ton_price / 1000
                        kg_results.append(f"🏗️ *ARS 550D TMT STEEL*\n💰 *₹{per_kg:.2f} / KG*\n_(Official Rate: ₹{ton_price:,.0f}/MT)_")
                        break # Logic hit aanathum stop pannidum
        return kg_results
    except Exception as e:
        print(f"Error: {e}")
        return []

def run_materials_broadcast():
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": "🏗️ *Re-scanning ARS Official Page (Deep Scan)...*", "parse_mode": "Markdown"})
    
    data = get_ars_per_kg_final()
    
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    header = "🧱 *OFFICIAL ARS PRICE REPORT* 🧱\n"
    meta = f"🕒 {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not data:
        # Plan E: If still no data, it means the site is purely JS driven
        body = "⚠️ *Status:* Site structure is too complex.\n_Checking alternative regional portal..._"
    else:
        body = "\n\n".join(data)
            
    footer = "\n━━━━━━━━━━━━━━━━━━━━\n📊 Source: ARS Group Official\n_Unit: Price per KG_"
    
    final_msg = header + meta + body + footer
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": final_msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    run_materials_broadcast()
