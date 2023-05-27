# laser.py
import pygame
from constants import HEIGHT


class Laser:
    def __init__(
        self, x, y, speed=6, angle=0, visible=True, color=(255, 0, 0), shape="rect"
    ):
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = angle
        self.visible = visible
        self.active = True
        self.color = color
        self.shape = shape

    def update(self):
        """Update laser position based on its speed."""
        self.y -= self.speed
        if self.y < 0:
            self.active = False

    def draw(self, screen):
        """Draw the laser on the screen."""
        if self.shape == "rect":
            pygame.draw.rect(screen, self.color, (self.x - 1, self.y, 2, 10))
        elif self.shape == "circle":
            pygame.draw.circle(screen, self.color, (self.x, self.y), 5)
        # Add more shape options if desired
