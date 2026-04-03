import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

# --- CONFIGURATION ---
TOKEN = "8236985453:AAHKOSEMhu4ATV0MwN4B-VaAmK9wmuWbJwo"
CHAT_ID = "1115358053" 
API_KEY = "5a50f090-2bd7-442f-b0c6-3888ee7620c5"

def get_ars_per_kg():
    # Official ARS Price Page
    target_url = "https://arsgroup.in/tmt-steel-price-today"
    
    # Using JS Render to ensure the price calculator loads fully
    proxy_url = f"https://api.webscraping.ai/html?api_key={API_KEY}&url={target_url}&render=true&wait=5000"
    
    kg_results = []
    try:
        response = requests.get(proxy_url, timeout=35)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Full page text search for the price pattern
            page_content = soup.get_text()
            
            # ARS site-la "Rs.70,000/MT" oru specific format-la irukkum
            if "Rs." in page_content and "/MT" in page_content:
                # Splitting the text to isolate the price number
                parts = page_content.split("Rs.")
                for part in parts[1:]:
                    if "/MT" in part:
                        price_val = part.split("/MT")[0].strip()
                        # Removing commas: "70,000" -> "70000"
                        clean_p = "".join(filter(str.isdigit, price_val))
                        
                        if clean_p and len(clean_p) >= 4:
                            ton_price = float(clean_p)
                            # CALCULATION: Price per KG
                            per_kg = ton_price / 1000
                            
                            kg_results.append(f"🏗️ *ARS 550D TMT STEEL*\n💰 *₹{per_kg:.2f} / KG*\n_(Official Rate: ₹{ton_price:,.0f}/MT)_")
                            break # First valid price-ah eduthutta pothum
        return kg_results
    except Exception as e:
        print(f"ARS Scraper Error: {e}")
        return []

def run_materials_broadcast():
    # Sending status message
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": "🏗️ *Fetching Today's ARS Steel Price (Per KG)...*", "parse_mode": "Markdown"})
    
    data = get_ars_per_kg()
    
    # IST Time Formatting
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    time_str = ist_now.strftime("%d-%m-%Y | %I:%M %p")
    
    header = "🧱 *OFFICIAL ARS PRICE REPORT* 🧱\n"
    meta = f"🕒 {time_str}\n━━━━━━━━━━━━━━━━━━━━\n"
    
    if not data:
        body = "⚠️ *Status:* Official site price not detected.\n_Reason: Site structure change or Maintenance._"
    else:
        body = "\n\n".join(data)
            
    footer = "\n━━━━━━━━━━━━━━━━━━━━\n📊 Source: ARS Group Official\n_Unit: Price per KG (Retail)_"
    
    final_msg = header + meta + body + footer
    
    # Final Send to Telegram
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                 params={"chat_id": CHAT_ID, "text": final_msg, "parse_mode": "Markdown", "disable_web_page_preview": True})

if __name__ == "__main__":
    run_materials_broadcast()
