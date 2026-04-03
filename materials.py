import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

# --- CONFIGURATION ---
TOKEN = "8236985453:AAHKOSEMhu4ATV0MwN4B-VaAmK9wmuWbJwo"
CHAT_ID = "1115358053" 
API_KEY = "5a50f090-2bd7-442f-b0c6-3888ee7620c5"

def get_buildiyo_steel_deep_scraping():
    target_url = "https://buildiyo.store/pages/today-steel-price"
    
    # IDEA 2: Wait time increased to 20s + Residential Proxy to bypass Cloudflare
    proxy_url = (
        f"https://api.webscraping.ai/html?api_key={API_KEY}"
        f"&url={target_url}&proxy=residential&render=true&wait=20000"
    )
    
    steel_data = []
    try:
        # Timeout increased to 40s to allow the 20s wait time to finish
        response = requests.get(proxy_url, timeout=45) 
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # IDEA 1: Specific Table Targeting using CSS Selector
            # Buildiyo's table is inside a div with class 'rte'
            rows = soup.select('div.rte table tr') or soup.select('table tr')
            
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 2:
                    brand = cols[0].get_text(strip=True)
                    price_str = cols[1].get_text(strip=True)
                    
                    # Look for prices like "Rs. 68,000"
                    if brand and "Rs" in price_str:
                        try:
                            # Extracting only numbers
                            clean_p = "".join(filter(str.isdigit, price_str))
                            ton_p = float(clean_p)
                            kg_p = ton_p / 1000
                            
                            steel_data.append(f"🏗️ *{brand}*\n💰 *₹{kg_p:.2f} / KG* _(₹{ton_p:,.0f}/T)_")
                        except:
                            continue
        else:
            print(f"API Error Code: {response.status_code}")
            
        return steel_data[:15]
    except Exception as e:
        print(f"Deep Scraping Exception: {e}")
        return []

def run_materials_broadcast():
    # Sending status message first
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": "🏗️ *Deep Scraping Steel Prices (Buildiyo)...*\n_Please wait 30-40 seconds..._", "parse_mode": "Markdown"})
    
    data = get_buildiyo_steel_deep_scraping()
    
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    header = "🧱 *TRICHY STEEL PRICE REPORT* 🧱\n"
    meta = f"🕒 {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not data:
        body = "⚠️ *Status:* Data still not found.\n_Possible reasons: Cloudflare blocked even the proxy or selector changed again._"
    else:
        body = "\n\n".join(data)
            
    footer = "\n━━━━━━━━━━━━━━━━━━━━\n📊 Source: Buildiyo Store\n_Wait Time: 20s | Proxy: Residential_"
    
    final_msg = header + meta + body + footer
    
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": final_msg, "parse_mode": "Markdown", "disable_web_page_preview": True})

if __name__ == "__main__":
    run_materials_broadcast()
