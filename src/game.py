import pygame_menu
from pygame_menu import themes
from pygame_menu.examples.simple import start_the_game, set_difficulty
from src.entities import *
from src.environment import *

pygame.init()

#setup pygame
screen = pygame.display.set_mode((1400, 800),pygame.RESIZABLE)
screen_width, screen_height = screen.get_size()

#define game variable
ROWS = 16
COLS = 150
TILE_SIZE = screen_height // ROWS
TILE_TYPES = 9
level = 1
SCROLL_THRESH = 200
bg_scroll = 0

#define colors
GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

#load images
pine1_image = pygame.image.load(f'image/backgroud/pine1.png').convert_alpha()
pine2_image = pygame.image.load(f'image/backgroud/pine2.png').convert_alpha()
mountain_image = pygame.image.load(f'image/backgroud/mountain.png').convert_alpha()
sky_image = pygame.image.load(f'image/backgroud/sky_cloud.png').convert_alpha()

#setup window's title
pygame.display.set_caption("Plateformer")

#create a new event to tell when the loading is over
END_LOADING = pygame.USEREVENT +1

#variable to follow the state of the game
current_state = "game"
selected_level = '1'
selected_difficulty = 'Easy'

#store tiles in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'image/tile/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

#create function for drawing bg
def draw_bg(screen_scroll):
    screen.fill(GREEN)
    width = sky_image.get_width()
    for x in range (4):
        screen.blit(sky_image, (x * width + screen_scroll, 0)) #mettre les images du plus loins au plus proche
        screen.blit(mountain_image, (x * width + screen_scroll, screen_height - mountain_image.get_height() - 300))
        screen.blit(pine1_image, (x * width + screen_scroll, screen_height - pine1_image.get_height() - 150))
        screen.blit(pine2_image, (x * width + screen_scroll, screen_height - pine2_image.get_height()))

#function to select a level
def level_selection():
    menu._open(world)

    match world:
        case 1:
            return 1
        case 2:
            return 2
        case 3:
            return 3
        case _:
            return None

#the player set a difficulty
def set_diffulty(value, difficulty):
    global selected_difficulty
    selected_difficulty = difficulty
    print(f"Difficulty selected: {difficulty}")

#function to select a level
def set_level(value, level):
    global selected_level
    selected_level = level
    print(f"Level selected = {selected_level}")

#function to set the difficulty
def start_game():
    global current_state
    print(f"Starting game with level: {selected_level} and difficulty: {selected_difficulty}")
    current_state = "game" #the state pass to "game"
    menu.disable() #the pass to off
    menu.close()

    print(f"Starting game with level : {selected_level}")


    if set_difficulty == 'Easy' and selected_level == 1:
        pass
    elif set_difficulty == 'Easy' and selected_level == 2:
        pass
    elif set_difficulty == 'Easy' and selected_level == 3:
        pass
    elif set_difficulty == 'Medium' and selected_level == 1:
        pass
    elif set_difficulty == 'Medium' and selected_level == 2:
        pass
    elif set_difficulty == 'Medium' and selected_level == 3:
        pass
    elif set_difficulty == 'Hard' and selected_level == 1:
        pass
    elif set_difficulty == 'Hard' and selected_level == 2:
        pass
    elif set_difficulty == 'Hard' and selected_level == 3:
        pass

    #play_level()

#define the loading
def loading():
    menu._open(loading)
    pygame.time.set_timer(update_loading, 30)
    # Définir un temps après lequel le chargement est terminé (ex: 3 secondes)
    pygame.time.set_timer(END_LOADING, 3000)  # 3000 ms = 3 secondes

#create a main menu when starting the game
def create_menu():
    menu = pygame_menu.Menu(
        height= screen_height,
        width= screen_width,
        theme=themes.THEME_DEFAULT,
        title="Welcome to Plateformer"
    )

    menu.add.text_input('Name : ', default="username",)
    menu.add.button('Play', level_selection)
    menu.add.button('Levels', set_level)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    return menu

#define the characteristic of each menu
#define create_menu by menu
menu = create_menu()
menu.enable()

#define the display of the level's menu
levels = pygame_menu.Menu("Levels", 1400, 800, theme=themes.THEME_BLUE)
levels.add.selector('world: ', [('easy', 1), ('medium', 2), ('hard', 3)], onchange=set_difficulty)

#define the display of loading
loading = pygame_menu.Menu('Loading the Game...', 1400, 800, theme=themes.THEME_DARK)
loading.add.progress_bar("Progress", progressbar_id= "1", default=0, width=200)
update_loading = pygame.USEREVENT + 0

#define the display of the the mouse
arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size = (10, 15))

#define the display of the level's selector
world = pygame_menu.Menu("Choose your level...", 1400, 800, theme=themes.THEME_SOLARIZED)
world.add.selector('Level: ', [('World 1:1','1'), ('world 1:2', 'Medium'), ('World 1:3','Hard')], onchange=start_game)
world.add.button("Back", pygame_menu.events.BACK)
world.add.button("Start Game", start_game)

#give the details about the player
player1 = Player(100, 300, 1, 5)

#define the collision
collide_damage = Collide_damage(x=0, y=0, max_damage=10)

#define the health_bar
health_bar = HealthBar(250,200,300,40,100, collide_damage=collide_damage)

#cooldown timer
last_collision_time = 0
cooldown = 1

#create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)
#load in level data and create world
with open(f'level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

#draw the tile
worlds = Worlds()
worlds.proccess_data(world_data)

# Platforms creation with TILE_SIZE based coordinates
platforms = [
    Platform(26, 14, 11, 1, 1, visible=False),
    Platform(40, 14, 10, 1, 2, visible=False),
    Platform(54, 14, 7, 1, 3, visible=False),
    Platform(61, 14, 6, 1, 4, visible=False),
    Platform(79, 14, 8, 1, 5, visible=False),
    Platform(96, 14, 5, 1, 6, visible=False),
    Platform(99, 10, 5, 1, 7, visible=False),
    Platform(93, 8, 5, 1, 8, visible=False),
    Platform(110, 7, 9, 1, 9, visible=False),
    Platform(120, 7, 9, 1, 10, visible=False),
    Platform(137, 14, 13, 1, 11, visible=False),
]

# enemies creation
enemies = []

for platform in platforms:
    enemies.append(Enemy(platform))

# create projectiles
bullets = []
shot_delay = 3000

run = True
jumping = False

#main loop
while run:
    screen_scroll = 0
    #print(f"current state {current_state}")
    current_time = pygame.time.get_ticks()

    #define the characteristic
    events = pygame.event.get()
    death = Collide_damage
    #Player = entities.Player

    for event in events:
        #quit pygame
        if event.type == pygame.QUIT:
            run = False
        #keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                current_state = "menu"
                menu.enable()
                # event : shoot when the key is pressed
            elif event.key == pygame.K_SPACE and player1.direction == 1:
                bullets.append(Projectiles(round(player1.rect.x + player1.width // 2 + 35), round(player1.rect.y + player1.height // 2 + 35), 5, (255, 255, 255), player1.direction,"player"))
            elif event.key == pygame.K_SPACE and player1.direction == -1:
                bullets.append(Projectiles(round(player1.rect.x + player1.width // 2 - 35), round(player1.rect.y + player1.height // 2 + 35), 5, (255, 255, 255), player1.direction,"player"))

    screen.fill((0, 0, 0))

    if current_state == "menu":
        # draw the menu
        if menu.is_enabled():
            menu.update(events)
            menu.draw(screen)
    elif current_state == "game":
        # Draw the game

        #Afficher le jeu
        # movements of the player
        keys = pygame.key.get_pressed()
        moving = False
        moving_l = False
        jumping = False
        on_ground = True

        # Mouvement left
        if keys[pygame.K_LEFT]:
            screen_scroll = player1.move(True, False, False, False,False, True)
            player1.update_action(1)  #Walking Animation

        # Mouvement right
        elif keys[pygame.K_RIGHT]:
            screen_scroll = player1.move(False, True,False, False ,False, True)
            player1.update_action(1)  #Walking Animation

        elif keys[pygame.K_UP]:
            player1.move(False, False, True, False, False, True)

        # Saut
        elif keys[pygame.K_DOWN]:
            player1.move(False, False, False, True, False, True)

        # Si aucune touche n'est pressée, remettre l'animation à 0 (idle)
        else:
            player1.update_action(0)

        # apply scroll to everything
        for platform in platforms:
            platform.rect.x += screen_scroll
        for enemy in enemies:
            enemy.rect.x += screen_scroll
        for bullet in bullets:
            bullet.x += screen_scroll

        # Update enemies + shooting if detecting the player
        for enemy in enemies:
            enemy.update(player1)

            # enemies shoot at a 5sec delay
            if enemy.shooting and current_time - enemy.last_shot_time >= shot_delay and enemy.direction == 1:
                bullets.append(Projectiles(round(enemy.rect.x + enemy.width // 2 + 35),
                                           round(enemy.rect.y + enemy.height // 2 + 40), 5, (255, 255, 255),
                                           enemy.direction, "enemy"))
                enemy.last_shot_time = current_time
            elif enemy.shooting and current_time - enemy.last_shot_time >= shot_delay and enemy.direction == -1:
                bullets.append(Projectiles(round(enemy.rect.x + enemy.width // 2 - 35),
                                           round(enemy.rect.y + enemy.height // 2 + 40), 5, (255, 255, 255),
                                           enemy.direction, "enemy"))
                enemy.last_shot_time = current_time

        # Update bullets and pop if they go off-screen
        for bullet in bullets:
            bullet_rect = pygame.Rect(bullet.x - bullet.radius, bullet.y - bullet.radius, bullet.radius * 2,
                                      bullet.radius * 2)

            if 0 <= bullet.x <= screen_width:
                bullet.update()
            else:
                bullets.remove(bullet)

            if bullet.shooter == "player":
                for enemy in enemies:
                    if bullet_rect.colliderect(enemy.hitbox_enemy):
                        enemy.hp -= 20
                        bullets.remove(bullet)
                        if enemy.hp <= 0:
                            enemies.remove(enemy)
                        break
            elif bullet.shooter == "enemy" and bullet_rect.colliderect(player1.hitbox_player):
                player1.hp -= 20
                bullets.remove(bullet)
                if player1.hp <= 0:
                    death.show_death_screen(self,screen)

        player1.update_animation()
        player1.reset()

        # draw at the screen
        draw_bg(screen_scroll)
        # update background
        worlds.draw(screen_scroll)

        player1.draw(screen)
        for platform in platforms:
            platform.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)
            # enemy.draw(screen)
            # health_bar.draw(screen)

    pygame.display.flip()
    pygame.display.update()