from machine import Pin, time_pulse_us
import time 
import powiadomienia
from wifi.py import wifi_connection

print("Łącze z WiFi")
wifi_connection()

kontaktron = Pin(20, Pin.IN, Pin.PULL_UP)   # GP20: czujnik otwarcia drzwi
led_czerwona = Pin(15, Pin.OUT)             # GP15: LED sygnalizacyjny

trigger = Pin(14, Pin.OUT)                  # GP14: trigger HC-SR04
echo = Pin(16, Pin.IN)                      # GP16: echo HC-SR04

PROG_ODLEGLOSCI = 0.50     # metry
SPEED_OF_SOUND = 340.29    # m/s

def zmierz_odleglosc():
    # wyślij impuls trigger
    trigger.low()
    time.sleep_us(2)
    trigger.high()
    time.sleep_us(10)
    trigger.low()

    # zmierz czas stanu wysokiego na echo
    czas = time_pulse_us(echo, 1, 30000)  # timeout 30 ms
    if czas < 0:
        return 999  # brak echa
    # czas w µs → sekundy
    dystans = (czas / 1_000_000) * (SPEED_OF_SOUND / 2)
    return dystans

def otwarcie():
    teraz = time.localtime()
    ts = "{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(*teraz[:6])
    print(f"Otwarcie drzwi! {ts}")
    wyslij_powiadomienie(f"OTWARTE DRZWI! {ts}")
    time.sleep(5)
    dystans = zmierz_odleglosc()
    if dystans < PROG_ODLEGLOSCI:
        print(f"🚪 Ruch! Drzwi/okno zostało otwarte! {ts}")
        wyslij_powiadomienie(f"Ruch! Drzwi/okno zostało otwarte! {ts}")
        led_czerwona.value(1)
    else:
        print(f"brak obiektu w zasiegu {ts}")
        wyslij_powiadomienie(f"Brak obiektu w zasiegu {teraz}")
        led_czerwona.value(0)

def zamkniecie():
    teraz = time.localtime()
    ts = "{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(*teraz[:6])
    wyslij_powiadomienie(f"Drzwi/okno zostało zamknięte. {ts}")
    led_czerwona.value(0)

stan_poprzedni = kontaktron.value()


print("System gotowy. Monitoruję kontaktron...")
wyslij_powiadomienie("System gotowy. Monitoruję kontaktron...")

while True:
    stan = kontaktron.value()
    if stan != stan_poprzedni:
        if stan == 1:   # zwolniony (pull-up) → drzwi otwarte
            otwarcie()
        else:
            zamkniecie()
        stan_poprzedni = stan
    time.sleep(0.05)  # odczyt co 50 ms
