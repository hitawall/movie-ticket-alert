import requests
import time
import os
from bs4 import BeautifulSoup
from twilio.rest import Client

MOVIE = "dhurandar"
DATE = "18"
MONTH = "march"

URL = "https://www.cinepolisindia.com/bengaluru/cinepolis-nexus-shantiniketan"

ALERT_SENT = False


def check_showtimes():

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(URL, headers=headers)

    soup = BeautifulSoup(r.text, "html.parser")

    text = soup.get_text().lower()

    if MOVIE in text and DATE in text and MONTH in text:
        return True

    return False


def send_whatsapp():

    account_sid = os.environ["TWILIO_SID"]
    auth_token = os.environ["TWILIO_TOKEN"]

    client = Client(account_sid, auth_token)

    client.messages.create(
        from_='whatsapp:+14155238886',
        body="🚨 DHURANDAR tickets available for March 18 at Cinepolis Nexus Shantiniketan!",
        to='whatsapp:+918295446444'
    )


def run():

    global ALERT_SENT

    while True:

        print("Checking Cinepolis Nexus Shantiniketan...")

        available = check_showtimes()

        if available and not ALERT_SENT:
            print("Tickets detected!")
            send_whatsapp()
            ALERT_SENT = True

        time.sleep(30)


if __name__ == "__main__":
    run()
