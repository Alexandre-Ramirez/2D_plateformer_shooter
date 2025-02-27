import sys

import pygame
import math
screen = pygame.display.set_mode((1400, 800),pygame.RESIZABLE)

class Player():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = velocity
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.hitbox_w = self.width + 5
        self.hitbox_h = self.height + 5
        self.update_hitbox()

    def update_hitbox(self):
        self.hitbox_player = pygame.Rect(
            self.x +(self.width-self.hitbox_w)//2,
            self.y +(self.height - self.hitbox_h)//2,
            self.hitbox_w,
            self.hitbox_h
        )

    def draw(self, surface):

        pygame.draw.rect(surface, 'red', self.rect)
        pygame.draw.rect(surface, 'black', self.hitbox_player,2)

    def move(self, dx, dy):
        #garde l'ancienne position avant le déplacement
        old_x = self.x
        old_y = self.y

        #déplacement
        self.x += dx
        self.y += dy

        self.limite_x = (60, 1340)
        self.limite_y = (60, 740)

        #Màj du joueur
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.update_hitbox()

        #vérif des limites
        if self.rect.left < self.limite_x[0] or self.rect.right > self.limite_x[1]:
            self.x = old_x
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        if self.rect.top < self.limite_y[0] or self.rect.bottom > self.limite_y[1]:
            self.y = old_y
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    def reset(self):
        self.x = self.x
        self.y = self.y
        self.rect.topleft = (self.x, self.y)
        self.update_hitbox()

class Enemy():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.velocity = velocity - 4

        self.hitbox_w = width + 5
        self.hitbox_h = height + 5
        self.update_hitbox()

    def update_hitbox(self):
        #met à jour la hitbox
        self.hitbox_enemy = pygame.Rect (
        self.rect.x + (self.width - self.hitbox_w) // 2,
        self.rect.y + (self.height - self.hitbox_h) // 2,
        self.hitbox_w,
        self.hitbox_h
    )

    def draw(self, window):

        pygame.draw.rect(window, 'green', self.rect)
        pygame.draw.rect(window, 'black', self.hitbox_enemy, 2)

    def move (self, dx, dy):
        #on garde l'ancienne position
        old_ex, old_ey = self.x, self.y

        self.rect.x += dx * velocity
        self.rect.y += dy * velocity

        self.limite_x = (60, 1340)
        self.limite_y = (60, 740)

        #MàJ de l'ennemie
        #self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        if self.rect.left < self.limite_x[0] or self.rect.right > self.limite_x[1]:
            self.rect.x = old_ex
            #self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        if self.rect.top < self.limite_y[0] or self.rect.bottom > self.limite_y[1]:
            self.rect.y = old_ey
            #self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.update_hitbox()

    def move_towards_player(self, player, ):
        #calculer la direction vers le joueur
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y

        #calculer la distance entre l'ennemi et le joueur
        dist = math.hypot(dx, dy)

        # Enemy AI: Move towards the player
        if dist != 0:
            dx /= dist
            dy /= dist

            #déplacer l'ennemi
            self.rect.x += dx * (self.velocity -2)
            self.rect.y += dy * (self.velocity -2)

            self.update_hitbox()

    def reset(self):
        self.rect.topleft = (self.x, self.y)

        self.update_hitbox()

class HealthBar():

    def __init__(self, x, y, width, height, max_hp, collide_damage):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hp = max_hp
        self.max_hp = max_hp
        self.collide_damage = collide_damage


    def draw(self, surface):
        #calculate health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, 'red', (700, 0, 300, 40))
        pygame.draw.rect(surface, 'green', (700, 0, int(300 * ratio), 40))

    def decrease_health(self,amount):
        self.hp -= amount
        print(f"Health decreased to {self.hp}")  # Debugging
        if self.hp <= 0:
            choice = self.collide_damage.show_death_screen(screen)
            if choice == "retry":
                self.reset()
                return "retry"
            elif choice == "exit":
                return "exit"
        return None

    def increase_health(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
            health = self.max_hp

    def reset(self):
        self.hp = self.max_hp

class Collide_damage():
    def __init__(self, x, y, max_damage):
        self.x = x
        self.y = y
        self.damage = max_damage
        self.max_damage = max_damage

    def show_death_screen(self,screen):
        font = pygame.font.Font(None, 74)
        text = font.render("You're dead dead!", True, (255, 0, 0))
        text_rect = text.get_rect(center=(400, 200))

        retry_button = pygame.Rect(250,300,200,50)
        exit_button = pygame.Rect(250, 400, 200, 50)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if retry_button.collidepoint(event.pos):
                        print("retry")
                        return "retry"
                    if exit_button.collidepoint(event.pos):
                        print("exit")
                        return "exit"

            #draw the window of death
            screen.fill((0,0,0))
            screen.blit(text, text_rect)

            #draw the buttons
            pygame.draw.rect(screen, (0,255,0), retry_button)
            pygame.draw.rect(screen, (255,0,0), exit_button)

            #text on the button
            font = pygame.font.Font(None, 36)
            retry_text = font.render("Retry", True, (0, 0, 0))
            exit_text = font.render("Exit", True, (0, 0, 0))
            screen.blit(retry_text, (retry_button.x +70, retry_button.y + 15))
            screen.blit(exit_text, (exit_button.x + 70, exit_button.y + 15))

            pygame.display.flip()

pygame.init()

velocity = 12