import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image
import pygame
import os
import time
import mysql.connector
import sys
class EightPuzzle:
    def __init__(self, username="Su12"):
        # Initialize pygame for sound
        pygame.mixer.init()

        # Record start time
        self.start = time.time()
        self.username = username  # Store username for database
        self.game_name = 6  # Identifier for the game

        self.window = ctk.CTk()
        self.window.title("8-Puzzle")
        self.window.geometry("1535x780+-7+0")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Bind window close event to save time to database
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Load sounds
        try:
            if os.path.exists("song/Mario Jump - QuickSounds.com.mp3"):
                self.move_sound = pygame.mixer.Sound("song/Mario Jump - QuickSounds.com.mp3")
            else:
                raise FileNotFoundError("move.wav not found")
            if os.path.exists("song/success.mp3"):
                self.win_sound = pygame.mixer.Sound("song/success.mp3")
            else:
                raise FileNotFoundError("win.wav not found")
        except FileNotFoundError as e:
            print(f"Sound file error: {e}. Sounds disabled.")
            self.move_sound = None
            self.win_sound = None

        # Load and split image
        self.tile_images = []
        self.blank_image = None
        try:
            num = random.randint(1, 3)
            if not os.path.exists(f"images/p{num}.png"):
                raise FileNotFoundError("puzzle_image.jpg not found")

            img = Image.open(f"images/p{num}.png")
            if img.size != (300, 300):
                print("Resizing puzzle_image.jpg to 300x300 pixels")
                img = img.resize((300, 300), Image.LANCZOS)
            tile_width, tile_height = 100, 100
            for i in range(3):
                for j in range(3):
                    left = j * tile_width
                    upper = i * tile_height
                    right = left + tile_width
                    lower = upper + tile_height
                    tile = img.crop((left, upper, right, lower))
                    self.tile_images.append(ctk.CTkImage(tile, size=(100, 100)))
            print("Images loaded successfully")
        except Exception as e:
            print(f"Image loading error: {e}. Using numbers instead.")
            self.tile_images = None
            self.blank_image = None

        # Initialize board (0 represents empty tile)
        self.board = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        self.solution = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        self.buttons = []
        self.number_labels = []
        self.status_label = None

        self.create_game_frame()
        self.shuffle_board()

    def on_closing(self):
        """Handle window close event to save played time to database."""
        end = time.time()
        result = int(end - self.start)  # Calculate time spent in seconds

        try:
            # Connect to MySQL database
            conn = mysql.connector.connect(
                host='localhost',
                password='Suj@y935974',
                user='root',
                database='game'
            )
            cursor = conn.cursor()
            # Update played_time and Recently_played in the database
            query = "UPDATE create_account SET played_time = %s, Recently_played = %s WHERE username = %s"
            values = (result, self.game_name, self.username)
            cursor.execute(query, values)
            conn.commit()
            cursor.close()
            conn.close()
            print(f"Played time {result} seconds saved for user {self.username}")
        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            messagebox.showerror("Database Error", "Failed to save game time to database.")

        # Quit pygame and close the window
        pygame.quit()
        self.window.destroy()

    def reset_game(self):
        """Reset the game board and UI elements."""
        self.board = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        self.shuffle_board()
        for button in self.buttons:
            button.configure(state="normal")
        for label in self.number_labels:
            label.configure(text_color="#ffffff")
        self.status_label.configure(text="Slide tiles to solve the puzzle!")

    def create_game_frame(self):
        self.game_frame = ctk.CTkFrame(self.window)
        self.game_frame.pack(expand=True, fill="both")

        # Title
        title_label = ctk.CTkLabel(
            self.game_frame,
            text="8-Puzzle",
            font=("Roboto", 36, "bold"),
            text_color="#ffffff"
        )
        title_label.place(relx=0.5, rely=0.1, anchor="center")

        # Status label
        self.status_label = ctk.CTkLabel(
            self.game_frame,
            text="Slide tiles to solve the puzzle!",
            font=("Roboto", 20),
            text_color="#ffffff"
        )
        self.status_label.place(relx=0.5, rely=0.18, anchor="center")

        # Grid
        grid_frame = ctk.CTkFrame(self.game_frame, fg_color="#1e1e2e")
        grid_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.buttons = []
        self.number_labels = []
        for i in range(3):
            for j in range(3):
                idx = i * 3 + j
                image = (self.tile_images[self.board[idx] - 1] if self.tile_images and self.board[idx] != 0 else
                         self.blank_image if self.tile_images and self.board[idx] == 0 else None)
                text = "" if self.tile_images else str(self.board[idx]) if self.board[idx] != 0 else ""
                button = ctk.CTkButton(
                    grid_frame,
                    text=text,
                    image=image,
                    width=100,
                    height=100,
                    font=("Roboto", 30),
                    corner_radius=10,
                    fg_color="#2a2a3a",
                    hover_color="#3b82f6",
                    command=lambda idx=idx: self.button_click(idx)
                )
                button.grid(row=i * 2, column=j, padx=5, pady=(5, 2))
                if self.board[idx] == 0:
                    button.configure(state="disabled", hover_color="#2a2a3a")
                self.buttons.append(button)

                label = ctk.CTkLabel(
                    grid_frame,
                    text=str(self.board[idx]) if self.board[idx] != 0 else "",
                    font=("Roboto", 12),
                    text_color="#ffffff"
                )
                label.grid(row=i * 2 + 1, column=j, padx=5, pady=(0, 5))
                self.number_labels.append(label)

        # Reset button
        reset_button = ctk.CTkButton(
            self.game_frame,
            text="Reset Puzzle",
            command=self.reset_game,
            width=250,
            height=50,
            font=("Roboto", 18),
            corner_radius=15,
            fg_color="#3b82f6",
            hover_color="#2563eb"
        )
        reset_button.place(relx=0.5, rely=0.85, anchor="center")

    def shuffle_board(self):
        """Shuffle the board with valid moves to ensure solvability."""
        for _ in range(1000):
            empty_index = self.board.index(0)
            neighbors = self.get_valid_moves(empty_index)
            if neighbors:
                move_index = random.choice(neighbors)
                self.board[empty_index], self.board[move_index] = self.board[move_index], self.board[empty_index]
        self.update_board()

    def get_valid_moves(self, empty_index):
        """Get valid moves for the empty tile."""
        row, col = empty_index // 3, empty_index % 3
        moves = []
        if row > 0:
            moves.append(empty_index - 3)  # Up
        if row < 2:
            moves.append(empty_index + 3)  # Down
        if col > 0:
            moves.append(empty_index - 1)  # Left
        if col < 2:
            moves.append(empty_index + 1)  # Right
        return moves

    def button_click(self, index):
        """Handle button click to move a tile."""
        empty_index = self.board.index(0)
        if index in self.get_valid_moves(empty_index):
            self.board[empty_index], self.board[index] = self.board[index], self.board[empty_index]
            self.update_board()
            if self.move_sound:
                self.move_sound.play()
            if self.board == self.solution:
                self.status_label.configure(text="Puzzle Solved!")
                messagebox.showinfo("Congratulations", "You solved the puzzle!")
                if self.win_sound:
                    self.win_sound.play()
                self.disable_buttons()

    def update_board(self):
        """Update the UI to reflect the current board state."""
        for i in range(9):
            image = (self.tile_images[self.board[i] - 1] if self.tile_images and self.board[i] != 0 else
                     self.blank_image if self.tile_images and self.board[i] == 0 else None)
            text = "" if self.tile_images else str(self.board[i]) if self.board[i] != 0 else ""
            self.buttons[i].configure(
                text=text,
                image=image,
                fg_color="#2a2a3a",
                hover_color="#3b82f6",
                state="normal" if self.board[i] != 0 else "disabled"
            )
            if self.board[i] == 0:
                self.buttons[i].configure(hover_color="#2a2a3a")
            self.number_labels[i].configure(
                text=str(self.board[i]) if self.board[i] != 0 else ""
            )
        self.status_label.configure(text="Slide tiles to solve the puzzle!")

    def disable_buttons(self):
        """Disable all buttons when the puzzle is solved."""
        for button in self.buttons:
            button.configure(
                state="disabled",
                fg_color="#4b4b5b",
                hover_color="#4b4b5b"
            )
        for label in self.number_labels:
            label.configure(text_color="#888888")

    def run(self):
        """Start the main event loop."""
        self.window.mainloop()

if __name__ == "__main__":
    username = sys.argv[1] if len(sys.argv) > 1 else None
    if not username:
        raise ValueError("Username must be provided")
    game = EightPuzzle(username=username)
    game.run()