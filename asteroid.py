# asteroid.py
import pygame
import numpy as np
import random
from constants import WIDTH, HEIGHT
import math
from noise import pnoise2
from powerup import PowerUp


def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))


class Asteroid:
    def __init__(self, x, y, size, speed):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.color = (100, 100, 100)
        self.destroyed = False
        self.rotation_angle = 0
        self.rotation_speed = 0

        # Generate custom polygon points
        self.points = self.generate_asteroid_shape()

        # Generate custom polygon points
        self.points = self.generate_asteroid_shape()

        # Generate the asteroid texture using Perlin noise
        self.texture = self.generate_texture()

    # previous code ...
    @classmethod
    def random_asteroid(cls):
        x = random.randint(40, WIDTH - 80)
        y = random.randint(-80, -40)  # Change the y value to spawn outside the screen
        size = random.randint(20, 40)
        speed = random.uniform(0.5, 2)

        return cls(x, y, size, speed)

    def generate_asteroid_shape(self):
        num_points = random.randint(12, 20)
        step_angle = (2 * math.pi) / num_points
        points = []

        for angle in range(num_points):
            noise = random.uniform(0.75, 1.25)
            outer_x = self.x + math.cos(angle * step_angle) * noise * self.size
            outer_y = self.y + math.sin(angle * step_angle) * noise * self.size
            points.append((outer_x, outer_y))

        # Create rounded edges using Bézier curves
        smooth_points = []
        for i in range(len(points)):
            current_point = points[i]
            next_point = points[(i + 1) % len(points)]
            control_point = (
                (current_point[0] + next_point[0]) / 2,
                (current_point[1] + next_point[1]) / 2,
            )
            smooth_points.append(control_point)
            smooth_points.append(next_point)

        return smooth_points

    def generate_texture(self):
        texture_surface = pygame.Surface(
            (self.size * 2, self.size * 2), pygame.SRCALPHA
        )

        grid_scale = 0.15

        for xi in range(self.size * 2):
            for yi in range(self.size * 2):
                value = pnoise2(
                    (self.x + xi) * grid_scale, (self.y + yi) * grid_scale, octaves=4
                )
                color_value = clamp(int((value + 1) * 128), 0, 255)
                texture_surface.set_at(
                    (xi, yi), (color_value, color_value, color_value)
                )

        # Create a mask surface to draw the texture only within the asteroid's shape
        mask_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.polygon(
            mask_surface,
            (255, 255, 255),
            [(x - self.x + self.size, y - self.y + self.size) for x, y in self.points],
        )

        # Blit the texture_surface onto the mask_surface using the BLEND_MULT flag
        mask_surface.blit(texture_surface, (0, 0), special_flags=pygame.BLEND_MULT)

        return mask_surface

    def rotate(self, angle):
        self.rotation_angle += angle
        rad_angle = math.radians(-angle)
        for i, (x, y) in enumerate(self.points):
            dx = x - self.x
            dy = y - self.y
            cos_angle = math.cos(rad_angle)
            sin_angle = math.sin(rad_angle)
            new_x = self.x + (dx * cos_angle - dy * sin_angle)
            new_y = self.y + (dx * sin_angle + dy * cos_angle)
            self.points[i] = (new_x, new_y)

    def update(self, dt):
        self.y += self.speed
        self.rotation_angle += self.rotation_speed * dt

        if self.y > HEIGHT + self.size:
            self.y = -self.size
            self.x = random.randint(0, WIDTH)
            self.rotation_speed = 0

    def hit(self, impact_angle, power_ups):
        if self.size > 10:
            self.size -= 3
            self.points = self.generate_asteroid_shape()
            self.texture = self.generate_texture()
            if random.random() < 0.2:  # 20% chance of creating a power-up
                power_up = PowerUp(self.x, self.y)
                power_ups.append(power_up)
        else:
            self.destroyed = True
        self.rotation_speed = impact_angle * 0.1

    def draw(self, surface):
        texture_x, texture_y = self.x - self.size, self.y - self.size

        # Create a rotated asteroid surface
        rotated_texture = pygame.transform.rotate(self.texture, self.rotation_angle)
        rotated_rect = rotated_texture.get_rect(center=(int(self.x), int(self.y)))

        # Blit the rotated asteroid
        surface.blit(rotated_texture, rotated_rect.topleft)
