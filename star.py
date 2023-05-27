# star.py
import random
from constants import HEIGHT, WIDTH


class Star:
    def __init__(self, x, y, speed, size, color, disappear):
        self.x = x
        self.y = y
        self.speed = speed
        self.size = size
        self.color = color
        self.disappear = disappear

    @classmethod
    def random_star(cls):
        """Create a random star within the specified constraints."""
        x = random.uniform(0, WIDTH)
        y = random.uniform(0, HEIGHT)
        speed = random.uniform(0.5, 3)
        size = random.randint(1, 2)
        color = (
            random.randint(200, 255),
            random.randint(200, 255),
            random.randint(200, 255),
        )
        disappear = (
            random.random() < 0.05
        )  # Adjust this probability to control disappearance chance
        return cls(x, y, speed, size, color, disappear)

    def update(self):
        """Update the star's position and color based on its speed."""
        self.y += self.speed

        if self.disappear:
            self.color = tuple(max(0, int(c * 0.995)) for c in self.color)

        if self.y > HEIGHT or max(self.color) == 0:
            self.y = 0
            self.x = random.randint(0, WIDTH)
            self.color = (
                random.randint(200, 255),
                random.randint(200, 255),
                random.randint(200, 255),
            )
