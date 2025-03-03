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
    def __init__(self, x, y, width, height, moving=False, speed=2, move_range=100):
        self.rect = pygame.Rect(x, y, width, height)
        self.moving = moving
        self.speed = speed
        self.move_range = move_range
        self.start_x = x
        self.direction = 1  # -1 to reverse

    def update(self):
        if self.moving:
            # movement
            self.rect.x += self.speed * self.direction
            if abs(self.rect.x - self.start_x) >= self.move_range:
                self.direction *= -1

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


# Create platforms
platforms = [
    Platform(200, 175, 400, 50),
    Platform(700, 350, 350, 50),
    Platform(350, 550, 250, 50, moving=True, speed=3, move_range=250)
]

# Create enemies
enemies = [Enemy(platform) for platform in platforms]

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update platforms and enemies
    for platform in platforms:
        platform.update()
    for enemy in enemies:
        enemy.update()

    # Draw everything
    screen.fill((0, 0, 0))  # Fill screen with black color
    for platform in platforms:
        platform.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)

    pygame.display.flip()  # Update the display

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()











### 1.	mouvements sur plateforme mobile générés par IA, pas encore compris comment ça marche.
### 2.	il faudrait donner aux plateformes un ID spécifique et tweak les attributes de la classe Enemy,
### 	sinon un ennemi spawn sur toutes les plateformes.
### 3.	plateformes mobiles de haut en bas ?