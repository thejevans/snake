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
from pynput import keyboard
import time
import curses

if __name__ == '__main__':
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    stdscr.clear()
    stdscr.addstr(1, 0, 'Press ESC to quit...')
    stdscr.addstr(0, 0, 'Key: ')
    with keyboard.Events() as events:
        while True:
            event = events.get()
            if event.key == keyboard.Key.esc:
                break
            stdscr.move(0, 5)
            stdscr.clrtoeol()
            stdscr.addstr(event.key.__repr__())
            stdscr.refresh()

    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
