#!/usr/bin/env python3

__author__ = 'Oleksandr Mykytenko'
__copyright__ = 'Copyright 2018, Mykytenko O.O.'
__email__ = ['alexandr.mykytenko@gmail.com']
__version__ = '0.0.1'

from diploma_lib.main_lib import *

TOOL_NAME = 'key_scanner'
THRESHOLD = 90


def scanner(opts):
    # Read command line arguments
    if opts.ver:
        print('IAM Key Scanner ver {}'.format(__version__))
        print(LOGO)
        exit(0)

    debug_mode = opts.debug

    input = opts.input
    output = opts.output
    enforce = opts.enforce

    if enforce:
        if not input:
            error('Please specify value for `input` parameter while using `enforce` option')

    # Reading environment variables
    if debug_mode: info('Reading ENV vars')
    env = read_env()

    # Create session for accessing cloud account
    if debug_mode: info('Creating session')
    session = create_cloud_session(env)

    # Listing all Users in account
    if debug_mode: info('Getting list of all users')
    users = get_list_of_users(session)
    if debug_mode:
        print_separator()
        for user in users:
            info('UserName: {}'.format(user))
        print_separator()

    # Listing all IAM keys in account
    if debug_mode: info('Getting list of keys')
    keys = get_list_of_keys(session, users)
    if debug_mode:
        print_separator()
        for key in keys:
            info('Key ID: {}'.format(key))
        print_separator()

    parameters = [
        {
            'name': 'Age Threshold',
            'value': THRESHOLD
        }
    ]

    render_template_keys(output, keys, parameters)


if __name__ == '__main__':
    opts = options_parser(TOOL_NAME).parse_args()
    scanner(opts)
