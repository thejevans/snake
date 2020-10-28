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

OPair = Tuple[int, int]

KEYMAP = {'':'up', '':'down', '':'left', '':'right'}

class Snake:
    """Class info...

    More class info...

    Attributes:
        size (Tuple[int, int]):
        growth (int):
        coil (int):
        head (Tuple[int, int]):
        tail (collections.Deque):
        food (Tuple[int, int]):
        score (int):

    """
    def __init__(self, size: OPair, growth: int) -> None:
        """Initializes the snake object.

        More function info...

        Args:
            size: Size of the playing field in (x, y).
            growth: Growth rate of the snake.
        """
        self.size = size
        self.growth = growth
        self.coil = 0
        self.head = (size[0]//2, size[1]//2)
        self.tail = deque([(self.head[0], self.head[1]-1),
                           (self.head[0], self.head[1]-2),
                          ])
        self.food = (size[0]//2, 3*size[1]//4)
        self.score = 0

    def display(self) -> None:
        """Function info...

        More function info...
        """
        outer = ''.join(['+', '-'*self.size[0], '+'])
        inner = ''.join(['|', ' '*self.size[0], '|'])

        score = str(self.score)
        top = score.join([outer[:len(outer)//2],
                          outer[len(outer)//2 + len(score):],
                         ])
        frame = [top, inner*self.size[1], outer]

        frame[len(frame) - self.food[1] - 1][self.food[0] + 1] = 'o'
        frame[len(frame) - self.head[1] - 1][self.head[0] + 1] = 'O'

        for x, y in self.tail:
            frame[len(frame) - y - 1][x + 1] = '*'

        print(frame)

    def move(self, direction: str) -> None:
        """Function info...

        More function info...

        Args:
            direction: The direction to move the head.
        """
        self.tail.appendleft(self.head)

        if self.coil <= 0:
            self.tail.pop()
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
        if ~(0 < self.head[0] < self.size[0]):
            return True
        if ~(0 < self.head[1] < self.size[1]):
            return True

        if self.head == self.food:
            self.eat()

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
                inverse.append(x, y)
        return inverse

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
