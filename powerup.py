# powerup.py
import pygame
import random
from constants import WIDTH, HEIGHT


# PowerUp class
class PowerUp:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 10
        self.active = True
        self.size = 10
        self.glow_radius = 20
        self.glow_alpha = 100
        self.glow_speed = 1

    def update(self, dt):
        # self.glow_radius += self.glow_speed * dt
        self.glow_alpha -= self.glow_speed * dt

        if self.glow_alpha <= 0:
            self.active = False

    def draw(self, screen):
        if self.active:
            # Draw the outer glow effect
            pygame.draw.circle(
                screen,
                (255, 255, 0, self.glow_alpha),
                (self.x, self.y),
                self.glow_radius,
            )

            # Draw the glass orb
            pygame.draw.circle(screen, (100, 100, 255), (self.x, self.y), self.radius)
            pygame.draw.circle(
                screen, (200, 200, 255, 50), (self.x, self.y), self.radius, 3
            )
