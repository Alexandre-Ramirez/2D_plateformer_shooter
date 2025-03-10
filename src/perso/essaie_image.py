import os
import pygame

image_path = 'image/background/main_menu.jpeg'
if not os.path.exists(image_path):
    print(f"Erreur : L'image '{image_path}' n'existe pas !")
else:
    menu_image = pygame.image.load(image_path)
    print("Image chargée avec succès !")
