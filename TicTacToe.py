import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import random
import mysql.connector
import time
import logging
import sys
# Set up basic logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class TicTacToe:
    def __init__(self,  window=None, username=""):
        self.window = window if window else ctk.CTk()
        self.window.title("Tic-Tac-Toe")
        self.window.geometry("1535x780+-7+0")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.window.configure(fg_color="#1e1e2e")
        # self.game_id = game_id
        self.current_player = "X"
        self.board = [""] * 9
        self.buttons = []
        self.play_with_computer = False
        self.difficulty = "Beginner"
        self.initial_frame = None
        self.difficulty_frame = None
        self.game_frame = None

        # Initialize timing variables
        self.start_time = time.time()  # Record start time
        self.end_time = 0
        self.username = username if username else "guest"  # Default to "guest" if empty
        self.game_name = 4  # Identifier for the game
        self.time_saved = False  # Flag to prevent multiple saves
        logging.debug("TicTacToe game initialized with username: %s", self.username)

        # Bind window close event to save time
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.create_initial_frame()

    def on_closing(self):
        """Handle window close event to save game time."""
        self.save_game_time()
        self.window.destroy()

    def save_game_time(self):
        """Save the time spent playing to the database."""
        if self.time_saved:
            return  # Prevent multiple saves
        try:
            self.end_time = time.time()  # Record end time
            time_taken = int(self.end_time - self.start_time)  # Calculate time spent
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

    def create_initial_frame(self):
        self.initial_frame = ctk.CTkFrame(self.window, fg_color="#1e1e2e")
        self.initial_frame.pack(expand=True)

        username_label = ctk.CTkLabel(
            self.initial_frame,
            text=f"Welcome {self.username} to Tic Tac Toe",
            font=("Bodoni MT", 50),
            text_color="#4A6FA5"
        )
        username_label.pack(pady=20)

        title_label = ctk.CTkLabel(self.initial_frame, text="Tic-Tac-Toe", font=("Arial Black", 30))
        title_label.pack(pady=20)

        player_button = ctk.CTkButton(
            self.initial_frame,
            text="Play with Player",
            command=lambda: self.start_toss(False),
            width=250,
            height=60,
            font=("Forte", 20)
        )
        player_button.pack(pady=20)

        computer_button = ctk.CTkButton(
            self.initial_frame,
            text="Play with Computer",
            command=self.show_difficulty_frame,
            width=250,
            height=60,
            font=("Forte", 20)
        )
        computer_button.pack(pady=20)

        back_button = ctk.CTkButton(
            self.initial_frame,
            text="Back to Home",
            command=self.return_to_main_menu,
            width=250,
            height=60,
            font=("Forte", 20),
            fg_color="#4A6FA5",
            hover_color="#3A5F8A"
        )
        back_button.pack(pady=20)

    def show_difficulty_frame(self):
        self.initial_frame.destroy()
        self.difficulty_frame = ctk.CTkFrame(self.window, fg_color="#1e1e2e")
        self.difficulty_frame.pack(expand=True)

        username_label = ctk.CTkLabel(
            self.difficulty_frame,
            text=f"Welcome, {self.username}!",
            font=("Bodoni MT", 40),
            text_color="#4A6FA5"
        )
        username_label.pack(pady=20)

        title_label = ctk.CTkLabel(self.difficulty_frame, text="Select Difficulty", font=("Forte", 30))
        title_label.pack(pady=20)

        beginner_button = ctk.CTkButton(
            self.difficulty_frame,
            text="Beginner",
            command=lambda: self.start_toss_with_difficulty("Beginner"),
            width=250,
            height=50,
            font=("Forte", 18)
        )
        beginner_button.pack(pady=15)

        intermediate_button = ctk.CTkButton(
            self.difficulty_frame,
            text="Intermediate",
            command=lambda: self.start_toss_with_difficulty("Intermediate"),
            width=250,
            height=50,
            font=("Forte", 18)
        )
        intermediate_button.pack(pady=15)

        hard_button = ctk.CTkButton(
            self.difficulty_frame,
            text="Hard",
            command=lambda: self.start_toss_with_difficulty("Hard"),
            width=250,
            height=50,
            font=("Forte", 18)
        )
        hard_button.pack(pady=15)

        back_button = ctk.CTkButton(
            self.difficulty_frame,
            text="Back to Menu",
            command=self.return_to_menu,
            width=250,
            height=50,
            font=("Forte", 18),
            fg_color="#4A6FA5",
            hover_color="#3A5F8A"
        )
        back_button.pack(pady=15)

    def create_game_frame(self):
        self.game_frame = ctk.CTkFrame(self.window, fg_color="#1e1e2e")
        self.game_frame.pack(expand=True)

        username_label = ctk.CTkLabel(
            self.game_frame,
            text=f"Welcome {self.username} to Tic Tac Toe",
            font=("Bodoni MT", 40),
            text_color="#4A6FA5"
        )
        username_label.pack(pady=20)

        title_label = ctk.CTkLabel(self.game_frame, text="Tic-Tac-Toe", font=("Arial Black", 30))
        title_label.pack(pady=20)

        grid_frame = ctk.CTkFrame(self.game_frame)
        grid_frame.pack(pady=20)

        self.buttons = []
        for i in range(3):
            for j in range(3):
                button = ctk.CTkButton(
                    grid_frame,
                    text="",
                    width=150,
                    height=150,
                    font=("Arial", 50),
                    command=lambda idx=i*3+j: self.button_click(idx)
                )
                button.grid(row=i, column=j, padx=10, pady=10)
                self.buttons.append(button)

        reset_button = ctk.CTkButton(
            self.game_frame,
            text="Reset Game",
            command=self.reset_game,
            width=250,
            height=50,
            font=("Arial", 18)
        )
        reset_button.pack(pady=10)

        back_button = ctk.CTkButton(
            self.game_frame,
            text="Back to Menu",
            command=self.return_to_main_menu,
            width=250,
            height=50,
            font=("Arial", 18),
            fg_color="#4A6FA5",
            hover_color="#3A5F8A"
        )
        back_button.pack(pady=10)

    def start_toss_with_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.play_with_computer = True
        self.difficulty_frame.destroy()
        self.toss()

    def start_toss(self, with_computer):
        self.play_with_computer = with_computer
        self.initial_frame.destroy()
        self.toss()

    def toss(self):
        toss_result = random.choice(["X", "O"])
        self.current_player = toss_result
        messagebox.showinfo("Toss Result", f"Player {toss_result} goes first!")
        self.create_game_frame()
        if self.play_with_computer and self.current_player == "O":
            self.computer_move()

    def button_click(self, index):
        if self.board[index] == "":
            self.board[index] = self.current_player
            self.buttons[index].configure(text=self.current_player)
            if self.check_winner():
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.disable_buttons()
                self.save_game_time()  # Save time on game over
            elif "" not in self.board:
                messagebox.showinfo("Game Over", "It's a tie!")
                self.disable_buttons()
                self.save_game_time()  # Save time on game over
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                if self.play_with_computer and self.current_player == "O":
                    self.computer_move()

    def computer_move(self):
        if self.difficulty == "Beginner":
            self.computer_move_beginner()
        elif self.difficulty == "Intermediate":
            self.computer_move_intermediate()
        else:
            self.computer_move_hard()

        if self.check_winner():
            messagebox.showinfo("Game Over", "Computer wins!")
            self.disable_buttons()
            self.save_game_time()  # Save time on game over
        elif "" not in self.board:
            messagebox.showinfo("Game Over", "It's a tie!")
            self.disable_buttons()
            self.save_game_time()  # Save time on game over
        else:
            self.current_player = "X"

    def computer_move_beginner(self):
        empty_cells = [i for i, cell in enumerate(self.board) if cell == ""]
        if empty_cells:
            index = random.choice(empty_cells)
            self.board[index] = "O"
            self.buttons[index].configure(text="O")

    def computer_move_intermediate(self):
        empty_cells = [i for i, cell in enumerate(self.board) if cell == ""]
        if empty_cells:
            for i in empty_cells:
                self.board[i] = "O"
                if self.check_winner():
                    self.buttons[i].configure(text="O")
                    return
                self.board[i] = ""
            for i in empty_cells:
                self.board[i] = "X"
                if self.check_winner():
                    self.board[i] = "O"
                    self.buttons[i].configure(text="O")
                    return
                self.board[i] = ""
            for i in empty_cells:
                self.board[i] = "O"
                win_possibilities = 0
                for j in [k for k in empty_cells if k != i]:
                    self.board[j] = "O"
                    if self.check_winner():
                        win_possibilities += 1
                    self.board[j] = ""
                if win_possibilities >= 2:
                    self.board[i] = "O"
                    self.buttons[i].configure(text="O")
                    return
                self.board[i] = ""
            for i in empty_cells:
                self.board[i] = "X"
                win_possibilities = 0
                for j in [k for k in empty_cells if k != i]:
                    self.board[j] = "X"
                    if self.check_winner():
                        win_possibilities += 1
                    self.board[j] = ""
                if win_possibilities >= 2:
                    self.board[i] = "O"
                    self.buttons[i].configure(text="O")
                    return
                self.board[i] = ""
            center = 4
            corners = [0, 2, 6, 8]
            edges = [1, 3, 5, 7]
            if center in empty_cells:
                self.board[center] = "O"
                self.buttons[center].configure(text="O")
            elif any(c in empty_cells for c in corners):
                corner = random.choice([c for c in corners if self.board[c] == ""])
                self.board[corner] = "O"
                self.buttons[corner].configure(text="O")
            else:
                edge = random.choice([e for e in edges if self.board[e] == ""])
                self.board[edge] = "O"
                self.buttons[edge].configure(text="O")

    def computer_move_hard(self):
        best_score = -float("inf")
        best_move = None
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "O"
                score = self.minimax(self.board, 0, False, -float("inf"), float("inf"))
                self.board[i] = ""
                if score > best_score:
                    best_score = score
                    best_move = i
                elif score == best_score and random.random() < 0.1:
                    best_move = i
        if best_move is not None:
            self.board[best_move] = "O"
            self.buttons[best_move].configure(text="O")

    def minimax(self, board, depth, is_maximizing, alpha, beta):
        winner = self.check_winner_symbol()
        if winner == "O":
            return 10 - depth
        elif winner == "X":
            return depth - 10
        if "" not in board:
            return 0

        if is_maximizing:
            best_score = -float("inf")
            for i in range(9):
                if board[i] == "":
                    board[i] = "O"
                    score = self.minimax(board, depth + 1, False, alpha, beta)
                    board[i] = ""
                    best_score = max(score, best_score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
            return best_score
        else:
            best_score = float("inf")
            for i in range(9):
                if board[i] == "":
                    board[i] = "X"
                    score = self.minimax(board, depth + 1, True, alpha, beta)
                    board[i] = ""
                    best_score = min(score, best_score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
            return best_score

    def check_winner(self):
        return self.check_winner_symbol() is not None

    def check_winner_symbol(self):
        for i in range(0, 9, 3):
            if self.board[i] == self.board[i+1] == self.board[i+2] != "":
                return self.board[i]
        for i in range(3):
            if self.board[i] == self.board[i+3] == self.board[i+6] != "":
                return self.board[i]
        if self.board[0] == self.board[4] == self.board[8] != "":
            return self.board[0]
        if self.board[2] == self.board[4] == self.board[6] != "":
            return self.board[2]
        return None

    def disable_buttons(self):
        for button in self.buttons:
            button.configure(state="disabled")

    def reset_game(self):
        self.board = [""] * 9
        self.current_player = "X"
        self.play_with_computer = False
        self.difficulty = "Beginner"
        for button in self.buttons:
            button.configure(text="", state="normal")
        self.game_frame.destroy()
        self.create_initial_frame()
        self.start_time = time.time()  # Reset start time for new session
        self.time_saved = False  # Allow saving time for new session

    def return_to_main_menu(self):
        self.save_game_time()
        self.window.destroy()

    def return_to_menu(self):
        self.save_game_time()
        for widget in self.window.winfo_children():
            widget.destroy()
        self.create_initial_frame()
        self.start_time = time.time()  # Reset start time for new session
        self.time_saved = False  # Allow saving time for new session

    def run(self):
        if not self.window.winfo_exists():
            return
        self.window.mainloop()

if __name__ == "__main__":
    username = sys.argv[1] if len ( sys.argv ) > 1 else None
    if not username:
        raise ValueError ( "Username must be provided" )
    game = TicTacToe(username=username)
    game.run()