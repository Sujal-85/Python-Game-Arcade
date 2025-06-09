import random
import pygame
import os
import csv
import button
import time
from pygame import mixer
from tkinter import *
import customtkinter
from subprocess import call
from PIL import Image,ImageTk
import random
import database
from mainGui import *
import mysql.connector
import time
import messagebox
class Shooter:

    # constructor
    def __init__(self , root2, username_lg="",shooter1=""):

        # -----------------------------------------------------------------------------------------------
        # -----------------------------------------------------------------------------------------------
        pygame.init ( )
        mixer.init ( )
        self.root2 = root2
        self.root2.geometry('1200x700+160+50')
        self.root2.resizable(False,False)
        # print(username_lg)

        def startGame():
            self.start = time.time()

            width = 1200
            height = 700

            screen = pygame.display.set_mode((width, height))
            pygame.display.set_caption('Shooter Game')

            clock = pygame.time.Clock()
            FPS = 60

            GRAVITY = 0.5
            scroll_thresh = 200
            rows = 16
            cols = 150
            TILE_SIZE = height // rows
            TILE_TYPES = 22
            screen_scroll = 0
            bg_scroll = 0
            level = 1
            max_levels = 3
            start_game = False
            # define player action variables
            moving_left = False
            moving_right = False
            shoot = False
            grenade = False
            grenade_thrown = False

            pygame.mixer.music.load('song/music.mp3')
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1, 0.0, 5000)
            jump_fx = pygame.mixer.Sound('song/jump.wav')
            jump_fx.set_volume(0.5)
            shot_fx = pygame.mixer.Sound('song/shot.wav')
            shot_fx.set_volume(0.5)
            grenade_fx = pygame.mixer.Sound('song/grenade.wav')
            grenade_fx.set_volume(0.5)
            coin_fx = pygame.mixer.Sound('song/collectcoin.mp3')
            coin_fx.set_volume(0.5)
            success_fx = pygame.mixer.Sound('song/success.mp3')
            success_fx.set_volume(0.5)

            start_img = pygame.image.load('images/start.png').convert_alpha()
            exit_img = pygame.image.load('images/exit_btn.png').convert_alpha()
            restart = pygame.image.load('images/restart.png').convert_alpha()
            bg_img = pygame.image.load('images/bgimg.png').convert_alpha()
            home = pygame.image.load('images/gamehouse.png').convert_alpha()
            Next = pygame.image.load('images/next.png').convert_alpha()

            pine1_img = pygame.image.load('images/pine1.png').convert_alpha()
            pine2_img = pygame.image.load('images/pine2.png').convert_alpha()
            mountain_img = pygame.image.load('images/mountain.png').convert_alpha()
            sky_img = pygame.image.load('images/sky_cloud.png').convert_alpha()

            img_list = []
            for x in range(TILE_TYPES):
                img = pygame.image.load(f'images/tiles/{x}.png')
                img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                img_list.append(img)
            bullet_img = pygame.image.load('images/bullet.png').convert_alpha()
            grenade_img = pygame.image.load('images/grenade.png').convert_alpha()
            heal_box_img = pygame.image.load('images/health_box.png').convert_alpha()
            ammo_box_img = pygame.image.load('images/ammo_box.png').convert_alpha()
            grenade_box_img = pygame.image.load('images/grenade_box.png').convert_alpha()
            coin_img = pygame.image.load('images/coin.png').convert_alpha()
            item_boxes = {
                'Health': heal_box_img,
                'Ammo': ammo_box_img,
                'Grenade': grenade_box_img,
                'coin': coin_img

            }
            b=(0,0,0,100)
            BG = (144, 201, 120)
            RED = (255, 0, 0)
            WHITE = (255, 255, 255)
            GREEN = (0, 255, 0)
            BLACK = (0, 10, 20)
            pink = (235, 65, 54)

            font = pygame.font.SysFont('Futura', 30)
            font1 = pygame.font.SysFont('Artifakt Element Heavy', 80)
            font2 = pygame.font.SysFont('Arial Black', 30)
            font3 = pygame.font.SysFont('Comic Sans MS', 30)

            def draw_text(text, font, text_col, x, y):
                img = font.render(text, True, text_col)
                screen.blit(img, (x, y))

            def draw_bg():
                screen.fill(BG)
                w = sky_img.get_width()
                for x in range(5):
                    screen.blit(sky_img, ((x * w) - bg_scroll * 0.5, 0))
                    screen.blit(mountain_img, ((x * w) - bg_scroll * 0.6, height - mountain_img.get_height() - 300))
                    screen.blit(pine1_img, ((x * w) - bg_scroll * 0.7, height - pine1_img.get_height() - 150))
                    screen.blit(pine2_img, ((x * w) - bg_scroll * 1, height - pine2_img.get_height()))

            def reset_level():
                enemy_group.empty()
                bullet_group.empty()
                grenade_group.empty()
                explosion_group.empty()
                item_box_group.empty()
                decoration_group.empty()
                water_group.empty()
                # coin_group.empty()
                exit_group.empty()

                # create empty tile list
                data = []
                for row in range(rows):
                    r = [-1] * cols
                    data.append(r)
                return data

            class Soldier(pygame.sprite.Sprite):
                frame_index: int

                def __init__(self, char_type, x, y, scale, speed, ammo, grenades):
                    pygame.sprite.Sprite.__init__(self)
                    self.alive = True
                    self.char_type = char_type
                    self.speed = speed
                    self.ammo = ammo
                    self.coin = 0
                    self.enemy_kill = 0
                    self.start_ammo = ammo
                    self.shoot_cooldown = 0
                    self.grenades = grenades
                    self.health = 100
                    self.max_health = self.health
                    self.direction = 1
                    self.vel_y = 0
                    self.jump = False
                    self.in_air = True
                    self.flip = False
                    self.animation_list = []
                    self.frame_index = 0
                    self.action = 0
                    self.update_time = pygame.time.get_ticks()

                    self.move_counter = 0
                    self.vision = pygame.Rect(0, 0, 150, 20)
                    self.idling = False
                    self.idling_counter = 0

                    animation_types = ['idle', 'run', 'jump', 'death']

                    for animation in animation_types:
                        temp_list = []
                        num_of_frames = len(os.listdir(f'images/{self.char_type}/{animation}'))
                        for i in range(num_of_frames):
                            img = pygame.image.load(f'images/{self.char_type}/{animation}/{i}.png').convert_alpha()
                            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                            temp_list.append(img)
                            # self.animation_list.append(img)
                        self.animation_list.append(temp_list)
                        # temp_list =[]
                        # for i in range(6):
                        #     img = pygame.image.load(images/{self.char_type}/run/{i}.png')
                        #     img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                        #     # self.animation_list.append(img)
                        #     temp_list.append(img)
                        #     # self.animation_list.append(img)
                        # self.animation_list.append(temp_list)
                    self.image = self.animation_list[self.action][self.frame_index]

                    self.rect = self.image.get_rect()
                    self.rect.center = (x, y)
                    self.width = self.image.get_width()
                    self.height = self.image.get_height()

                def update(self):
                    self.update_animation()
                    self.check_alive()

                    if self.shoot_cooldown > 0:
                        self.shoot_cooldown -= 1

                def move(self, ml, mr):

                    screen_scroll = 0
                    dx = 0
                    dy = 0
                    if ml:
                        dx = -self.speed
                        self.flip = True
                        self.direction = -1

                    if mr:
                        dx = self.speed
                        self.flip = False
                        self.direction = 1

                    if self.jump and self.in_air == False:
                        self.vel_y = -11
                        self.jump = False
                        self.in_air = True

                    self.vel_y += GRAVITY
                    if self.vel_y > 10:
                        self.vel_y
                    dy += self.vel_y

                    for tile in world.obstacle_list:
                        if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                            dx = 0
                            # if self.char_type == 'enemy':
                            #     self.direction *= -1
                            #     self.move_counter = 0
                        if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                            if self.vel_y < 0:
                                self.vel_y = 0
                                dy = tile[1].bottom - self.rect.top
                            elif self.vel_y >= 0:
                                self.vel_y = 0
                                self.in_air = False
                                dy = tile[1].top - self.rect.bottom

                    if pygame.sprite.spritecollide(self, water_group, False):
                        self.health = 0

                    level_complete = False
                    if pygame.sprite.spritecollide(self, exit_group, False):
                        level_complete = True

                    if self.rect.bottom > height:
                        self.health = 0

                    if not self.alive:
                        self.enemy_kill += 1

                    if self.char_type == 'player':
                        if self.rect.left + dx < 0 or self.rect.right + dx > width:
                            dx = 0

                    self.rect.x += dx
                    self.rect.y += dy

                    if self.char_type == 'player':
                        if (self.rect.right > width - scroll_thresh and bg_scroll < (world.level_length * TILE_SIZE) - width \
                                or (self.rect.left < scroll_thresh) and bg_scroll > abs(dx)):
                            self.rect.x -= dx
                            screen_scroll = -dx

                    return screen_scroll, level_complete

                def shoot(self):
                    if self.shoot_cooldown == 0 and self.ammo > 0:
                        self.shoot_cooldown = 30
                        bullet = Bullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery,
                                        self.direction)
                        bullet_group.add(bullet)
                        self.ammo -= 1
                        shot_fx.play()

                def ai(self):
                    if self.alive and player.alive:
                        if self.idling == False and random.randint(1, 500) == 1:
                            self.update_action(0)
                            self.idling = True
                            self.idling_counter = 50
                        if self.vision.colliderect(player.rect):
                            self.update_action(0)
                            self.shoot()

                        else:
                            if not self.idling:
                                if self.direction == 1:
                                    ai_moving_right = True

                                else:
                                    ai_moving_right = False

                                ai_moving_left = not ai_moving_right
                                self.move(ai_moving_left, ai_moving_right)
                                self.update_action(1)
                                self.move_counter += 1
                                self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

                                if self.move_counter > TILE_SIZE:
                                    self.direction *= -1
                                    self.move_counter *= -1

                            else:
                                self.idling_counter -= 1
                                if self.idling_counter <= 0:
                                    self.idling = False
                    self.rect.x += screen_scroll

                def update_animation(self):
                    ANIMATION_COOLDOWN = 100
                    self.image = self.animation_list[self.action][self.frame_index]
                    if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
                        self.update_time = pygame.time.get_ticks()
                        self.frame_index += 1

                    if self.frame_index >= len(self.animation_list[self.action]):
                        if self.action == 3:
                            self.frame_index = len(self.animation_list[self.action]) - 1

                        else:
                            self.frame_index = 0

                def update_action(self, new_action):
                    if new_action != self.action:
                        self.action = new_action
                        self.frame_index = 0
                        self.update_time = pygame.time.get_ticks()

                def check_alive(self):
                    if self.health <= 0:
                        self.health = 0
                        self.speed = 0
                        self.alive = False
                        self.update_action(3)

                def draw(self):
                    screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

            class World():
                def __init__(self):
                    self.obstacle_list = []

                def process_data(self, data):
                    self.level_length = len(data[0])

                    for y, row in enumerate(data):

                        for x, tile in enumerate(row):
                            if tile >= 0:
                                img = img_list[tile]
                                img_rect = img.get_rect()
                                img_rect.x = x * TILE_SIZE
                                img_rect.y = y * TILE_SIZE
                                tile_data = (img, img_rect)
                                if tile >= 0 and tile <= 8:
                                    self.obstacle_list.append(tile_data)
                                elif tile >= 9 and tile <= 10:
                                    water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                                    water_group.add(water)
                                elif tile >= 11 and tile <= 14:
                                    decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                                    decoration_group.add(decoration)
                                elif tile == 15:
                                    player = Soldier('player', x * TILE_SIZE, y * TILE_SIZE, 1.65, 5, 20, 5)
                                    health_bar = HealthBar(10, 10, player.health, player.health)
                                elif tile == 16:
                                    enemy = Soldier('enemy', x * TILE_SIZE, y * TILE_SIZE, 1.65, 2, 20, 0)
                                    enemy_group.add(enemy)
                                elif tile == 19:
                                    item_box = ItemBox('Health', x * TILE_SIZE, y * TILE_SIZE)
                                    item_box_group.add(item_box)
                                elif tile == 17:
                                    item_box = ItemBox('Ammo', x * TILE_SIZE, y * TILE_SIZE)
                                    item_box_group.add(item_box)
                                elif tile == 18:
                                    item_box = ItemBox('Grenade', x * TILE_SIZE, y * TILE_SIZE)
                                    item_box_group.add(item_box)
                                elif tile == 21:
                                    item_box = ItemBox('coin', x * TILE_SIZE, y * TILE_SIZE)
                                    item_box_group.add(item_box)
                                elif tile == 20:
                                    exit1 = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                                    exit_group.add(exit1)
                    return player, health_bar

                def draw(self):
                    for tile in self.obstacle_list:
                        tile[1][0] += screen_scroll
                        screen.blit(tile[0], tile[1])

            class Decoration(pygame.sprite.Sprite):
                def __init__(self, img, x, y):
                    pygame.sprite.Sprite.__init__(self)
                    self.image = img
                    self.rect = self.image.get_rect()
                    self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

                def update(self):
                    self.rect.x += screen_scroll

            class Water(pygame.sprite.Sprite):
                def __init__(self, img, x, y):
                    pygame.sprite.Sprite.__init__(self)
                    self.image = img
                    self.rect = self.image.get_rect()
                    self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

                def update(self):
                    self.rect.x += screen_scroll

            class Exit(pygame.sprite.Sprite):
                def __init__(self, img, x, y):
                    pygame.sprite.Sprite.__init__(self)
                    self.image = img
                    self.rect = self.image.get_rect()
                    self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

                def update(self):
                    self.rect.x += screen_scroll

            class ItemBox(pygame.sprite.Sprite):
                def __init__(self, item_type, x, y, ):
                    pygame.sprite.Sprite.__init__(self)
                    self.item_type = item_type
                    self.image = item_boxes[self.item_type]
                    self.rect = self.image.get_rect()
                    self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

                def update(self):
                    self.rect.x += screen_scroll
                    if pygame.sprite.collide_rect(self, player):
                        if self.item_type == 'Health':
                            player.health += 25
                            if player.health > player.max_health:
                                player.health = player.max_health

                        elif self.item_type == 'Ammo':
                            player.ammo += 15
                        elif self.item_type == 'Grenade':
                            player.grenades += 3
                        elif self.item_type == 'coin':
                            coin_fx.play()
                            player.coin += 1

                        self.kill()

            class HealthBar:
                def __init__(self, x, y, health, max_health):
                    self.x = x
                    self.y = y
                    self.health = health
                    self.max_health = max_health

                def draw(self, health):
                    self.health = health

                    ratio = self.health / self.max_health
                    pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
                    pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
                    pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))

            class Bullet(pygame.sprite.Sprite):
                def __init__(self, x, y, direction):
                    pygame.sprite.Sprite.__init__(self)
                    self.speed = 10
                    self.image = bullet_img
                    self.rect = self.image.get_rect()
                    self.rect.center = (x, y)
                    self.direction = direction

                def update(self):
                    self.rect.x += (self.direction * self.speed) + screen_scroll
                    if self.rect.right < 0 or self.rect.left > width:
                        self.kill()

                    for tile in world.obstacle_list:
                        if tile[1].colliderect(self.rect):
                            self.kill()
                    if pygame.sprite.spritecollide(player, bullet_group, False):
                        if player.alive:
                            player.health -= 5
                            self.kill()
                    for enemy in enemy_group:
                        if pygame.sprite.spritecollide(enemy, bullet_group, False):
                            if enemy.alive:
                                enemy.health -= 50
                                # print(enemy.health)
                                if enemy.health == 0:
                                    player.enemy_kill += 1

                                self.kill()

            class Grenade(pygame.sprite.Sprite):
                def __init__(self, x, y, direction):
                    pygame.sprite.Sprite.__init__(self)
                    self.timer = 100
                    self.vel_y = -11
                    self.speed = 7
                    self.image = grenade_img
                    self.rect = self.image.get_rect()
                    self.rect.center = (x, y)
                    self.width = self.image.get_width()
                    self.height = self.image.get_height()
                    self.direction = direction

                def update(self, enemy_health=None):
                    self.vel_y += GRAVITY
                    dx = self.direction * self.speed
                    dy = self.vel_y

                    for tile in world.obstacle_list:
                        if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                            self.direction *= -1
                            dx = self.direction * self.speed
                        if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                            self.speed = 0
                            if self.vel_y < 0:
                                self.vel_y = 0
                                dy = tile[1].bottom - self.rect.top
                            elif self.vel_y >= 0:
                                self.vel_y = 0
                                dy = tile[1].top - self.rect.bottom

                            self.direction *= -1
                            dx = self.direction * self.speed

                    self.rect.x += dx + screen_scroll
                    self.rect.y += dy

                    self.timer -= 1
                    if self.timer <= 0:
                        self.kill()
                        grenade_fx.play()
                        explosion = Explosion(self.rect.x, self.rect.y, 0.5)
                        explosion_group.add(explosion)
                        if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and \
                                abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                            player.health -= 50

                        for enemy in enemy_group:
                            if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and \
                                    abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                                enemy.health -= 50

            class Explosion(pygame.sprite.Sprite):
                def __init__(self, x, y, scale):
                    pygame.sprite.Sprite.__init__(self)
                    self.images = []
                    for num in range(1, 6):
                        img = pygame.image.load(f'images/exp{num}.png').convert_alpha()
                        img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                        self.images.append(img)

                    self.frame_index = 0
                    self.image = self.images[self.frame_index]
                    self.rect = self.image.get_rect()
                    self.rect.center = (x, y)
                    self.counter = 0

                def update(self):
                    self.rect.x += screen_scroll
                    EXPLOSION_SPEED = 4
                    self.counter += 1
                    if self.counter >= EXPLOSION_SPEED:
                        self.counter = 0
                        self.frame_index += 1
                        if self.frame_index >= len(self.images):
                            self.kill()
                        else:
                            self.image = self.images[self.frame_index]

            class ScreenFade:
                def __init__(self, direction, colour, speed):
                    self.direction = direction
                    self.colour = colour
                    self.speed = speed
                    self.fade_counter = 0

                def fade(self):
                    fade_complete = False
                    self.fade_counter += self.speed
                    pygame.draw.rect(screen, self.colour, (0, 0, width, 0 + self.fade_counter))
                    if self.fade_counter >= width:
                        fade_complete = True

                    return fade_complete

            class ScreenFad_Success:
                def __init__(self, direction, colour, speed):
                    self.direction = direction
                    self.colour = colour
                    self.speed = speed
                    self.fade_counter = 0

                def fade(self):
                    fade_complete = False
                    self.fade_counter += self.speed
                    pygame.draw.rect(screen, self.colour, (0, 0, width, 0 + self.fade_counter))
                    if self.fade_counter >= width:
                        fade_complete = True

                    return fade_complete

            death_fade = ScreenFade(2, BLACK, 7)
            success_fade = ScreenFade(5, BLACK, 6)

            start_button = button.Button(width // 2 - 160, height // 2, start_img, 1)
            # exit_button = button.Button(width // 2 -110 , height // 2 + 50,exit_img, 1 )
            # restart_button = button.Button(width // 2 - 80  , height // 2 +40, restart, 2 )
            home_button = button.Button(width // 2 - 300, height // 2 + 30, home, 1)
            NEXT_button = button.Button(width // 2 + 190, height // 2 + 90, Next, 1)

            enemy_group = pygame.sprite.Group()
            bullet_group = pygame.sprite.Group()
            grenade_group = pygame.sprite.Group()
            explosion_group = pygame.sprite.Group()
            item_box_group = pygame.sprite.Group()
            decoration_group = pygame.sprite.Group()
            water_group = pygame.sprite.Group()
            # coin_group = pygame.sprite.Group()
            exit_group = pygame.sprite.Group()

            # create empty tile list
            world_data = []
            for row in range(rows):
                r = [-1] * cols
                world_data.append(r)

            with open(f'csv files/level{level}_data.csv', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                        world_data[x][y] = int(tile)
            world = World()
            player, health_bar = world.process_data(world_data)

            run = True
            while run:

                clock.tick(FPS)

                if not start_game:
                    start_game = True
                    conn = mysql.connector.connect ( host = 'localhost' , password = 'Suj@y935974' ,
                                                     user = 'root' , database = 'game' )
                    Cursor_obj = conn.cursor ( )
                    query = " update create_account set Recently_played = %s where username= %s"
                    val = (shooter1 , username_lg)
                    Cursor_obj.execute ( query , val )
                    conn.commit ( )
                    conn.close ( )
                else:
                    draw_bg()
                    world.draw()
                    health_bar.draw(player.health)

                    draw_text('AMMO:', font, WHITE, 10, 35)
                    # for x in range(player.ammo):
                    draw_text(f'{player.ammo}', font, WHITE, 90, 35)
                    screen.blit(bullet_img, (130, 40))
                    draw_text('GRENADES:', font, WHITE, 10, 60)
                    for x in range(player.grenades):
                        screen.blit(grenade_img, (135 + (x * 15), 60))
                    draw_text('COINS:', font, WHITE, 10, 85)
                    screen.blit(coin_img, (120, 80))
                    draw_text(f'{player.coin}', font, WHITE, 90, 85)
                    # entry = Entry ( screen , fg = 'blue' , bg = 'white',border = 0 )
                    # entry.place ( x = 500 , y = 160 )
                    # for x in range(3600, 0, -1):
                    #     seconds = x % 60
                    #     minutes = int(x / 60) % 60
                    #     hours = int(x / 3600)
                    #     draw_text(f"Time :    {hours:02}   :    {minutes:02}   :  {seconds:02} ",font3, WHITE, 800,25 )

                    player.update()
                    player.draw()

                    for enemy in enemy_group:
                        enemy.ai()
                        enemy.update()
                        enemy.draw()

                    bullet_group.update()
                    grenade_group.update()
                    explosion_group.update()
                    item_box_group.update()
                    decoration_group.update()
                    water_group.update()
                    exit_group.update()
                    bullet_group.draw(screen)
                    grenade_group.draw(screen)
                    explosion_group.draw(screen)
                    item_box_group.draw(screen)
                    decoration_group.draw(screen)
                    water_group.draw(screen)
                    exit_group.draw(screen)

                    if player.alive:

                        if shoot:
                            player.shoot()


                        elif grenade and grenade_thrown == False and player.grenades > 0:
                            grenade = Grenade(player.rect.centerx + (0.5 * player.rect.size[0]),
                                              player.rect.top, player.direction)
                            grenade_group.add(grenade)
                            grenade_thrown = True
                            player.grenades -= 1

                        if player.in_air:
                            player.update_action(2)

                        elif moving_left or moving_right:
                            player.update_action(1)
                        else:
                            player.update_action(0)
                        # player1.draw()
                        screen_scroll, level_complete = player.move(moving_left, moving_right)
                        bg_scroll -= screen_scroll
                        if level_complete:
                            pygame.mixer.music.stop()
                            success_fx.play(2, 0, 1000)
                            if success_fade.fade():

                                restart_button = button.Button(width // 2 - 80, height // 2 + 40, restart, 2)
                                screen_scroll = 0
                                draw_text('Shooter Game', font1, WHITE, 350, 70)
                                draw_text(f'Level {level} : Level is successfully completed !  ', font2, WHITE, 280, 200)
                                #
                                draw_text(f'Coins:   {player.coin} ', font3, WHITE, 370, 270)
                                draw_text(f'Enemy Kills:   {player.enemy_kill} ', font3, WHITE, 630, 270)
                                draw_text('Home', font3, WHITE, 360, 540)
                                draw_text('Next', font3, WHITE, 800, 540)
                                draw_text ( 'Your Score : ' , font3 , WHITE , 480 , 340 )
                                screen.blit(coin_img, (520, 270))

                                if player.coin == 25 and player.enemy_kill == 23:
                                    draw_text ( f'2500' , font3 , WHITE , 660 , 340 )
                                    try:
                                        conn = mysql.connector.connect ( host = 'localhost' , password = 'Suj@y935974' ,
                                                                         user = 'root' , database = 'game' )
                                        Cursor_obj = conn.cursor ( )
                                        query = " update create_account set score_shooter = %s where username= %s"
                                        val = (f'Level {level} score :2500' , username_lg)
                                        Cursor_obj.execute ( query , val )
                                        conn.commit ( )
                                        conn.close ( )

                                    except:
                                        messagebox.showinfo ( "Invalid" , "Something Went Wrong !" )

                                elif (player.coin < 25 or player.coin >= 23) and player.enemy_kill > 22:
                                    draw_text ( f'2000' , font3 , WHITE , 660 , 340 )
                                    try:
                                        conn = mysql.connector.connect ( host = 'localhost' , password = 'Suj@y935974' ,
                                                                         user = 'root' , database = 'game' )
                                        Cursor_obj = conn.cursor ( )
                                        query = " update create_account set score_shooter = %s where username= %s"
                                        val = (f'Level {level} score :2000' , username_lg)
                                        Cursor_obj.execute ( query , val )
                                        conn.commit ( )
                                        conn.close ( )

                                    except:
                                        messagebox.showinfo ( "Invalid" , "Something Went Wrong !" )

                                elif (player.coin < 23 or player.coin >=21) and player.enemy_kill > 20:
                                    draw_text ( f'1500' , font3 , WHITE , 660 , 340 )
                                    try:
                                        conn = mysql.connector.connect ( host = 'localhost' , password = 'Suj@y935974' ,
                                                                         user = 'root' , database = 'game' )
                                        Cursor_obj = conn.cursor ( )
                                        query = " update create_account set score_shooter = %s where username= %s"
                                        val = (f'Level {level} score :1500' , username_lg)
                                        Cursor_obj.execute ( query , val )
                                        conn.commit ( )
                                        conn.close ( )

                                    except:
                                        messagebox.showinfo ( "Invalid" , "Something Went Wrong !" )

                                elif (player.coin < 21 or player.coin >=18) and player.enemy_kill >=18:
                                    draw_text ( f'1000' , font3 , WHITE , 660 , 340 )
                                    try:
                                        conn = mysql.connector.connect ( host = 'localhost' , password = 'Suj@y935974' ,
                                                                         user = 'root' , database = 'game' )
                                        Cursor_obj = conn.cursor ( )
                                        query = " update create_account set score_shooter = %s where username= %s"
                                        val = (f'Level {level} score :1000' , username_lg)
                                        Cursor_obj.execute ( query , val )
                                        conn.commit ( )
                                        conn.close ( )


                                    except:
                                        messagebox.showinfo ( "Invalid" , "Something Went Wrong !" )

                                elif (player.coin < 18 or player.coin >=15) and player.enemy_kill >=12:
                                    draw_text ( f'800' , font3 , WHITE , 660 , 340 )
                                    try:
                                        conn = mysql.connector.connect ( host = 'localhost' , password = 'Suj@y935974' ,
                                                                         user = 'root' , database = 'game' )
                                        Cursor_obj = conn.cursor ( )
                                        query = " update create_account set score_shooter = %s where username= %s"
                                        val = (f'Level {level} score :800' , username_lg)
                                        Cursor_obj.execute ( query , val )
                                        conn.commit ( )
                                        conn.close ( )


                                    except:
                                        messagebox.showinfo ( "Invalid" , "Something Went Wrong !" )

                                elif (player.coin < 15 or player.coin >=10) and player.enemy_kill >=9:
                                    draw_text ( f'600' , font3 , WHITE , 660 , 340 )
                                    try:
                                        conn = mysql.connector.connect ( host = 'localhost' , password = 'Suj@y935974' ,
                                                                         user = 'root' , database = 'game' )
                                        Cursor_obj = conn.cursor ( )
                                        query = " update create_account set score_shooter = %s where username= %s"
                                        val = (f'Level {level} score :600' , username_lg)
                                        Cursor_obj.execute ( query , val )
                                        conn.commit ( )
                                        conn.close ( )


                                    except:
                                        messagebox.showinfo ( "Invalid" , "Something Went Wrong !" )

                                elif (player.coin < 10 or player.coin >=6) and player.enemy_kill >= 6:
                                    draw_text ( f'400' , font3 , WHITE , 660 , 340 )
                                    try:
                                        conn = mysql.connector.connect ( host = 'localhost' , password = 'Suj@y935974' ,
                                                                         user = 'root' , database = 'game' )
                                        Cursor_obj = conn.cursor ( )
                                        query = " update create_account set score_shooter = %s where username= %s"
                                        val = (f'Level {level} score :400' , username_lg)
                                        Cursor_obj.execute ( query , val )
                                        conn.commit ( )
                                        conn.close ( )


                                    except:
                                        messagebox.showinfo ( "Invalid" , "Something Went Wrong !" )

                                elif (player.coin < 6 or player.coin >=4) and player.enemy_kill >=4:
                                    draw_text ( f'300' , font3 , WHITE , 660 , 340 )
                                    try:
                                        conn = mysql.connector.connect ( host = 'localhost' , password = 'Suj@y935974' ,
                                                                         user = 'root' , database = 'game' )
                                        Cursor_obj = conn.cursor ( )
                                        query = " update create_account set score_shooter = %s where username= %s"
                                        val = (f"Level {level} score :300" , username_lg)
                                        Cursor_obj.execute ( query , val )
                                        conn.commit ( )
                                        conn.close ( )

                                    except:
                                        messagebox.showinfo ( "Invalid" , "Something Went Wrong !" )

                                elif (player.coin < 4 or player.coin >=2) and player.enemy_kill >=2:
                                    draw_text ( f'200' , font3 , WHITE , 660 , 340 )
                                    try:
                                        conn = mysql.connector.connect ( host = 'localhost' , password = 'Suj@y935974' ,
                                                                         user = 'root' , database = 'game' )
                                        Cursor_obj = conn.cursor ( )
                                        query = " update create_account set score_shooter = %s where username= %s"
                                        val = (f"Level {level} score :200" , username_lg)
                                        Cursor_obj.execute ( query , val )
                                        conn.commit ( )
                                        conn.close ( )


                                    except:
                                        messagebox.showinfo ( "Invalid" , "Something Went Wrong !" )

                                elif (player.coin < 2 or player.coin >=1) and player.enemy_kill >=1:
                                    draw_text ( f'100' , font3 , WHITE , 660 , 340 )
                                    try:
                                        conn = mysql.connector.connect ( host = 'localhost' , password = 'Suj@y935974' ,
                                                                         user = 'root' , database = 'game' )
                                        Cursor_obj = conn.cursor ( )
                                        query = " update create_account set score_shooter = %s where username= %s"
                                        val = (f'Level {level} score :100' , username_lg)
                                        Cursor_obj.execute ( query , val )
                                        # messagebox.showinfo ( "Success" , "Thank You ! For Rating Us" )
                                        conn.commit ( )
                                        conn.close ( )

                                    except:
                                        messagebox.showinfo ( "Invalid" , "Something Went Wrong !" )

                                elif (player.coin >1 and player.enemy_kill) == 0:
                                    draw_text ( '0' , font3 , WHITE , 660 , 340 )
                                    try:
                                        conn = mysql.connector.connect ( host = 'localhost' , password = 'Suj@y935974' ,user = 'root' ,database = 'game' )
                                        Cursor_obj = conn.cursor ( )
                                        query = " update create_account set score_shooter = %s where username= %s"
                                        val = ( f'Level {level} score :0', username_lg)
                                        Cursor_obj.execute ( query , val )
                                        # messagebox.showinfo ( "Success" , "Thank You ! For Rating Us" )
                                        conn.commit ( )
                                        conn.close ( )

                                    except:
                                        messagebox.showinfo ( "Invalid" , "Something Went Wrong !" )


                                success_fx.stop()

                                if home_button.draw(screen):
                                    self.end = time.time ( )
                                    self.result = int ( self.end - self.start )
                                    print ( self.result )
                                    self.conn1 = mysql.connector.connect ( host = 'localhost' ,
                                                                           password = 'Suj@y935974' , user = 'root' ,
                                                                           database = 'game' )
                                    self.Cursor_obj = self.conn1.cursor ( )
                                    self.Cursor_obj.execute (
                                        f" update create_account set played_time = '{self.result}' where username= '{username_lg}'" ,
                                        () )

                                    self.conn1.commit ( )
                                    self.conn1.close ( )
                                    pygame.quit()
                                    import mainGui
                                    self.root2.destroy ( )
                                    self.root1 = Tk ( )
                                    self.obj = mainGui.Game ( self.root1 , username_lg )

                                elif restart_button.draw(screen):
                                    pygame.mixer.music.play()
                                    bg_scroll = 0
                                    world_data = reset_level()
                                    with open(f'level{level}_data.csv', newline='') as csvfile:
                                        reader = csv.reader(csvfile, delimiter=',')
                                        for x, row in enumerate(reader):
                                            for y, tile in enumerate(row):
                                                world_data[x][y] = int(tile)
                                    world = World()
                                    player, health_bar = world.process_data(world_data)

                                    startGame()


                                elif NEXT_button.draw(screen):
                                    pygame.mixer.music.play()
                                    level += 1
                                    bg_scroll = 0
                                    world_data = reset_level()
                                    with open(f'level{level}_data.csv', newline='') as csvfile:
                                        reader = csv.reader(csvfile, delimiter=',')
                                        for x, row in enumerate(reader):
                                            for y, tile in enumerate(row):
                                                world_data[x][y] = int(tile)
                                    world = World()
                                    player, health_bar = world.process_data(world_data)






                    else:
                        screen_scroll = 0
                        pygame.mixer.music.stop()

                        if death_fade.fade():
                            restart_button = button.Button(width // 2 + 70, height // 2 + 40, restart, 2)
                            draw_text('Shooter Game', font1, WHITE, 320, 70)
                            draw_text(f'Level {level}:  Mission Failed. ', font2, WHITE, 385, 240)
                            draw_text ( 'Home' , font3 , WHITE , 355 , 540 )
                            draw_text ( 'Restart' , font3 , WHITE , 710 , 540 )
                            #
                            # draw_text(f'Coins: {player.coin} ', font2, WHITE, 320, 300)
                            # screen.blit(coin_img, (470, 305))
                            draw_text('Try Again !', font3, WHITE, 500, 320)

                            if home_button.draw(screen):
                                self.end = time.time ( )
                                self.result = int ( self.end - self.start )
                                print ( self.result )
                                self.conn1 = mysql.connector.connect ( host = 'localhost' , password = 'Suj@y935974' ,
                                                                       user = 'root' ,
                                                                       database = 'game' )
                                self.Cursor_obj = self.conn1.cursor ( )
                                self.Cursor_obj.execute (
                                    f" update create_account set played_time = '{self.result}' where username= '{username_lg}'" ,
                                    () )

                                self.conn1.commit ( )
                                self.conn1.close ( )
                                pygame.quit()
                                import mainGui
                                self.root2.destroy ( )
                                self.root1 = Tk ( )
                                self.obj = mainGui.Game ( self.root1 , username_lg )
                            elif restart_button.draw(screen):
                                pygame.mixer.music.play()
                                bg_scroll = 0
                                world_data = reset_level()
                                with open(f'level{level}_data.csv', newline='') as csvfile:
                                    reader = csv.reader(csvfile, delimiter=',')
                                    for x, row in enumerate(reader):
                                        for y, tile in enumerate(row):
                                            world_data[x][y] = int(tile)
                                world = World()
                                player, health_bar = world.process_data(world_data)
                                startGame()

                for event in pygame.event.get():
                    # quit game
                    if event.type == pygame.QUIT:
                        run = False


                    # keyboard presses
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                            moving_left = True
                        if event.key == pygame.K_d:
                            moving_right = True
                        if event.key == pygame.K_SPACE:
                            shoot = True
                        if event.key == pygame.K_q:
                            grenade = True
                        if event.key == pygame.K_w and player.alive:
                            player.jump = True
                            jump_fx.play()
                        if event.key == pygame.K_ESCAPE:
                            run = False

                    # keyboard button released
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_a:
                            moving_left = False
                        if event.key == pygame.K_d:
                            moving_right = False
                        if event.key == pygame.K_SPACE:
                            shoot = False
                        if event.key == pygame.K_q:
                            grenade = False
                            grenade_thrown = False

                pygame.display.update()
            pygame.quit()
            self.end = time.time()
            self.result = int(self.end- self.start)
            # print(self.result)
            self.conn1 = mysql.connector.connect ( host = 'localhost' , password = 'Suj@y935974' , user = 'root' ,
                                             database = 'game' )
            self.Cursor_obj = self.conn1.cursor ( )
            self.Cursor_obj.execute(f" update create_account set played_time = '{self.result}' where username= '{username_lg}'",())

            self.conn1.commit ( )
            self.conn1.close ( )

        def home():
            import mainGui
            self.root2.destroy()
            self.root1 = Tk ( )
            self.obj = mainGui.Game( self.root1 , username_lg )

        def how_to_play():
            call ( ['python' , 'how to play shooter game.py'] )

        self.img34 = PhotoImage(file='images/bgimg.png')
        Label(root2, image=self.img34, width=1208, height=700).place(x=-5.5,y=2)

        self.img1 = PhotoImage(file='images/gamehouse1.png')

        self.b = customtkinter.CTkButton(master=self.root2,  width=10, image=  self.img1, text='Home', fg_color = '#FFFADA',
                                                                 bg_color = 'blue',border_spacing=5, text_color = 'blue', font=('Futura',20,
                                                                                            'bold'),command=home)
        self.b.place(x=10, y=10)
        self.b1 = customtkinter.CTkButton(master=self.root2,  width=36, text='Start Game', bg_color='Red',border_spacing=5,font=('Futura',20,'bold'), command=startGame)
        self.b1.place(x=500, y=500)

        self.b2 = customtkinter.CTkButton(master=self.root2,  width=36, text='Help ?', bg_color='blue',border_spacing=5,fg_color = 'white',text_color = 'red',   font=('Futura',20,'bold'),command = how_to_play)
        self.b2.place(x=1100, y=20)

if __name__=='__main__':
    root2 = Tk ( )
    for f in root2.winfo_children ( ):
        f.destroy ( )
    obj = Shooter( root2, username_lg="", shooter1="")
    root2.mainloop()

