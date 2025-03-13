#sleep permet de suspendre l'exécution d'un programme pendant une durée spécifique
from time import sleep
from unittest import case
import pygame
import pygame_menu
from pygame_menu import themes
from pygame_menu.examples.simple import start_the_game, set_difficulty
import time

from src import entities
from src.entities import *
from src.environment import *

pygame.init()
#setup pygame
screen = pygame.display.set_mode((1400, 800),pygame.RESIZABLE)
x,y = screen.get_size()

#setup window's title
pygame.display.set_caption("Plateformer")


#take the size of the screen
screen_width, screen_height = screen.get_size()

# create a new event to telle when the loading is over
END_LOADING = pygame.USEREVENT +1

#level by default
selected_level = 'Easy'
selected_difficulty = 'Easy'

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
"""
def play_level():

    running = True

    while running:

        events = pygame.event.get()
        death = Collide_damage
        Player = entities.Player
        Enemy = entities.Enemy

        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                running = False

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            player1.move(-player1.velocity, 0)
        if key[pygame.K_RIGHT]:
            player1.move(player1.velocity, 0)
        if key[pygame.K_UP]:
            player1.move(0, -player1.velocity)
        if key[pygame.K_DOWN]:
            player1.move(0, player1.velocity)

        pygame.display.flip()

        # Enemy AI: Move towards the player
        #enemy.move_towards_player(player1)

        # pygame.draw.rect(window, (255,0,0), player)
        #player1.draw(screen)
        #enemy.draw(screen)
        #health_bar.draw(screen)

        pygame.display.update()

"""
#def set_level(value, level):

#the player set a difficulty
def set_diffulty(value, difficulty):
    global selected_level
    selected_level = level
    print(f"Level selected = {selected_level}")

    #print(value)
    #print(difficulty)
#define with the choosen level the start of the game
def start_game():
    print(f"Starting game with level : {selected_level}")
    menu._open(loading)
    pygame.time.set_timer(update_loading, 30)
    # Définir un temps après lequel le chargement est terminé (ex: 3 secondes)
    pygame.time.set_timer(END_LOADING, 3000)  # 3000 ms = 3 secondes

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


def level_menu():
    menu._open(level)

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
    menu.add.button('Levels', level_menu)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    return menu

#define the characteristic of each menu
#define create_menu by menu
menu = create_menu()

#define the display of the level's menu
level = pygame_menu.Menu("Levels", 1400, 800, theme=themes.THEME_BLUE)
level.add.selector('world: ', [('easy',1), ('medium',2), ('hard',3)], onchange=set_difficulty)

#define the display of loading
loading = pygame_menu.Menu('Loading the Game...', 1400, 800, theme=themes.THEME_DARK)
loading.add.progress_bar("Progress", progressbar_id= "1", default=0, width=200)
update_loading = pygame.USEREVENT + 0

#define the display of the the mouse
arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size = (10, 15))

#define the display of the level's selector
world = pygame_menu.Menu("Choose your level...", 1400, 800, theme=themes.THEME_SOLARIZED)
world.add.selector('Level: ', [('World 1:1','1'), ('world 1:2', 'Medium'), ('World 1:3','Hard')], onchange=start_game())
world.add.button("Back", pygame_menu.events.BACK)
world.add.button("Start Game", start_game)

#give the details about the player
player1 = Player(100, 100, 1)
enemy = Enemy(200, 200, 50, 50)

#define the collision
collide_damage = Collide_damage(x=0, y=0, max_damage=10)

#define the health_bar
health_bar = HealthBar(250,200,300,40,100, collide_damage=collide_damage)

#cooldown timer
last_collision_time = 0
cooldown = 1

run = True
jumping = False
#main loop
while run:

    #define the characteristic
    events = pygame.event.get()
    death = Collide_damage
    Player = entities.Player
    Enemy = entities.Enemy

    #movements of the player
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player1.move(-player1.velocity, 0)
    if key[pygame.K_RIGHT]:
        player1.move(player1.velocity, 0)
    if key[pygame.K_UP] or key[pygame.K_SPACE]:
        jumping = True
    if key[pygame.K_DOWN]:
        player1.move(0, player1.velocity)

    if jumping:
        Player.jump(player1,1,20,20)


    pygame.display.flip()

    for event in events:
        if event.type == update_loading:
            progress = loading.get_widget("1")
            progress.set_value(progress.get_value() +1)
            if progress.get_value() == 100:
                pygame.time.set_timer(update_loading, 0)
        if event.type == pygame.QUIT:
            run = False
        if event.type == END_LOADING:
            menu._open(world)

    if menu.is_enabled():
        menu.update(events)
        menu.draw(screen)
        if (menu.get_current().get_selected_widget()):
            arrow.draw(screen, menu.get_current().get_selected_widget())

    # Enemy AI: Move towards the player
    enemy.move_towards_player(player1)

    #draw at the screen
    player1.draw(screen)
    enemy.draw(screen)
    health_bar.draw(screen)

    pygame.display.update()
"""
   #define the hitbox with the health bar
    if player1.hitbox_player.colliderect(enemy.hitbox_enemy):
        #the player lose 2hp of life
        result = health_bar.decrease_health(2)
        #test if the collision is regonize
        print("Collision detected! Health decreased.")
        #if the player loose all his life a window pop up and he can choose between "retry" and "exit"
        #if he clicks on retry the game reset
        if result == "retry":
            Player.reset(player1) #the player reset at his origin place
            Enemy.reset(enemy) #the enemy reset at his origin place
            health_bar.reset() #the health bar reset at 100
            #if he clicks on exit
        elif result == "exit" or result == pygame.QUIT:
            run = False  # quit the game
"""

"""
    if player1.hitbox_player.colliderect(enemy.hitbox_enemy):
        if not collision_occurred:
            print("Collision detected! Health decreased.")
            health_bar.decrease_health(2)
            collision_occurred = True
        else:
            print("Collision still active, but health not decreased.")
            health_bar.decrease_health(2)
            collision_occurred = True
    else:
        print("No collision. Resetting flag.")
        collision_occurred = False
"""
""" 
            if player1.hitbox_player.colliderect(enemy.hitbox_enemy):
                if not collision_occurred:
                    print("collision")
                    health_bar.decrease_health(2)
                    collision_occurred = True
                else:
                    collision_occurred = False
"""