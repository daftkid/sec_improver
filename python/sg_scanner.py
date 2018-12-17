#!/usr/bin/env python3

__author__ = 'Oleksandr Mykytenko'
__copyright__ = 'Copyright 2018, Mykytenko O.O.'
__email__ = ['alexandr.mykytenko@gmail.com']
__version__ = '0.0.1'

from diploma_lib.main_lib import *

TOOL_NAME = 'sg_scanner'


def scanner(opts):
    # Read command line arguments
    if opts.ver:
        print('SG Scanner ver {}'.format(__version__))
        print(LOGO)
        exit(0)

    debug_mode = opts.debug

    input = opts.input
    if not opts.html_output:
        error('Please specify path to HTML output file!')
    else:
        html_output = opts.html_output
    if not opts.csv_output:
        error('Please specify path to CSV output file!')
    else:
        csv_output = opts.csv_output
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

    # Listing all SGs in the account
    if debug_mode: info('Getting list of security groups')
    sgs = get_list_of_sgs(session)
    if debug_mode:
        print_separator()
        for sg in sgs:
            info('SG ID: {}'.format(sg['GroupId']))
        print_separator()

    # Parsing the data
    if debug_mode: info('Parsing data')
    sec_groups = parse_sgs(sgs)

    render_template_sgs(html_output, sec_groups)

    print(json.dumps(sec_groups, indent=4))


if __name__ == '__main__':
    opts = options_parser(TOOL_NAME).parse_args()
    scanner(opts)
