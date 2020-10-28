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

from typing import List, Tuple

from pynput import keyboard

OPair = Tuple[int, int]

KEYMAP = {'':'up', '':'down', '':'left', '':'right'}

class Snake:
    """
    Class Docstring
    """
    def __init__(self, size: OPair, growth: int) -> None:
        return NotImplementedError

    def display(self) -> None:
        return NotImplementedError

    def move(self, direction: str) -> bool:
        return NotImplementedError

    def collision(self) -> bool:
        return NotImplementedError

    def eat(self) -> None:
        return NotImplementedError

if __name__ == '__main__':
    TICK = 0.5
    SIZE = (50, 50)
    GROWTH = 3
    snake = Snake(SIZE, GROWTH)
    previous = 'up'

    snake.display()

    with keyboard.Events() as events:
        t_i = time.perf_counter()

        while ~snake.collision():
            event = events.get(TICK)

            if event is not None:
                previous = KEYMAP[event]

            if (time.perf_counter() - t_i) > TICK:
                t_i = time.perf_counter()
                snake.move(previous)
                snake.display()

    print('GAME OVER')
    input("Press the <ENTER> key to continue...")

