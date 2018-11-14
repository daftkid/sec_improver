import boto3
import json
from os import environ
from botocore import exceptions


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


def get_list_of_keys(session):
    pass


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
