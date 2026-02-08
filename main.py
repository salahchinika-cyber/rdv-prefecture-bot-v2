import requests
import time
import os
from bs4 import BeautifulSoup
from datetime import datetime, date
import re

# TOKEN SÉCURISÉ
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = "1244185550"
URL = "https://www.rdv-prefecture.interieur.gouv.fr/rdvpref/reservation/demarche/11800/creneau/"
CHECK_INTERVAL = 60

if not BOT_TOKEN:
    print("❌ BOT_TOKEN manquant")
    exit(1)

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

def extract_dates(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    text = soup.get_text()
    dates = re.findall(r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{4})\b', text)
    parsed
