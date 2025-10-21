import network
import time

SSID = "SSID"
PASSWORD = "PASSWORD"
def wifi_connection():

    # utworzenie interfejsu Wi-Fi w trybie stacji (klient)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    print("Łączenie z siecią Wi-Fi...")
    max_czekanie = 10
    while max_czekanie > 0:
        if wlan.isconnected():
            break
        print("Czekam na połączenie...")
        time.sleep(1)
        max_czekanie -= 1

    if wlan.isconnected():
        print("Połączono z Wi-Fi!")
        print("Adres IP:", wlan.ifconfig()[0])
    else:
        print("❌ Nie udało się połączyć z siecią Wi-Fi.")