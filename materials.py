import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

# --- CONFIGURATION ---
TOKEN = "8236985453:AAHKOSEMhu4ATV0MwN4B-VaAmK9wmuWbJwo"
CHAT_ID = "1115358053"
API_KEY = "45b4f3e2-b8db-473c-8b38-374fa0b0febe"

def get_trichy_material_prices():
    # URL for Construction Materials in Trichy
    target_url = "https://dir.indiamart.com/tiruchirappalli/construction-material.html"
    
    # Using residential proxy + JS rendering to bypass IndiaMART blocks
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={target_url}&proxy=residential&render=true&wait=10000"
    
    materials_data = []
    try:
        # Increased timeout to 29s to stay just under Render/Cron-job limits
        response = requests.get(proxy_url, timeout=29)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml') # 'lxml' is faster if installed
            
            # UPDATED SELECTORS: IndiaMART often uses these specific classes
            # Product cards usually have 'm_cpn' or 'lst_cl'
            items = soup.select('li.lst_cl') or soup.select('.m_cpn') 
            
            for item in items:
                try:
                    # Look for Product Name
                    name_tag = item.select_one('.pnt') or item.select_one('.pro_nm')
                    # Look for Price
                    price_tag = item.select_one('.prc') or item.select_one('.price')
                    
                    if name_tag:
                        name = name_tag.get_text(strip=True)
                        price = price_tag.get_text(strip=True) if price_tag else "Price on Request"
                        
                        # Filter out ads or empty results
                        if len(name) > 2:
                            materials_data.append(f"🏗️ *{name}*\n💰 {price}")
                except Exception:
                    continue
        else:
            print(f"Scraper Error: Status {response.status_code}")
            
    except Exception as e:
        print(f"Connection Error: {e}")
        
    return materials_data[:10] 

def run_materials():
    # 1. Send initial status to Telegram
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": "🏗️ *Fetching Live Material Prices (Trichy)...*", "parse_mode": "Markdown"})
    
    data = get_trichy_material_prices()
    
    # IST Time
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    header = "🧱 *TRICHY MATERIAL PRICES* 🧱\n"
    meta = f"🕒 {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not data:
        body = "⚠️ *Status:* No data found.\n_Possible reasons: High traffic block or selector change._"
    else:
        body = "\n\n".join(data)
            
    footer = "\n━━━━━━━━━━━━━━━━━━━━\n📊 Data: IndiaMART Trichy"
    
    # 2. Send final results
    final_msg = header + meta + body + footer
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": final_msg, "parse_mode": "Markdown", "disable_web_page_preview": True})

if __name__ == "__main__":
    run_materials()
