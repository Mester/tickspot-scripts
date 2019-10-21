from datetime import timedelta
import requests
import click

API_URL = 'https://www.tickspot.com/79559/api/v2/'


@click.group()
@click.option('--token', 'api_token', required=True, help='Your api token')
@click.option('--email', required=True, help='Your email')
@click.option('--user_agent', default='MyCoolApp', help='Optional name for User-Agent')
@click.pass_context
def cli(ctx, api_token, email, user_agent):
    headers = {
        'Authorization': f'Token token={api_token}',
        'User-Agent': f'{user_agent} ({email})',
    }
    ctx.ensure_object(dict)
    ctx.obj['HEADERS'] = headers


@cli.command()
@click.option('--task_id', type=click.INT, required=False, help='Id for the task')
@click.option('--from_date', type=click.DateTime(['%Y-%m-%d']), required=False, help='Starting day')
@click.option('--to_date', type=click.DateTime(['%Y-%m-%d']), required=False, help='Last day (including)')
@click.option('--hours', default=8, help='Amount of hours to fill in')
@click.option('--notes', default="", help='Optional note to fill in')
@click.pass_context
def create_entries(ctx, task_id, from_date, to_date, hours, notes):
    url = API_URL + "entries.json"

    for single_date in daterange(from_date, to_date):
        data = {
            "date": single_date.strftime('%Y-%m-%d'),
            "hours": hours,
            "notes": notes,
            "task_id": task_id,
        }
        # r = requests.post(url, json=data, headers=ctx.obj['HEADERS'])
        r = click.echo(url)
        r = click.echo(data)
        r = click.echo(ctx.obj['HEADERS'])


def daterange(from_date, to_date):
    for n in range(int((to_date - from_date).days + 1)):
        yield from_date + timedelta(n)


if __name__ == '__main__':
    cli()
