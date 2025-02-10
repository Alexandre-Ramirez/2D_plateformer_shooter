import pygame

# defining gravity value
gravity = 9.81

class Platform:
    def __init__(self, x, y, width, height, moving=False, speed=2, move_range=100):
        self.rect = pygame.Rect(x, y, width, height)
        self.moving = moving
        self.speed = speed
        self.move_range = move_range
        self.start_x = x  # Position initiale pour le mouvement horizontal
        self.direction = 1  # 1 = droite, -1 = gauche

    def update(self):
        """Met à jour la position de la plateforme si elle est mobile (mouvement horizontal)."""
        if self.moving:
            self.rect.x += self.speed * self.direction
            if abs(self.rect.x - self.start_x) >= self.move_range:
                self.direction *= -1  # Inverser la direction

    def draw(self, surface, color=(255, 255, 255)):
        pygame.draw.rect(surface, color, self.rect)


# Création des plateformes. à priori à mettre dans la boucle, après l'initiation de Pygame
#platforms = [
    #Platform(200, 175, 400, 50),  # Plateforme fine
    #Platform(700, 350, 350, 50),  # Plateforme épaisse
    #Platform(350, 550, 250, 50, moving=True, speed=3, move_range=250)  # Plateforme mobile
#]