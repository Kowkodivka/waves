import pygame
import sys

FPS = 60
WIDTH, HEIGHT = 400, 400
SCALE = 5

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DECAY_FACTOR = 0.95

particles = [[None for _ in range(HEIGHT // SCALE)] for _ in range(WIDTH // SCALE)]


class Particle:
    def __init__(self, x, y):
        self.pos = [x, y]
        self.vel = 0
        self.height = 0
        self.acceleration = 0.1
        self.mass = 1


def get_coordinates_around(particle):
    coordinates_around = []
    for y in range(particle.pos[1] - 1, particle.pos[1] + 2):
        for x in range(particle.pos[0] - 1, particle.pos[0] + 2):
            if (x, y) != (particle.pos[0], particle.pos[1]):
                try:
                    coordinates_around.append(particles[x][y].height)
                except IndexError:
                    continue
    return coordinates_around


def logic():
    for y in range(HEIGHT // SCALE):
        for x in range(WIDTH // SCALE):
            particle = particles[x][y]
            others = get_coordinates_around(particle)
            medium_h = sum(others) / len(others)
            delta_h = medium_h - particle.height
            particle.vel += delta_h * particle.acceleration * particle.mass
            particle.vel *= DECAY_FACTOR
            particle.height += particle.vel


def interpolate_color(value):
    if value <= 0:
        return (0, 0, 0)
    elif value >= 255:
        return (255, 255, 255)
    else:
        return (value, value, value)


def draw(screen):
    for i in range(HEIGHT // SCALE):
        for j in range(WIDTH // SCALE):
            particle = particles[j][i]
            color_value = int(128 + particle.height * SCALE)
            color_value = max(0, min(255, color_value))
            color = interpolate_color(color_value)
            pygame.draw.rect(screen, color, (j * SCALE, i * SCALE, SCALE, SCALE))


def main():
    global WIDTH, HEIGHT

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("waves")
    clock = pygame.time.Clock()

    for i in range(HEIGHT // SCALE):
        for j in range(WIDTH // SCALE):
            particles[j][i] = Particle(j, i)

    for j in range(WIDTH // SCALE):
        particles[j][HEIGHT // (SCALE * 4)].height = -1000

    for j in range(WIDTH // SCALE):
        for offset in range(10):
            if j == WIDTH // (SCALE * 2) + offset or j == WIDTH // (SCALE * 2) - offset:
                particles[j][HEIGHT // (SCALE * -2)].mass = 1
            else:
                particles[j][HEIGHT // (SCALE * -2)].mass = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.VIDEORESIZE:
                WIDTH = event.w
                HEIGHT = event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

        screen.fill(BLACK)
        logic()
        draw(screen)
        pygame.display.flip()
        # clock.tick(FPS)


if __name__ == "__main__":
    main()
