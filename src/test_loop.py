import pygame

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1200, 900
FPS = 60

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platform Game")

# Clock to control frame rate
clock = pygame.time.Clock()


class Platform:
    def __init__(self, x, y, width, height, moving_hor=False, moving_ver=False, speed=2, move_range=100, platform_id=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.moving_hor = moving_hor
        self.moving_ver = moving_ver
        self.platform_id = platform_id
        self.speed = speed
        self.move_range = move_range
        self.start_x = x
        self.start_y = y
        self.direction = 1  # -1 to reverse
        self.ver_direction = 1

    def update(self):
        if self.moving_hor:
            # movement
            self.rect.x += self.speed * self.direction
            if abs(self.rect.x - self.start_x) >= self.move_range:
                self.direction *= -1

        if self.moving_ver:
            # Vertical movement
            self.rect.y += self.speed * self.ver_direction
            if abs(self.rect.y - self.start_y) >= self.move_range:
                self.ver_direction *= -1

    def draw(self, surface, color=(255, 255, 255)):
        pygame.draw.rect(surface, color, self.rect)


class Enemy:
    def __init__(self, platform):
        self.width = 40
        self.height = 40
        self.platform = platform
        self.rect = pygame.Rect(platform.rect.x + platform.rect.width // 2 - self.width // 2,
                                platform.rect.y - self.height, self.width, self.height)
        self.speed = 2
        self.direction = 1
        self.last_platform_x = platform.rect.x  # Store the last known platform x position -- IA

    def update(self):
        # movement
        self.rect.x += self.speed * self.direction

        if self.rect.left <= self.platform.rect.left or self.rect.right >= self.platform.rect.right:
            self.direction *= -1

        # Adjust enemy position based on platform movement -- IA
        platform_dx = self.platform.rect.x - self.last_platform_x
        self.rect.x += platform_dx  # Apply platform displacement

        # Update last known platform position -- IA
        self.last_platform_x = self.platform.rect.x

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)  # Red enemy

class Projectiles:
    def __init__(self, x, y, radius, color, direction):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.direction = direction
        self.velocity = 10 * direction

    def update(self):
        self.x += self.velocity

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)



# create platforms
platforms = [
    Platform(200, 175, 400, 50, platform_id=1),
    Platform(700, 350, 350, 50, moving_ver=True, platform_id=2),
    Platform(350, 550, 250, 50, moving_hor=True, speed=3, move_range=250, platform_id=3)
]

# separate list for individual spawns
platform_with_spawns = [1, 3]

# create enemies
enemies = [Enemy(platform) for platform in platforms if platform.platform_id in platform_with_spawns]

# create projectiles
bullets = []
last_shot_time = 0
shot_delay = 3000


# Game loop
running = True
while running:

    current_time = pygame.time.get_ticks()

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #event : shoot when the key is pressed
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if len(bullets) < 5 and enemies:
                    enemy = enemies[0]
                    bullets.append(Projectiles(round(enemy.rect.x + enemy.width // 2),
                                               round(enemy.rect.y + enemy.height // 2),
                                               5, (255, 255, 255), 1))

    # enemies shoot at a 5sec delay
    if enemies and current_time - last_shot_time >= shot_delay:
        for enemy in enemies:
            bullets.append(Projectiles(round(enemy.rect.x + enemy.width // 2), round(enemy.rect.y + enemy.height // 2),5, (255, 255, 255), 1))
        last_shot_time = current_time

    # Update platforms and enemies
    for platform in platforms:
        platform.update()
    for enemy in enemies:
        enemy.update()

    for bullet in bullets:
        if bullet.x < 1200 and bullet.x > 0:
            bullet.update()
        else:
            bullets.pop(bullets.index(bullet))

    # Draw everything
    screen.fill((0, 0, 0))  # Fill screen with black color
    for platform in platforms:
        platform.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)

    pygame.display.flip()  # Update the display

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()