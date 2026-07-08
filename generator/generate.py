import uuid
import random
import argparse
import time

from datetime import datetime, timedelta

import clickhouse_connect

SENDERS = [
    "Google",
    "Steam",
    "Amazon",
    "PayPal",
    "Uber",
    "WhatsApp",
    "Meta",
    "Grab",
    "Airbnb",
    "Netflix",
    "LinkedIn",
    "Outlook",
    "Twilio",
    "DHL",
    "Vodafone",
    "monitoring",
    "Spotify",
    "Bolt",
    "not_defined"
]

COUNTRIES = [
    "Russian Federation",
    "Kazakhstan",
    "Azerbaijan",
    "Kyrgyzstan",
    "Tajikistan",
    "Belarus",
    "Uzbekistan",
    "Armenia",
    "Georgia",
    "Israel",
    "Moldova",
    "Abkhazia",
    "not_defined"
]

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
    "DELIVRD",
    "UNDELIV",
    "EXPIRED",
    "NO ROUTES",
    "SENT",
    "ROUTE FAILED",
    "REJECTD",
    "VND CHN NOT BND",
    "SUBMIT_RESP TIMEOUT",
    "UNKNOWN"
]

RECEIVER_OPERATORS = [
    "MTS",
    "Beeline",
    "MegaFon",
    "Azercell",
    "MKS",
    "Tele2",
    "All networks",
    "MEGACOM(Alfa Telecom)",
    "Indigo Tajikistan",
    "Beeline (Sky Mobile)",
    "K-Cell",
    "O!(Nurtelecom)",
    "Scartel",
    "MobiUZ (MTS)",
    "velcom",
    "Altel",
    "not_defined"
]

BATCH_SIZE = 10000


def create_client():

    while True:
        try:
            client = clickhouse_connect.get_client(
                host="clickhouse01",
                port=8123,
                username="default",
                password="default123",
                database="sms"
            )
            client.command("SELECT 1")
            print("ClickHouse is ready")
            return client
        except Exception as e:
            print(
                f"Waiting ClickHouse... {e}"
            )
            time.sleep(5)



def generate_receiver_and_country():

    country = random.choice(COUNTRIES)

    if country == "not_defined":
        receiver = random.randint(
            3_000_000_000,
            99_999_999_999
        )
    else:
        code = COUNTRY_CODES[country]
        subscriber = "".join(
            random.choices(
                "0123456789",
                k=8
            )
        )
        receiver = int(
            code + subscriber
        )
    return {
        "country": country,
        "receiver": receiver
    }



def generate(rows: int):

    client = create_client()
    apps = []

    # 10 клиентов
    # у каждого 4 приложения
    for customer_id in range(1, 11):
        for _ in range(4):
            apps.append(
                (
                    customer_id,
                    uuid.uuid4()
                )
            )
    batch = []
    start = datetime(
        2025,
        1,
        1
    )
    inserted = 0

    for _ in range(rows):
        customer_id, application_uuid = random.choice(
            apps
        )
        sent_date = start + timedelta(
            seconds=random.randint(
                1,
                31_536_000
            )
        )
        receiver = generate_receiver_and_country()
        row = (
            customer_id,
            application_uuid,
            uuid.uuid4(),
            sent_date,
            random.choice(SENDERS),
            receiver["receiver"],
            receiver["country"],
            random.randint(1,14),
            random.choice(STATUSES),
            random.randint(1,3),
            random.randint(100,3000),
            round(random.random(),2),
            "USD",
            random.choice(RECEIVER_OPERATORS),
            random.randint(0,1),
            sent_date,
            sent_date,
            None
        )
        batch.append(row)

        if len(batch) >= BATCH_SIZE:
            client.insert(
                "sms.messages_mart",
                batch
            )
            inserted += len(batch)
            print(
                f"Inserted {inserted}/{rows}"
            )
            batch = []
    # остаток

    if batch:
        client.insert("sms.messages_mart", batch)
        inserted += len(batch)
        print(f"Inserted {inserted}/{rows}")

    print("Generation completed")



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--rows",
        type=int,
        default=1_000_000
    )
    args = parser.parse_args()
    generate(args.rows)