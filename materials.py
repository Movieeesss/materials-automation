import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

# --- CONFIGURATION ---
TOKEN = "8236985453:AAHKOSEMhu4ATV0MwN4B-VaAmK9wmuWbJwo"
CHAT_ID = "1115358053" 
API_KEY = "5a50f090-2bd7-442f-b0c6-3888ee7620c5"

def get_indiamart_trichy_per_kg():
    # Specific URL for Trichy Steel Dealers
    target_url = "https://dir.indiamart.com/tiruchirappalli/tmt-steel-bars.html"
    
    # 25 credits per run - Using residential proxy for high success rate
    proxy_url = (
        f"https://api.webscraping.ai/html?api_key={API_KEY}"
        f"&url={target_url}&proxy=residential&render=true&wait=10000"
    )
    
    kg_data = []
    try:
        response = requests.get(proxy_url, timeout=45)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            items = soup.select('.m_cpn') or soup.select('li.lst_cl')
            
            for item in items:
                name_tag = item.select_one('.pnt') or item.select_one('.pro_nm')
                price_tag = item.select_one('.prc') or item.select_one('.price')
                
                if name_tag and price_tag:
                    brand = name_tag.get_text(strip=True)
                    price_str = price_tag.get_text(strip=True)
                    
                    if any(x in brand.upper() for x in ["STEEL", "TMT", "AGNI", "ARS", "KAAVERI"]):
                        # Extracting digits only
                        clean_p = "".join(filter(str.isdigit, price_str))
                        
                        if clean_p and len(clean_p) >= 4:
                            ton_p = float(clean_p)
                            per_kg = ton_p / 1000
                            kg_data.append(f"🏗️ *{brand}*\n💰 *₹{per_kg:.2f} / KG* _(₹{ton_p:,.0f}/Ton)_")
        return kg_data[:10]
    except Exception as e:
        print(f"Error: {e}")
        return []

# Indha function name thaan app.py-la import aagum
def run_materials_broadcast():
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": "📍 *Scanning Trichy Market (IndiaMART)...*\n_Calculating Per KG Price..._", "parse_mode": "Markdown"})
    
    data = get_indiamart_trichy_per_kg()
    
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    header = "🧱 *TRICHY STEEL PRICE (PER KG)* 🧱\n"
    meta = f"🕒 {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not data:
        body = "⚠️ *Status:* No data found. Check API credits or Site structure."
    else:
        body = "\n\n".join(data)
            
    footer = "\n━━━━━━━━━━━━━━━━━━━━\n📊 Data: IndiaMART Trichy\n_Prices approx. Excl. GST_"
    final_msg = header + meta + body + footer
    
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": final_msg, "parse_mode": "Markdown", "disable_web_page_preview": True})
