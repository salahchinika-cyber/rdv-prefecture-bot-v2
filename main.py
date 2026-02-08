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

# === DÉMARRAGE SILENCIEUX ===
send_telegram("🤖 **Surveillance RDV 11800 ACTIVE** ✅\n\n⏱️ Vérifications silencieuses 24/7\n🚨 Alerte UNIQUEMENT pour créneaux MEILLEURS\n\n*Status mutés - seul les alertes sonnent*")

print("🚀 Surveillance DISCRÈTE démarrée")
last_closest_date = None
checks = 0
status_counter = 0  # Compteur pour status RARE

while True:
    checks += 1
    current_date = check_prefecture()
    
    if current_date:
        # ALERTE UNIQUEMENT si date MEILLEURE (pas de spam)
        if last_closest_date is None or current_date < last_closest_date:
            last_closest_date = current_date
            days_ahead = (current_date - date.today()).days
            
            alert_msg = f"""🚨 **NOUVEAU CRÉNEAU MEILLEUR !**

📅 {current_date.strftime('%d/%m/%Y')} ({days_ahead} jours)
👇 {URL}"""
            send_telegram(alert_msg)
    
    # STATUS TRÈS RARE : 1 FOIS PAR JOUR (24h = 1440 checks)
    status_counter += 1
    if status_counter >= 1440:  # 1x par jour
        uptime_days = checks * CHECK_INTERVAL / 86400
        status_msg = f"📊 Status quotidien | {uptime_days:.1f}j | Meilleure date: {last_closest_date.strftime('%d/%m/%Y') if last_closest_date else 'aucune'}"
        send_telegram(status_msg)
        status_counter = 0
    
    time.sleep(CHECK_INTERVAL)
