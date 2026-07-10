import clickhouse_connect
import requests
from datetime import datetime
import time


NAGER_URL = "https://date.nager.at/api/v4/Holidays"
YEAR = datetime.now().year
headers = {
    "User-Agent": "sms-analytics-platform/1.0"
}

def get_client():

    return clickhouse_connect.get_client(
        host="clickhouse01",
        port=8123,
        username="default",
        password="default123",
        database="sms"
    )


def get_countries(client):

    countries = [
        row[0].decode()
        if isinstance(row[0], bytes)
        else row[0]
        for row in client.query(
            """
            SELECT country_code
            FROM sms.country_dictionary
            """
        ).result_rows]
    
    print(countries)
    return countries
    



def fetch_holidays(country):

    url = (
        f"https://date.nager.at/api/v4/Holidays/{country}/{YEAR}"
    )

    print(url)

    response = requests.get(
        url,
        timeout=10
    )

    print(
        country,
        response.status_code,
        response.headers.get("content-type")
    )

    if response.status_code != 200:
        print(
            response.text[:200]
        )
        return []

    try:
        return response.json()

    except requests.exceptions.JSONDecodeError:

        print(
            f"Invalid JSON from {country}"
        )

        print(
            response.text[:500]
        )

        return []



def insert_holidays(client, holidays):

    rows = []

    now = datetime.now()


    for h in holidays:

        rows.append(
            (
                h["countryCode"],
                datetime.strptime(h["date"],"%Y-%m-%d").date(),
                h["name"],
                h.get("localName", h["name"]),
                h.get("holidayTypes", []),
                now,
                now
            )
        )

    if rows:
        client.insert(
            "sms.public_holidays",
            rows,
            column_names=[
                "country_code",
                "holiday_date",
                "holiday_name",
                "local_name",
                "holiday_type",
                "created_at",
                "updated_at"
            ]
        )
    time.sleep(1)



def main():

    client = get_client()

    countries = get_countries(client)


    total = 0


    for country in countries:

        holidays = fetch_holidays(
            country
        )

        insert_holidays(
            client,
            holidays
        )

        total += len(holidays)


        print(
            f"{country}: {len(holidays)}"
        )


    print(
        f"Loaded: {total}"
    )



if __name__ == "__main__":
    main()