import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

# --- CONFIGURATION ---
TOKEN = "8236985453:AAHKOSEMhu4ATV0MwN4B-VaAmK9wmuWbJwo"
CHAT_ID = "1115358053" 
API_KEY = "5a50f090-2bd7-442f-b0c6-3888ee7620c5"

def get_buildiyo_steel_prices():
    target_url = "https://buildiyo.store/pages/today-steel-price"
    # Wait time increased to 10s (10000ms) for Cloudflare bypass
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={target_url}&render=true&wait=10000"
    
    steel_data = []
    try:
        response = requests.get(proxy_url, timeout=35) # Increased timeout
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Refined Selector: Targets all table rows directly
            rows = soup.select('table tr') or soup.find_all('tr')
            
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 2:
                    brand = cols[0].get_text(strip=True)
                    price_str = cols[1].get_text(strip=True)
                    
                    # Filtering valid brand and price
                    if brand and "Rs" in price_str:
                        try:
                            # Cleaning: "Rs. 68,500" -> 68500
                            clean_price = "".join(filter(str.isdigit, price_str))
                            ton_price = float(clean_price)
                            
                            # CALCULATION: PER KG
                            kg_price = ton_price / 1000
                            
                            steel_data.append(f"🏗️ *{brand}*\n💰 *₹{kg_price:.2f} / KG* _(₹{ton_price:,.0f}/Ton)_")
                        except:
                            continue
        else:
            print(f"API Error: {response.status_code}")
            
        return steel_data[:15] # Top 15 Brands
    except Exception as e:
        print(f"Scraper Exception: {e}")
        return []

def run_materials_broadcast():
    # Initial status
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": "🏗️ *Fetching Live Steel Prices (Per KG)...*", "parse_mode": "Markdown"})
    
    data = get_buildiyo_steel_prices()
    
    # IST Time
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    header = "🧱 *TRICHY STEEL PRICE REPORT* 🧱\n"
    meta = f"🕒 {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not data:
        body = "⚠️ *Status:* No data found.\n_Possible reasons: Selector mismatch or site loading delay._"
    else:
        body = "\n\n".join(data)
            
    footer = "\n━━━━━━━━━━━━━━━━━━━━\n📊 Data: Buildiyo Store\n_Prices approx. Excl. GST_"
    
    final_msg = header + meta + body + footer
    
    # Send Final Report
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": final_msg, "parse_mode": "Markdown", "disable_web_page_preview": True})

if __name__ == "__main__":
    run_materials_broadcast()
