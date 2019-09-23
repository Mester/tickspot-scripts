import requests
import click

API_URL = 'https://www.tickspot.com/**/api/v2/'
API_TOKEN = '**'
EMAIL = '**'


@click.command()
def main_method():
    headers = {
        'Authorization': 'Token token={}'.format(API_TOKEN),
        'User-Agent': 'MyCoolApp ({})'.format(EMAIL),
    }

    r = requests.get(API_URL + 'projects.json', headers=headers)
    print(r)


if __name__ == '__main__':
    main_method()
