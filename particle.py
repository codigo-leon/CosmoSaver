# particle.py

import pygame
import random
import math


class Particle:
    def __init__(self, x, y, speed, angle, size, color):
        self.x = x
        self.y = y
        self.speed = speed
        self.angle_rad = math.radians(angle)
        self.size = size
        self.color = color

    def update(self, dt):
        self.x += math.cos(self.angle_rad) * self.speed * dt
        self.y += math.sin(self.angle_rad) * self.speed * dt
        self.size *= 0.98

    def draw(self, surface):
        pygame.draw.circle(
            surface, self.color, (int(self.x), int(self.y)), int(self.size)
        )
