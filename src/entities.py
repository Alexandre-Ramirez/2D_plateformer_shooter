import sys
import os
import pygame
import math
from environment import Worlds

screen = pygame.display.set_mode((1400, 800))
screen_width, screen_height = screen.get_size()

my_world = Worlds()

class Player():
    def __init__(self,x, y, scale, velocity):
        self.x = x
        self.y = y
        self.width = 140
        self.height  = 140
        self.flip = False
        self.velocity = velocity
        self.direction = 1
        self.screen_width = 1400
        self.SCROLL_THRESH = 200

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
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        #load all the image for the okayer
        animation_types = ['idle', 'run', 'jump', 'crunch']
        for animation in animation_types:
            #reset temporary the list of image
            temp_list = []
            #count number of files in the folder
            folder_path = f'image/player/{animation}'

            # Vérifie que le dossier existe avant de charger les images
            if os.path.exists(folder_path):
                # Récupère uniquement les fichiers PNG triés
                files = sorted([f for f in os.listdir(folder_path) if f.endswith('.png')])

                for file in files:
                    img_path = os.path.join(folder_path, file)
                    img = pygame.image.load(img_path)
                    img = pygame.transform.scale(img, (self.width, self.height))
                    temp_list.append(img)
                self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        # hitbox
        self.hitbox_w = int(self.width * 0.3)
        self.hitbox_h = int(self.height * 0.5)
        self.update_hitbox()

        self.hp = 100

        """
        self.anim_index = 0
        self.anim_timer = 0
        # load the jump sprite
        self.jump_sprites_right = [
            pygame.image.load(f'image/player/sprite_1.png').convert_alpha(),
            pygame.image.load(f'image/player/sprite_2.png').convert_alpha(),
            pygame.image.load(f'image/player/sprite_3.png').convert_alpha(),
            pygame.image.load(f'image/player/sprite_4.png').convert_alpha(),
            pygame.image.load(f'image/player/sprite_5.png').convert_alpha(),
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
    """

    def update_hitbox(self):
        #met à jour la hitbox
        self.hitbox_player = pygame.Rect (self.rect.x + (self.width - self.hitbox_w) // 2, self.rect.y + (self.height - self.hitbox_h) // 2 + 35, self.hitbox_w, self.hitbox_h)

    def draw(self, surface):
        surface.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        pygame.draw.rect(surface, (255, 0, 0), self.hitbox_player, 2)

    def move(self, moving_l, moving_r,moving_h,moving_d, jumping, on_ground):

        screen_scroll = 0

        dx=0
        dy=0

        if moving_l:
            dx = -self.velocity
            self.flip = True
            self.direction = -1
        if moving_r:
            dx = self.velocity
            self.flip = False
            self.direction = 1
        if moving_h:
            dy = -self.velocity
            self.flip = False
            self.direction = -1
        if moving_d:
            dy = self.velocity
            self.flip = False
            self.direction = 1
        if jumping and on_ground == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

            """
            self.vel_y += 0.75
            if self.vel_y > 10:
                self.vel_y
            dy += self.vel_y
            """
            if not self.on_ground:
                self.vel_y += self.gravity
                self.y += self.vel_y
                self.rect.topleft = (self.x, self.y)

            # check collision with floor
            """
            if self.rect.bottom + dy > 300:
                dy = 300 - self.rect.bottom
                self.in_air = False
            """
            print(f"Liste des obstacle: {my_world.obstacles_list}")
            # check collision with obstacle
            for tile in my_world.obstacles_list:
                # Impression pour voir la position du joueur et des obstacles
                print(f"Joueur - Rect : ({self.rect.x}, {self.rect.y}), Vitesse Y : {self.vel_y}")
                print(f"Obstacle - Rect : ({tile[1].x}, {tile[1].y}), Taille : ({tile[1].width}, {tile[1].height})")
                # check for colision in the y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + self.vel_y, self.width, self.height):
                    print(f"Collision détectée !")
                    if self.vel_y >= 0:  # player falling
                        self.y = tile[1].top - self.height  # put the player on top of the obstacle
                        self.vel_y = 0  # stop the falling
                        self.on_ground = True  # the player is on the ground
                        break
                    elif self.vel_y < 0:  # the player jump
                        self.y = tile[1].bottom  # the player goes on top of the obstacle
                        self.vel_y = 0  # stop the movement
                        break

            # update rectangle position
            self.rect.x += dx
            self.rect.y += dy






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

    """
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

        #check collision with obstacle
        for tile in my_world.obstacles_list:
            # Impression pour voir la position du joueur et des obstacles
            print(f"Joueur - Rect : ({self.rect.x}, {self.rect.y}), Vitesse Y : {self.vel_y}")
            print(f"Obstacle - Rect : ({tile[1].x}, {tile[1].y}), Taille : ({tile[1].width}, {tile[1].height})")
            #check for colision in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + self.vel_y, self.width, self.height):
                print(f"Collision détectée !")
                if self.vel_y > 0: #player falling
                    self.y = tile[1].top - self.height #put the player on top of the obstacle
                    self.vel_y = 0 #stop the falling
                    self.on_ground = True #the player is on the ground
                    break
                elif self.vel_y < 0: #the player jump
                    self.y = tile[1].bottom #the player goes on top of the obstacle
                    self.vel_y = 0 #stop the movement
                    break

        self.rect.topleft = (self.x, self.y)
        #self.update_hitbox()

        ###
            #check for colision in the y direction
            if tile[0].colliderect(self.rect.x, self.rect.y + self.y, self.width, self.height):
                #check if below the ground, jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                #check if above the ground, falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom

        self.rect.x += dx
        self.rect.y += dy

            if self.y >= 400:
                self.y = 400
                self.rect.topleft = (self.x, self.y) --> a voir
                self.jumping = False
                self.on_ground = True
                self.vel_y = 0
    
    """
    def update_animation(self):
        #update aniation
        ANIMATION_COOLDOWN = 100
        #update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if the animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


    def reset(self):
        self.x = self.x
        self.y = self.y
        self.rect.topleft = (self.x, self.y)
        #self.update_hitbox()
        #self.apply_gravity()

class Enemy:
    def __init__(self, platform):
        self.width = 150
        self.height = 150
        self.platform = platform
        self.rect = pygame.Rect(platform.rect.x + platform.rect.width // 2 - self.width // 2, platform.rect.y - self.height, self.width, self.height)
        self.speed = 1
        self.direction = 1
        self.detection_range = 400
        self.shooting = False
        self.last_shot_time = 0

        self.image1 = pygame.image.load("Images_ennemis/base_soldier.png")
        self.image1 = pygame.transform.scale(self.image1, (self.width, self.height))
        self.image2 = pygame.image.load("Images_ennemis/mid-ak47.png")
        self.image2 = pygame.transform.scale(self.image2, (self.width, self.height))
        self.image3 = pygame.image.load("Images_ennemis/high-magnum.png")
        self.image3 = pygame.transform.scale(self.image3, (self.width, self.height))

        # Assign HP to the 3 enemy types
        if platform.platform_id in [9, 10]:
            self.hp = 120
        elif platform.platform_id == 11:
            self.hp = 160
        else:
            self.hp = 80

        self.hitbox_w = int(self.width * 0.3)
        self.hitbox_h = int(self.height * 0.5)
        self.update_hitbox()

    def detect_player(self, player):
        # measure the distance
        distance_x = abs(self.hitbox_enemy.centerx - player.hitbox_player.centerx)
        vertical_overlap = (player.hitbox_player.bottom >= self.hitbox_enemy.top and player.hitbox_player.top <= self.hitbox_enemy.bottom)

        # turn the enemy around and start shooting
        if distance_x <= self.detection_range and vertical_overlap:
            self.shooting = True
            if player.hitbox_player.centerx < self.hitbox_enemy.centerx:
                self.direction = -1
            else:
                self.direction = 1
        else:
            self.shooting = False

    def update_hitbox(self):
        #met à jour la hitbox
        if self.direction == -1:
            self.hitbox_enemy = pygame.Rect (self.rect.x + (self.width - self.hitbox_w) // 2 + 11, self.rect.y + (self.height - self.hitbox_h) // 2 + 38, self.hitbox_w, self.hitbox_h)
        elif self.platform.platform_id == 11 and self.direction == -1:
            self.hitbox_enemy = pygame.Rect(self.rect.x + (self.width - self.hitbox_w) // 2 + 25, self.rect.y + (self.height - self.hitbox_h) // 2 + 38, self.hitbox_w, self.hitbox_h)
        elif self.platform.platform_id == 11 and self.direction == 1:
            self.hitbox_enemy = pygame.Rect(self.rect.x + (self.width - self.hitbox_w) // 2 - 14, self.rect.y + (self.height - self.hitbox_h) // 2 + 38, self.hitbox_w, self.hitbox_h)
        else:
            self.hitbox_enemy = pygame.Rect(self.rect.x + (self.width - self.hitbox_w) // 2 - 8, self.rect.y + (self.height - self.hitbox_h) // 2 + 38, self.hitbox_w, self.hitbox_h)

    def draw(self, surface):
        if self.platform.platform_id in [9, 10]:
            image = self.image2
        elif self.platform.platform_id == 11:
            image = self.image3
        else:
            image = self.image1

        if self.direction == 1:
            image = pygame.transform.flip(image, True, False)

        surface.blit(image, self.rect.topleft)
        pygame.draw.rect(surface, (255, 0, 0), self.hitbox_enemy, 2)


    def update(self, player):
        self.detect_player(player)

        # movement when not shooting
        if not self.shooting:
            self.rect.x += self.speed * self.direction
        # patrolling pattern
        #edge_offset = 2
        if (self.hitbox_enemy.left <= self.platform.rect.left and self.direction == -1) or (self.hitbox_enemy.right >= self.platform.rect.right and self.direction == 1):
            self.direction *= -1

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

class Projectiles:
    def __init__(self, x, y, radius, color, direction, shooter):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.direction = direction
        self.velocity = 10 * direction
        self.shooter = shooter

    def update(self):
        self.x += self.velocity

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

pygame.init()

velocity = 12