import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

# --- CONFIGURATION ---
TOKEN = "8236985453:AAHKOSEMhu4ATV0MwN4B-VaAmK9wmuWbJwo"
CHAT_ID = "1115358053" 
API_KEY = "5a50f090-2bd7-442f-b0c6-3888ee7620c5"

def get_indiamart_trichy_per_kg():
    # Targeting TMT Steel in Trichy region
    target_url = "https://dir.indiamart.com/tiruchirappalli/tmt-steel-bars.html"
    
    # Using Residential Proxy + JS Render (25 Credits per run)
    # Trichy local dealers data-vukaga ithu thevai
    proxy_url = (
        f"https://api.webscraping.ai/html?api_key={API_KEY}"
        f"&url={target_url}&proxy=residential&render=true&wait=10000"
    )
    
    kg_data = []
    try:
        # High timeout for 10s wait + rendering
        response = requests.get(proxy_url, timeout=45)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            
            # IndiaMART product card selectors
            items = soup.select('.m_cpn') or soup.select('li.lst_cl')
            
            for item in items:
                name_tag = item.select_one('.pnt') or item.select_one('.pro_nm')
                price_tag = item.select_one('.prc') or item.select_one('.price')
                
                if name_tag and price_tag:
                    brand = name_tag.get_text(strip=True)
                    price_str = price_tag.get_text(strip=True)
                    
                    # Filtering for Trichy top brands (Agni, ARS, etc.)
                    brand_upper = brand.upper()
                    if any(x in brand_upper for x in ["STEEL", "TMT", "AGNI", "ARS", "KAAVERI"]):
                        
                        # CLEANING & CALCULATION LOGIC
                        # "Rs 68,000/Metric Ton" -> 68000
                        clean_p = "".join(filter(str.isdigit, price_str))
                        
                        if clean_p and len(clean_p) >= 4: # Filtering dummy prices (like ₹1 or ₹100)
                            ton_p = float(clean_p)
                            per_kg = ton_p / 1000
                            
                            kg_data.append(f"🏗️ *{brand}*\n💰 *₹{per_kg:.2f} / KG* _(₹{ton_p:,.0f}/Ton)_")
                        
        return kg_data[:10] # Top 10 regional results
        
    except Exception as e:
        print(f"Scraping Error: {e}")
        return []

def run_trichy_per_kg_broadcast():
    # Initial Telegram Status
    status_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.get(status_url, params={"chat_id": CHAT_ID, "text": "📍 *Scanning Trichy Market (IndiaMART)...*\n_Calculating Per KG Price..._", "parse_mode": "Markdown"})
    
    data = get_indiamart_trichy_per_kg()
    
    # Time adjustment for IST
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    header = "🧱 *TRICHY STEEL PRICE (PER KG)* 🧱\n"
    meta = f"🕒 {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not data:
        body = "⚠️ *Status:* No data from Trichy dealers.\n_Reason: Site rendering issue or Dealer update delay._"
    else:
        body = "\n\n".join(data)
            
    footer = "\n━━━━━━━━━━━━━━━━━━━━\n📊 Data: IndiaMART Tiruchirappalli\n_Note: GST & Transport extra._"
    
    final_msg = header + meta + body + footer
    
    # Final Report to Telegram
    requests.get(status_url, params={"chat_id": CHAT_ID, "text": final_msg, "parse_mode": "Markdown", "disable_web_page_preview": True})

if __name__ == "__main__":
    run_trichy_per_kg_broadcast()
