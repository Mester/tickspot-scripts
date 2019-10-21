from datetime import timedelta
import requests
import click

API_URL = 'https://www.tickspot.com/79559/api/v2/'


@click.command()
@click.option('--token', 'api_token', required=True, help='Your api token')
@click.option('--email', required=True, help='Your email')
@click.option('--from_date', type=click.DateTime(['%Y-%m-%d']), required=True, help='Starting day')
@click.option('--to_date', type=click.DateTime(['%Y-%m-%d']), required=True, help='Last day (including)')
@click.option('--user_agent', default='MyCoolApp', help='Optional name for User-Agent')
def main_method(api_token, email, from_date, to_date, user_agent):
    headers = {
        'Authorization': f'Token token={api_token}',
        'User-Agent': f'{user_agent} ({email})',
    }

    create_entries(12453101, headers, from_date, to_date)


def create_entries(task_id, headers, from_date, to_date, hours=8, notes=""):
    url = API_URL + "entries.json"

    for single_date in daterange(from_date, to_date):
        data = {
            "date": single_date.strftime('%Y-%m-%d'),
            "hours": hours,
            "notes": notes,
            "task_id": task_id,
        }
        r = requests.post(url, json=data, headers=headers)


def daterange(from_date, to_date):
    for n in range(int((to_date - from_date).days + 1)):
        yield from_date + timedelta(n)


if __name__ == '__main__':
    main_method()
