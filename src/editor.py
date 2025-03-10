import pygame
import button
import csv
import os
import pickle

base_dir = os.path.dirname(__file__)

#1h57:04


pygame.init()

clock = pygame.time.Clock()
FPS = 60

#game window
screen_w, screen_h = 800, 640
lower_margin = 90
side_margin = 300

screen = pygame.display.set_mode((screen_w + side_margin, screen_h + lower_margin))
pygame.display.set_caption('Level editor')

#define game variables
ROWS = 16
MAX_COLS = 150
TILE_SIZE = screen_w // ROWS
TILE_TYPES = 8
level = 0
current_tile = 0
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1

#load images
pine1_image = pygame.image.load(os.path.join(base_dir, 'image/backgroud/pine1.png')).convert_alpha()
pine2_image = pygame.image.load(os.path.join(base_dir,'image/backgroud/pine2.png')).convert_alpha()
mountain_image = pygame.image.load(os.path.join(base_dir,'image/backgroud/mountain.png')).convert_alpha()
sky_image = pygame.image.load(os.path.join(base_dir,'image/backgroud/sky_cloud.png')).convert_alpha()
#store tiles in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(os.path.join(base_dir,f'image/tile/{x}.png')).convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE , TILE_SIZE))
    img_list.append(img)

save_img = pygame.image.load(os.path.join(base_dir,'image/tile/save_btn.png')).convert_alpha()
load_img = pygame.image.load(os.path.join(base_dir,'image/tile/load_btn.png')).convert_alpha()

#define colors
GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

#define font
font = pygame.font.SysFont('comicsans', 30)

#create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * MAX_COLS
    world_data.append(r)


#create ground
for tile in range(0, MAX_COLS):
    world_data[ROWS - 1][tile] = 0
print(world_data)

#function for outputting text onto the screen
def draw_text(text,font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#create function for drawing bg
def draw_bg():
    screen.fill(GREEN)
    width = sky_image.get_width()
    for x in range (4):
        screen.blit(sky_image, ((x * width) -scroll * 0.5,0)) #mettre les images du plus loins au plus proche
        screen.blit(mountain_image, ((x * width) -scroll * 0.6, screen_h - mountain_image.get_height() - 300))
        screen.blit(pine1_image, ((x * width) -scroll * 0.7, screen_h - pine1_image.get_height() - 150))
        screen.blit(pine2_image, ((x * width) -scroll * 0.8, screen_h - pine2_image.get_height()))

#draw grid
def draw_grid():
    #vertical lines
    for c in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0),(c * TILE_SIZE - scroll, screen_h))

    #horizental lines
    for r in range(ROWS - 2):
        pygame.draw.line(screen, WHITE,(0, r * TILE_SIZE),(screen_w, r * TILE_SIZE ))

#function for drawing the world tiles
def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))

#create buttons
save_button = button.Button(screen_w // 2 + 150, screen_h + 40, save_img, 1)
load_button = button.Button(screen_w // 2 + 350, screen_h + 40, load_img, 1)
#make a button list
button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
    tile_button = button.Button(screen_w + (75 * button_col) +50, 75 * button_row +50, img_list[i], 1)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = 0


run = True
while run:

    clock.tick(FPS)

    draw_bg()
    draw_grid()
    draw_world()

    draw_text(f'Level: {level}', font, WHITE, 10, screen_h + lower_margin - 90)
    draw_text('Press UP or DOWN to change level', font, WHITE, 10, screen_h + lower_margin - 60)

    #save and load data
    if save_button.draw(screen):
        file_path = f'level{level}_data.csv'
        print(f"Saving to: {os.path.abspath(file_path)}")
        #save level data
        try:
            with open(f'level{level}_data.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')

                for row in world_data:
                    writer.writerow(row)
            print("Level saved")
        except Exception as e:
            print(f"Error saving level: {e}")




    if load_button.draw(screen):
        #load in level data
        #reset scroll back to the start of the level
        scroll = 0
        with open(f'level{level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for y, row in enumerate(reader):
                for x, tile in enumerate(row):
                    world_data[y][x] = int(tile)



    #draw tile panel and tiles
    pygame.draw.rect(screen, GREEN, (screen_w, 0, side_margin, screen_h))
    #pygame.draw.rect(screen, GREEN, (0, screen_h, screen_w, lower_margin))

    #choose a tile
    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count

    #highlight the selected tile
    pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

    #scroll the map
    if scroll_left == True and scroll > 0 :
        scroll -= 5 * scroll_speed
    if scroll_right == True and scroll < (MAX_COLS * TILE_SIZE) - screen_w :
        scroll += 5 * scroll_speed

    #add new tiles to th screen
    #get mouse position
    pos = pygame.mouse.get_pos()
    x = (pos[0] + scroll) // TILE_SIZE
    y = pos[1] // TILE_SIZE

    #check that the coordinates are within the tile area
    if pos[0] < screen_w and pos[1] < screen_h:
        #update tile value
        if pygame.mouse.get_pressed()[0] == 1:
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile
        if pygame.mouse.get_pressed()[2] == 1:
            world_data[y][x] = -1
            print("efface")

    print(x,y)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level += 1
            if event.key == pygame.K_DOWN and level > 0:
                level -= 1
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 1

    pygame.display.update()

pygame.quit()