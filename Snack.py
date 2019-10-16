import random


class Snack:
    def __init__(self, position=None, color=None):
        if position is None:
            self.position = (random.randint(0, 49) * 10, random.randint(0, 49) * 10)
        else:
            self.position = position

        if color is None:
            self.color = (random.randint(0, 254), random.randint(0, 254), random.randint(0, 254))
        else:
            self.color = color

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.position == other.position
        else:
            return False
