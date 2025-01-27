#sleep permet de suspendre l'exécution d'un programme pendant une durée spécifique
from time import sleep
import pygame
import pygame_menu
from pygame_menu import themes
from pygame_menu.examples.simple import start_the_game, set_difficulty

pygame.init()
#setup pygame
screen = pygame.display.set_mode((800, 600),pygame.RESIZABLE)

#setup window's title
pygame.display.set_caption("Plateformer")
#setup bg color
#color = (125,125,125)

def set_diffulty(value, difficulty):
    print(value)
    print(difficulty)

def start_game():
    pass

def level_menu():
    mainmenu._open(level)

mainmenu = pygame_menu.Menu("Welcome to platfomer", 600, 400, theme=themes.THEME_DEFAULT)

mainmenu.add.text_input('Name : ', default="username",)
mainmenu.add.button('Play', start_game)
mainmenu.add.button('Levels', level_menu)
mainmenu.add.button('Quit', pygame_menu.events.EXIT)

level = pygame_menu.Menu("Levels", 600, 400, theme=themes.THEME_BLUE)
level.add.selector('Difficulty: ', [('Easy',1), ('Medium',2), ('Hard',3)], onchange=set_difficulty)

loading = pygame_menu.Menu('Loading the Game', 600, 400, theme=themes.THEME_DARK)
loading.add.progress_bar("Progress", progressbar_id= "1", default=0, width=200)
update_loading = pygame.USEREVENT + 0

arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size = (10, 15))


run = True
while run:

    events = pygame.event.get()

    for event in events:
        if event.type == update_loading:
            progress = loading.get_widget("1")
            progress.set_value(progress.get_value() +1)
            if progress.get_value() == 100:
                pygame.time.set_timer(update_loading, 0)
        if event.type == pygame.QUIT:
            run = False

    if mainmenu.is_enabled():
        mainmenu.update(events)
        mainmenu.draw(screen)
        if (mainmenu.get_current().get_selected_widget()):
            arrow.draw(screen, mainmenu.get_current().get_selected_widget())

    pygame.display.update()
