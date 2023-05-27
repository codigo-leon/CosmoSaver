# spaceship.py
import pygame

MAIN_METALLIC_COLOR = (150, 150, 150)
REFLECTION_COLOR = (250, 250, 250)
WINDOW_BLUE_COLOR = (0, 170, 255)
WINDOW_DARK_BLUE_COLOR = (0, 90, 175)


def draw_metallic_triangle(surface, points, main_color, reflection_color, steps=3):
    for i in range(steps):
        current_color = tuple(
            int(main_color[j] * (1 - i / steps) + reflection_color[j] * (i / steps))
            for j in range(3)
        )

        clipped_points = [
            (
                (points[0][0] + points[2][0]) // 2
                + (i - steps // 2) * (points[2][0] - points[0][0]) // steps,
                points[0][1] + (points[2][1] - points[0][1]) * i // steps,
            ),
            (
                (points[0][0] + points[1][0]) // 2
                + (i - steps // 2) * (points[1][0] - points[0][0]) // steps,
                points[0][1] + (points[2][1] - points[0][1]) * (i + 1) // steps,
            ),
            (
                (points[1][0] + points[2][0]) // 2
                + (i - steps // 2) * (points[2][0] - points[1][0]) // steps,
                points[0][1] + (points[2][1] - points[0][1]) * (i + 1) // steps,
            ),
        ]

        pygame.draw.polygon(
            surface, current_color, [points[0], clipped_points[0], clipped_points[1]]
        )

        pygame.draw.polygon(
            surface, current_color, [points[1], clipped_points[1], clipped_points[2]]
        )

        pygame.draw.polygon(
            surface, current_color, [points[2], clipped_points[2], clipped_points[0]]
        )
        pygame.draw.polygon(
            surface, WINDOW_DARK_BLUE_COLOR, [(25, 20), (25, 40), (10, 50)]
        )
        pygame.draw.polygon(surface, WINDOW_BLUE_COLOR, [(25, 20), (25, 40), (40, 50)])


def draw_spaceship(screen, x, y):
    """Draw the spaceship on the screen."""

    # Spaceship body
    spaceship_body = pygame.Surface((50, 50), pygame.SRCALPHA)
    body_points = [(0, 50), (25, 0), (50, 50)]
    draw_metallic_triangle(
        spaceship_body, body_points, MAIN_METALLIC_COLOR, REFLECTION_COLOR
    )
    screen.blit(spaceship_body, (x - 25, y))

    # Windows
    # pygame.draw.polygon(screen, WINDOW_BLUE_COLOR, [(0, 10), (10, 20), (20, 0)])
    # pygame.draw.circle(screen, WINDOW_BLUE_COLOR, (x + 10, y + 18), 4)

    # Spaceship wings
    # spaceship_left_wing = pygame.Surface((35, 20), pygame.SRCALPHA)
    # spaceship_right_wing = pygame.Surface((35, 20), pygame.SRCALPHA)

    # left_wing_points = [(0, 0), (35, 0), (0, 20)]
    # right_wing_points = [(35, 0), (0, 0), (35, 20)]

    # draw_metallic_triangle(
    #    spaceship_left_wing, left_wing_points, MAIN_METALLIC_COLOR, REFLECTION_COLOR
    # )
    # draw_metallic_triangle(
    #    spaceship_right_wing, right_wing_points, MAIN_METALLIC_COLOR, REFLECTION_COLOR
    # )

    # Spaceship exhaust
    # pygame.draw.rect(screen, MAIN_METALLIC_COLOR, (x - 3, y + 18, 6, 10))
