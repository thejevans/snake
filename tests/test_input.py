__author__ = 'John Evans'
__copyright__ = 'Copyright 2020 John Evans'
__credits__ = ['John Evans']
__license__ = 'Apache License 2.0'
__version__ = '0.0.1'
__maintainer__ = 'John Evans'
__email__ = 'thejevans@gmail.com'
__status__ = 'Development'

"""
Docstring
"""

import sys
import select
import time

if __name__ == '__main__':
    while True:
        timeout = 1
        rlist, wlist, xlist = select.select([sys.stdin], [], [], timeout)
        print(rlist)
