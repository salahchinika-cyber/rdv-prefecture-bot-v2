import requests
import time

BOT_TOKEN = "8434146068:AAFITjTpkQwNPp0PasgcwOzUtyuwsBra3mo"
CHAT_ID = "1244185550"

def send_test():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": "✅ BOT FONCTIONNE ! Surveillance RDV active !"}
    
    response = requests.post(url, data=data)
    result = response.json()
    
    print("Résultat:", result)
    
    if result.get("ok"):
        print("✅ MESSAGE ENVOYÉ SUR TELEGRAM !")
        return True
    else:
        print("❌ ERREUR:", result)
        return False

if __name__ == "__main__":
    print("🚀 Test bot...")
    if send_test():
        print("🎉 BOT PARFAIT ! Il peut surveiller les RDV !")
    else:
        print("❌ Problème détecté")
