import pygame
import math

pygame.init()

WIDTH, HEIGHT = 1500, 1600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

# INITIALIZATION OF COLORS TO PLANETS

YELLOW = (255, 204, 0)  # SUN
BROWN = (165, 42, 42)  # MERCURY
WHITE = (255, 255, 224)  # VENUS
BLUE = (100, 149, 237)  # EARTH
RED = (165, 42, 42)  # MARS
ORANGE = (255, 165, 0)  # JUPITER
PALE = (238, 232, 170)  # SATURN
LBLUE = (135, 206, 250)  # URANUS
DBLUE = (0, 0, 128)  # NEPTUNE
LBROWN = (218, 165, 32)  # PLUTO


class Planet:
    # DEPLOYING CONSTANTS
    # astronomical unit
    AU = 149.6e6 * 1000  # km to mtrs
    # gravitational constant for force and attraction
    G = 6.67428e-11
    # scale for simulating real values(ex. 1mtr ps to pixels)
    SCALE = 70 / AU  # Adjusted scaling factor
    # Timestep to calculate rotations around sun
    TIMESTEP = 3600 * 24  # Representing 1 Day

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, WIN):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        updated_points = []
        if len(self.orbit) >= 2:
            for point in self.orbit:
                px, py = point  # Renaming to px and py to avoid overwriting x and y
                px = px * self.SCALE + WIDTH / 2
                py = py * self.SCALE + HEIGHT / 2
                updated_points.append((px, py))

            pygame.draw.lines(WIN, self.color, False, updated_points, 2)

        pygame.draw.circle(WIN, self.color, (int(x), int(y)), self.radius)

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x  # CALCULATED DIST BETWEEN 2 OBJECTS
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance ** 2  # CALCULATE FORCE IN STRAIGHT LINE
        theta = math.atan2(distance_y, distance_x)  # CURVATURE ANGLE (FORCE)
        force_x = math.cos(theta) * force  # CURVATURE FORCE
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, Planets):
        total_fx = total_fy = 0
        for Planet in Planets:
            if self == Planet:
                continue

            fx, fy = self.attraction(Planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))


def main():
    run = True
    clock = pygame.time.Clock()
    sun = Planet(0, 0, 43, YELLOW, 1.98892 * 10 ** 30)
    sun.sun = True

    # PLANET INITIALISATION AND COLOR
    mercury = Planet(-0.970 * Planet.AU, 0, 8, BROWN, 3.30 * 10 ** 24)
    mercury.y_vel = -30.4 * 1000

    venus = Planet(-1.500 * Planet.AU, 0, 14, WHITE, 4.8685 * 10 ** 24)
    venus.y_vel = -25.42 * 1000

    earth = Planet(-2.270 * Planet.AU, 0, 16, BLUE, 5.9742 * 10 ** 24)
    earth.y_vel = 20.783 * 1000

    mars = Planet(-3.300 * Planet.AU, 0, 12, RED, 6.39 * 10 ** 23)
    mars.y_vel = 16.483 * 1000

    jupiter = Planet(-4.8 * Planet.AU, 0, 30, ORANGE, 3.30 * 10 ** 24)
    jupiter.y_vel = 13.283 * 1000

    #saturn = Planet(5.5 * Planet.AU, 0, 30, PALE, 3.30 * 10 ** 24)
    #saturn.y_vel = -12.783 * 1000

    #uranus = Planet(6.950 * Planet.AU, 0, 12, LBLUE, 6.39 * 10 ** 23)
    #uranus.y_vel = -9.783 * 1000

    #neptune = Planet(8.2 * Planet.AU, 0, 12, DBLUE, 6.39 * 10 ** 23)
    #neptune.y_vel = 8.783 * 1000

    #pluto = Planet(9.5 * Planet.AU, 0, 8, LBROWN, 3.30 * 10 ** 24)
    #pluto.y_vel = -7.783 * 1000

    # COLLECTING ARRAY FOR CONSTANT
    planets = [sun, mercury, venus, earth, mars, jupiter] #saturn, uranus, neptune, pluto]

    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))  # CHANGING BG COLOR

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:  # Changed from Planets to planets
            planet.update_position(planets)  # Changed from Planets to planets
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()


main()
