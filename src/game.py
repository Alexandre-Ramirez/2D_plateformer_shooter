#sleep permet de suspendre l'exécution d'un programme pendant une durée spécifique
from time import sleep
import pygame
import pygame_menu
from pygame_menu import themes
from pygame_menu.examples.simple import start_the_game, set_difficulty

pygame.init()
#setup pygame
screen = pygame.display.set_mode((1400, 800),pygame.RESIZABLE)

#setup window's title
pygame.display.set_caption("Plateformer")
#setup bg color
#color = (125,125,125)

#def draw_menu(screen):
    #take the size of the screen
screen_width, screen_height = screen.get_size()

# Crée un nouvel événement personnalisé pour signaler la fin du chargement
END_LOADING = pygame.USEREVENT +1

#def level_selection():
 #   menu._open(world)

def set_diffulty(value, difficulty):
    print(value)
    print(difficulty)

def start_game():
    menu._open(loading)
    pygame.time.set_timer(update_loading, 30)

    # Définir un temps après lequel le chargement est terminé (ex: 3 secondes)
    pygame.time.set_timer(END_LOADING, 3000)  # 3000 ms = 3 secondes

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
    menu.add.button('Play', start_game)
    menu.add.button('Levels', level_menu)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    return menu

menu = create_menu()

level = pygame_menu.Menu("Levels", 1400, 800, theme=themes.THEME_BLUE)
level.add.selector('Difficulty: ', [('Easy',1), ('Medium',2), ('Hard',3)], onchange=set_difficulty)

loading = pygame_menu.Menu('Loading the Game...', 1400, 800, theme=themes.THEME_DARK)
loading.add.progress_bar("Progress", progressbar_id= "1", default=0, width=200)
update_loading = pygame.USEREVENT + 0

arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size = (10, 15))

world = pygame_menu.Menu("Choose your level...", 1400, 800, theme=themes.THEME_SOLARIZED)
world.add.selector('Level: ', ['Easy', 'Medium', 'Hard'])
world.add.button("Back", pygame_menu.events.BACK)




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
        if event.type == END_LOADING:
            menu._open(world)

    if menu.is_enabled():
        menu.update(events)
        menu.draw(screen)
        if (menu.get_current().get_selected_widget()):
            arrow.draw(screen, menu.get_current().get_selected_widget())

    pygame.display.update()
