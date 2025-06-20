import pygame as pg
import time
from bird import Bird
from pipe import Pipe
import mysql.connector
from mainGui import *

pg.init ( )
class Game:
	def __init__(self, username_lg="", flappy=""):
		# setting window config
		self.start = time.time ( )
		self.ground2_rect = None
		self.ground1_rect = None
		self.ground2_img = None
		self.ground1_img = None
		self.bg_img = None
		self.width = 600
		self.height = 768
		self.scale_factor = 1.5
		self.win = pg.display.set_mode ( (self.width , self.height) )
		self.clock = pg.time.Clock ( )
		self.move_speed = 250
		self.is_game_started = True
		self.start_monitoring = False
		self.score = 0
		self.bird = Bird ( self.scale_factor )
		self.flappy = flappy

		self.is_enter_pressed = False
		self.font = pg.font.Font ( "asset/font.ttf" , 24 )
		self.pipes = []
		self.pipe_generate_counter = 71
		self.score_text = self.font.render ( "Score: 0" , True , (255 , 0 , 0) )
		self.score_text_rect = self.score_text.get_rect ( center = (100 , 30) )
		self.restart_text = self.font.render ( "Restart" , True , (255 , 0 , 0) )
		self.restart_text_rect = self.restart_text.get_rect ( center = (300 , 700) )
		self.setUpBgAndGround ( )
		# print(username_lg)
		self.username = username_lg

		self.gameLoop ( )
	def gameLoop(self):
		last_time = time.time ( )
		while True:
			# calculating delta time
			new_time = time.time ( )
			dt = new_time - last_time
			last_time = new_time

			for event in pg.event.get ( ):
				if event.type == pg.QUIT:
					end = time.time ( )
					result = int ( end - self.start )
					# print ( result )
					conn1 = mysql.connector.connect ( host = 'localhost' , password = 'Suj@y935974' ,
														   user = 'root' ,
														   database = 'game' )
					Cursor_obj = conn1.cursor ( )
					Cursor_obj.execute (
						f" update create_account set played_time = '{result}' where username= '{self.username}'" ,
						() )

					conn1.commit ( )
					conn1.close ( )
					pg.quit()
				if event.type == pg.KEYDOWN and self.is_game_started:
					if event.key == pg.K_RETURN:
						self.is_enter_pressed = True
						self.bird.update_on = True
					if event.key == pg.K_SPACE and self.is_enter_pressed:
						self.bird.flap ( dt )
				if event.type == pg.MOUSEBUTTONDOWN:
					if self.restart_text_rect.collidepoint ( pg.mouse.get_pos ( ) ):
						self.restartGame ( )

			self.updateEverything ( dt )

			self.checkCollisions ( )
			self.checkScore ( )
			self.drawEverything ( )
			pg.display.update ( )
			self.clock.tick ( 60 )

	def restartGame(self):
		self.score = 0
		self.score_text = self.font.render ( "Score: 0" , True , (255 , 0 , 0) )
		self.is_enter_pressed = False
		self.is_game_started = True
		self.bird.resetposition ( )
		self.pipes.clear ( )
		self.pipe_generate_counter = 71
		self.bird.update_on = False

	def checkCollisions(self):
		if len ( self.pipes ):
			if self.bird.rect.bottom > 568:
				self.bird.update_on = False
				self.is_enter_pressed = False
				self.is_game_started = False
			if (self.bird.rect.colliderect ( self.pipes[0].rect_down ) or
					self.bird.rect.colliderect ( self.pipes[0].rect_up )):
				self.is_enter_pressed = False
				self.is_game_started = False

	def checkScore(self):
		if len ( self.pipes ) > 0:
			if (self.bird.rect.left > self.pipes[0].rect_down.left and self.bird.rect.right < self.pipes[
				0].rect_down.right and not self.start_monitoring):
				self.start_monitoring = True
			if self.bird.rect.left > self.pipes[0].rect_down.right and self.start_monitoring:
				self.start_monitoring = False
				self.score += 1
				self.score_text = self.font.render ( f"Score: {self.score}" , True , (255 , 255 , 255) )
				try:
					conn = mysql.connector.connect ( host = 'localhost' , password = 'Suj@y935974' ,
													 user = 'root' , database = 'game' )
					Cursor_obj = conn.cursor ( )
					query = " update create_account set score_flappy = %s,Recently_played=%s where username= %s"
					val = (f'score : {self.score}',self.flappy,self.username)
					Cursor_obj.execute ( query , val )
					conn.commit ( )
					conn.close ( )

				except:
					pass
					# messagebox.showinfo ( "Invalid" , "Something Went Wrong !" )

	def updateEverything(self , dt):
		if self.is_enter_pressed:
			# moving the ground
			self.ground1_rect.x -= int ( self.move_speed * dt )
			self.ground2_rect.x -= int ( self.move_speed * dt )

			if self.ground1_rect.right < 0:
				self.ground1_rect.x = self.ground2_rect.right
			if self.ground2_rect.right < 0:
				self.ground2_rect.x = self.ground1_rect.right

			# generating pipes
			if self.pipe_generate_counter > 70:
				self.pipes.append ( Pipe ( self.scale_factor , self.move_speed ) )
				self.pipe_generate_counter = 0

			self.pipe_generate_counter += 1

			# moving the pipes
			for pipe in self.pipes:
				pipe.update ( dt )

			# removing pipes if out of screen
			if len ( self.pipes ) != 0:
				if self.pipes[0].rect_up.right < 0:
					self.pipes.pop ( 0 )

		# moving the bird
		self.bird.update ( dt )

	def drawEverything(self):
		self.win.blit ( self.bg_img , (0 , -300) )
		for pipe in self.pipes:
			pipe.drawPipe ( self.win )
		self.win.blit ( self.ground1_img , self.ground1_rect )
		self.win.blit ( self.ground2_img , self.ground2_rect )
		self.win.blit ( self.bird.image , self.bird.rect )
		self.win.blit ( self.score_text , self.score_text_rect )
		if not self.is_game_started:
			self.win.blit ( self.restart_text , self.restart_text_rect )

	def setUpBgAndGround(self):
		# loading images for bg and ground
		self.bg_img = pg.transform.scale_by ( pg.image.load ( "asset/bg.png" ).convert ( ) , self.scale_factor )
		self.ground1_img = pg.transform.scale_by ( pg.image.load ( "asset/ground.png" ).convert ( ) ,
												   self.scale_factor )
		self.ground2_img = pg.transform.scale_by ( pg.image.load ( "asset/ground.png" ).convert ( ) ,
												   self.scale_factor )

		self.ground1_rect = self.ground1_img.get_rect ( )
		self.ground2_rect = self.ground2_img.get_rect ( )

		self.ground1_rect.x = 0
		self.ground2_rect.x = self.ground1_rect.right
		self.ground1_rect.y = 568
		self.ground2_rect.y = 568



if __name__=='__main__':
	obj = Game(username_lg = "", flappy="" )

