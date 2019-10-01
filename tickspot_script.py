import requests
import click

API_URL = 'https://www.tickspot.com/79559/api/v2/'


@click.command()
@click.option('--token', 'api_token', required=True, help='Your api token')
@click.option('--email', help='Your email')
@click.option('--user_agent', default='MyCoolApp', help='Optional name for User-Agent')
def main_method(api_token, email, user_agent):
    headers = {
        'Authorization': f'Token token={api_token}',
        'User-Agent': f'{user_agent} ({email})',
    }

    r = requests.get(API_URL + 'projects.json', headers=headers)
    print(r.text)


if __name__ == '__main__':
    main_method()
