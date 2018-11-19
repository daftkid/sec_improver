import boto3
import json
from os import environ
from botocore import exceptions
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from jinja2 import Template, Environment, FileSystemLoader
from datetime import datetime

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
    parser.add_argument('-o', '--output', help='Path to file with report', dest='output', default='./keys_report.html')

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


def get_list_of_keys(session, users):
    try:
        iam = session.client('iam')

        resp = []
        res = []

        for username in users:
            resp.extend(iam.list_access_keys(
                UserName=username
            )['AccessKeyMetadata'])

        for item in resp:
            temp = {}
            temp['key_id'] = item['AccessKeyId']
            temp['username'] = item['UserName']
            temp['status'] = item['Status']
            temp['date_created'] = item['CreateDate']
            temp['key_age'] = 'test'#calc_key_age(item['CreateDate'])
            res.append(temp)

        return res
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


def render_template_keys(path, data):
    env = Environment(loader=FileSystemLoader(searchpath='./templates/'))
    template = env.get_template('key_report.j2')

    render_template = template.render(data=data)
    with open(path, 'w') as result_file:
        result_file.write(render_template)
