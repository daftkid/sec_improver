import boto3
import json
import csv
from os import environ
from botocore import exceptions
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from jinja2 import Template, Environment, FileSystemLoader
from datetime import datetime, timezone

TOOLS = {
    'key_scanner': '',
    'sg_scanner': '',
    'unused_res_scanner': ''
}

LOGO = 'Designed and developed by Oleksandr Mykytenko, Kharkiv, Ukraine, 2018'


def read_env():
    res = {
        'cloud_secret_key_id': environ.get('AWS_ACCESS_KEY_ID'),
        'cloud_secret_access_key': environ.get('AWS_SECRET_ACCESS_KEY')
    }

    return res


def create_cloud_session(creds):
    try:
        session = boto3.Session(
            aws_access_key_id=creds['cloud_secret_key_id'],
            aws_secret_access_key=creds['cloud_secret_access_key']
        )
        return session
    except exceptions.ClientError as e:
        error(e)


def options_parser(tool):
    if tool not in TOOLS:
        error('Non-existent tool is provided: {}'.format(tool))

    parser = ArgumentParser(
        description=TOOLS[tool],
        formatter_class=ArgumentDefaultsHelpFormatter
    )

    parser.add_argument('-D', '--debug', help='Enable Debug mode', action='store_true', dest='debug', default=False)
    parser.add_argument('-v', '--version', help='Print the current version of the tool', action='store_true', dest='ver')

    parser.add_argument('-e', '--enforce', help='Specify if it is needed to apply changes', action='store_true', dest='enforce', default=False)

    parser.add_argument('-i', '--input', help='Path to the file which has to be applied', dest='input')
    parser.add_argument('-r', '--html-output', help='Path to file with HTML report', dest='html_output', default='./keys_report.html')
    parser.add_argument('-c', '--csv-output', help='Path to file with CSV report', dest='csv_output', default='./keys_report.csv')

    return parser


def get_list_of_users(session):
    try:
        iam = session.client('iam')

        paginator = iam.get_paginator('list_users')
        pages = paginator.paginate()

        users = []

        for page in pages:
            for user in page['Users']:
                users.append(user['UserName'])

        return users

    except Exception as e:
        error(e)


def get_list_of_keys(session, users, threshold=90):
    try:
        iam = session.client('iam')

        resp = []
        res = []

        for username in users:
            resp.extend(iam.list_access_keys(
                UserName=username
            )['AccessKeyMetadata'])

        for item in resp:
            time_delta = datetime.now().replace(tzinfo=timezone.utc) - item['CreateDate']
            temp = {
                'key_id': item['AccessKeyId'],
                'username': item['UserName'],
                'status': item['Status'],
                'date_created': item['CreateDate'].strftime('%x %X'),
                'last_used': key_last_used(iam, item['AccessKeyId']),
                'key_age': time_delta.days
            }

            if temp['key_age'] > threshold:
                temp['action'] = 'remove'
            else:
                temp['action'] = 'not required'

            res.append(temp)

        sorted_res = sorted(res, key=lambda x: x['key_age'], reverse=True)

        return sorted_res
    except KeyError as e:
        error('Wrong key: {}'.format(e))
    except exceptions.ClientError as e:
        error(e)


def key_last_used(client, key_id):
    try:
        iam = client

        res = iam.get_access_key_last_used(
            AccessKeyId=key_id
        )

        if 'LastUsedDate' in res['AccessKeyLastUsed']:
            return res['AccessKeyLastUsed']['LastUsedDate'].strftime('%x %X')
        else:
            return 'N/A'
    except KeyError as e:
        error('Wrong key: {}'.format(e))
    except exceptions.ClientError as e:
        error(e)


def calc_key_age(timestamp):
    now = datetime.utcnow()
    return now - timestamp


def error(msg):
    banner = '[ ERROR ]'
    print('{} {}'.format(banner, msg))
    exit(1)


def info(msg):
    banner = '[ INFO  ]'
    print('{} {}'.format(banner, msg))


def warn(msg):
    banner = '[ WARN  ]'
    print('{} {}'.format(banner, msg))


def print_separator():
    print('===========================================')


def render_template_keys(path, data, parameters):
    env = Environment(loader=FileSystemLoader(searchpath='./templates/'))
    template = env.get_template('key_report.j2')

    now = datetime.now()

    render_template = template.render(data=data, time=datetime.strftime(now, '%x %X'), parameters=parameters)
    if 'html' not in path:
        path = '{}/keys_report_{}.html'.format(path, datetime.strftime(now, '%Y-%m-%d_%H-%M'))
    with open(path, 'w') as result_file:
        result_file.write(render_template)

    info('HTML Report has been generated! Please review the file {}'.format(path))
    return path


def write_to_csv(path, data):
    if not len(data):
        warn('Input data for writing into CSV file is empty! CSV will not be written')
        return ''
    if 'csv' not in path:
        path = '{}/keys_report_{}.csv'.format(path, datetime.strftime(datetime.now(), '%Y-%m-%d_%H-%M'))
    with open(path, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
        writer.writeheader()

        for row in data:
            writer.writerow(row)

    info('CSV Report has been generated! Please review the file {}'.format(path))
    return path


def generate_parameter(key, value):
    return {
        'name': key,
        'value': value
    }
