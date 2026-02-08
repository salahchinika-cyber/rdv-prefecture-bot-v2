import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime, date
import re

BOT_TOKEN = "8434146068:AAFITjTpkQwNPp0PasgcwOzUtyuwsBra3mo"
CHAT_ID = "1244185550"
URL = "https://www.rdv-prefecture.interieur.gouv.fr/rdvpref/reservation/demarche/11800/creneau/"
CHECK_INTERVAL = 60

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

def extract_dates(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    text = soup.get_text()
    dates = re.findall(r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{4})\b', text)
    parsed_dates = []
    
    for date_str in dates:
        try:
            date_str = date_str.replace('-', '/')
            d = datetime.strptime(date_str, '%d/%m/%Y').date()
            if d >= date(2026, 2, 1):
                parsed_dates.append(d)
        except:
            continue
    
    return sorted(set(parsed_dates))

def get_closest_date(html_text):
    dates = extract_dates(html_text)
    return dates[0] if dates else None

def check_prefecture():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        resp = requests.get(URL, headers=headers, timeout=20)
        return get_closest_date(resp.text)
    except:
        return None

# === DÉMARRAGE ===
startup_msg = """🤖 **SURVEILLANCE INFINIE RDV 11800** 🔄

📍 Démarche: Remise titre séjour Loire-Atlantique
⏱️ Fréquence: toutes les 60s
🎯 Alerte: TOUT nouveau créneau MEILLEUR
💾 Status: Surveillance 24/7 INFINIE

**🚀 Bot lancé le {datetime.now().strftime('%d/%m %H:%M')}**"""
send_telegram(startup_msg)

print("🚀 Surveillance infinie démarrée")
last_closest_date = None
checks = 0

while True:  # 🔄 BOUCLE INFINIE
    checks += 1
    print(f"Check #{checks} - {datetime.now().strftime('%H:%M:%S')}")
    
    current_date = check_prefecture()
    
    if current_date:
        print(f"📅 Date trouvée: {current_date}")
        
        # ALERTE si première date OU date MEILLEURE
        if last_closest_date is None or current_date < last_closest_date:
            last_closest_date = current_date
            days_ahead = (current_date - date.today()).days
            
            alert_msg = f"""🚨 **NOUVEAU MEILLEUR CRÉNEAU !** 🚨

📅 **Date**: `{current_date.strftime('%d/%m/%Y')}`
⏳ **Dans**: {days_ahead} jours
👇 `{URL}`
📈 **Amélioration** vs précédent

*Surveillance continue...* 🔄"""
            send_telegram(alert_msg)
        else:
            print(f"ℹ️ {current_date} = pas mieux que {last_closest_date}")
    else:
        print("ℹ️ Aucune date détectée")
    
    # STATUS RÉGULIERS (toutes les 10min)
    if checks % 10 == 0:
        uptime_hours = checks * CHECK_INTERVAL / 3600
        st
