import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import time
from random import randint
import customtkinter as ctk
import mysql.connector
import logging

# Set up basic logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Ludo:
    def __init__(self, root, username=""):
        self.window = root
        self.window.geometry("1535x780+-7+0")
        self.window.title("Play Ludo with Sam")
        self.window.iconbitmap("Images/ludo_icon.ico")
        self.window.resizable(False, False)
        self.window.configure(bg="#1e1e2e")

        # Initialize images for dice blocks
        self.block_six_side = ImageTk.PhotoImage(
            Image.open("Images/6_block.png").resize((33, 33), Image.LANCZOS))
        self.block_five_side = ImageTk.PhotoImage(
            Image.open("Images/5_block.png").resize((33, 33), Image.LANCZOS))
        self.block_four_side = ImageTk.PhotoImage(
            Image.open("Images/4_block.png").resize((33, 33), Image.LANCZOS))
        self.block_three_side = ImageTk.PhotoImage(
            Image.open("Images/3_block.png").resize((33, 33), Image.LANCZOS))
        self.block_two_side = ImageTk.PhotoImage(
            Image.open("Images/2_block.png").resize((33, 33), Image.LANCZOS))
        self.block_one_side = ImageTk.PhotoImage(
            Image.open("Images/1_block.png").resize((33, 33), Image.LANCZOS))

        # Initialize timing variables
        self.start_time = time.time()
        self.end_time = 0
        self.username = username if username else "guest"
        self.game_name = 5
        self.time_saved = False
        logging.debug("Ludo game initialized with username: %s", self.username)

        # Bind window close event
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Title label
        title_label = ctk.CTkLabel(
            self.window,
            text="Ludo Game",
            font=("Roboto", 36, "bold"),
            text_color="#ffffff"
        )
        title_label.place(relx=0.5, rely=0.1 / 2, anchor="center")

        # Canvas setup
        self.make_canvas = tk.Canvas(self.window, bg="#1e1e2e", width=800, height=630)
        self.make_canvas.pack(fill=tk.BOTH)

        # Containers for game data
        self.made_red_coin = []
        self.made_green_coin = []
        self.made_yellow_coin = []
        self.made_sky_blue_coin = []
        self.red_number_label = []
        self.green_number_label = []
        self.yellow_number_label = []
        self.sky_blue_number_label = []
        self.block_value_predict = []  # Initialize empty list
        self.total_people_play = []
        self.block_number_side = [
            self.block_one_side,
            self.block_two_side,
            self.block_three_side,
            self.block_four_side,
            self.block_five_side,
            self.block_six_side
        ]
        self.red_coord_store = [-1, -1, -1, -1]
        self.green_coord_store = [-1, -1, -1, -1]
        self.yellow_coord_store = [-1, -1, -1, -1]
        self.sky_blue_coord_store = [-1, -1, -1, -1]
        self.red_coin_position = [-1, -1, -1, -1]
        self.green_coin_position = [-1, -1, -1, -1]
        self.yellow_coin_position = [-1, -1, -1, -1]
        self.sky_blue_coin_position = [-1, -1, -1, -1]
        self.move_red_counter = 0
        self.move_green_counter = 0
        self.move_yellow_counter = 0
        self.move_sky_blue_counter = 0
        self.take_permission = 0
        self.six_with_overlap = 0
        self.six_counter = 0
        self.time_for = -1
        self.right_star = None
        self.down_star = None
        self.left_star = None
        self.up_star = None

        # Initialize game board and UI
        self.board_set_up()
        self.instruction_btn_red()
        self.instruction_btn_sky_blue()
        self.instruction_btn_yellow()
        self.instruction_btn_green()
        self.take_initial_control()

    def on_closing(self):
        """Handle window close event to save game time."""
        if not self.time_saved:
            self.save_game_time()
        self.window.destroy()

    def save_game_time(self):
        """Save the time spent playing to the database."""
        if self.time_saved:
            return
        try:
            self.end_time = time.time()
            time_taken = int(self.end_time - self.start_time)
            conn = mysql.connector.connect(
                host='localhost',
                password='Suj@y935974',
                user='root',
                database='game'
            )
            cursor = conn.cursor()
            query = "UPDATE create_account SET played_time = %s, Recently_played = %s WHERE username = %s"
            values = (time_taken, self.game_name, self.username)
            cursor.execute(query, values)
            conn.commit()
            cursor.close()
            conn.close()
            self.time_saved = True
            logging.debug(f"Played time {time_taken} seconds saved for user {self.username}")
        except mysql.connector.Error as e:
            logging.error(f"Database error: {e}")
            messagebox.showerror("Database Error", "Failed to save game time to database.")
        except Exception as e:
            logging.error(f"Error in save_game_time: {e}")
            messagebox.showerror("Error", "An unexpected error occurred while saving game time.")

    def board_set_up(self):
        # Cover Box made
        self.make_canvas.create_rectangle ( 100 , 15 , 100 + (40 * 15) , 15 + (40 * 15) , width = 6 , fill = "white" )
        self.make_canvas.place ( x = "380" , y = "100" )

        # Square box
        self.make_canvas.create_rectangle ( 100 , 15 , 100 + 240 , 15 + 240 , width = 3 ,
                                            fill = "red" )  # left up large square
        self.make_canvas.create_rectangle ( 100 , (15 + 240) + (40 * 3) , 100 + 240 , (15 + 240) + (40 * 3) + (40 * 6) ,
                                            width = 3 , fill = "#04d9ff" )  # left down large square
        self.make_canvas.create_rectangle ( 340 + (40 * 3) , 15 , 340 + (40 * 3) + (40 * 6) , 15 + 240 , width = 3 ,
                                            fill = "#00FF00" )  # right up large square
        self.make_canvas.create_rectangle ( 340 + (40 * 3) , (15 + 240) + (40 * 3) , 340 + (40 * 3) + (40 * 6) ,
                                            (15 + 240) + (40 * 3) + (40 * 6) , width = 3 ,
                                            fill = "yellow" )  # right down large square

        # Left 3 box(In white region)
        self.make_canvas.create_rectangle ( 100 , (15 + 240) , 100 + 240 , (15 + 240) + 40 , width = 3 )
        self.make_canvas.create_rectangle ( 100 + 40 , (15 + 240) + 40 , 100 + 240 , (15 + 240) + 40 + 40 , width = 3 ,
                                            fill = "#F00000" )
        self.make_canvas.create_rectangle ( 100 , (15 + 240) + 80 , 100 + 240 , (15 + 240) + 80 + 40 , width = 3 )

        # right 3 box(In white region)
        self.make_canvas.create_rectangle ( 100 + 240 , 15 , 100 + 240 + 40 , 15 + (40 * 6) , width = 3 )
        self.make_canvas.create_rectangle ( 100 + 240 + 40 , 15 + 40 , 100 + 240 + 80 , 15 + (40 * 6) , width = 3 ,
                                            fill = "#00FF00" )
        self.make_canvas.create_rectangle ( 100 + 240 + 80 , 15 , 100 + 240 + 80 + 40 , 15 + (40 * 6) , width = 3 )

        # up 3 box(In white region)
        self.make_canvas.create_rectangle ( 340 + (40 * 3) , 15 + 240 , 340 + (40 * 3) + (40 * 6) , 15 + 240 + 40 ,
                                            width = 3 )
        self.make_canvas.create_rectangle ( 340 + (40 * 3) , 15 + 240 + 40 , 340 + (40 * 3) + (40 * 6) - 40 ,
                                            15 + 240 + 80 , width = 3 , fill = "yellow" )
        self.make_canvas.create_rectangle ( 340 + (40 * 3) , 15 + 240 + 80 , 340 + (40 * 3) + (40 * 6) ,
                                            15 + 240 + 120 , width = 3 )

        # down 3 box(In white region)
        self.make_canvas.create_rectangle ( 100 , (15 + 240) + (40 * 3) , 100 + 240 + 40 ,
                                            (15 + 240) + (40 * 3) + (40 * 6) , width = 3 )
        self.make_canvas.create_rectangle ( 100 + 240 + 40 , (15 + 240) + (40 * 3) , 100 + 240 + 40 + 40 ,
                                            (15 + 240) + (40 * 3) + (40 * 6) - 40 , width = 3 , fill = "#04d9ff" )
        self.make_canvas.create_rectangle ( 100 + 240 + 40 + 40 , (15 + 240) + (40 * 3) , 100 + 240 + 40 + 40 + 40 ,
                                            (15 + 240) + (40 * 3) + (40 * 6) , width = 3 )

        # All left separation line
        start_x = 100 + 40
        start_y = 15 + 240
        end_x = 100 + 40
        end_y = 15 + 240 + (40 * 3)
        for _ in range ( 5 ):
            self.make_canvas.create_line ( start_x , start_y , end_x , end_y , width = 3 )
            start_x += 40
            end_x += 40

        # All right separation line
        start_x = 100 + 240 + (40 * 3) + 40
        start_y = 15 + 240
        end_x = 100 + 240 + (40 * 3) + 40
        end_y = 15 + 240 + (40 * 3)
        for _ in range ( 5 ):
            self.make_canvas.create_line ( start_x , start_y , end_x , end_y , width = 3 )
            start_x += 40
            end_x += 40

        # All up separation done
        start_x = 100 + 240
        start_y = 15 + 40
        end_x = 100 + 240 + (40 * 3)
        end_y = 15 + 40
        for _ in range ( 5 ):
            self.make_canvas.create_line ( start_x , start_y , end_x , end_y , width = 3 )
            start_y += 40
            end_y += 40

        # All down separation done
        start_x = 100 + 240
        start_y = 15 + (40 * 6) + (40 * 3) + 40
        end_x = 100 + 240 + (40 * 3)
        end_y = 15 + (40 * 6) + (40 * 3) + 40
        for _ in range ( 5 ):
            self.make_canvas.create_line ( start_x , start_y , end_x , end_y , width = 3 )
            start_y += 40
            end_y += 40

        # Square box(Coins containers) white region make
        self.make_canvas.create_rectangle ( 100 + 20 , 15 + 40 - 20 , 100 + 40 + 60 + 40 + 60 + 20 ,
                                            15 + 40 + 40 + 40 + 100 - 20 , width = 3 , fill = "white" )
        self.make_canvas.create_rectangle ( 340 + (40 * 3) + 40 - 20 , 15 + 40 - 20 ,
                                            340 + (40 * 3) + 40 + 60 + 40 + 40 + 20 + 20 ,
                                            15 + 40 + 40 + 40 + 100 - 20 , width = 3 , fill = "white" )
        self.make_canvas.create_rectangle ( 100 + 20 , 340 + 80 - 20 + 15 , 100 + 40 + 60 + 40 + 60 + 20 ,
                                            340 + 80 + 60 + 40 + 40 + 20 + 15 , width = 3 , fill = "white" )
        self.make_canvas.create_rectangle ( 340 + (40 * 3) + 40 - 20 , 340 + 80 - 20 + 15 ,
                                            340 + (40 * 3) + 40 + 60 + 40 + 40 + 20 + 20 ,
                                            340 + 80 + 60 + 40 + 40 + 20 + 15 , width = 3 , fill = "white" )

        # Left up square inside box made
        self.make_canvas.create_rectangle ( 100 + 40 , 15 + 40 , 100 + 40 + 40 , 15 + 40 + 40 , width = 3 ,
                                            fill = "red" )
        self.make_canvas.create_rectangle ( 100 + 40 + 60 + 60 , 15 + 40 , 100 + 40 + 60 + 40 + 60 , 15 + 40 + 40 ,
                                            width = 3 , fill = "red" )
        self.make_canvas.create_rectangle ( 100 + 40 , 15 + 40 + 100 , 100 + 40 + 40 , 15 + 40 + 40 + 100 , width = 3 ,
                                            fill = "red" )
        self.make_canvas.create_rectangle ( 100 + 40 + 60 + 60 , 15 + 40 + 100 , 100 + 40 + 60 + 40 + 60 ,
                                            15 + 40 + 40 + 100 , width = 3 , fill = "red" )

        # Right up square inside box made
        self.make_canvas.create_rectangle ( 340 + (40 * 3) + 40 , 15 + 40 , 340 + (40 * 3) + 40 + 40 , 15 + 40 + 40 ,
                                            width = 3 , fill = "#00FF00" )
        self.make_canvas.create_rectangle ( 340 + (40 * 3) + 40 + 60 + 40 + 20 , 15 + 40 ,
                                            340 + (40 * 3) + 40 + 60 + 40 + 40 + 20 , 15 + 40 + 40 , width = 3 ,
                                            fill = "#00FF00" )
        self.make_canvas.create_rectangle ( 340 + (40 * 3) + 40 , 15 + 40 + 100 , 340 + (40 * 3) + 40 + 40 ,
                                            15 + 40 + 40 + 100 , width = 3 , fill = "#00FF00" )
        self.make_canvas.create_rectangle ( 340 + (40 * 3) + 40 + 60 + 40 + 20 , 15 + 40 + 100 ,
                                            340 + (40 * 3) + 40 + 60 + 40 + 40 + 20 , 15 + 40 + 40 + 100 , width = 3 ,
                                            fill = "#00FF00" )

        # Left down square inside box made
        self.make_canvas.create_rectangle ( 100 + 40 , 340 + 80 + 15 , 100 + 40 + 40 , 340 + 80 + 40 + 15 , width = 3 ,
                                            fill = "#04d9ff" )
        self.make_canvas.create_rectangle ( 100 + 40 + 60 + 40 + 20 , 340 + 80 + 15 , 100 + 40 + 60 + 40 + 40 + 20 ,
                                            340 + 80 + 40 + 15 , width = 3 , fill = "#04d9ff" )
        self.make_canvas.create_rectangle ( 100 + 40 , 340 + 80 + 60 + 40 + 15 , 100 + 40 + 40 ,
                                            340 + 80 + 60 + 40 + 40 + 15 , width = 3 , fill = "#04d9ff" )
        self.make_canvas.create_rectangle ( 100 + 40 + 60 + 40 + 20 , 340 + 80 + 60 + 40 + 15 ,
                                            100 + 40 + 60 + 40 + 40 + 20 , 340 + 80 + 60 + 40 + 40 + 15 , width = 3 ,
                                            fill = "#04d9ff" )

        # Right down square inside box made
        self.make_canvas.create_rectangle ( 340 + (40 * 3) + 40 , 340 + 80 + 15 , 340 + (40 * 3) + 40 + 40 ,
                                            340 + 80 + 40 + 15 , width = 3 , fill = "yellow" )
        self.make_canvas.create_rectangle ( 340 + (40 * 3) + 40 + 60 + 40 + 20 , 340 + 80 + 15 ,
                                            340 + (40 * 3) + 40 + 60 + 40 + 40 + 20 , 340 + 80 + 40 + 15 , width = 3 ,
                                            fill = "yellow" )
        self.make_canvas.create_rectangle ( 340 + (40 * 3) + 40 , 340 + 80 + 60 + 40 + 15 , 340 + (40 * 3) + 40 + 40 ,
                                            340 + 80 + 60 + 40 + 40 + 15 , width = 3 , fill = "yellow" )
        self.make_canvas.create_rectangle ( 340 + (40 * 3) + 40 + 60 + 40 + 20 , 340 + 80 + 60 + 40 + 15 ,
                                            340 + (40 * 3) + 40 + 60 + 40 + 40 + 20 , 340 + 80 + 60 + 40 + 40 + 15 ,
                                            width = 3 , fill = "yellow" )

        # sky_blue start position
        self.make_canvas.create_rectangle ( 100 + 240 , 340 + (40 * 5) - 5 , 100 + 240 + 40 , 340 + (40 * 6) - 5 ,
                                            fill = "#04d9ff" , width = 3 )
        # Red start position
        self.make_canvas.create_rectangle ( 100 + 40 , 15 + (40 * 6) , 100 + 40 + 40 , 15 + (40 * 6) + 40 ,
                                            fill = "red" , width = 3 )
        # Green start position
        self.make_canvas.create_rectangle ( 100 + (40 * 8) , 15 + 40 , 100 + (40 * 9) , 15 + 40 + 40 ,
                                            fill = "#00FF00" , width = 3 )
        # Yellow start position
        self.make_canvas.create_rectangle ( 100 + (40 * 6) + (40 * 3) + (40 * 4) , 15 + (40 * 8) ,
                                            100 + (40 * 6) + (40 * 3) + (40 * 5) , 15 + (40 * 9) , fill = "yellow" ,
                                            width = 3 )

        # Triangle in middle
        self.make_canvas.create_polygon ( 100 + 240 , 15 + 240 , 100 + 240 + 60 , 15 + 240 + 60 , 100 + 240 ,
                                          15 + 240 + (40 * 3) , width = 3 , fill = "red" , outline = "black" )
        self.make_canvas.create_polygon ( 100 + 240 + (40 * 3) , 15 + 240 , 100 + 240 + 60 , 15 + 240 + 60 ,
                                          100 + 240 + (40 * 3) , 15 + 240 + (40 * 3) , width = 3 , fill = "yellow" ,
                                          outline = "black" )
        self.make_canvas.create_polygon ( 100 + 240 , 15 + 240 , 100 + 240 + 60 , 15 + 240 + 60 , 100 + 240 + (40 * 3) ,
                                          15 + 240 , width = 3 , fill = "#00FF00" , outline = "black" )
        self.make_canvas.create_polygon ( 100 + 240 , 15 + 240 + (40 * 3) , 100 + 240 + 60 , 15 + 240 + 60 ,
                                          100 + 240 + (40 * 3) , 15 + 240 + (40 * 3) , width = 3 , fill = "#04d9ff" ,
                                          outline = "black" )

        # Make coin for red left up block
        red_1_coin = self.make_canvas.create_oval ( 100 + 40 , 15 + 40 , 100 + 40 + 40 , 15 + 40 + 40 , width = 3 ,
                                                    fill = "red" , outline = "black" )
        red_2_coin = self.make_canvas.create_oval ( 100 + 40 + 60 + 60 , 15 + 40 , 100 + 40 + 60 + 40 + 60 ,
                                                    15 + 40 + 40 , width = 3 , fill = "red" , outline = "black" )
        red_3_coin = self.make_canvas.create_oval ( 100 + 40 + 60 + 60 , 15 + 40 + 100 , 100 + 40 + 60 + 60 + 40 ,
                                                    15 + 40 + 40 + 100 , width = 3 , fill = "red" , outline = "black" )
        red_4_coin = self.make_canvas.create_oval ( 100 + 40 , 15 + 40 + 100 , 100 + 40 + 40 , 15 + 40 + 40 + 100 ,
                                                    width = 3 , fill = "red" , outline = "black" )
        self.made_red_coin.append ( red_1_coin )
        self.made_red_coin.append ( red_2_coin )
        self.made_red_coin.append ( red_3_coin )
        self.made_red_coin.append ( red_4_coin )

        # Make coin under number label for red left up block
        red_1_label = tk.Label ( self.make_canvas , text = "1" , font = ("Arial" , 15 , "bold") , bg = "red" ,
                                 fg = "black" )
        red_1_label.place ( x = 100 + 40 + 10 , y = 15 + 40 + 5 )
        red_2_label = tk.Label ( self.make_canvas , text = "2" , font = ("Arial" , 15 , "bold") , bg = "red" ,
                                 fg = "black" )
        red_2_label.place ( x = 100 + 40 + 60 + 60 + 10 , y = 15 + 40 + 5 )
        red_3_label = tk.Label ( self.make_canvas , text = "3" , font = ("Arial" , 15 , "bold") , bg = "red" ,
                                 fg = "black" )
        red_3_label.place ( x = 100 + 40 + 60 + 60 + 10 , y = 15 + 40 + 100 + 5 )
        red_4_label = tk.Label ( self.make_canvas , text = "4" , font = ("Arial" , 15 , "bold") , bg = "red" ,
                                 fg = "black" )
        red_4_label.place ( x = 100 + 40 + 10 , y = 15 + 40 + 100 + 5 )
        self.red_number_label.append ( red_1_label )
        self.red_number_label.append ( red_2_label )
        self.red_number_label.append ( red_3_label )
        self.red_number_label.append ( red_4_label )

        # Make coin for green right up block
        green_1_coin = self.make_canvas.create_oval ( 340 + (40 * 3) + 40 , 15 + 40 , 340 + (40 * 3) + 40 + 40 ,
                                                      15 + 40 + 40 , width = 3 , fill = "#00FF00" , outline = "black" )
        green_2_coin = self.make_canvas.create_oval ( 340 + (40 * 3) + 40 + 60 + 40 + 20 , 15 + 40 ,
                                                      340 + (40 * 3) + 40 + 60 + 40 + 40 + 20 , 15 + 40 + 40 ,
                                                      width = 3 , fill = "#00FF00" , outline = "black" )
        green_3_coin = self.make_canvas.create_oval ( 340 + (40 * 3) + 40 + 60 + 40 + 20 , 15 + 40 + 100 ,
                                                      340 + (40 * 3) + 40 + 60 + 40 + 40 + 20 , 15 + 40 + 40 + 100 ,
                                                      width = 3 , fill = "#00FF00" , outline = "black" )
        green_4_coin = self.make_canvas.create_oval ( 340 + (40 * 3) + 40 , 15 + 40 + 100 , 340 + (40 * 3) + 40 + 40 ,
                                                      15 + 40 + 40 + 100 , width = 3 , fill = "#00FF00" ,
                                                      outline = "black" )
        self.made_green_coin.append ( green_1_coin )
        self.made_green_coin.append ( green_2_coin )
        self.made_green_coin.append ( green_3_coin )
        self.made_green_coin.append ( green_4_coin )

        # Make coin under number label for green right up block
        green_1_label = tk.Label ( self.make_canvas , text = "1" , font = ("Arial" , 15 , "bold") , bg = "#00FF00" ,
                                   fg = "black" )
        green_1_label.place ( x = 340 + (40 * 3) + 40 + 10 , y = 15 + 40 + 5 )
        green_2_label = tk.Label ( self.make_canvas , text = "2" , font = ("Arial" , 15 , "bold") , bg = "#00FF00" ,
                                   fg = "black" )
        green_2_label.place ( x = 340 + (40 * 3) + 40 + 40 + 60 + 30 , y = 15 + 40 + 5 )
        green_3_label = tk.Label ( self.make_canvas , text = "3" , font = ("Arial" , 15 , "bold") , bg = "#00FF00" ,
                                   fg = "black" )
        green_3_label.place ( x = 340 + (40 * 3) + 40 + 40 + 60 + 30 , y = 15 + 40 + 100 + 5 )
        green_4_label = tk.Label ( self.make_canvas , text = "4" , font = ("Arial" , 15 , "bold") , bg = "#00FF00" ,
                                   fg = "black" )
        green_4_label.place ( x = 340 + (40 * 3) + 40 + 10 , y = 15 + 40 + 100 + 5 )
        self.green_number_label.append ( green_1_label )
        self.green_number_label.append ( green_2_label )
        self.green_number_label.append ( green_3_label )
        self.green_number_label.append ( green_4_label )

        # Make coin for sky_blue left down block
        sky_blue_1_coin = self.make_canvas.create_oval ( 100 + 40 , 340 + 80 + 15 , 100 + 40 + 40 , 340 + 80 + 40 + 15 ,
                                                         width = 3 , fill = "#04d9ff" , outline = "black" )
        sky_blue_2_coin = self.make_canvas.create_oval ( 100 + 40 + 60 + 40 + 20 , 340 + 80 + 15 ,
                                                         100 + 40 + 60 + 40 + 40 + 20 , 340 + 80 + 40 + 15 , width = 3 ,
                                                         fill = "#04d9ff" , outline = "black" )
        sky_blue_3_coin = self.make_canvas.create_oval ( 100 + 40 + 60 + 40 + 20 , 340 + 80 + 60 + 40 + 15 ,
                                                         100 + 40 + 60 + 40 + 40 + 20 , 340 + 80 + 60 + 40 + 40 + 15 ,
                                                         width = 3 , fill = "#04d9ff" , outline = "black" )
        sky_blue_4_coin = self.make_canvas.create_oval ( 100 + 40 , 340 + 80 + 60 + 40 + 15 , 100 + 40 + 40 ,
                                                         340 + 80 + 60 + 40 + 40 + 15 , width = 3 , fill = "#04d9ff" ,
                                                         outline = "black" )
        self.made_sky_blue_coin.append ( sky_blue_1_coin )
        self.made_sky_blue_coin.append ( sky_blue_2_coin )
        self.made_sky_blue_coin.append ( sky_blue_3_coin )
        self.made_sky_blue_coin.append ( sky_blue_4_coin )

        # Make coin under number label for sky_blue left down block
        sky_blue_1_label = tk.Label ( self.make_canvas , text = "1" , font = ("Arial" , 15 , "bold") , bg = "#04d9ff" ,
                                      fg = "black" )
        sky_blue_1_label.place ( x = 100 + 40 + 10 , y = 30 + (40 * 6) + (40 * 3) + 40 + 10 )
        sky_blue_2_label = tk.Label ( self.make_canvas , text = "2" , font = ("Arial" , 15 , "bold") , bg = "#04d9ff" ,
                                      fg = "black" )
        sky_blue_2_label.place ( x = 100 + 40 + 60 + 60 + 10 , y = 30 + (40 * 6) + (40 * 3) + 40 + 10 )
        sky_blue_3_label = tk.Label ( self.make_canvas , text = "3" , font = ("Arial" , 15 , "bold") , bg = "#04d9ff" ,
                                      fg = "black" )
        sky_blue_3_label.place ( x = 100 + 40 + 60 + 60 + 10 , y = 30 + (40 * 6) + (40 * 3) + 40 + 60 + 40 + 10 )
        sky_blue_4_label = tk.Label ( self.make_canvas , text = "4" , font = ("Arial" , 15 , "bold") , bg = "#04d9ff" ,
                                      fg = "black" )
        sky_blue_4_label.place ( x = 100 + 40 + 10 , y = 30 + (40 * 6) + (40 * 3) + 40 + 60 + 40 + 10 )
        self.sky_blue_number_label.append ( sky_blue_1_label )
        self.sky_blue_number_label.append ( sky_blue_2_label )
        self.sky_blue_number_label.append ( sky_blue_3_label )
        self.sky_blue_number_label.append ( sky_blue_4_label )

        # Make coin for yellow right down block
        yellow_1_coin = self.make_canvas.create_oval ( 340 + (40 * 3) + 40 , 340 + 80 + 15 , 340 + (40 * 3) + 40 + 40 ,
                                                       340 + 80 + 40 + 15 , width = 3 , fill = "yellow" ,
                                                       outline = "black" )
        yellow_2_coin = self.make_canvas.create_oval ( 340 + (40 * 3) + 40 + 60 + 40 + 20 , 340 + 80 + 15 ,
                                                       340 + (40 * 3) + 40 + 60 + 40 + 40 + 20 , 340 + 80 + 40 + 15 ,
                                                       width = 3 , fill = "yellow" , outline = "black" )
        yellow_3_coin = self.make_canvas.create_oval ( 340 + (40 * 3) + 40 + 60 + 40 + 20 , 340 + 80 + 60 + 40 + 15 ,
                                                       340 + (40 * 3) + 40 + 60 + 40 + 40 + 20 ,
                                                       340 + 80 + 60 + 40 + 40 + 15 , width = 3 , fill = "yellow" ,
                                                       outline = "black" )
        yellow_4_coin = self.make_canvas.create_oval ( 340 + (40 * 3) + 40 , 340 + 80 + 60 + 40 + 15 ,
                                                       340 + (40 * 3) + 40 + 40 , 340 + 80 + 60 + 40 + 40 + 15 ,
                                                       width = 3 , fill = "yellow" , outline = "black" )
        self.made_yellow_coin.append ( yellow_1_coin )
        self.made_yellow_coin.append ( yellow_2_coin )
        self.made_yellow_coin.append ( yellow_3_coin )
        self.made_yellow_coin.append ( yellow_4_coin )

        # Make coin under number label for yellow right down block
        yellow_1_label = tk.Label ( self.make_canvas , text = "1" , font = ("Arial" , 15 , "bold") , bg = "yellow" ,
                                    fg = "black" )
        yellow_1_label.place ( x = 340 + (40 * 3) + 40 + 10 , y = 30 + (40 * 6) + (40 * 3) + 40 + 10 )
        yellow_2_label = tk.Label ( self.make_canvas , text = "2" , font = ("Arial" , 15 , "bold") , bg = "yellow" ,
                                    fg = "black" )
        yellow_2_label.place ( x = 340 + (40 * 3) + 40 + 40 + 60 + 30 , y = 30 + (40 * 6) + (40 * 3) + 40 + 10 )
        yellow_3_label = tk.Label ( self.make_canvas , text = "3" , font = ("Arial" , 15 , "bold") , bg = "yellow" ,
                                    fg = "black" )
        yellow_3_label.place ( x = 340 + (40 * 3) + 40 + 40 + 60 + 30 , y = 30 + (40 * 6) + (40 * 3) + 40 + 100 + 10 )
        yellow_4_label = tk.Label ( self.make_canvas , text = "4" , font = ("Arial" , 15 , "bold") , bg = "yellow" ,
                                    fg = "black" )
        yellow_4_label.place ( x = 340 + (40 * 3) + 40 + 10 , y = 30 + (40 * 6) + (40 * 3) + 40 + 100 + 10 )
        self.yellow_number_label.append ( yellow_1_label )
        self.yellow_number_label.append ( yellow_2_label )
        self.yellow_number_label.append ( yellow_3_label )
        self.yellow_number_label.append ( yellow_4_label )

        # Make star safe zone
        # Right star
        common_x = 340 + (40 * 6) + 20
        common_y = 15 + 240 + 2
        coord = [common_x , common_y , common_x + 5 , common_y + 15 , common_x + 15 , common_y + 15 , common_x + 8 ,
                 common_y + 20 , common_x + 15 , common_y + 25 , common_x + 5 , common_y + 25 , common_x ,
                 common_y + 25 + 10 , common_x - 5 , common_y + 25 , common_x - 16 , common_y + 25 , common_x - 8 ,
                 common_y + 15 + 5 , common_x - 15 , common_y + 15 , common_x - 5 , common_y + 15]
        self.make_canvas.create_polygon ( coord , width = 3 , fill = "blue" )

        # Up star
        common_x = 100 + 240 + 2 + 18
        common_y = 15 + (40 * 2) + 2
        coord = [common_x , common_y , common_x + 5 , common_y + 15 , common_x + 15 , common_y + 15 , common_x + 8 ,
                 common_y + 20 , common_x + 15 , common_y + 25 , common_x + 5 , common_y + 25 , common_x ,
                 common_y + 25 + 10 , common_x - 5 , common_y + 25 , common_x - 16 , common_y + 25 , common_x - 8 ,
                 common_y + 15 + 5 , common_x - 15 , common_y + 15 , common_x - 5 , common_y + 15]
        self.make_canvas.create_polygon ( coord , width = 3 , fill = "blue" )

        # Left star
        common_x = 100 + (40 * 2) + 2 + 18
        common_y = 15 + 240 + (40 * 2) + 2
        coord = [common_x , common_y , common_x + 5 , common_y + 15 , common_x + 15 , common_y + 15 , common_x + 8 ,
                 common_y + 20 , common_x + 15 , common_y + 25 , common_x + 5 , common_y + 25 , common_x ,
                 common_y + 25 + 10 , common_x - 5 , common_y + 25 , common_x - 16 , common_y + 25 , common_x - 8 ,
                 common_y + 15 + 5 , common_x - 15 , common_y + 15 , common_x - 5 , common_y + 15]
        self.make_canvas.create_polygon ( coord , width = 3 , fill = "blue" )

        # Down star
        common_x = 100 + 240 + (40 * 2) + 2 + 18
        common_y = 15 + (40 * 6) + (40 * 3) + (40 * 3) + 2
        coord = [common_x , common_y , common_x + 5 , common_y + 15 , common_x + 15 , common_y + 15 , common_x + 8 ,
                 common_y + 20 , common_x + 15 , common_y + 25 , common_x + 5 , common_y + 25 , common_x ,
                 common_y + 25 + 10 , common_x - 5 , common_y + 25 , common_x - 16 , common_y + 25 , common_x - 8 ,
                 common_y + 15 + 5 , common_x - 15 , common_y + 15 , common_x - 5 , common_y + 15]
        self.make_canvas.create_polygon ( coord , width = 3 , fill = "blue" )

    def take_initial_control(self):
        # Initialize buttons after block_value_predict is populated
        for i in range(len(self.block_value_predict)):
            self.block_value_predict[i][1]['state'] = tk.DISABLED

        # Create Toplevel window for player input
        top = tk.Toplevel(self.window)
        top.geometry("600x150+475+270")
        top.maxsize(600, 150)
        top.minsize(600, 150)
        top.config(bg="orange")
        top.iconbitmap("Images/ludo_icon.ico")
        top.transient(self.window)  # Tie Toplevel to main window
        top.grab_set()  # Make Toplevel modal

        head = tk.Label(top, text="-:Total number of players:-", font=("Arial", 25, "bold", "italic"),
                        bg="orange", fg="chocolate")
        head.place(x=70, y=30)
        take_entry = tk.Entry(top, font=("Arial", 18, "bold", "italic"), relief=tk.SUNKEN, bd=7, width=12)
        take_entry.place(x=150, y=80)
        take_entry.focus()

        def filtering():
            response_take = self.input_filtering(take_entry.get())
            if response_take and 2 <= int(take_entry.get()) <= 4:
                for player_index in range(int(take_entry.get())):
                    self.total_people_play.append(player_index)
                print(self.total_people_play)
                self.make_command()
                top.destroy()
            else:
                messagebox.showerror("Input Error", "Please input number of players between 2 and 4")

        submit_btn = tk.Button(top, text="Submit", bg="black", fg="#00FF00",
                               font=("Arial", 13, "bold"), relief=tk.RAISED, bd=8, command=filtering)
        submit_btn.place(x=350, y=80)

    def input_filtering(self , take_input):
        try:
            int ( take_input )
            if int ( take_input ) > 4 or int ( take_input ) < 1:
                return False
            return True
        except:
            return False

    def make_prediction(self , color_indicator):
        try:
            if color_indicator == "red":
                block_value_predict = self.block_value_predict[0]
                permanent_block_number = self.move_red_counter = randint ( 1 , 6 )
            elif color_indicator == "sky_blue":
                block_value_predict = self.block_value_predict[1]
                permanent_block_number = self.move_sky_blue_counter = randint ( 1 , 6 )
            elif color_indicator == "yellow":
                block_value_predict = self.block_value_predict[2]
                permanent_block_number = self.move_yellow_counter = randint ( 1 , 6 )
            else:
                block_value_predict = self.block_value_predict[3]
                permanent_block_number = self.move_green_counter = randint ( 1 , 6 )

            block_value_predict[1]['state'] = tk.DISABLED

            # Illusion of coin floating
            temp_counter = 15
            while temp_counter > 0:
                move_temp_counter = randint ( 1 , 6 )
                block_value_predict[0]['image'] = self.block_number_side[move_temp_counter - 1]
                self.window.update ( )
                time.sleep ( 0.1 )
                temp_counter -= 1

            print ( "Prediction result: " , permanent_block_number )

            # Permanent predicted value containing image set
            block_value_predict[0]['image'] = self.block_number_side[permanent_block_number - 1]
            self.instructional_btn_customization_based_on_current_situation ( color_indicator , permanent_block_number ,
                                                                              block_value_predict )
        except:
            print ( "Force stop error" )

    def instructional_btn_customization_based_on_current_situation(self , color_indicator , permanent_block_number ,
                                                                   block_value_predict):
        if color_indicator == "red":
            temp_coin_position = self.red_coin_position
        elif color_indicator == "green":
            temp_coin_position = self.green_coin_position
        elif color_indicator == "yellow":
            temp_coin_position = self.yellow_coin_position
        else:
            temp_coin_position = self.sky_blue_coin_position

        all_in = 1
        for i in range ( 4 ):
            if temp_coin_position[i] == -1:
                all_in = 1
            else:
                all_in = 0
                break

        if permanent_block_number == 6:
            self.six_counter += 1
        else:
            self.six_counter = 0

        if ((all_in == 1 and permanent_block_number == 6) or (all_in == 0)) and self.six_counter < 3:
            permission = 1
            if color_indicator == "red":
                temp = self.red_coord_store
            elif color_indicator == "green":
                temp = self.green_coord_store
            elif color_indicator == "yellow":
                temp = self.yellow_coord_store
            else:
                temp = self.sky_blue_coord_store

            if permanent_block_number < 6:
                if self.six_with_overlap == 1:
                    self.time_for -= 1
                    self.six_with_overlap = 0
                for i in range ( 4 ):
                    if temp[i] == -1:
                        permission = 0
                    elif temp[i] > 100:
                        if temp[i] + permanent_block_number <= 106:
                            permission = 1
                            break
                        else:
                            permission = 0
                    else:
                        permission = 1
                        break
            else:
                for i in range ( 4 ):
                    if temp[i] > 100:
                        if temp[i] + permanent_block_number <= 106:
                            permission = 1
                            break
                        else:
                            permission = 0
                    else:
                        permission = 1
                        break
            if permission == 0:
                self.make_command ( )
            else:
                block_value_predict[3]['state'] = tk.NORMAL
                block_value_predict[1]['state'] = tk.DISABLED
        else:
            block_value_predict[1]['state'] = tk.NORMAL
            if self.six_with_overlap == 1:
                self.time_for -= 1
                self.six_with_overlap = 0
            self.make_command ( )

        if permanent_block_number == 6 and self.six_counter < 3 and block_value_predict[3]['state'] == tk.NORMAL:
            self.time_for -= 1
        else:
            self.six_counter = 0

    def make_command(self):
        if self.time_for == -1:
            pass
        else:
            self.block_value_predict[self.total_people_play[self.time_for]][1]['state'] = tk.DISABLED
        if self.time_for == len ( self.total_people_play ) - 1:
            self.time_for = -1

        self.time_for += 1
        self.block_value_predict[self.total_people_play[self.time_for]][1]['state'] = tk.NORMAL

    def instruction_btn_red(self):
        block_predict_red = tk.Label ( self.make_canvas , image = self.block_number_side[0] )
        block_predict_red.place ( x = 45 , y = 15 )
        predict_red = tk.Button ( self.make_canvas , bg = "black" , fg = "#00FF00" , relief = tk.RAISED , bd = 5 ,
                                  text = "Predict" , font = ("Arial" , 8 , "bold") ,
                                  command = lambda: self.make_prediction ( "red" ) )
        predict_red.place ( x = 37 , y = 15 + 40 )
        entry_take_red = tk.Entry ( self.make_canvas , bg = "white" , fg = "blue" ,
                                    font = ("Arial" , 25 , "bold" , "italic") , width = 2 , relief = tk.SUNKEN ,
                                    bd = 5 )
        entry_take_red.place ( x = 40 , y = 15 + 80 )
        final_move = tk.Button ( self.make_canvas , bg = "black" , fg = "#00FF00" , relief = tk.RAISED , bd = 5 ,
                                 text = "Give" , font = ("Arial" , 8 , "bold") ,
                                 command = lambda: self.main_controller ( "red" , entry_take_red.get ( ) ) ,
                                 state = tk.DISABLED )
        final_move.place ( x = 42 , y = 15 + 140 )
        tk.Label ( self.make_canvas , text = "Player 1" , bg = "#4d4dff" , fg = "gold" ,
                   font = ("Arial" , 15 , "bold") ).place ( x = 15 , y = 15 + 140 + 40 )
        self.store_instructional_btn ( block_predict_red , predict_red , entry_take_red , final_move )

    def instruction_btn_sky_blue(self):
        block_predict_sky_blue = tk.Label ( self.make_canvas , image = self.block_number_side[0] )
        block_predict_sky_blue.place ( x = 45 , y = 15 + (40 * 6 + 40 * 3) + 10 )
        predict_sky_blue = tk.Button ( self.make_canvas , bg = "black" , fg = "#00FF00" , relief = tk.RAISED , bd = 5 ,
                                       text = "Predict" , font = ("Arial" , 8 , "bold") ,
                                       command = lambda: self.make_prediction ( "sky_blue" ) )
        predict_sky_blue.place ( x = 37 , y = 15 + (40 * 6 + 40 * 3) + 40 + 10 )
        entry_take_sky_blue = tk.Entry ( self.make_canvas , bg = "white" , fg = "blue" ,
                                         font = ("Arial" , 25 , "bold" , "italic") , width = 2 , relief = tk.SUNKEN ,
                                         bd = 5 )
        entry_take_sky_blue.place ( x = 40 , y = 15 + (40 * 6 + 40 * 3) + 40 + 50 )
        final_move = tk.Button ( self.make_canvas , bg = "black" , fg = "#00FF00" , relief = tk.RAISED , bd = 5 ,
                                 text = "Give" , font = ("Arial" , 8 , "bold") ,
                                 command = lambda: self.main_controller ( "sky_blue" , entry_take_sky_blue.get ( ) ) ,
                                 state = tk.DISABLED )
        final_move.place ( x = 42 , y = 15 + (40 * 6 + 40 * 3) + 40 + 110 )
        tk.Label ( self.make_canvas , text = "Player 2" , bg = "#4d4dff" , fg = "gold" ,
                   font = ("Arial" , 15 , "bold") ).place ( x = 15 , y = 15 + (40 * 6 + 40 * 3) + 40 + 110 + 40 )
        self.store_instructional_btn ( block_predict_sky_blue , predict_sky_blue , entry_take_sky_blue , final_move )

    def instruction_btn_yellow(self):
        block_predict_yellow = tk.Label ( self.make_canvas , image = self.block_number_side[0] )
        block_predict_yellow.place ( x = 100 + (40 * 6 + 40 * 3 + 40 * 6 + 10) + 10 , y = 15 + (40 * 6 + 40 * 3) + 10 )
        predict_yellow = tk.Button ( self.make_canvas , bg = "black" , fg = "#00FF00" , relief = tk.RAISED , bd = 5 ,
                                     text = "Predict" , font = ("Arial" , 8 , "bold") ,
                                     command = lambda: self.make_prediction ( "yellow" ) )
        predict_yellow.place ( x = 100 + (40 * 6 + 40 * 3 + 40 * 6 + 2) + 10 , y = 15 + (40 * 6 + 40 * 3) + 40 + 10 )
        entry_take_yellow = tk.Entry ( self.make_canvas , bg = "white" , fg = "blue" ,
                                       font = ("Arial" , 25 , "bold" , "italic") , width = 2 , relief = tk.SUNKEN ,
                                       bd = 5 )
        entry_take_yellow.place ( x = 100 + (40 * 6 + 40 * 3 + 40 * 6 + 2) + 13 , y = 15 + (40 * 6 + 40 * 3) + 40 + 50 )
        final_move = tk.Button ( self.make_canvas , bg = "black" , fg = "#00FF00" , relief = tk.RAISED , bd = 5 ,
                                 text = "Give" , font = ("Arial" , 8 , "bold") ,
                                 command = lambda: self.main_controller ( "yellow" , entry_take_yellow.get ( ) ) ,
                                 state = tk.DISABLED )
        final_move.place ( x = 100 + (40 * 6 + 40 * 3 + 40 * 6 + 2) + 17 , y = 15 + (40 * 6 + 40 * 3) + 40 + 110 )
        tk.Label ( self.make_canvas , text = "Player 3" , bg = "#4d4dff" , fg = "gold" ,
                   font = ("Arial" , 15 , "bold") ).place ( x = 100 + (40 * 6 + 40 * 3 + 40 * 6 + 3) ,
                                                            y = 15 + (40 * 6 + 40 * 3) + 40 + 110 + 40 )
        self.store_instructional_btn ( block_predict_yellow , predict_yellow , entry_take_yellow , final_move )

    def instruction_btn_green(self):
        block_predict_green = tk.Label ( self.make_canvas , image = self.block_number_side[0] )
        block_predict_green.place ( x = 100 + (40 * 6 + 40 * 3 + 40 * 6 + 10) + 10 , y = 15 )
        predict_green = tk.Button ( self.make_canvas , bg = "black" , fg = "#00FF00" , relief = tk.RAISED , bd = 5 ,
                                    text = "Predict" , font = ("Arial" , 8 , "bold") ,
                                    command = lambda: self.make_prediction ( "green" ) )
        predict_green.place ( x = 100 + (40 * 6 + 40 * 3 + 40 * 6 + 2) + 10 , y = 15 + 40 )
        entry_take_green = tk.Entry ( self.make_canvas , bg = "white" , fg = "blue" ,
                                      font = ("Arial" , 25 , "bold" , "italic") , width = 2 , relief = tk.SUNKEN ,
                                      bd = 5 )
        entry_take_green.place ( x = 100 + (40 * 6 + 40 * 3 + 40 * 6 + 2) + 13 , y = 15 + 80 )
        final_move = tk.Button ( self.make_canvas , bg = "black" , fg = "#00FF00" , relief = tk.RAISED , bd = 5 ,
                                 text = "Give" , font = ("Arial" , 8 , "bold") ,
                                 command = lambda: self.main_controller ( "green" , entry_take_green.get ( ) ) ,
                                 state = tk.DISABLED )
        final_move.place ( x = 100 + (40 * 6 + 40 * 3 + 40 * 6 + 2) + 17 , y = 15 + 140 )
        tk.Label ( self.make_canvas , text = "Player 4" , bg = "#4d4dff" , fg = "gold" ,
                   font = ("Arial" , 15 , "bold") ).place ( x = 100 + (40 * 6 + 40 * 3 + 40 * 6 + 3) ,
                                                            y = 15 + 140 + 40 )
        self.store_instructional_btn ( block_predict_green , predict_green , entry_take_green , final_move )

    def store_instructional_btn(self , block_indicator , predictor , entry_controller , give_finally):
        temp = []
        temp.append ( block_indicator )
        temp.append ( predictor )
        temp.append ( entry_controller )
        temp.append ( give_finally )
        self.block_value_predict.append ( temp )

    def red_circle_start_position(self , coin_number):
        self.make_canvas.delete ( self.made_red_coin[int ( coin_number ) - 1] )
        self.made_red_coin[int ( coin_number ) - 1] = self.make_canvas.create_oval ( 100 + 40 , 15 + (40 * 6) ,
                                                                                     100 + 40 + 40 ,
                                                                                     15 + (40 * 6) + 40 , fill = "red" ,
                                                                                     width = 3 , outline = "black" )
        self.red_number_label[int ( coin_number ) - 1].place_forget ( )
        red_start_label_x = 100 + 40 + 10
        red_start_label_y = 15 + (40 * 6) + 5
        self.red_number_label[int ( coin_number ) - 1].place ( x = red_start_label_x , y = red_start_label_y )
        self.red_coin_position[int ( coin_number ) - 1] = 1
        self.window.update ( )
        time.sleep ( 0.2 )

    def green_circle_start_position(self , coin_number):
        self.make_canvas.delete ( self.made_green_coin[int ( coin_number ) - 1] )
        self.made_green_coin[int ( coin_number ) - 1] = self.make_canvas.create_oval ( 100 + (40 * 8) , 15 + 40 ,
                                                                                       100 + (40 * 9) , 15 + 40 + 40 ,
                                                                                       fill = "#00FF00" , width = 3 )
        self.green_number_label[int ( coin_number ) - 1].place_forget ( )
        green_start_label_x = 100 + (40 * 8) + 10
        green_start_label_y = 15 + 40 + 5
        self.green_number_label[int ( coin_number ) - 1].place ( x = green_start_label_x , y = green_start_label_y )
        self.green_coin_position[int ( coin_number ) - 1] = 14
        self.window.update ( )
        time.sleep ( 0.2 )

    def yellow_circle_start_position(self , coin_number):
        self.make_canvas.delete ( self.made_yellow_coin[int ( coin_number ) - 1] )
        self.made_yellow_coin[int ( coin_number ) - 1] = self.make_canvas.create_oval (
            100 + (40 * 6) + (40 * 3) + (40 * 4) , 15 + (40 * 8) , 100 + (40 * 6) + (40 * 3) + (40 * 5) ,
            15 + (40 * 9) , fill = "yellow" , width = 3 )
        self.yellow_number_label[int ( coin_number ) - 1].place_forget ( )
        yellow_start_label_x = 100 + (40 * 6) + (40 * 3) + (40 * 4) + 10
        yellow_start_label_y = 15 + (40 * 8) + 5
        self.yellow_number_label[int ( coin_number ) - 1].place ( x = yellow_start_label_x , y = yellow_start_label_y )
        self.yellow_coin_position[int ( coin_number ) - 1] = 27
        self.window.update ( )
        time.sleep ( 0.2 )

    def sky_blue_circle_start_position(self , coin_number):
        self.make_canvas.delete ( self.made_sky_blue_coin[int ( coin_number ) - 1] )
        self.made_sky_blue_coin[int ( coin_number ) - 1] = self.make_canvas.create_oval ( 100 + 240 ,
                                                                                          340 + (40 * 5) - 5 ,
                                                                                          100 + 240 + 40 ,
                                                                                          340 + (40 * 6) - 5 ,
                                                                                          fill = "#04d9ff" , width = 3 )
        self.sky_blue_number_label[int ( coin_number ) - 1].place_forget ( )
        sky_blue_start_label_x = 100 + 240 + 10
        sky_blue_start_label_y = 340 + (40 * 5) - 5 + 5
        self.sky_blue_number_label[int ( coin_number ) - 1].place ( x = sky_blue_start_label_x ,
                                                                    y = sky_blue_start_label_y )
        self.sky_blue_coin_position[int ( coin_number ) - 1] = 40
        self.window.update ( )
        time.sleep ( 0.2 )

    def main_controller(self , color_coin , coin_number):
        processing_result = self.input_filtering ( coin_number )  # Value filtering
        if processing_result is True:
            pass
        else:
            messagebox.showerror ( "Wrong input number" , "Please input the coin number between 1 to 4" )
            return

        if color_coin == "red":
            self.block_value_predict[0][3]['state'] = tk.DISABLED  # Fixed here

            if self.move_red_counter == 106:
                messagebox.showwarning ( "Destination reached" , "Reached at the destination" )

            elif self.red_coin_position[int ( coin_number ) - 1] == -1 and self.move_red_counter == 6:
                self.red_circle_start_position ( coin_number )
                self.red_coord_store[int ( coin_number ) - 1] = 1

            elif self.red_coin_position[int ( coin_number ) - 1] > -1:
                take_coord = self.make_canvas.coords ( self.made_red_coin[int ( coin_number ) - 1] )
                red_start_label_x = take_coord[0] + 10
                red_start_label_y = take_coord[1] + 5
                self.red_number_label[int ( coin_number ) - 1].place ( x = red_start_label_x , y = red_start_label_y )

                if self.red_coin_position[int ( coin_number ) - 1] + self.move_red_counter <= 106:
                    self.red_coin_position[int ( coin_number ) - 1] = self.motion_of_coin (
                        self.red_coin_position[int ( coin_number ) - 1] , self.made_red_coin[int ( coin_number ) - 1] ,
                        self.red_number_label[int ( coin_number ) - 1] , red_start_label_x , red_start_label_y ,
                        "red" , self.move_red_counter
                    )
                else:
                    messagebox.showerror ( "Not possible" , "Sorry, not permitted" )
                    self.block_value_predict[0][3]['state'] = tk.NORMAL  # Fixed here
                    return

                if self.red_coin_position[int ( coin_number ) - 1] in [22 , 9 , 48 , 35 , 14 , 27 , 40]:
                    pass
                else:
                    if self.red_coin_position[int ( coin_number ) - 1] < 100:
                        self.coord_overlap ( self.red_coin_position[int ( coin_number ) - 1] , color_coin ,
                                             self.move_red_counter )

                self.red_coord_store[int ( coin_number ) - 1] = self.red_coin_position[int ( coin_number ) - 1]

            else:
                messagebox.showerror ( "Wrong choice" , "Sorry, Your coin is not permitted to travel" )
                self.block_value_predict[0][3]['state'] = tk.NORMAL  # Fixed here
                return

            self.block_value_predict[0][1]['state'] = tk.NORMAL  # Fixed here

        elif color_coin == "green":
            self.block_value_predict[3][3]['state'] = tk.DISABLED  # Fixed here

            if self.move_green_counter == 106:
                messagebox.showwarning ( "Destination reached" , "Reached at the destination" )

            elif self.green_coin_position[int ( coin_number ) - 1] == -1 and self.move_green_counter == 6:
                self.green_circle_start_position ( coin_number )
                self.green_coord_store[int ( coin_number ) - 1] = 14

            elif self.green_coin_position[int ( coin_number ) - 1] > -1:
                take_coord = self.make_canvas.coords ( self.made_green_coin[int ( coin_number ) - 1] )
                green_start_label_x = take_coord[0] + 10
                green_start_label_y = take_coord[1] + 5
                self.green_number_label[int ( coin_number ) - 1].place ( x = green_start_label_x ,
                                                                         y = green_start_label_y )

                if self.green_coin_position[int ( coin_number ) - 1] + self.move_green_counter <= 106:
                    self.green_coin_position[int ( coin_number ) - 1] = self.motion_of_coin (
                        self.green_coin_position[int ( coin_number ) - 1] ,
                        self.made_green_coin[int ( coin_number ) - 1] ,
                        self.green_number_label[int ( coin_number ) - 1] , green_start_label_x , green_start_label_y ,
                        "green" , self.move_green_counter
                    )
                else:
                    messagebox.showerror ( "Not possible" , "No path available" )
                    self.block_value_predict[3][3]['state'] = tk.NORMAL  # Fixed here
                    return

                if self.green_coin_position[int ( coin_number ) - 1] in [22 , 9 , 48 , 35 , 1 , 27 , 40]:
                    pass
                else:
                    if self.green_coin_position[int ( coin_number ) - 1] < 100:
                        self.coord_overlap ( self.green_coin_position[int ( coin_number ) - 1] , color_coin ,
                                             self.move_green_counter )

                self.green_coord_store[int ( coin_number ) - 1] = self.green_coin_position[int ( coin_number ) - 1]

            else:
                messagebox.showerror ( "Wrong choice" , "Sorry, Your coin is not permitted to travel" )
                self.block_value_predict[3][3]['state'] = tk.NORMAL  # Fixed here
                return

            self.block_value_predict[3][1]['state'] = tk.NORMAL  # Fixed here

        elif color_coin == "yellow":
            self.block_value_predict[2][3]['state'] = tk.DISABLED  # Fixed here

            if self.move_yellow_counter == 106:
                messagebox.showwarning ( "Destination reached" , "Reached at the destination" )

            elif self.yellow_coin_position[int ( coin_number ) - 1] == -1 and self.move_yellow_counter == 6:
                self.yellow_circle_start_position ( coin_number )
                self.yellow_coord_store[int ( coin_number ) - 1] = 27

            elif self.yellow_coin_position[int ( coin_number ) - 1] > -1:
                take_coord = self.make_canvas.coords ( self.made_yellow_coin[int ( coin_number ) - 1] )
                yellow_start_label_x = take_coord[0] + 10
                yellow_start_label_y = take_coord[1] + 5
                self.yellow_number_label[int ( coin_number ) - 1].place ( x = yellow_start_label_x ,
                                                                          y = yellow_start_label_y )

                if self.yellow_coin_position[int ( coin_number ) - 1] + self.move_yellow_counter <= 106:
                    self.yellow_coin_position[int ( coin_number ) - 1] = self.motion_of_coin (
                        self.yellow_coin_position[int ( coin_number ) - 1] ,
                        self.made_yellow_coin[int ( coin_number ) - 1] ,
                        self.yellow_number_label[int ( coin_number ) - 1] , yellow_start_label_x ,
                        yellow_start_label_y ,
                        "yellow" , self.move_yellow_counter
                    )
                else:
                    messagebox.showerror ( "Not possible" , "No path available" )
                    self.block_value_predict[2][3]['state'] = tk.NORMAL  # Fixed here
                    return

                if self.yellow_coin_position[int ( coin_number ) - 1] in [22 , 9 , 48 , 35 , 1 , 14 , 40]:
                    pass
                else:
                    if self.yellow_coin_position[int ( coin_number ) - 1] < 100:
                        self.coord_overlap ( self.yellow_coin_position[int ( coin_number ) - 1] , color_coin ,
                                             self.move_yellow_counter )

                self.yellow_coord_store[int ( coin_number ) - 1] = self.yellow_coin_position[int ( coin_number ) - 1]

            else:
                messagebox.showerror ( "Wrong choice" , "Sorry, Your coin is not permitted to travel" )
                self.block_value_predict[2][3]['state'] = tk.NORMAL  # Fixed here
                return

            self.block_value_predict[2][1]['state'] = tk.NORMAL  # Fixed here

        elif color_coin == "sky_blue":
            self.block_value_predict[1][3]['state'] = tk.DISABLED  # Fixed here
            if self.move_sky_blue_counter == 106:  # Fixed: Changed move_red_counter to move_sky_blue_counter
                messagebox.showwarning ( "Destination reached" , "Reached at the destination" )

            elif self.sky_blue_coin_position[int ( coin_number ) - 1] == -1 and self.move_sky_blue_counter == 6:
                self.sky_blue_circle_start_position ( coin_number )
                self.sky_blue_coord_store[int ( coin_number ) - 1] = 40

            elif self.sky_blue_coin_position[int ( coin_number ) - 1] > -1:
                take_coord = self.make_canvas.coords ( self.made_sky_blue_coin[int ( coin_number ) - 1] )
                sky_blue_start_label_x = take_coord[0] + 10
                sky_blue_start_label_y = take_coord[1] + 5
                self.sky_blue_number_label[int ( coin_number ) - 1].place ( x = sky_blue_start_label_x ,
                                                                            y = sky_blue_start_label_y )

                if self.sky_blue_coin_position[int ( coin_number ) - 1] + self.move_sky_blue_counter <= 106:
                    self.sky_blue_coin_position[int ( coin_number ) - 1] = self.motion_of_coin (
                        self.sky_blue_coin_position[int ( coin_number ) - 1] ,
                        self.made_sky_blue_coin[int ( coin_number ) - 1] ,
                        self.sky_blue_number_label[int ( coin_number ) - 1] , sky_blue_start_label_x ,
                        sky_blue_start_label_y ,
                        "sky_blue" , self.move_sky_blue_counter
                    )
                else:
                    messagebox.showerror ( "Not possible" , "No path available" )
                    self.block_value_predict[1][3]['state'] = tk.NORMAL  # Fixed here
                    return

                if self.sky_blue_coin_position[int ( coin_number ) - 1] in [22 , 9 , 48 , 35 , 1 , 14 , 27]:
                    pass
                else:
                    if self.sky_blue_coin_position[int ( coin_number ) - 1] < 100:
                        self.coord_overlap ( self.sky_blue_coin_position[int ( coin_number ) - 1] , color_coin ,
                                             self.move_sky_blue_counter )

                self.sky_blue_coord_store[int ( coin_number ) - 1] = self.sky_blue_coin_position[
                    int ( coin_number ) - 1]

            else:
                messagebox.showerror ( "Wrong choice" , "Sorry, Your coin is not permitted to travel" )
                self.block_value_predict[1][3]['state'] = tk.NORMAL  # Fixed here
                return

            self.block_value_predict[1][1]['state'] = tk.NORMAL  # Fixed here

        print ( self.red_coord_store )
        print ( self.green_coord_store )
        print ( self.yellow_coord_store )
        print ( self.sky_blue_coord_store )

        permission_granted_to_proceed = True

        if color_coin == "red" and self.red_coin_position[int ( coin_number ) - 1] == 106:
            permission_granted_to_proceed = self.check_winner_and_runner ( color_coin )
        elif color_coin == "green" and self.green_coin_position[int ( coin_number ) - 1] == 106:
            permission_granted_to_proceed = self.check_winner_and_runner ( color_coin )
        elif color_coin == "yellow" and self.yellow_coin_position[int ( coin_number ) - 1] == 106:
            permission_granted_to_proceed = self.check_winner_and_runner ( color_coin )
        elif color_coin == "sky_blue" and self.sky_blue_coin_position[int ( coin_number ) - 1] == 106:
            permission_granted_to_proceed = self.check_winner_and_runner ( color_coin )

        if permission_granted_to_proceed:  # if that is False, Game is over and not proceed more
            self.make_command ( )

    def motion_of_coin(self, counter_coin, specific_coin, number_label, number_label_x, number_label_y, color_coin, path_counter):
        number_label.place(x=number_label_x, y=number_label_y)
        while True:
            if path_counter == 0:
                break
            elif (counter_coin == 51 and color_coin == "red") or (counter_coin == 12 and color_coin == "green") or (counter_coin == 25 and color_coin == "yellow") or (counter_coin == 38 and color_coin == "sky_blue") or counter_coin >= 100:
                if counter_coin < 100:
                    counter_coin = 100
                counter_coin = self.under_room_traversal_control(specific_coin, number_label, number_label_x, number_label_y, path_counter, counter_coin, color_coin)
                if counter_coin == 106:
                    messagebox.showinfo("Destination reached", "Congrats! You are now at the destination")
                    if path_counter == 6:
                        self.six_with_overlap = 1
                    else:
                        self.time_for -= 1
                break
            counter_coin += 1
            path_counter -= 1
            number_label.place_forget()
            if counter_coin <= 5:
                self.make_canvas.move(specific_coin, 40, 0)
                number_label_x += 40
            elif counter_coin == 6:
                self.make_canvas.move(specific_coin, 40, -40)
                number_label_x += 40
                number_label_y -= 40
            elif 6 < counter_coin <= 11:
                self.make_canvas.move(specific_coin, 0, -40)
                number_label_y -= 40
            elif counter_coin <= 13:
                self.make_canvas.move(specific_coin, 40, 0)
                number_label_x += 40
            elif counter_coin <= 18:
                self.make_canvas.move(specific_coin, 0, 40)
                number_label_y += 40
            elif counter_coin == 19:
                self.make_canvas.move(specific_coin, 40, 40)
                number_label_x += 40
                number_label_y += 40
            elif counter_coin <= 24:
                self.make_canvas.move(specific_coin, 40, 0)
                number_label_x += 40
            elif counter_coin <= 26:
                self.make_canvas.move(specific_coin, 0, 40)
                number_label_y += 40
            elif counter_coin <= 31:
                self.make_canvas.move(specific_coin, -40, 0)
                number_label_x -= 40
            elif counter_coin == 32:
                self.make_canvas.move(specific_coin, -40, 40)
                number_label_x -= 40
                number_label_y += 40
            elif counter_coin <= 37:
                self.make_canvas.move(specific_coin, 0, 40)
                number_label_y += 40
            elif counter_coin <= 39:
                self.make_canvas.move(specific_coin, -40, 0)
                number_label_x -= 40
            elif counter_coin <= 44:
                self.make_canvas.move(specific_coin, 0, -40)
                number_label_y -= 40
            elif counter_coin == 45:
                self.make_canvas.move(specific_coin, -40, -40)
                number_label_x -= 40
                number_label_y -= 40
            elif counter_coin <= 50:
                self.make_canvas.move(specific_coin, -40, 0)
                number_label_x -= 40
            elif counter_coin == 51:
                self.make_canvas.move(specific_coin, 0, -40)
                number_label_y -= 40
            self.window.update()
            time.sleep(0.2)
            number_label.place(x=number_label_x, y=number_label_y)
        return counter_coin

    def under_room_traversal_control(self, specific_coin, number_label, number_label_x, number_label_y, path_counter, counter_coin, color_coin):
        number_label.place(x=number_label_x, y=number_label_y)
        start_x = 100 + 240
        start_y = 15 + 240 + 40
        if color_coin == "red":
            start_x = 100 + 240
            start_y = 15 + 240 + 40
        elif color_coin == "green":
            start_x = 100 + 240 + 40
            start_y = 15 + 240
        elif color_coin == "yellow":
            start_x = 100 + 240 + 40
            start_y = 15 + 240 + 80
        elif color_coin == "sky_blue":
            start_x = 100 + 240
            start_y = 15 + 240 + 80
        for i in range(path_counter):
            if counter_coin < 106:
                counter_coin += 1
                if color_coin == "red":
                    self.make_canvas.move(specific_coin, 0, 40)
                    number_label_y += 40
                elif color_coin == "green":
                    self.make_canvas.move(specific_coin, -40, 0)
                    number_label_x -= 40
                elif color_coin == "yellow":
                    self.make_canvas.move(specific_coin, 40, 0)
                    number_label_x += 40
                elif color_coin == "sky_blue":
                    self.make_canvas.move(specific_coin, 0, -40)
                    number_label_y -= 40
                self.window.update()
                time.sleep(0.2)
                number_label.place(x=number_label_x, y=number_label_y)
        return counter_coin

    def coord_overlap(self, current_position, color_coin, path_counter):
        if color_coin == "red":
            temp_store = self.red_coord_store
        elif color_coin == "green":
            temp_store = self.green_coord_store
        elif color_coin == "yellow":
            temp_store = self.yellow_coord_store
        else:
            temp_store = self.sky_blue_coord_store

        for i in range(4):
            if color_coin != "red" and self.red_coord_store[i] == current_position and current_position not in [1, 14, 27, 40, 9, 22, 35, 48]:
                self.red_coord_store[i] = -1
                self.make_canvas.delete(self.made_red_coin[i])
                self.made_red_coin[i] = self.make_canvas.create_oval(100+40, 15+40, 100+40+40, 15+40+40, width=3, fill="red", outline="black")
                self.red_number_label[i].place(x=100+40+10, y=15+40+5)
                self.red_coin_position[i] = -1
                if path_counter == 6:
                    self.six_with_overlap = 1
                else:
                    self.time_for -= 1
            elif color_coin != "green" and self.green_coord_store[i] == current_position and current_position not in [1, 14, 27, 40, 9, 22, 35, 48]:
                self.green_coord_store[i] = -1
                self.make_canvas.delete(self.made_green_coin[i])
                self.made_green_coin[i] = self.make_canvas.create_oval(340+(40*3)+40, 15 + 40, 340+(40*3)+40 + 40, 15 + 40 + 40, width=3, fill="#00FF00", outline="black")
                self.green_number_label[i].place(x=340+(40*3)+40+10, y=15+40+5)
                self.green_coin_position[i] = -1
                if path_counter == 6:
                    self.six_with_overlap = 1
                else:
                    self.time_for -= 1
            elif color_coin != "yellow" and self.yellow_coord_store[i] == current_position and current_position not in [1, 14, 27, 40, 9, 22, 35, 48]:
                self.yellow_coord_store[i] = -1
                self.make_canvas.delete(self.made_yellow_coin[i])
                self.made_yellow_coin[i] = self.make_canvas.create_oval(340+(40*3)+40, 340+80+15, 340+(40*3)+40+40, 340+80+40+15, width=3, fill="yellow", outline="black")
                self.yellow_number_label[i].place(x=340+(40*3)+40+10, y=340+80+15+5)
                self.yellow_coin_position[i] = -1
                if path_counter == 6:
                    self.six_with_overlap = 1
                else:
                    self.time_for -= 1
            elif color_coin != "sky_blue" and self.sky_blue_coord_store[i] == current_position and current_position not in [1, 14, 27, 40, 9, 22, 35, 48]:
                self.sky_blue_coord_store[i] = -1
                self.make_canvas.delete(self.made_sky_blue_coin[i])
                self.made_sky_blue_coin[i] = self.make_canvas.create_oval(100+40, 340+80+15, 100+40+40, 340+80+40+15, width=3, fill="#04d9ff", outline="black")
                self.sky_blue_number_label[i].place(x=100+40+10, y=340+80+15+5)
                self.sky_blue_coin_position[i] = -1
                if path_counter == 6:
                    self.six_with_overlap = 1
                else:
                    self.time_for -= 1

    def check_winner_and_runner(self, color_coin):
        destination_reached = 0
        if color_coin == "red":
            temp_store = self.red_coord_store
            temp_delete = 0
        elif color_coin == "green":
            temp_store = self.green_coord_store
            temp_delete = 3
        elif color_coin == "yellow":
            temp_store = self.yellow_coord_store
            temp_delete = 2
        else:
            temp_store = self.sky_blue_coord_store
            temp_delete = 1

        for take in temp_store:
            if take == 106:
                destination_reached = 1
            else:
                destination_reached = 0
                break

        if destination_reached == 1:
            self.take_permission += 1
            if self.take_permission == 1:
                messagebox.showinfo("Winner", "Congrats! You are the winner")
            elif self.take_permission == 2:
                messagebox.showinfo("Winner", "Wow! You are 1st runner")
            elif self.take_permission == 3:
                messagebox.showinfo("Winner", "Wow! You are 2nd runner")

            self.block_value_predict[temp_delete][1]['state'] = tk.DISABLED
            self.total_people_play.remove(temp_delete)

            if len(self.total_people_play) == 1:
                messagebox.showinfo("Game Over", "Good bye!!!!")
                self.block_value_predict[0][1]['state'] = tk.DISABLED
                if not self.time_saved:
                    self.save_game_time()  # Save time when game ends
                return False
            else:
                self.time_for -= 1
        else:
            print("Winner not decided")

        return True


if __name__ == '__main__':
    window = tk.Tk()
    obj = Ludo(window, username="")
    window.mainloop()
