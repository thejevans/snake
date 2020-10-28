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
from collections import deque
from itertools import product
import time
import random
import curses

OPair = Tuple[int, int]

KEYMAP = {
    keyboard.Key.up:'up',
    keyboard.Key.down:'down',
    keyboard.Key.left:'left',
    keyboard.Key.right:'right',
}

class Snake:
    """Class info...

    More class info...

    Attributes:
        size (OPair):
        growth (int):
        coil (int):
        head (OPair):
        tail (collections.Deque):
        food (OPair):
        score (int):
        window (curses.window):
        win_size (OPair):
        to_remove (List[OPair]):
    """
    def __init__(self, size: OPair, growth: int, window: curses.window
    ) -> None:
        """Initializes the snake object.

        More function info...

        Args:
            size: Size of the playing field in (x, y).
            growth: Growth rate of the snake.
        """
        self.size = size
        self.win_size = (size[1] + 2, size[0] + 2)
        self.growth = growth
        self.coil = 0
        self.head = (size[0]//2, size[1]//2)
        self.tail = deque([(self.head[0], self.head[1]-1),
                           (self.head[0], self.head[1]-2),
                          ])
        self.food = (size[0]//2, 3*size[1]//4)
        self.score = 0
        self.window = window
        self.to_remove = []

    def update_display(self, debug: bool = False) -> None:
        """Function info...

        More function info...
        """
        if debug:
            self.window.move(1, 1)
            self.window.addstr('Head: ' + str(self.head))

            self.window.move(2, 1)
            self.window.addstr('Food: ' + str(self.food))

            self.window.move(3, 1)
            if self.collision():
                self.window.addstr('Collision!')
            else:
                self.window.addstr(' '*10)

        self.window.move(0, self.win_size[1]//2)
        self.window.addstr(str(self.score))

        self.window.move(self.size[1] - self.food[1] - 1, self.food[0] + 1)
        self.window.addch('o')

        for x, y in self.to_remove:
            self.window.move(self.size[1] - y - 1, x + 1)
            self.window.addch(' ')

        self.to_remove = []

        self.window.move(self.size[1] - self.head[1] - 1, self.head[0] + 1)
        self.window.addch('O')

        self.window.move(self.size[1] - self.tail[0][1] - 1, self.tail[0][0] + 1)
        self.window.addch('*')

        self.window.refresh()

    def move(self, direction: str) -> None:
        """Function info...

        More function info...

        Args:
            direction: The direction to move the head.
        """
        self.tail.appendleft(self.head)

        if self.coil <= 0:
            self.to_remove.append(self.tail.pop())
        else:
            self.coil -= 1

        if direction == 'up':
            self.head = (self.head[0], self.head[1] + 1)
        elif direction == 'down':
            self.head = (self.head[0], self.head[1] - 1)
        elif direction == 'left':
            self.head = (self.head[0] - 1, self.head[1])
        elif direction == 'right':
            self.head = (self.head[0] + 1, self.head[1])

        self.score += 1

    def collision(self) -> bool:
        """Function info...

        More function info...

        Returns:
            True if head is somewhere it's not supposed to be, False otherwise.
        """
        if self.head in self.tail:
            return True
        if not (0 < self.head[0] < self.size[0]):
            return True
        if not (0 < self.head[1] < self.size[1]):
            return True

        if self.head == self.food:
            self.eat()
            return True

        return False

    def eat(self) -> None:
        """Function info...

        More function info...
        """
        self.coil = self.growth
        self.food = random.choice(self.inverse_snake())
        self.score += 10

    def inverse_snake(self) -> List[OPair]:
        """Function info...

        More function info...

        Returns:
            A list of ordered pairs of the playing field where the snake isn't.
        """
        inverse = []
        for x, y in product(range(self.size[0]), range(self.size[1])):
            if (x, y) not in self.tail and [x, y] != self.head:
                inverse.append((x, y))
        return inverse

class SnakeDisplay:
    """Class info...

    More Class info...

    Attributes:
        snake (Snake):
        window (curses.window)
        size (OPair):
        growth (int):
        win_size (OPair):
    """
    def __init__(self, size: OPair, growth: int) -> None:
        """Function info:

        More function info...

        Args:
            size:
            growth:
        """
        self.win_size = (size[1] + 2, size[0] + 2)
        self.size = size
        self.growth = growth
        self.window = None
        self.snake = None

    def __enter__(self) -> Snake:
        """Function info...

        More function info...

        Returns:
            
        """
        self.window = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.window.keypad(True)
        self.window.clear()
        self.init_display()
        self.snake = Snake(self.size, self.growth, self.window)
        return self.snake

    def __exit__(self, type, value, traceback) -> None:
        """Function info...

        More function info...

        Args:
            type:
            value:
            traceback:
        """
        curses.nocbreak()
        self.window.keypad(False)
        curses.echo()
        curses.endwin()

    def init_display(self) -> None:
        """Function info...

        More function info...
        """
        outer = ''.join(['+', '-'*(self.win_size[1] - 2), '+'])
        inner = ''.join(['|', ' '*(self.win_size[1] - 2), '|'])

        self.window.addstr(0, 0, outer)
        self.window.addstr(self.win_size[0] - 1, 0, outer)

        for i in range(self.win_size[0] - 2):
            self.window.addstr(i + 1, 0, inner)

        self.window.refresh()

if __name__ == '__main__':
    TICK = 0.0625
    SIZE = (50, 25)
    GROWTH = 3
    previous = 'up'

    with keyboard.Events() as events, SnakeDisplay(SIZE, GROWTH) as snake:

        t_i = time.perf_counter()

        while not snake.collision():
            event = events.get(TICK)

            if event is not None:
                if event.key == keyboard.Key.esc:
                    break
                elif event.key in KEYMAP:
                    previous = KEYMAP[event.key]

            if (time.perf_counter() - t_i) > TICK:
                t_i = time.perf_counter()
                snake.move(previous)
                snake.update_display(debug=True)

    print('GAME OVER')
    input("Press the <ENTER> key to continue...")
