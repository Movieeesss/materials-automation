import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

# --- CONFIGURATION ---
TOKEN = "8236985453:AAHKOSEMhu4ATV0MwN4B-VaAmK9wmuWbJwo"
CHAT_ID = "1115358053" # Ippo unga personal ID, apparaum users.json loop panni mathikalam
API_KEY = "5a50f090-2bd7-442f-b0c6-3888ee7620c5"

def get_buildiyo_steel_prices():
    target_url = "https://buildiyo.store/pages/today-steel-price"
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={target_url}&render=true&wait=5000"
    
    steel_data = []
    try:
        response = requests.get(proxy_url, timeout=30)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            tables = soup.find_all('table')
            
            for table in tables:
                rows = table.find_all('tr')
                for row in rows[1:]:
                    cols = row.find_all('td')
                    if len(cols) >= 2:
                        brand = cols[0].get_text(strip=True)
                        price_str = cols[1].get_text(strip=True)
                        
                        if brand and "Rs" in price_str:
                            try:
                                # Price cleaning (Rs. 68,500 -> 68500)
                                clean_price = price_str.replace('Rs.', '').replace(',', '').strip()
                                ton_price = float(clean_price)
                                
                                # CALCULATION: PER KG
                                kg_price = ton_price / 1000
                                
                                steel_data.append(f"🏗️ *{brand}*\n💰 *₹{kg_price:.2f} / KG* _(₹{ton_price:,.0f}/Ton)_")
                            except:
                                continue
        return steel_data[:12] # Top 12 results
    except Exception as e:
        print(f"Error: {e}")
        return []

def run_materials_broadcast():
    # 1. Send status
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": "🏗️ *Fetching Live Steel Prices (Per KG)...*", "parse_mode": "Markdown"})
    
    data = get_buildiyo_steel_prices()
    
    # IST Time
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    header = "🧱 *TRICHY STEEL PRICE REPORT* 🧱\n"
    meta = f"🕒 {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not data:
        body = "⚠️ *Status:* Data not found. Check website structure."
    else:
        body = "\n\n".join(data)
            
    footer = "\n━━━━━━━━━━━━━━━━━━━━\n📊 Data: Buildiyo Store\n_Prices excl. GST & Loading_"
    
    final_msg = header + meta + body + footer
    
    # 2. Final Message
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": final_msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    run_materials_broadcast()
