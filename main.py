import time
import requests
from bs4 import BeautifulSoup
from telegram import Bot
from datetime import datetime, date
import re

# TES IDENTIFIANTS
BOT_TOKEN = "8434146068:AAFITjTpkQwNPp0PasgcwOzUtyuwsBra3mo"
CHAT_ID = "1244185550"
URL = "https://www.rdv-prefecture.interieur.gouv.fr/rdvpref/reservation/demarche/11800/creneau/"
CHECK_INTERVAL = 45

bot = Bot(token=BOT_TOKEN)

class PrefectureBot:
    def __init__(self):
        self.last_date_found = None
        self.start_time = datetime.now()
        
    def send_telegram(self, message):
        try:
            bot.send_message(chat_id=CHAT_ID, text=message)
            print(f"✅ Message envoyé")
            return True
        except Exception as e:
            print(f"❌ Erreur Telegram: {e}")
            return False
    
    def check_prefecture(self):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            resp = requests.get(URL, timeout=20, headers=headers)
            resp.raise_for_status()
            
            soup = BeautifulSoup(resp.text, "html.parser")
            page_text = soup.get_text().lower()
            
            # Si "aucun créneau disponible" DIS PARAÎT
            if "aucun créneau disponible" not in page_text:
                return True, "Créneau détecté !"
            return False, "Aucun nouveau créneau"
        except:
            return False, "Erreur requête"
    
    def is_better_slot(self, has_slot):
        if self.last_date_found is None and has_slot:
            return True
        return has_slot

def main():
    bot_monitor = PrefectureBot()
    
    # MESSAGE CONFIRMATION
    startup_msg = f"""🤖 **BOT PRÉFECTURE 11800 ACTIVÉ** ✅

📍 URL: {URL}
⏱️ Vérif: toutes les 45s
📅 Date: {date.today().strftime('%d/%m/%Y')}

**Surveillance 24/7 active !** 🎯"""
    
    if not bot_monitor.send_telegram(startup_msg):
        print("❌ ERREUR FATALE: Telegram ne répond pas")
        return
    
    print("🚀 Bot actif !")
    checks = 0
    
    while True:
        checks += 1
        print(f"🔍 Check #{checks}")
        
        has_slot, status = bot_monitor.check_prefecture()
        
        if has_slot and bot_monitor.is_better_slot(has_slot):
            alert_msg = f"""🚨 **CRÉNEAU DISPONIBLE 11800** 🚨

{status}
VA RÉSERVER: {URL}

*(Ton 31/03 reste backup)*"""
            bot_monitor.send_telegram(alert_msg)
            bot_monitor.send_telegram("✅ Bot arrêté après alerte")
            break
        
        # Status régulier
        if checks % 10 == 0:
            uptime = int((datetime.now() - bot_monitor.start_time).total_seconds()/60)
            bot_monitor.send_telegram(f"✅ Bot OK | Check #{checks} | {uptime}min")
        
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
