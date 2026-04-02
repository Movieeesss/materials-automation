import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

# --- CONFIGURATION ---
TOKEN = "8236985453:AAHKOSEMhu4ATV0MwN4B-VaAmK9wmuWbJwo"
CHAT_ID = "1115358053"
API_KEY = "45b4f3e2-b8db-473c-8b38-374fa0b0febe"

def get_trichy_material_prices():
    # URL targeting Construction Materials in Trichy
    target_url = "https://dir.indiamart.com/tiruchirappalli/construction-material.html"
    
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={target_url}&proxy=residential&render=true&wait=10000"
    
    materials_data = []
    try:
        response = requests.get(proxy_url, timeout=28)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # IndiaMART usually stores items in 'ls_item' or similar card classes
            # We look for product names and price strings
            items = soup.find_all('li', class_='lst_cl') # Common IndiaMART class
            
            for item in items:
                try:
                    name = item.find('span', class_='pnt').text.strip()
                    price = item.find('span', class_='prc').text.strip()
                    if name and price:
                        materials_data.append(f"🏗️ *{name}*\n💰 Price: {price}")
                except:
                    continue
        else:
            print(f"Material Error: Status {response.status_code}")
    except Exception as e:
        print(f"Connection Error: {e}")
        
    return materials_data[:10] # Top 10 results to avoid Telegram message limits

def run_materials():
    # Notify Telegram
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": "🏗️ *Fetching Live Material Prices (Trichy)...*", "parse_mode": "Markdown"})
    
    data = get_trichy_material_prices()
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    header = "🧱 *TRICHY MATERIAL PRICES* 🧱\n"
    meta = f"🕒 {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not data:
        body = "⚠️ No price data found. Check if the page layout changed."
    else:
        body = "\n\n".join(data)
            
    footer = "\n━━━━━━━━━━━━━━━━━━━━\n📊 Data from IndiaMART Trichy"
    
    final_msg = header + meta + body + footer
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": final_msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    run_materials()
