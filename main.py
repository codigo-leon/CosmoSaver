# main.py
import pygame
import math
import sys
import random
from spaceship import draw_spaceship
from star import Star
from constants import WIDTH, HEIGHT, STAR_COUNT, DARK_PURPLE
from laser import Laser
from asteroid import Asteroid
from particle import Particle
from pygame import mixer
from powerup import PowerUp


# Font constants
FONT_SIZE = 40
FONT_COLOR = (255, 255, 255)
FONT_ANIMATION_SPEED = 0.5


def draw_gradient_background(screen):
    for y in range(HEIGHT):
        gradient_color = (0, 0, y * 40 // 600)
        pygame.draw.line(screen, gradient_color, (0, y), (WIDTH, y))


def update_and_draw_lasers(screen, lasers):
    for laser in lasers:
        laser.update()
        laser.draw(screen)

    for laser in lasers:
        if not laser.active:
            lasers.remove(laser)


def create_star_list(count):
    return [Star.random_star() for _ in range(count)]


def handle_events(spaceship_position, lasers, dt, laser_sound, engine):
    x = spaceship_position["x"]
    y = spaceship_position["y"]
    laser1 = Laser(x, y, speed=6, color=(255, 0, 0), shape="rect")  # Default laser type
    laser2 = Laser(
        x, y, speed=8, color=(0, 255, 0), shape="circle"
    )  # Laser type with different speed, color, and shape
    laser3 = Laser(
        x, y, speed=10, color=(0, 0, 255), shape="rect"
    )  # Another laser type with different properties
    acceleration = 300 * dt
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        spaceship_position["x_velocity"] -= acceleration
        engine.play()
    if keys[pygame.K_RIGHT]:
        spaceship_position["x_velocity"] += acceleration
        engine.play()
    if keys[pygame.K_UP]:
        spaceship_position["y_velocity"] -= acceleration
        engine.play()
    if keys[pygame.K_DOWN]:
        spaceship_position["y_velocity"] += acceleration
        engine.play()

    spaceship_position["x_velocity"] *= 0.95
    spaceship_position["y_velocity"] *= 0.95

    spaceship_position["x"] += spaceship_position["x_velocity"] * dt
    spaceship_position["y"] += spaceship_position["y_velocity"] * dt

    spaceship_position["x"] = max(20, min(WIDTH - 20, spaceship_position["x"]))
    spaceship_position["y"] = max(20, min(HEIGHT - 20, spaceship_position["y"]))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # laser = Laser(spaceship_position["x"], spaceship_position["y"])
                lasers.append(laser2)
                laser_sound.play()


def update_and_draw_stars(screen, stars):
    for star in stars:
        star.update()
        pygame.draw.circle(screen, star.color, (int(star.x), int(star.y)), star.size)


def draw_score(screen, score, font):
    score_text = font.render(f"Score: {score}", True, FONT_COLOR)
    score_rect = score_text.get_rect(topright=(WIDTH - 20, 20))
    screen.blit(score_text, score_rect)


def main():
    spaceship_position = {
        "x": WIDTH // 2,
        "y": HEIGHT - 50,
        "x_velocity": 0,
        "y_velocity": 0,
    }
    particles = []
    lasers = []
    power_ups = []

    asteroids = [Asteroid.random_asteroid() for _ in range(10)]

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Gradient Space Background Animation")

    clock = pygame.time.Clock()

    stars = create_star_list(STAR_COUNT)
    laser_sound = pygame.mixer.Sound("laser.wav")
    laser_sound.set_volume(0.2)
    asteroid_hit = pygame.mixer.Sound("asteroid_hit.wav")
    engine = pygame.mixer.Sound("engine.wav")
    # Load the audio file into the mixer
    music = mixer.music.load("music.mp3")

    # Set the desired volume
    mixer.music.set_volume(0.7)

    # Play the music
    mixer.music.play(-1)

    spawn_timer = 2

    # Initialize font and animation variables
    font = pygame.font.Font(None, FONT_SIZE)
    score = 0
    animated_score = 0
    combo_counter = 0

    def detect_collision(lasers, asteroids):
        nonlocal score, animated_score, combo_counter

        for power_up in power_ups:
            dx = power_up.x - spaceship_position["x"]
            dy = power_up.y - spaceship_position["y"]
            distance_squared = dx**2 + dy**2

            if distance_squared <= (power_up.size + 10) ** 2:  # Collision detected
                # Apply power-up effect
                # Example: Increase spaceship speed
                # spaceship_position["x_velocity"] *= 1.5
                # spaceship_position["y_velocity"] *= 1.5

                power_up.active = False  # Remove the power-up

        new_asteroids = []

        for asteroid in asteroids:
            asteroid.update(dt)
            if asteroid.y > HEIGHT + asteroid.size:
                asteroid.destroyed = True
            else:
                asteroid.draw(screen)
                new_asteroids.append(asteroid)

        for laser in lasers:
            if laser.y < 0:
                combo_counter = 0
            if not laser.active:
                continue
            for asteroid in new_asteroids:
                dx = laser.x - asteroid.x
                dy = laser.y - asteroid.y
                if dx**2 + dy**2 <= asteroid.size**2:
                    laser.active = False
                    impact_angle = math.degrees(math.atan2(dy, dx)) - 90
                    asteroid.hit(impact_angle, power_ups)
                    asteroid_hit.play()
                    score += 10
                    combo_counter += 1
                    animated_score += 10  # Increment animated score

                    # Render the combo counter text
                    # Emit particles from the asteroid impact location
                    for _ in range(10):
                        angle = random.uniform(0, 360)
                        speed = random.uniform(50, 150)
                        size = random.uniform(1, 3)
                        particle_color = asteroid.color
                        particles.append(
                            Particle(
                                laser.x, laser.y, speed, angle, size, particle_color
                            )
                        )

        new_asteroids = [
            asteroid for asteroid in new_asteroids if not asteroid.destroyed
        ]
        combo_text = font.render(f"Combo: {combo_counter}", True, (255, 255, 255))

        # Display the combo counter text on the screen
        screen.blit(combo_text, (10, 10))

        return new_asteroids

    while True:
        dt = clock.tick(60) / 1000
        handle_events(spaceship_position, lasers, dt, laser_sound, engine)
        draw_gradient_background(screen)
        update_and_draw_lasers(screen, lasers)
        update_and_draw_stars(screen, stars)

        # Update and draw power-ups
        new_power_ups = []
        for power_up in power_ups:
            power_up.update(dt)
            if power_up.active:
                power_up.draw(screen)
                new_power_ups.append(power_up)
        power_ups = new_power_ups

        # Update and draw particles
        new_particles = []
        for particle in particles:
            particle.update(dt)
            particle.draw(screen)
            if particle.size > 0.1:
                new_particles.append(particle)
        particles = new_particles

        draw_spaceship(screen, spaceship_position["x"], spaceship_position["y"])

        # Draw score
        draw_score(screen, score, font)

        asteroids = detect_collision(lasers, asteroids)
        spawn_timer -= dt
        if spawn_timer <= 0:
            if len(asteroids) < 15:
                asteroids.append(Asteroid.random_asteroid())
            spawn_timer = random.uniform(0.5, 1.5)

        pygame.display.flip()


if __name__ == "__main__":
    main()
