import pygame
import random
import math

# Constants
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
SHIP_SIZE = 30
ASTEROID_SIZE = 40
BULLET_SIZE = 4
MAX_ASTEROIDS = 5

def wrap_position(pos, width, height):
    x, y = pos
    return x % width, y % height

class Ship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.dx = 0
        self.dy = 0

    def rotate(self, direction):
        self.angle += direction * 5

    def thrust(self):
        rad = math.radians(self.angle)
        self.dx += math.cos(rad) * 0.2
        self.dy += math.sin(rad) * 0.2

    def move(self, width, height):
        self.x += self.dx
        self.y += self.dy
        self.x, self.y = wrap_position((self.x, self.y), width, height)
        # Friction
        self.dx *= 0.99
        self.dy *= 0.99

    def draw(self, screen):
        rad = math.radians(self.angle)
        tip = (self.x + math.cos(rad) * SHIP_SIZE, self.y + math.sin(rad) * SHIP_SIZE)
        left = (self.x + math.cos(rad + 2.5) * SHIP_SIZE * 0.6, self.y + math.sin(rad + 2.5) * SHIP_SIZE * 0.6)
        right = (self.x + math.cos(rad - 2.5) * SHIP_SIZE * 0.6, self.y + math.sin(rad - 2.5) * SHIP_SIZE * 0.6)
        pygame.draw.polygon(screen, BLUE, [tip, left, right])

class Asteroid:
    def __init__(self, x, y, dx, dy, size=ASTEROID_SIZE):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.size = size

    def move(self, width, height):
        self.x += self.dx
        self.y += self.dy
        self.x, self.y = wrap_position((self.x, self.y), width, height)

    def draw(self, screen):
        pygame.draw.circle(screen, GREY, (int(self.x), int(self.y)), self.size)

    def get_rect(self):
        return pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)

class Bullet:
    def __init__(self, x, y, angle):
        rad = math.radians(angle)
        self.x = x
        self.y = y
        self.dx = math.cos(rad) * 8
        self.dy = math.sin(rad) * 8
        self.lifetime = 60  # frames

    def move(self, width, height):
        self.x += self.dx
        self.y += self.dy
        self.x, self.y = wrap_position((self.x, self.y), width, height)
        self.lifetime -= 1

    def draw(self, screen):
        pygame.draw.circle(screen, ORANGE, (int(self.x), int(self.y)), BULLET_SIZE)

    def is_alive(self):
        return self.lifetime > 0

class GameEngine:
    def __init__(self):
        self.width = 640
        self.height = 480
        self.is_running = False

    def start(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Asteroids Clone")
        self.clock = pygame.time.Clock()
        self.ship = Ship(self.width // 2, self.height // 2)
        self.asteroids = []
        self.bullets = []
        self.score = 0
        self.is_running = True
        self.spawn_asteroids()
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)
        pygame.quit()

    def spawn_asteroids(self):
        self.asteroids = []
        for _ in range(MAX_ASTEROIDS):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            dx = random.uniform(-2, 2)
            dy = random.uniform(-2, 2)
            self.asteroids.append(Asteroid(x, y, dx, dy))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Fire bullet
                    rad = math.radians(self.ship.angle)
                    bx = self.ship.x + math.cos(rad) * SHIP_SIZE
                    by = self.ship.y + math.sin(rad) * SHIP_SIZE
                    self.bullets.append(Bullet(bx, by, self.ship.angle))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.ship.rotate(-1)
        if keys[pygame.K_RIGHT]:
            self.ship.rotate(1)
        if keys[pygame.K_UP]:
            self.ship.thrust()

    def update(self):
        self.ship.move(self.width, self.height)
        for asteroid in self.asteroids:
            asteroid.move(self.width, self.height)
        for bullet in self.bullets:
            bullet.move(self.width, self.height)
        self.bullets = [b for b in self.bullets if b.is_alive()]

        # Bullet-asteroid collision
        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.get_rect().collidepoint(bullet.x, bullet.y):
                    self.bullets.remove(bullet)
                    self.asteroids.remove(asteroid)
                    self.score += 10
                    break

        # Respawn asteroids if all destroyed
        if not self.asteroids:
            self.spawn_asteroids()

        # Ship-asteroid collision
        ship_rect = pygame.Rect(self.ship.x - SHIP_SIZE//2, self.ship.y - SHIP_SIZE//2, SHIP_SIZE, SHIP_SIZE)
        for asteroid in self.asteroids:
            if ship_rect.colliderect(asteroid.get_rect()):
                self.is_running = False  # Game over

    def render(self):
        self.screen.fill(BLACK)
        self.ship.draw(self.screen)
        for asteroid in self.asteroids:
            asteroid.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        font = pygame.font.SysFont("Arial", 24)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        pygame.display.flip()