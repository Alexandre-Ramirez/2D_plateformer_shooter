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
#setup bg color
#color = (125,125,125)

#def draw_menu(screen):
    #take the size of the screen
screen_width, screen_height = screen.get_size()

# Crée un nouvel événement personnalisé pour signaler la fin du chargement
END_LOADING = pygame.USEREVENT +1
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
        enemy.move_towards_player(player1)

        # pygame.draw.rect(window, (255,0,0), player)
        player1.draw(screen)
        enemy.draw(screen)
        health_bar.draw(screen)

        pygame.display.update()


#def set_level(value, level):

def set_diffulty(value, difficulty):
    global selected_level
    selected_level = level
    print(f"Level selected = {selected_level}")

    #print(value)
    #print(difficulty)

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

    play_level()


def level_menu():
    menu._open(level)

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

menu = create_menu()

level = pygame_menu.Menu("Levels", 1400, 800, theme=themes.THEME_BLUE)
level.add.selector('world: ', [('easy',1), ('medium',2), ('hard',3)], onchange=set_difficulty)

loading = pygame_menu.Menu('Loading the Game...', 1400, 800, theme=themes.THEME_DARK)
loading.add.progress_bar("Progress", progressbar_id= "1", default=0, width=200)
update_loading = pygame.USEREVENT + 0

arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size = (10, 15))

world = pygame_menu.Menu("Choose your level...", 1400, 800, theme=themes.THEME_SOLARIZED)
world.add.selector('Level: ', [('World 1:1','1'), ('world 1:2', 'Medium'), ('World 1:3','Hard')], onchange=start_game())
world.add.button("Back", pygame_menu.events.BACK)
world.add.button("Start Game", start_game)

player1 = Player(100, 100, 50, 50)
enemy = Enemy(200, 200, 50, 50)

collide_damage = Collide_damage(x=0, y=0, max_damage=10)

health_bar = HealthBar(250,200,300,40,100, collide_damage=collide_damage)

#cooldown timer
last_collision_time = 0
cooldown = 1

run = True
while run:

    events = pygame.event.get()
    #death = Collide_damage
    #Player = entities.Player
    #Enemy = entities.Enemy

    #key = pygame.key.get_pressed()
    #if key[pygame.K_LEFT]:
     #   player1.move(-player1.velocity, 0)
    #if key[pygame.K_RIGHT]:
     #   player1.move(player1.velocity, 0)
    #if key[pygame.K_UP]:
     #   player1.move(0, -player1.velocity)
    #if key[pygame.K_DOWN]:
     #   player1.move(0, player1.velocity)

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
    #enemy.move_towards_player(player1)

    #pygame.draw.rect(window, (255,0,0), player)
    #player1.draw(screen)
    #enemy.draw(screen)
    #health_bar.draw(screen)

    pygame.display.update()
"""
    if player1.hitbox_player.colliderect(enemy.hitbox_enemy):
        result = health_bar.decrease_health(2)
        print("Collision detected! Health decreased.")
        if result == "retry":
            Player.reset(player1)
            Enemy.reset(enemy)
            health_bar.reset()
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

