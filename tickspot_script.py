from datetime import timedelta, date

import click
import requests

API_URL = 'https://www.tickspot.com/79559/api/v2'


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
@click.option('--task_id', type=click.INT, required=True, help='Id for the task')
@click.option('--from_date', type=click.DateTime(['%Y-%m-%d']), required=True, help='Starting day')
@click.option('--to_date', type=click.DateTime(['%Y-%m-%d']), required=True, help='Last day (including)')
@click.option('--hours', default=8, help='Amount of hours to fill in')
@click.option('--notes', default="", help='Optional note to fill in')
@click.pass_context
def create_entries(ctx, task_id, from_date, to_date, hours, notes):
    url = API_URL + "/entries.json"

    for single_date in daterange(from_date, to_date):
        data = {
            "date": single_date.strftime('%Y-%m-%d'),
            "hours": hours,
            "notes": notes,
            "task_id": task_id,
        }
        r = requests.post(url, json=data, headers=ctx.obj['HEADERS'])


@cli.command()
@click.option('--task_id', type=click.INT, required=True, help='Id for the task')
@click.option('--hours', default=8, help='Amount of hours to fill in')
@click.option('--notes', default="", help='Optional note to fill in')
@click.pass_context
def create_entry_today(ctx, task_id, hours, notes):
    url = API_URL + "/entries.json"

    data = {
        "date": date.today().strftime('%Y-%m-%d'),
        "hours": hours,
        "notes": notes,
        "task_id": task_id,
    }
    requests.post(url, json=data, headers=ctx.obj['HEADERS'])


@cli.command()
@click.option('--project_id', help="Id for the project to get list of tasks from")
@click.pass_context
def get_tasks(ctx, project_id):
    if project_id:
        url = API_URL + f'/projects/{project_id}/tasks.json'
    else:
        url = API_URL + '/tasks.json'

    r = requests.get(url, headers=ctx.obj['HEADERS'])
    try:
        r.raise_for_status()
        for task in r.json():
            click.echo(f'id: {task["id"]}, name: {task["name"]}, project_id: {task["project_id"]}')
    except Exception as e:
        click.echo(e)
        click.echo(f'{r.text} {r.status_code}')


@cli.command()
@click.option('--project_id', help='Specific project to get info on')
@click.pass_context
def get_projects(ctx, project_id):
    if project_id:
        url = API_URL + f'/projects/{project_id}.json'
    else:
        url = API_URL + '/projects.json'

    r = requests.get(url, headers=ctx.obj['HEADERS'])
    try:
        r.raise_for_status()
        if project_id:
            project = r.json()
            click.echo(f'id: {project["id"]}, name: {project["name"]}')
        else:
            for project in r.json():
                click.echo(f'id: {project["id"]}, name: {project["name"]}')
    except Exception as e:
        click.echo(e)
        click.echo(f'{r.text} {r.status_code}')


def daterange(from_date, to_date):
    for n in range(int((to_date - from_date).days + 1)):
        yield from_date + timedelta(n)


if __name__ == '__main__':
    cli()
