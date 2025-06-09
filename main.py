import math
import random
from tkinter import *
import pygame
from mainGui import *
from pygame import mixer
import time
import customtkinter
class Space:

    # constructor
    def __init__(self , root2, username_lg="",space=""):
        pygame.init ( )
        self.start = time.time ( )
        self.root2 = root2
        self.root2.geometry('1200x700+160+50')
        self.root2.resizable(False,False)
        # print(username_lg)

        def startGame():


            pygame.init ( )
            # Create the screen
            self.screen = pygame.display.set_mode ( (800 , 600) )

            # Background
            self.background = pygame.image.load ( 'spaceInvader/background.png' )

            # Sound
            mixer.music.load ( "spaceInvader/background.wav" )
            mixer.music.play ( -1 )

            # Caption and Icon
            pygame.display.set_caption ( "Space Invader" )
            self.icon = pygame.image.load ( 'spaceInvader/ufo.png' )
            pygame.display.set_icon ( self.icon )

            # Player
            self.playerImg = pygame.image.load ( 'spaceInvader/player.png' )
            self.playerX = 370
            self.playerY = 480
            self.playerX_change = 0

            # Enemy
            self.enemyImg = []
            self.enemyX = []
            self.enemyY = []
            self.enemyX_change = []
            self.enemyY_change = []
            self.num_of_enemies = 6

            for i in range ( self.num_of_enemies ):
                self.enemyImg.append ( pygame.image.load ( 'spaceInvader/enemy.png' ) )
                self.enemyX.append ( random.randint ( 0 , 736 ) )
                self.enemyY.append ( random.randint ( 50 , 150 ) )
                self.enemyX_change.append ( 4 )
                self.enemyY_change.append ( 40 )

            self.bulletImg = pygame.image.load ( 'spaceInvader/bullet.png' )
            self.bulletX = 0
            self.bulletY = 480
            self.bulletX_change = 0
            self.bulletY_change = 10
            self.bullet_state = "ready"

            # Score

            self.score_value = 0
            self.font = pygame.font.Font ( 'freesansbold.ttf' , 32 )

            self.textX = 10
            self.testY = 10

            # Game Over
            self.over_font = pygame.font.Font ( 'freesansbold.ttf' , 64 )

            def show_score(x , y):
                self.score = self.font.render ( "Score : " + str ( self.score_value ) , True , (255 , 255 , 255) )
                self.screen.blit ( self.score , (x , y) )

            def game_over_text():
                try:
                    conn = mysql.connector.connect ( host = 'localhost' , password = 'Suj@y935974' ,
                                                     user = 'root' , database = 'game' )
                    Cursor_obj = conn.cursor ( )
                    query = " update create_account set score_space = %s, Recently_played =%s where username= %s"
                    val = (f'score : {self.score_value}',space, username_lg)
                    Cursor_obj.execute ( query , val )
                    # messagebox.showinfo ( "Success" , "Thank You ! For Rating Us" )
                    conn.commit ( )
                    conn.close ( )

                except:
                    pass
                # messagebox.showinfo ( "Invalid" , "Something Went Wrong !" )
                self.over_text = self.over_font.render ( "GAME OVER" , True , (255 , 255 , 255) )
                self.screen.blit ( self.over_text , (200 , 250) )

            def player(x , y):
                self.screen.blit ( self.playerImg , (x , y) )

            def enemy(x , y , i):
                self.screen.blit ( self.enemyImg[i] , (x , y) )

            def fire_bullet(x , y):
                global bullet_state
                self.bullet_state = "fire"
                self.screen.blit ( self.bulletImg , (x + 16 , y + 10) )

            def isCollision(enemyX , enemyY , bulletX , bulletY):
                self.distance = math.sqrt ( math.pow ( enemyX - bulletX , 2 ) + (math.pow ( enemyY - bulletY , 2 )) )
                if self.distance < 27:
                    return True
                else:
                    return False

            def reset_game():
                global playerX , playerY , score_value , bullet_state , bulletY
                self.playerX = 370
                self.playerY = 480
                self.score_value = 0
                self.bullet_state = "ready"
                bulletY = 480
                for i in range ( self.num_of_enemies ):
                    self.enemyX[i] = random.randint ( 0 , 736 )
                    self.enemyY[i] = random.randint ( 50 , 150 )

            # Game Loop

            while True:

                # RGB = Red, Green, Blue
                self.screen.fill ( (0 , 0 , 0) )
                # Background Image
                self.screen.blit ( self.background , (0 , 0) )
                for event in pygame.event.get ( ):
                    if event.type == pygame.QUIT:
                        pygame.quit()

                    # if keystroke is pressed check whether its right or left
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.playerX_change = -5
                        if event.key == pygame.K_RIGHT:
                            self.playerX_change = 5
                        if event.key == pygame.K_SPACE:
                            if self.bullet_state == "ready":
                                self.bulletSound = mixer.Sound ( "spaceInvader/laser.wav" )
                                self.bulletSound.play ( )
                                # Get the current x cordinate of the spaceship
                                self.bulletX = self.playerX
                                fire_bullet ( self.bulletX , self.bulletY )
                        if event.key == pygame.K_r:
                            reset_game ( )

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                            self.playerX_change = 0

                # Player Movement
                self.playerX += self.playerX_change
                if self.playerX <= 0:
                    self.playerX = 0
                elif self.playerX >= 736:
                    self.playerX = 736

                # Enemy Movement
                for i in range ( self.num_of_enemies ):

                    # Game Over
                    if self.enemyY[i] > 440:
                        for j in range ( self.num_of_enemies ):
                            self.enemyY[j] = 2000
                        game_over_text ( )
                        break

                    self.enemyX[i] += self.enemyX_change[i]
                    if self.enemyX[i] <= 0:
                        self.enemyX_change[i] = 4
                        self.enemyY[i] += self.enemyY_change[i]
                    elif self.enemyX[i] >= 736:
                        self.enemyX_change[i] = -4
                        self.enemyY[i] += self.enemyY_change[i]

                    # Collision
                    self.collision = isCollision ( self.enemyX[i] , self.enemyY[i] , self.bulletX , self.bulletY )
                    if self.collision:
                        self.explosionSound = mixer.Sound ( "spaceInvader/explosion.wav" )
                        self.explosionSound.play ( )
                        self.bulletY = 480
                        self.bullet_state = "ready"
                        self.score_value += 1
                        self.enemyX[i] = random.randint ( 0 , 736 )
                        self.enemyY[i] = random.randint ( 50 , 150 )

                    enemy ( self.enemyX[i] , self.enemyY[i] , i )

                # Bullet Movement
                if self.bulletY <= 0:
                    self.bulletY = 480
                    self.bullet_state = "ready"

                if self.bullet_state == "fire":
                    fire_bullet ( self.bulletX , self.bulletY )
                    self.bulletY -= self.bulletY_change

                player ( self.playerX , self.playerY )
                show_score ( self.textX , self.testY )
                pygame.display.update ( )


        def home():
            self.end = time.time ( )
            self.result = int ( self.end - self.start )
            # print ( self.result )
            self.conn1 = mysql.connector.connect ( host = 'localhost' , password = 'Suj@y935974' , user = 'root' ,
                                                   database = 'game' )
            self.Cursor_obj = self.conn1.cursor ( )
            self.Cursor_obj.execute (
                f" update create_account set played_time = '{self.result}' where username= '{username_lg}'" , () )

            self.conn1.commit ( )
            self.conn1.close ( )
            import mainGui
            self.root2.destroy()
            self.root1 = Tk ( )
            self.obj = mainGui.Game( self.root1 , username_lg )

        def how_to_play():
            call ( ['python' , 'how to play space invader.py'] )

        self.img34 = PhotoImage(file='images/space invader2.png')
        Label(root2, image=self.img34, width=1208, height=700).place(x=-5.5,y=2)

        self.img1 = PhotoImage(file='images/gamehouse1.png')

        self.b = customtkinter.CTkButton(master=self.root2,  width=10, image=  self.img1, text='Home', fg_color = '#FFFADA',
                                                                 bg_color = 'blue',border_spacing=5, text_color = 'blue', font=('Futura',20,
                                                                                            'bold'),command=home)
        self.b.place(x=10, y=10)
        self.b1 = customtkinter.CTkButton(master=self.root2,  width=36, text='Start Game', bg_color='Red',border_spacing=5,font=('Futura',20,'bold'), command=startGame)
        self.b1.place(x=500, y=500)

        self.b2 = customtkinter.CTkButton(master=self.root2,  width=36, text='Help ?', bg_color='blue',border_spacing=5,fg_color = 'white',text_color = 'red',   font=('Futura',20,'bold'), command = how_to_play)
        self.b2.place(x=1100, y=20)


if __name__=='__main__':
    root2 = Tk ( )
    for f in root2.winfo_children ( ):
        f.destroy ( )
    obj = Space( root2, username_lg="",space="")
    root2.mainloop()