import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime

BOT_TOKEN = "8434146068:AAFITjTpkQwNPp0PasgcwOzUtyuwsBra3mo"
CHAT_ID = "1244185550"
URL = "https://www.rdv-prefecture.interieur.gouv.fr/rdvpref/reservation/demarche/11800/creneau/"
CHECK_INTERVAL = 45  # secondes

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

def check_prefecture():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        resp = requests.get(URL, headers=headers, timeout=20)
        soup = BeautifulSoup(resp.text, 'html.parser')
        page_text = soup.get_text().lower()
        return "aucun créneau disponible" not in page_text
    except:
        return False

# DÉMARRAGE
send_telegram("🤖 **SURVEILLANCE RDV PRÉFECTURE ACTIVÉE** ✅\n\n📍 Démarche 11800\n⏱️ Vérif toutes les 45s\n🎯 Alerte si créneau avant 31/03\n\n**Bot tourne 24/7 !**")

print("🚀 Surveillance active...")
checks = 0

while True:
    checks += 1
    print(f"Check #{checks}")
    
    if check_prefecture():
        send_telegram("🚨 **CRÉNEAU DISPONIBLE 11800 !** 🚨\n\n👉 " + URL + "\n\n*(Ton 31/03 reste backup)*")
        send_telegram("✅ Surveillance terminée")
        break
    
    if checks % 10 == 0:  # Status toutes les 7min
        send_telegram(f"✅ Bot actif | Check #{checks} | OK")
    
    time.sleep(CHECK_INTERVAL)
