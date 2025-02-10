import pygame

# defining gravity value
gravity = 9.81

# creating the platforms
platform_slim = pygame.Rect(100, 175, 450, 50)
platform_thick = pygame.Rect(300, 350, 350, 250)
platform_moving = pygame.Rect(450, 700, 200, 75)

# managing platform_moving's movement
platform_moving_vel = 5
# add in the game loop :    if platform_moving.left >= 300 or platform_moving.left < 100 :
#                               platform_moving_vel *= -1