import requests

TOKEN = 'Telegram_Token'
CHAT_ID = 'Chat_Id_Telegram'

def wyslij_powiadomienie(tresc):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    dane = {'chat_id': CHAT_ID, 'text': tresc}
    requests.post(url, data=dane)
