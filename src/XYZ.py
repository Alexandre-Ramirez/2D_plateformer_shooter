import pygame
import pygame_menu
from pygame_menu import themes
import csv
from src.XYZ_entities import *

pygame.init()
# Setup pygame
screen = pygame.display.set_mode((1400, 800), pygame.RESIZABLE)
screen_width, screen_height = screen.get_size()

# Define game variables
ROWS = 16
COLS = 150
TILE_SIZE = screen_height // ROWS
TILE_TYPES = 9
level = 1
SCROLL_THRESH = 200
bg_scroll = 0

# Define colors
GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

# Load images
pine1_image = pygame.image.load('image/backgroud/pine1.png').convert_alpha()
pine2_image = pygame.image.load('image/backgroud/pine2.png').convert_alpha()
mountain_image = pygame.image.load('image/backgroud/mountain.png').convert_alpha()
sky_image = pygame.image.load('image/backgroud/sky_cloud.png').convert_alpha()

# Setup window's title
pygame.display.set_caption("Plateformer")

# Store tiles in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'image/tile/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

class Worlds():
    def __init__(self):
        self.obstacles_list = []

    def proccess_data(self, data):
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 8:
                        self.obstacles_list.append(tile_data)

    def draw(self, screen_scroll):
        for tile in self.obstacles_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])

class Platform:
    def __init__(self, grid_x, grid_y, width_in_blocks, height_in_blocks, platform_id=None, visible=True):
        self.tile_size = TILE_SIZE
        self.rect = pygame.Rect(grid_x * self.tile_size, grid_y * self.tile_size, width_in_blocks * self.tile_size, height_in_blocks * self.tile_size)
        self.platform_id = platform_id
        self.visible = visible

    def update_position(self, screen_scroll):
        self.rect.x += screen_scroll

    def draw(self, surface, color=(255, 0, 0)):
        if self.visible:
            pygame.draw.rect(surface, color, self.rect)

# Create function for drawing bg
def draw_bg(screen_scroll):
    screen.fill(GREEN)
    width = sky_image.get_width()
    for x in range(4):
        screen.blit(sky_image, (x * width + screen_scroll, 0))
        screen.blit(mountain_image, (x * width + screen_scroll, screen_height - mountain_image.get_height() - 300))
        screen.blit(pine1_image, (x * width + screen_scroll, screen_height - pine1_image.get_height() - 150))
        screen.blit(pine2_image, (x * width + screen_scroll, screen_height - pine2_image.get_height()))

# Create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)
# Load in level data and create world
with open(f'level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

worlds = Worlds()
worlds.proccess_data(world_data)

player1 = Player(100, 300, 1)

# Platforms creation with TILE_SIZE based coordinates
platforms = [
    Platform(40, 14, 5, 1, 1, visible=False),
    Platform(45, 14, 5, 1, 2, visible=False),
    Platform(57, 14, 5, 1, 3, visible=False),
    Platform(62, 14, 5, 1, 4, visible=False),
    Platform(72, 14, 4, 1, 5, visible=False),
    Platform(96, 14, 5, 1, 6, visible=False),
    Platform(99, 10, 5, 1, 7, visible=False),
    Platform(93, 8, 5, 1, 8, visible=False),
    Platform(111, 7, 5, 1, 9, visible=False),
    Platform(120, 7, 5, 1, 10, visible=False),
    Platform(135, 14, 5, 1, 11, visible=False),
]

# enemies creation
enemies = []

for platform in platforms:
    enemies.append(Enemy(platform))

# create projectiles
bullets = []
last_shot_time = 0
shot_delay = 3000



run = True
jumping = False
# Main loop
while run:
    screen_scroll = 0
    events = pygame.event.get()

    current_time = pygame.time.get_ticks()

    # handle events
    for event in events:
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

        # event : shoot when the key is pressed
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(Projectiles(round(player1.rect.x + player1.width // 2), round(player1.rect.y + player1.height // 2),5, (255, 255, 255), 1))


    # Handle movement
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        screen_scroll = player1.move(-player1.velocity, 0)
    if key[pygame.K_RIGHT]:
        screen_scroll = player1.move(player1.velocity, 0)

    # apply scroll to everything
    for platform in platforms:
        platform.update_position(screen_scroll)
    for enemy in enemies:
        enemy.rect.x += screen_scroll
    for bullet in bullets:
        bullet.x += screen_scroll

    # enemies shoot at a 5sec delay
    if enemies and current_time - last_shot_time >= shot_delay:
        for enemy in enemies:
            bullets.append(Projectiles(round(enemy.rect.x + enemy.width // 2), round(enemy.rect.y + enemy.height // 2), 5,(255, 255, 255), enemy.direction))
        last_shot_time = current_time

    # Update enemies and projectiles
    for enemy in enemies:
        enemy.update()

    for bullet in bullets:
        if bullet.x < 1200 and bullet.x > 0:
            bullet.update()
        else:
            bullets.pop(bullets.index(bullet))

    # Draw everything
    screen.fill((0, 0, 0))
    draw_bg(screen_scroll)
    worlds.draw(screen_scroll)
    player1.draw(screen)
    for platform in platforms:
        platform.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)


    pygame.display.flip()
    pygame.display.update()