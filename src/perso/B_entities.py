
import sys

import pygame
import math

from pygame_menu.examples.timer_clock import surface



screen = pygame.display.set_mode((1400, 800))
screen_width, screen_height = screen.get_size()

class Player():
    def __init__(self, x, y, scale):
        self.x = x
        self.y = y
        self.scale = scale
        self.player_image = pygame.image.load('image/player/sprite_8.png')
        self.width = self.player_image.get_width()
        self.height = self.player_image.get_height()
        self.velocity = velocity
        self.rect = self.player_image.get_rect()
        self.rect.center = (self.x, self.y)
        self.screen_width = 1400
        self.SCROLL_THRESH = 200

        #hitbox
        self.hitbox_w = self.width + 5
        self.hitbox_h = self.height + 5
        self.update_hitbox()

        #add jumping
        self.jumping = False
        self.vel_y = 0
        self.jump_height = 15
        self.gravity = 9.81
        self.on_ground = True

        #moves limit
        self.limite_x = (60, 1340)
        self.limite_y = (60, 740)

        #sprite
        #animation sprite
        self.anim_index = 0
        self.anim_timer = 0
        # load the jump sprite
        self.jump_sprites_right = [
            pygame.image.load(f'image/player/sprite_6.png').convert_alpha(),
            pygame.image.load(f'image/player/sprite_7.png').convert_alpha(),
            pygame.image.load(f'image/player/sprite_8.png').convert_alpha(),
            pygame.image.load(f'image/player/sprite_9.png').convert_alpha(),
            pygame.image.load(f'image/player/sprite_10.png').convert_alpha(),
        ]

        self.jump_sprites_left = [pygame.transform.flip(img, True, False) for img in self.jump_sprites_right]

        # load the walking sprite
        self.walk_sprites_right = [
            pygame.image.load(f'image/player/sprite_6.png').convert_alpha(),
            pygame.image.load(f'image/player/sprite_7.png').convert_alpha(),
            pygame.image.load(f'image/player/sprite_8.png').convert_alpha(),
            pygame.image.load(f'image/player/sprite_9.png').convert_alpha(),
            pygame.image.load(f'image/player/sprite_10.png').convert_alpha()
        ]

        self.walk_sprites_left = [pygame.transform.flip(img, True, False) for img in self.walk_sprites_right]

    def update_anim(self, moving, player_direction):
        if moving:
            self.anim_timer += 1
            if self.anim_timer >= 5:
                self.anim_index = (self.anim_index + 1) % len(self.anim_index)
                self.anim_timer = 0
        else:
            self.anim_timer = 0

    def update_hitbox(self):
        self.hitbox_player = pygame.Rect(
            self.x +(self.width-self.hitbox_w)//2,
            self.y +(self.height - self.hitbox_h)//2,
            self.hitbox_w,
            self.hitbox_h
        )

    def draw(self, surface, player_direction):
        if player_direction == "right":
            current_image = self.walk_sprites_right[self.anim_index]
        elif player_direction == "left":
            current_image = self.walk_sprites_left[self.anim_index]
        surface.blit(current_image, (self.x, self.y))
        pygame.draw.rect(surface, 'black', self.hitbox_player,2)

    def move(self, dx, dy):

        screen_scroll = 0

        #garde l'ancienne position avant le déplacement
        old_x = self.x
        old_y = self.y

        #déplacement
        self.x += dx
        self.y += dy

        # Màj du joueur
        self.rect.topleft = (self.x, self.y)
        self.update_hitbox()

        #maj scroll based on player position
        if self.rect.right > self.screen_width - self.SCROLL_THRESH or self.rect.left < self.SCROLL_THRESH:
            self.rect.x -= -dx
            screen_scroll = -dx

        #vérif des limites
        if self.rect.left < self.limite_x[0] or self.rect.right > self.limite_x[1]:
            self.x = old_x
            #self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        if self.rect.top < self.limite_y[0] or self.rect.bottom > self.limite_y[1]:
            self.y = old_y
            #self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        return screen_scroll

    def jumps(self):
        print(f"{self.y}")
        if not self.jumping:
            self.vel_y = self.jump_speed
            self.jumping = True

        if self.jumping:
            self.vel_y += self.y_gravity
            self.y += self.vel_y

            if self.y >= 400:
                self.y = 400
                self.jumping = False
                #self.update_hitbox()
                self.vel_y = 0

    def jump(self):
        if self.on_ground:
            print("Tentative de saut !")
            self.vel_y = -self.jump_height
            self.on_ground = False

    def apply_gravity(self):
        if not self.on_ground:
            self.vel_y += self.gravity
            self.y += self.vel_y
            self.rect.topleft = (self.x, self.y)

            if self.y <= 400:
                self.y = 400
                self.rect.topleft = (self.x, self.y)
                self.on_ground = True
                self.vel_y = 0

    def reset(self):
        self.x = self.x
        self.y = self.y
        self.rect.topleft = (self.x, self.y)
        self.update_hitbox()
        self.apply_gravity()

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
        #size and position of the death window
        death_screen_width = 400
        death_screen_height = 200
        death_screen_x = (screen.get_width() - death_screen_width) //2 #center horizental
        death_screen_y = (screen.get_height() - death_screen_height) //2 #center verticaly

        #create a surface semi transparant for the backscreen
        overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0,0,0, 128)) #light black 128/255

        #font and text
        font = pygame.font.Font(None, 74)
        text = font.render("You're dead dead!", True, (255, 0, 0))
        text_rect = text.get_rect(center=(death_screen_width //2,50))

        #buttons
        retry_button = pygame.Rect(50,100,120,50)
        exit_button = pygame.Rect(230, 100, 120, 50)

        #text ont the buttons
        font = pygame.font.Font(None, 36)
        retry_text = font.render("Retry", True, (0, 0, 0)) #black text
        retry_text_rect = retry_text.get_rect(center=retry_button.center)#center on the buttons

        exit_text = font.render("Exit", True, (0, 0, 0)) #black text
        exit_text_rect = exit_text.get_rect(center=exit_button.center) #center on the button

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #ajust the coordination of the mouse with the window of death
                    mouse_x, mouse_y = event.pos
                    relative_mouse_x = mouse_x - death_screen_x
                    relative_mouse_y = mouse_y - death_screen_y

                    if retry_button.collidepoint(relative_mouse_x, relative_mouse_y):
                        print("retry")
                        return "retry"
                    if exit_button.collidepoint(relative_mouse_x, relative_mouse_y):
                        print("exit")
                        return "exit"

            #draw the back screen
            screen.blit(overlay, (0, 0))

            #draw the window of death
            death_screen = pygame.Surface((death_screen_width, death_screen_height))
            death_screen.fill((50, 50, 50))
            death_screen.blit(text, text_rect)

            #draw the buttons
            pygame.draw.rect(death_screen, (0,255,0), retry_button)
            pygame.draw.rect(death_screen, (255,0,0), exit_button)

            #draw the text on the butons
            death_screen.blit(retry_text, retry_text_rect)
            death_screen.blit(exit_text, exit_text_rect)

            screen.blit(death_screen, (death_screen_x, death_screen_y))

            pygame.display.flip()

pygame.init()

velocity = 12
