#!/usr/bin/env python3

__author__ = 'Oleksandr Mykytenko'
__copyright__ = 'Copyright 2018, Mykytenko O.O.'
__email__ = ['alexandr.mykytenko@gmail.com']
__version__ = '0.0.1'

from diploma_lib.main_lib import *

with open('test_data.json', 'r') as data_file:
    data = json.load(data_file)
    render_template_keys('/tmp/keys_report.html', data)
