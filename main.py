import pygame
import sys
import math

FPS = 60
WIDTH, HEIGHT = 680, 480

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

K = 0.5
M = 100
D = 0.5 

particles = []

class Particle:
    def __init__(self, x, y):
        self.pos = [x, y]
        self.vel = [0, 0]

def find_angle(particle, other_particle):
    delta_y = other_particle.pos[1] - particle.pos[1]
    angle_rad = math.atan2(delta_y, 0)
    angle_deg = math.degrees(angle_rad)
    
    return angle_deg

def logic(s):
    for i in range(len(particles)):
        acc = [0, 0]
        particle = particles[i]

        if i == 0:
            other_particle = particles[i + 1]
            angle = find_angle(particles[0], particles[1])
            acc[1] += K * (abs(other_particle.pos[1] - particle.pos[1]) - s) * math.sin(angle) / M
        elif i == len(particles) - 1:
            prev_particle = particles[i - 1]
            angle = find_angle(prev_particle, particle)
            acc[1] += K * (abs(prev_particle.pos[1] - particle.pos[1]) - s) * math.sin(angle) / M
        else:
            prev_particle = particles[i - 1]
            next_particle = particles[i + 1]

            angle_prev = find_angle(prev_particle, particle)
            angle_next = find_angle(particle, next_particle)

            acc[1] += K * (abs(prev_particle.pos[1] - particle.pos[1]) - s) * math.sin(angle_prev) / M
            acc[1] += K * (abs(next_particle.pos[1] - particle.pos[1]) - s) * math.sin(angle_next) / M

        particle.vel[1] += acc[1]
        particle.vel[1] *= D
        particle.pos[1] += particle.vel[1]

def draw(screen):
    for particle in particles:
        pygame.draw.circle(screen, BLACK, (int(particle.pos[0]), int(particle.pos[1])), 1)
        
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("waves")
    clock = pygame.time.Clock()

    num_particles = 50
    spacing = 10

    total_width = num_particles * spacing
    start_x = (WIDTH - total_width) // 2 + spacing // 2

    for i in range(num_particles):
        x = start_x + i * spacing
        y = HEIGHT // 2
        particles.append(Particle(x, y))

    particles[0].pos[1] += 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)
        logic(spacing)
        draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
