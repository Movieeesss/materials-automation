import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

# --- CONFIGURATION ---
TOKEN = "8236985453:AAHKOSEMhu4ATV0MwN4B-VaAmK9wmuWbJwo"
CHAT_ID = "1115358053" 
API_KEY = "5a50f090-2bd7-442f-b0c6-3888ee7620c5"

def get_material_prices_v2():
    # More reliable source for Steel & Cement
    target_url = "https://constructionestimatorindia.com/construction-material-prices/"
    # Normal proxy + Render (Saves credits and highly effective)
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={target_url}&render=true&wait=5000"
    
    final_data = []
    try:
        response = requests.get(proxy_url, timeout=40)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # This site uses standard tables, which is stable for long term
            rows = soup.find_all('tr')
            
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 2:
                    material = cols[0].get_text(strip=True)
                    price_str = cols[1].get_text(strip=True)
                    
                    # Target: Steel and Cement specifically for Structural Engineering
                    mat_upper = material.upper()
                    if any(x in mat_upper for x in ["STEEL", "CEMENT", "TMT"]):
                        
                        # Calculation for Steel per KG
                        if "STEEL" in mat_upper or "TMT" in mat_upper:
                            try:
                                # Extract digits: "₹ 65,000" -> 65000
                                clean_p = "".join(filter(str.isdigit, price_str))
                                if clean_p:
                                    ton_p = float(clean_p)
                                    kg_p = ton_p / 1000
                                    final_data.append(f"🏗️ *{material}*\n💰 *₹{kg_p:.2f} / KG* _(₹{ton_p:,.0f}/T)_")
                            except: continue
                        else:
                            # For Cement (Show as is)
                            final_data.append(f"🧱 *{material}*\n💰 {price_str}")
                            
        return final_data[:15]
    except Exception as e:
        print(f"Scraper Error: {e}")
        return []

def run_materials_broadcast():
    # 1. Initial Status
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": "🏗️ *Fetching Live Material Prices (Steel & Cement)...*", "parse_mode": "Markdown"})
    
    data = get_material_prices_v2()
    
    # IST Time
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    header = "🧱 *TRICHY MATERIAL PRICES* 🧱\n"
    meta = f"🕒 {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not data:
        body = "⚠️ *Status:* Data source temporarily unavailable.\n_Trying to reconnect in next cycle..._"
    else:
        body = "\n\n".join(data)
            
    footer = "\n━━━━━━━━━━━━━━━━━━━━\n📊 Data: Construction Estimator\n_Prices approx. Excl. GST_"
    
    final_msg = header + meta + body + footer
    
    # 2. Final Message
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": final_msg, "parse_mode": "Markdown", "disable_web_page_preview": True})

if __name__ == "__main__":
    run_materials_broadcast()
