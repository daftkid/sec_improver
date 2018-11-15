#!/usr/bin/env python3

__author__ = 'Oleksandr Mykytenko'
__copyright__ = 'Copyright 2018, Mykytenko O.O.'
__email__ = ['alexandr.mykytenko@gmail.com']
__version__ = '0.0.1'

from diploma_lib.main_lib import *

TOOL_NAME = 'key_scanner'


def scanner(opts):
    # Read command line arguments
    if opts.ver:
        print('IAM Key Scanner ver {}'.format(__version__))
        print(LOGO)
        exit(0)

    debug_mode = opts.debug

    # Reading environment variables
    if debug_mode: info('Reading ENV vars')
    env = read_env()

    # Create session for accessing cloud account
    if debug_mode: info('Creating session')
    session = create_cloud_session(env)


if __name__ == '__main__':
    opts = options_parser(TOOL_NAME).parse_args()
    scanner(opts)
