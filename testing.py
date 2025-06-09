
import sys
# import soundfile as sf
from pygame import *
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


class Mario:

    # constructor
    def __init__(self , root2, username_lg="", mario_played=""):

        # -----------------------------------------------------------------------------------------------
        # -----------------------------------------------------------------------------------------------

        self.root2 = root2
        self.root2.geometry ( '1200x700+160+50' )
        self.root2.resizable ( False , False )
        print ( username_lg )


# from pysndfx import AudioEffectsChain
        def start_game1():
            self.start = time.time()
            pygame.init ( )
            mixer.init ( )
            WINDOW_WIDTH = 1200
            WINDOW_HEIGHT = 700
            FPS = 20
            BLACK = (0, 0, 0)
            GREEN = (0, 255, 0)
            ADD_NEW_FLAME_RATE = 25
            cactus_img = pygame.image.load('img/cactus_bricks.png')
            cactus_img_rect = cactus_img.get_rect()
            cactus_img_rect.left = 0
            fire_img = pygame.image.load('img/fire_bricks.png')
            fire_img_rect = fire_img.get_rect()
            fire_img_rect.left = 0
            CLOCK = pygame.time.Clock()
            font = pygame.font.SysFont('forte', 20)
            start_game = False

            canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
            pygame.display.set_caption('Mario')


            class Topscore:
                def __init__(self):
                    self.high_score = 0
                def top_score(self, score):
                    if score > self.high_score:
                        self.high_score = score

                        try:
                            conn = mysql.connector.connect ( host = 'localhost' , password = 'Suj@y935974' ,
                                                             user = 'root' , database = 'game' )
                            Cursor_obj = conn.cursor ( )
                            query = " update create_account set score_mario = %s, Recently_played = %s where username= %s"
                            val = (f'Level {LEVEL} score :{self.high_score}', mario_played , username_lg)
                            Cursor_obj.execute ( query , val )
                            conn.commit ( )
                            conn.close ( )

                        except:
                            messagebox.showinfo ( "Invalid" , "Something Went Wrong !" )
                    return self.high_score

            topscore = Topscore()


            class Dragon:
                dragon_velocity = 10

                def __init__(self):
                    self.dragon_img = pygame.image.load('img/dragon.png')
                    self.dragon_img_rect = self.dragon_img.get_rect()
                    self.dragon_img_rect.width -= 10
                    self.dragon_img_rect.height -= 10
                    self.dragon_img_rect.top = WINDOW_HEIGHT/2
                    self.dragon_img_rect.right = WINDOW_WIDTH
                    self.up = False
                    self.down = True

                def update(self):
                    canvas.blit(self.dragon_img, self.dragon_img_rect)
                    if self.dragon_img_rect.top <= cactus_img_rect.bottom:
                        self.up = False
                        self.down = True
                    elif self.dragon_img_rect.bottom >= fire_img_rect.top:
                        self.up = True
                        self.down = False

                    if self.up:
                        self.dragon_img_rect.top -= self.dragon_velocity
                    elif self.down:
                        self.dragon_img_rect.top += self.dragon_velocity


            class Flames:
                flames_velocity = 20

                def __init__(self):
                    self.flames = pygame.image.load('img/fireball.png')
                    self.flames_img = pygame.transform.scale(self.flames, (20, 20))
                    self.flames_img_rect = self.flames_img.get_rect()
                    self.flames_img_rect.right = dragon.dragon_img_rect.left
                    self.flames_img_rect.top = dragon.dragon_img_rect.top + 30


                def update(self):
                    canvas.blit(self.flames_img, self.flames_img_rect)

                    if self.flames_img_rect.left > 0:
                        self.flames_img_rect.left -= self.flames_velocity


            class Mario:
                Mario_velocity = 10

                def __init__(self):
                    self.mario_img = pygame.image.load('img/running.png')
                    self.mario_img_rect = self.mario_img.get_rect()
                    self.mario_img_rect.left = 20
                    self.mario_img_rect.top = WINDOW_HEIGHT/2 - 100
                    self.down = True
                    self.up = False

                def update(self):
                    canvas.blit(self.mario_img, self.mario_img_rect)
                    if self.mario_img_rect.top <= cactus_img_rect.bottom:
                        game_over()
                        if SCORE > self.mario_score:
                            self.mario_score = SCORE
                    if self.mario_img_rect.bottom >= fire_img_rect.top:
                        game_over()
                        if SCORE > self.mario_score:
                            self.mario_score = SCORE
                    if self.up:
                        self.mario_img_rect.top -= 10
                    if self.down:
                        self.mario_img_rect.bottom += 10


            def game_over():
                pygame.mixer.music.stop()
                music = pygame.mixer.Sound('song/Mario Death - QuickSounds.com.mp3')

                # sound_path = 'Mario Death - QuickSounds.com.mp3'
                # s, rate = sf.read(sound_path)
                # fx = (AudioEffectsChain().speed(0.8))
                # fx(s, sample_in=rate)
                # dst = 'test_1.2.wav'
                # sf.write(dst, s, rate, 'PCM_16')
                music.play()
                topscore.top_score(SCORE)
                canvas.fill ( BLACK )
                game_over_img = pygame.image.load('img/end.png')
                game_over_img_rect = game_over_img.get_rect()
                game_over_img_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
                canvas.blit(game_over_img, game_over_img_rect)
                #
                # def home1():
                #     import mainGui
                #     self.root2.destroy ( )
                #     self.root1 = Tk ( )
                #     self.obj = mainGui.Game ( self.root1 , username_lg )
                #
                # self.b =Button (canvas, width = 10 , image = self.img1 ,
                #                                    text = 'Home' ,font = ('Futura' , 20 ,'bold') , command = home1 )
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            self.end = time.time ( )
                            self.result = int ( self.end - self.start )
                            print ( self.result)
                            self.conn1 = mysql.connector.connect ( host = 'localhost' , password = 'Suj@y935974' ,
                                                                   user = 'root' ,
                                                                   database = 'game' )
                            self.Cursor_obj = self.conn1.cursor ( )
                            self.Cursor_obj.execute (
                                f" update create_account set played_time = '{self.result}' where username= '{username_lg}'" ,
                                () )

                            self.conn1.commit ( )
                            self.conn1.close ( )
                            # sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                pygame.quit()
                                # sys.exit()
                                # music.stop()
                            game_loop()
                    pygame.display.update()


            def start_game():
                canvas.fill ( BLACK )
                start_img = pygame.image.load ( 'img/start.png' )
                start_img_rect = start_img.get_rect ( )
                start_img_rect.center = (WINDOW_WIDTH / 2 , WINDOW_HEIGHT / 2)
                canvas.blit ( start_img , start_img_rect )
                while True:
                    for event in pygame.event.get ( ):
                        if event.type == pygame.QUIT:
                            pygame.quit ( )
                            # sys.exit ( )
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                pygame.quit ( )
                                # sys.exit ( )
                            game_loop ( )
                    pygame.display.update ( )




            def check_level(SCORE):
                global LEVEL
                if SCORE in range(0, 10):
                    cactus_img_rect.bottom = 50
                    fire_img_rect.top = WINDOW_HEIGHT - 50
                    LEVEL = 1
                elif SCORE in range(10, 20):
                    cactus_img_rect.bottom = 100
                    fire_img_rect.top = WINDOW_HEIGHT - 100
                    LEVEL = 2
                elif SCORE in range(20, 30):
                    cactus_img_rect.bottom = 150
                    fire_img_rect.top = WINDOW_HEIGHT - 150
                    LEVEL = 3
                elif SCORE in range(30,40) :
                    cactus_img_rect.bottom = 200
                    fire_img_rect.top = WINDOW_HEIGHT - 200
                    LEVEL = 4
                elif SCORE in range(40,50) :
                    cactus_img_rect.bottom = 200
                    fire_img_rect.top = WINDOW_HEIGHT - 250
                    LEVEL = 5
                elif SCORE in range(50,70) :
                    cactus_img_rect.bottom = 200
                    fire_img_rect.top = WINDOW_HEIGHT - 300
                    LEVEL = 6






            def game_loop():
                while True:
                    global dragon
                    dragon = Dragon()
                    flames = Flames()
                    mario = Mario()
                    add_new_flame_counter = 0
                    global SCORE
                    SCORE = 0
                    global  HIGH_SCORE
                    flames_list = []
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load('song/SuperMarioBros.mp3')
                    pygame.mixer.music.play(-1, 0.0)
                    while True:
                        canvas.fill(BLACK)
                        check_level(SCORE)
                        dragon.update()
                        add_new_flame_counter += 1

                        if add_new_flame_counter == ADD_NEW_FLAME_RATE:
                            add_new_flame_counter = 0
                            new_flame = Flames()
                            flames_list.append(new_flame)
                        for f in flames_list:
                            if f.flames_img_rect.left <= 0:
                                flames_list.remove(f)
                                SCORE += 1
                            f.update()

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_UP:
                                    mario.up = True
                                    mario.down = False
                                elif event.key == pygame.K_DOWN:
                                    mario.down = True
                                    mario.up = False
                            if event.type == pygame.KEYUP:
                                if event.key == pygame.K_UP:
                                    mario.up = False
                                    mario.down = True
                                elif event.key == pygame.K_DOWN:
                                    mario.down = True
                                    mario.up = False

                        score_font = font.render('Score:'+str(SCORE), True, GREEN)
                        score_font_rect = score_font.get_rect()
                        score_font_rect.center = (200, cactus_img_rect.bottom + score_font_rect.height/2)
                        canvas.blit(score_font, score_font_rect)

                        level_font = font.render('Level:'+str(LEVEL), True, GREEN)
                        level_font_rect = level_font.get_rect()
                        level_font_rect.center = (500, cactus_img_rect.bottom + score_font_rect.height/2)
                        canvas.blit(level_font, level_font_rect)

                        top_score_font = font.render('Top Score:'+str(topscore.high_score),True,GREEN)
                        top_score_font_rect = top_score_font.get_rect()
                        top_score_font_rect.center = (800, cactus_img_rect.bottom + score_font_rect.height/2)
                        canvas.blit(top_score_font, top_score_font_rect)

                        canvas.blit(cactus_img, cactus_img_rect)
                        canvas.blit(fire_img, fire_img_rect)
                        mario.update()
                        for f in flames_list:
                            if f.flames_img_rect.colliderect(mario.mario_img_rect):
                                game_over()
                                if SCORE > mario.mario_score:
                                    mario.mario_score = SCORE
                        pygame.display.update()
                        CLOCK.tick(FPS)

                        # pygame.mixer.music.stop()
            start_game()


        def home1():
            import mainGui
            self.root2.destroy ( )
            self.root1 = Tk ( )
            self.obj = mainGui.Game ( self.root1 , username_lg )

        def how_to_play():
            call ( ['python' , 'how to play mario vs dragon game.py'] )

        self.img34 = PhotoImage ( file = 'images/mario1.png' )
        Label ( root2 , image = self.img34 , width = 1208 , height = 700 ).place ( x = -5.5 , y = 2 )

        self.img1 = PhotoImage ( file = 'images/gamehouse1.png' )

        self.b = customtkinter.CTkButton ( master = self.root2 , width = 10 , image = self.img1 ,
                                           text = 'Home' ,
                                           fg_color = '#FFFADA' ,
                                           bg_color = 'blue' , border_spacing = 5 , text_color = 'blue' ,
                                           font = ('Futura' , 20 ,
                                                   'bold') , command = home1 )
        self.b.place ( x = 10 , y = 10 )
        self.b1 = customtkinter.CTkButton ( master = self.root2 , width = 36 , text = 'Start Game' ,
                                            bg_color = 'Red' ,
                                            border_spacing = 5 ,
                                            font = ('Futura' , 20 , 'bold') , command = start_game1 )
        self.b1.place ( x = 500 , y = 500 )

        self.b2 = customtkinter.CTkButton ( master = self.root2 , width = 36 , text = 'Help ?' ,
                                            bg_color = 'blue' ,
                                            border_spacing = 5 , fg_color = 'white' ,
                                            text_color = 'red' , font = ('Futura' , 20 , 'bold') , command = how_to_play)
        self.b2.place ( x = 1100 , y = 20 )


if __name__=='__main__':
    root2 = Tk ( )
    for f in root2.winfo_children ( ):
        f.destroy ( )
    obj = Mario( root2, username_lg="", mario_played="")
    root2.mainloop()




