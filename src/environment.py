import pygame

#setup pygame
screen = pygame.display.set_mode((1400, 800),pygame.RESIZABLE)
screen_width, screen_height = screen.get_size()
#define game variable
ROWS = 16
COLS = 150
TILE_SIZE = screen_height // ROWS
TILE_TYPES = 9

# defining gravity value
gravity = 9.81
#store tiles in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'image/tile/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

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



class Worlds():
    def __init__(self):
        self.obstacles_list = []
        #store tiles in a list

    def proccess_data(self, data ):
        #iterate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile == 0:
                        self.obstacles_list.append(tile_data)
                    elif tile >=0 and tile <= 8:
                        self.obstacles_list.append(tile_data)
                    elif tile >= 8 and tile <= 8:
                        pass #decortion
                    elif tile == 10: #create a player
                        pass

    def draw(self, screen_scroll):
        for tile in self.obstacles_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])

# Création des plateformes: à priori à mettre dans la boucle, après l'initiation de Pygame
#platforms = [
    #Platform(200, 175, 400, 50),
    #Platform(700, 350, 350, 50),
    #Platform(350, 550, 250, 50, moving=True, speed=3, move_range=250)
#]