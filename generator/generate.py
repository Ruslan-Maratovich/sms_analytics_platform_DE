import uuid
import random
import argparse

from datetime import datetime, timedelta
import clickhouse_connect

SENDERS = [
    "Google", "Steam", "Amazon", "PayPal", "Uber", "WhatsApp", "Meta",
        "Grab", "Airbnb", "Netflix", "LinkedIn", "Outlook", "Twilio", "DHL",
        "Vodafone", "monitoring", "Spotify", "Bolt", "not_defined"]

COUNTRIES = [
    "Russian Federation", "Kazakhstan", "Azerbaijan", "Kyrgyzstan", "Tajikistan",
    "Belarus", "Uzbekistan", "Armenia", "Georgia", "Israel", "Moldova", "Abkhazia",
    "not_defined"]

COUNTRY_CODES = {
    "Russian Federation": "7",
    "Kazakhstan": "7",
    "Azerbaijan": "994",
    "Kyrgyzstan": "996",
    "Tajikistan": "992",
    "Belarus": "375",
    "Uzbekistan": "998",
    "Armenia": "374",
    "Georgia": "995",
    "Israel": "972",
    "Moldova": "373",
    "Abkhazia": "840",
}


STATUSES = [
    "DELIVRD", "UNDELIV", "EXPIRED", "NO ROUTES", "SENT", "ROUTE FAILED",
    "REJECTD", "VND CHN NOT BND", "SUBMIT_RESP TIMEOUT", "UNKNOWN"
]

RECEIVER_OPERATORS = [
    "MTS", "Beeline", "MegaFon", "Azercell", "MKS", "Tele2", "All networks",
    "MEGACOM(Alfa Telecom)", "Indigo Tajikistan", "Beeline (Sky Mobile)", "K-Cell",
    "O!(Nurtelecom)", "Scartel", "MobiUZ (MTS)", "velcom", "Altel", "not_defined"
]

def generate_receiver_and_country():
    country = random.choice(COUNTRIES)

    if country == "not_defined":
        # Просто случайный номер без привязки к стране
        receiver = random.randint(3_000_000_000, 99_999_999_999)
    else:
        code = COUNTRY_CODES[country]
        subscriber = "".join(random.choices("0123456789", k=8))
        receiver = int(code + subscriber)

    return {
        "country": country,
        "receiver": receiver,
    }

def generate(rows: int):

    client = clickhouse_connect.get_client(
    host="clickhouse",
    port=8123,
    username="default",
    password="default123",
    database="sms"
    )   

    apps = []
    # создаем клиентов 1-10 с индентификаторами UUID
    # customer_id 
    # application_uuid
    # message_id
    for customer in range(1, 11):
        for _ in range(4):
            apps.append((customer, uuid.uuid4()))
    batch = []
    start = datetime(2025, 1, 1)

    for _ in range(1_000_000):
    #    рандомный выбор customer_id с application_uuid
        customer, app = random.choice(apps)

    #   Дата/время отправки SMS
    #    31 536 000 - секунд в году, то есть с 2025 по 2026 согласно ТЗ
        sent = start + timedelta(
            seconds=random.randint(1, 31_536_000)
        )
    #   генерируем country и receiver
        receiver = generate_receiver_and_country()

    #   формируем поле для таблицы messages_mart 
        row = (
    #           customer_id
                customer,
    #           application_uuid
                app,
    #           message_id
                uuid.uuid4(),
    #           sent_date
                sent,
    #           sender
                random.choice(SENDERS),
    #           receiver
                receiver["receiver"],
    #           country
                receiver["country"],
    #           segment_count 1-14
                random.randint(1, 14),
    #           delivery_status
                random.choice(STATUSES),
    #           attempt_number 1-3
                random.randint(1, 3),
    #           delivery_time
                random.randint(100, 3000),
    #           price sms 0.0-1.0
                round(random.random(), 1),
    #           currency
                "USD",
    #           receiver_operator
                random.choice(RECEIVER_OPERATORS),
    #           direction
                random.randint(0, 1),
    #           metadate 
    #           created_at
                sent,
    #           updated_at
                sent,
    #           deleted_at
                None
            )
        batch.append(row)
        if len(batch) == 10_000:
            client.insert("sms.messages_mart", batch)
            batch = []


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=1_000_000)

    args = parser.parse_args()

    generate(args.rows)