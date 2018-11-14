#!/usr/bin/env python3

from diploma_lib.main_lib import *


def scanner():
    debug_mode = True

    # Reading environment variables
    if debug_mode: info('Reading ENV vars')
    env = read_env()

    # Create session for accessing cloud account
    if debug_mode: info('Creating session')
    session = create_cloud_session(env)


if __name__ == '__main__':
    scanner()
