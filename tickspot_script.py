from pprint import pprint
import requests
import click

API_URL = 'https://www.tickspot.com/79559/api/v2/'


@click.command()
@click.option('--token', 'api_token', required=True, help='Your api token')
@click.option('--email', required=True, help='Your email')
@click.option('--user_agent', default='MyCoolApp', help='Optional name for User-Agent')
def main_method(api_token, email, user_agent):
    headers = {
        'Authorization': f'Token token={api_token}',
        'User-Agent': f'{user_agent} ({email})',
    }

    payload = {'start_date': "'2019-10-01'", 'end_date': "'2019-10-14'"}

    r = requests.get(API_URL + 'entries.json', headers=headers, params=payload)
    print(r.text)
    # pprint(r.json())

    create_entry("'2019-10-14'", 12453101, headers)


def create_entry(date, task_id, headers, hours=8, notes=""):
    url = API_URL + "entries.json"
    data = {
        "date": date,
        "hours": hours,
        "notes": notes,
        "task_id": task_id,
        # "user_id": 343724
    }

    r = requests.post(url, json=data, headers=headers)
    print(r.text)
    # print(r.headers)
    pprint(r.json())


if __name__ == '__main__':
    main_method()
