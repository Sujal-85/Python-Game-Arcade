import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk, ImageDraw
import cv2
import os
import mysql.connector
import customtkinter as ctk
from subprocess import call
from tkinter.ttk import Separator
import Ludo_game
class Game:
    def __init__(self, root1, username_lg="su12"):
        self.root = root1
        self.root.geometry("1535x780+-7+0")
        self.root.title('Exsto Gaming Platform')
        self.root.configure(bg='#121212')

        # Theme configuration
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Color palette
        self.colors = {
            'bg': '#121212',
            'card': '#1E1E1E',
            'accent': '#4A6FA5',
            'text': '#FFFFFF',
            'secondary_text': '#B0B0B0',
            'highlight': '#3A5F8A',
            'divider': '#2E2E2E'
        }

        self.userName = username_lg
        self.which_game = [0, 1, 2, 3, 4, 5, 6, 7]  # Updated game IDs
        self.profile_img_navbar = None  # For navbar (60x60)
        self.profile_img_large = None  # For profile view (200x200)
        self.load_profile_images()
        # Initialize all UI components
        self.initialize_ui()

        # Load user data if logged in
        if self.userName:
            self.load_user_data()

    def initialize_ui(self):
        self.create_header()
        self.create_main_content_area()
        self.load_all_images()
        self.create_game_cards()
        self.create_recently_played_section()
        self.create_navigation_controls()
        self.create_search_bar()

    def create_header(self):
        self.header_frame = ctk.CTkFrame(
            master=self.root,
            width=1535,
            height=110,
            fg_color=self.colors['card'],
            corner_radius=0
        )
        self.header_frame.place(x=-7, y=0)

        # Logo
        self.logo_img = ctk.CTkImage(
            light_image=Image.open("images/logo1.png"),
            size=(80, 80)
        )
        self.logo_label = ctk.CTkLabel(
            master=self.header_frame,
            image=self.logo_img,
            text=""
        )
        self.logo_label.place(x=10, y=15)

        # Title
        self.title_label = ctk.CTkLabel(
            master=self.header_frame,
            text="Exsto Gaming",
            font=('Helvetica', 32, 'bold'),
            text_color=self.colors['accent']
        )
        self.title_label.place(x=100, y=35)

    def create_main_content_area(self):
        # Create a canvas for scrollable content
        self.canvas = tk.Canvas(
            self.root,
            bg=self.colors['bg'],
            highlightthickness=0
        )
        self.canvas.place(x=-7, y=110, width=1535, height=670)

        # Add scrollbar
        self.scrollbar = tk.Scrollbar(
            self.root,
            orient=tk.VERTICAL,
            command=self.canvas.yview
        )
        self.scrollbar.place(x=1518, y=110, height=670)

        # Configure canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a frame inside the canvas for content
        self.main_frame = ctk.CTkFrame(
            master=self.canvas,
            width=1535,
            height=800,  # Increased height to accommodate all content
            fg_color=self.colors['bg'],
            corner_radius=0
        )

        # Add main_frame to canvas
        self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw")

        # Update scroll region when main_frame size changes
        self.main_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Bind mouse wheel to canvas scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def load_profile_images(self):
        """Load profile images with proper sizing"""
        try:
            if not self.userName:
                default_img = Image.open("images/profile.png") if os.path.exists(
                    "images/profile.png") else Image.new('RGBA', (60, 60), (70, 70, 70))
                self.profile_img_navbar = ctk.CTkImage(default_img, size=(60, 60))
                return

            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Suj@y935974',
                database='game'
            )
            cursor = conn.cursor()
            cursor.execute(
                f"SELECT profile_photo FROM create_account WHERE username='{self.userName}'"
            )
            profile_photo_path = cursor.fetchone()[0]
            conn.close()

            if profile_photo_path and os.path.exists(profile_photo_path):
                profile_img = Image.open(profile_photo_path)
            else:
                profile_img = Image.open("images/profile.png") if os.path.exists(
                    "images/profile.png") else Image.new('RGBA', (60, 60), (70, 70, 70))

            # Create both sized images
            self.profile_img_navbar = ctk.CTkImage(profile_img.resize((60, 60)), size=(60, 60))
            self.profile_img_large = ctk.CTkImage(profile_img.resize((200, 200)), size=(200, 200))

        except Exception as e:
            print(f"Error loading profile images: {e}")
            default_img = Image.new('RGBA', (60, 60), (70, 70, 70))
            self.profile_img_navbar = ctk.CTkImage(default_img, size=(60, 60))
            self.profile_img_large = ctk.CTkImage(default_img.resize((200, 200)), size=(200, 200))

    def load_all_images(self):
        # Game thumbnails
        self.game_images = {
            'mario': self.load_and_process_image("images/mario1.png", (310, 130)),
            'shooter': self.load_and_process_image("images/bgimg.png", (310, 130)),
            'flappy': self.load_and_process_image("images/FALPPYBIRD LOGO1.png", (310, 130)),
            'space': self.load_and_process_image("images/space invader1.png", (310, 130)),
            'tictactoe': self.load_and_process_image("images/tictactoe.png", (310, 130)),
            'ludo': self.load_and_process_image("images/Ludo.png", (310, 130)),
            '8puzzle': self.load_and_process_image("images/8 puzzle.png", (310, 130)),
            'quiz': self.load_and_process_image("images/quiz.png", (310, 130))
        }

        # Ratings (increased height)
        self.rating_images = {
            3.6: self.load_and_process_image("images/rating3.6.png", (300, 120)),
            4.3: self.load_and_process_image("images/rating 4.3.png", (300, 120)),
            4.5: self.load_and_process_image("images/rating 4.5.png", (300, 120)),
            4.8: self.load_and_process_image("images/rating 4.8.png", (300, 120))
        }

        # Icons
        self.icons = {
            'search': self.load_and_process_image("images/search.png", (30, 30)),
            'back': self.load_and_process_image("images/back1.png", (40, 40)),
            'play': self.load_and_process_image("images/play.png", (150, 60)),
            'rate': self.load_and_process_image("images/rate us.png", (40, 40)),
            'medal': self.load_and_process_image("images/medal1.png", (40, 40)),
            'star': self.load_and_process_image("images/starfill1.png", (20, 20))
        }

    def load_and_process_image(self, path, size):
        try:
            img = cv2.imread(path)
            img = cv2.resize(img, size)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            return ImageTk.PhotoImage(Image.fromarray(img))
        except:
            # Fallback to placeholder if image not found
            img = Image.new('RGB', size, (70, 70, 70))
            return ImageTk.PhotoImage(img)

    def create_game_cards(self):
        # Top Games label
        top_games_label = ctk.CTkLabel(
            master=self.main_frame,
            text="Top Games",
            font=('Helvetica', 24, 'bold'),
            text_color=self.colors['accent']
        )
        top_games_label.place(x=600, y=10)

        # Mario Card
        self.create_game_card(
            game_id=0,
            title="Mario vs Dragon",
            image=self.game_images['mario'],
            rating_image=self.rating_images[3.6],
            x_pos=15,
            y_pos=50
        )

        # Shooter Card
        self.create_game_card(
            game_id=1,
            title="Shooter Game",
            image=self.game_images['shooter'],
            rating_image=self.rating_images[4.5],
            x_pos=340,
            y_pos=50
        )

        # Flappy Bird Card
        self.create_game_card(
            game_id=2,
            title="Flappy Bird",
            image=self.game_images['flappy'],
            rating_image=self.rating_images[4.3],
            x_pos=670,
            y_pos=50
        )

        # Space Invader Card
        self.create_game_card(
            game_id=3,
            title="Space Invader",
            image=self.game_images['space'],
            rating_image=self.rating_images[4.8],
            x_pos=1010,
            y_pos=50
        )

        # Featured Games label
        featured_games_label = ctk.CTkLabel(
            master=self.main_frame,
            text="Featured Games",
            font=('Helvetica', 24, 'bold'),
            text_color=self.colors['accent']
        )
        featured_games_label.place(x=570, y=390)

        # Tic-Tac-Toe Card
        self.create_game_card(
            game_id=4,
            title="Tic Tac Toe",
            image=self.game_images['tictactoe'],
            rating_image=self.rating_images[4.8],
            x_pos=15,
            y_pos=430
        )

        # Ludo Card
        self.create_game_card(
            game_id=5,
            title="Ludo Game",
            image=self.game_images['ludo'],
            rating_image=self.rating_images[4.5],
            x_pos=340,
            y_pos=430
        )

        # 8 Puzzle Card
        self.create_game_card(
            game_id=6,
            title="8 Puzzle",
            image=self.game_images['8puzzle'],
            rating_image=self.rating_images[4.3],
            x_pos=670,
            y_pos=430
        )

        # Quiz Card
        self.create_game_card(
            game_id=7,
            title="Quiz Game",
            image=self.game_images['quiz'],
            rating_image=self.rating_images[4.5],
            x_pos=1010,
            y_pos=430
        )

    def create_game_card(self, game_id, title, image, rating_image, x_pos, y_pos):
        card_frame = ctk.CTkFrame(
            master=self.main_frame,
            width=310,
            height=330,
            fg_color=self.colors['card'],
            corner_radius=15
        )
        card_frame.place(x=x_pos, y=y_pos)

        img_label = tk.Label(
            master=card_frame,
            image=image,
            bg=self.colors['card']
        )
        img_label.place(x=5, y=5)

        title_label = ctk.CTkLabel(
            master=card_frame,
            text=title,
            font=('Helvetica', 18, 'bold'),
            text_color=self.colors['accent']
        )
        title_label.place(x=10, y=150)

        rating_label = tk.Label(
            master=card_frame,
            image=rating_image,
            bg=self.colors['card'],
            height=150
        )
        rating_label.place(x=5, y=180)

        play_btn = ctk.CTkButton(
            master=card_frame,
            text="View Details",
            width=100,
            height=30,
            fg_color=self.colors['accent'],
            hover_color=self.colors['highlight'],
            command=lambda gid=game_id: self.show_game_details(gid)
        )
        play_btn.place(x=200, y=150)

    def create_recently_played_section(self):
        self.recent_frame = ctk.CTkFrame(
            master=self.main_frame,
            width=200,
            height=600,
            fg_color=self.colors['card'],
            corner_radius=15
        )
        self.recent_frame.place(x=1330, y=20)

        recent_title = ctk.CTkLabel(
            master=self.recent_frame,
            text="Recently Played",
            font=('Helvetica', 16, 'bold'),
            text_color=self.colors['accent']
        )
        recent_title.place(x=20, y=20)

        Separator(
            master=self.recent_frame,
            orient='horizontal',
            style='TSeparator'
        ).place(x=20, y=50, width=160)

        # Default content
        self.recent_content = ctk.CTkLabel(
            master=self.recent_frame,
            text="Sign in to track your games" if not self.userName else "No recent games",
            font=('Helvetica', 12),
            text_color=self.colors['secondary_text'],
            wraplength=160
        )
        self.recent_content.place(x=20, y=80)

    def create_navigation_controls(self):
        self.login_btn = ctk.CTkButton(
            master=self.header_frame,
            text="Login",
            width=100,
            height=40,
            fg_color='transparent',
            border_color=self.colors['accent'],
            border_width=2,
            hover_color=self.colors['divider'],
            font=('Helvetica', 14, 'bold'),
            command=self.login
        )
        self.login_btn.place(x=1100, y=35)

        self.signup_btn = ctk.CTkButton(
            master=self.header_frame,
            text="Sign Up",
            width=100,
            height=40,
            fg_color=self.colors['accent'],
            hover_color=self.colors['highlight'],
            font=('Helvetica', 14, 'bold'),
            command=self.new_account
        )
        self.signup_btn.place(x=1220, y=35)

        # Profile button with user image if available
        self.profile_img_navbar = ctk.CTkImage(
            light_image=Image.open("images/profile.png"),
            size=(60, 60)
        )

        self.profile_btn = ctk.CTkButton(
            master=self.header_frame,
            text="",
            image=self.profile_img_navbar,
            width=70,
            height=70,
            fg_color='transparent',
            hover_color=self.colors['divider'],
            command=self.show_profile
        )
        self.profile_btn.place(x=1350, y=25)

    def create_search_bar(self):
        self.search_entry = ctk.CTkEntry(
            master=self.header_frame,
            width=400,
            height=40,
            placeholder_text="Search games...",
            font=('Helvetica', 14),
            corner_radius=20
        )
        self.search_entry.place(x=550, y=35)

        search_btn = ctk.CTkButton(
            master=self.header_frame,
            image=ctk.CTkImage(Image.open("images/search.png")),
            text="",
            width=40,
            height=40,
            fg_color='transparent',
            hover_color=self.colors['divider'],
            command=self.search_games
        )
        search_btn.place(x=960, y=35)

    def search_games(self):
        query = self.search_entry.get().lower()
        if not query:
            return

        # Game search mapping
        game_mapping = {
            'mario': 0,
            'dragon': 0,
            'mario vs dragon': 0,
            'shooter': 1,
            'shooter game': 1,
            'flappy': 2,
            'flappy bird': 2,
            'space': 3,
            'invader': 3,
            'space invader': 3,
            'tic': 4,
            'tic tac toe': 4,
            'ludo': 5,
            'ludo game': 5,
            '8 puzzle': 6,
            'puzzle': 6,
            'quiz':7,
            "quiz game":7,
            "Quiz": 7,
        }

        # Find matching game
        matched_game = None
        for term, game_id in game_mapping.items():
            if query in term:
                matched_game = game_id
                break

        if matched_game is not None:
            self.show_game_details(matched_game)
        else:
            messagebox.showinfo("Search", "No matching games found")

    def show_game_details(self, game_id):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        back_btn = ctk.CTkButton(
            master=self.main_frame,
            text="← Back to Games",
            font=('Helvetica', 14),
            fg_color='transparent',
            hover_color=self.colors['divider'],
            command=self.show_home_view
        )
        back_btn.place(x=20, y=20)

        # Show appropriate game details
        if game_id == 0:
            self.create_mario_details()
        elif game_id == 1:
            self.create_shooter_details()
        elif game_id == 2:
            self.create_flappy_details()
        elif game_id == 3:
            self.create_space_details()
        elif game_id == 4:
            self.create_tictactoe_details()
        elif game_id == 5:
            self.create_ludo_details()
        elif game_id == 6:
            self.create_8puzzle_details()
        elif game_id == 7:
            self.create_quiz_details()

    def create_mario_details(self):
        # Game image
        game_img = tk.Label(
            master=self.main_frame,
            image=self.game_images['mario'],
            bg=self.colors['bg']
        )
        game_img.place(x=50, y=80)

        # Game title
        title = ctk.CTkLabel(
            master=self.main_frame,
            text="Mario vs Dragon",
            font=('Helvetica', 28, 'bold'),
            text_color=self.colors['accent']
        )
        title.place(x=400, y=80)

        # Game description
        desc_frame = ctk.CTkFrame(
            master=self.main_frame,
            width=800,
            height=200,
            fg_color=self.colors['card'],
            corner_radius=10
        )
        desc_frame.place(x=400, y=130)

        desc_text = """Dragon Dodge: Mario’s Quest is a thrilling 2D arcade-style platformer inspired by Mario’s origins in Donkey Kong (1981). In this reimagined adventure, Mario faces a fire-breathing dragon in a desert kingdom filled with perilous obstacles. The player must guide Mario through three increasingly challenging levels, dodging fireballs hurled by the dragon and avoiding deadly cacti scattered across the terrain. Each level ramps up the difficulty with faster fireballs, denser cactus placements, and dynamic environmental hazards. The game ends if Mario collides with a fireball or cactus, requiring quick reflexes and strategic movement to survive. With vibrant pixel-art visuals, retro-inspired sound effects, and a progressive difficulty curve, this game tests players’ agility and determination to become a desert hero!"""

        desc_label = ctk.CTkLabel(
            master=desc_frame,
            text=desc_text,
            font=('Helvetica', 16),
            text_color=self.colors['text'],
            wraplength=780,
            justify='left'
        )
        desc_label.place(x=10, y=10)

        # Action buttons
        self.create_game_action_buttons(0, 150, 350)

    def create_shooter_details(self):
        # Game image
        game_img = tk.Label(
            master=self.main_frame,
            image=self.game_images['shooter'],
            bg=self.colors['bg']
        )
        game_img.place(x=50, y=80)

        # Game title
        title = ctk.CTkLabel(
            master=self.main_frame,
            text="Shooter Game",
            font=('Helvetica', 28, 'bold'),
            text_color=self.colors['accent']
        )
        title.place(x=400, y=80)

        # Game description
        desc_frame = ctk.CTkFrame(
            master=self.main_frame,
            width=800,
            height=200,
            fg_color=self.colors['card'],
            corner_radius=10
        )
        desc_frame.place(x=400, y=130)

        desc_text = """BattleForge: Arena of Infinite Constructs is an adrenaline-pumping 2D shooter that thrusts players into a futuristic cyberpunk world where rogue AI constructs wage war against humanity. Choose from a diverse arsenal of high-tech weapons, from precision sniper rifles to devastating shotguns, and dive into heart-pounding battles. Team up with friends in cooperative multiplayer or go solo in challenging missions across dynamic arenas. With fast-paced gameplay, strategic depth, and a variety of game modes, BattleForge offers endless excitement for both casual players and hardcore shooter fans. Survive enemy waves, outsmart opponents, and rise to the top of the leaderboards in this action-packed adventure!"""

        desc_label = ctk.CTkLabel(
            master=desc_frame,
            text=desc_text,
            font=('Helvetica', 16),
            text_color=self.colors['text'],
            wraplength=780,
            justify='left'
        )
        desc_label.place(x=10, y=10)

        # Action buttons
        self.create_game_action_buttons(1, 150, 350)

    def create_flappy_details(self):
        # Game image
        game_img = tk.Label(
            master=self.main_frame,
            image=self.game_images['flappy'],
            bg=self.colors['bg']
        )
        game_img.place(x=50, y=80)

        # Game title
        title = ctk.CTkLabel(
            master=self.main_frame,
            text="Flappy Bird",
            font=('Helvetica', 28, 'bold'),
            text_color=self.colors['accent']
        )
        title.place(x=400, y=80)

        # Game description
        desc_frame = ctk.CTkFrame(
            master=self.main_frame,
            width=800,
            height=200,
            fg_color=self.colors['card'],
            corner_radius=10
        )
        desc_frame.place(x=400, y=130)

        desc_text = """Flappy Bird: Skybound Journey is a deceptively simple yet addictive 2D arcade-style game that challenges players to guide Faby, a plucky bird, through an endless series of pipe obstacles. With a single tap, players make Faby ascend, battling gravity’s constant pull to navigate gaps in pairs of pipes set at random heights. The goal is to fly as far as possible without colliding with the pipes or ground, racking up points for each successful pass. Featuring charming pixel-art visuals, retro-inspired sound effects, and a relentless difficulty curve, this game tests patience, precision, and reflexes. Whether you’re aiming for a personal best or competing on global leaderboards, Flappy Bird delivers a timeless, frustratingly fun experience that keeps players coming back for “just one more try."""

        desc_label = ctk.CTkLabel(
            master=desc_frame,
            text=desc_text,
            font=('Helvetica', 16),
            text_color=self.colors['text'],
            wraplength=780,
            justify='left'
        )
        desc_label.place(x=10, y=10)

        # Action buttons
        self.create_game_action_buttons(2, 150, 350)

    def create_space_details(self):
        # Game image
        game_img = tk.Label(
            master=self.main_frame,
            image=self.game_images['space'],
            bg=self.colors['bg']
        )
        game_img.place(x=50, y=80)

        # Game title
        title = ctk.CTkLabel(
            master=self.main_frame,
            text="Space Invader",
            font=('Helvetica', 28, 'bold'),
            text_color=self.colors['accent']
        )
        title.place(x=400, y=80)

        # Game description
        desc_frame = ctk.CTkFrame(
            master=self.main_frame,
            width=800,
            height=200,
            fg_color=self.colors['card'],
            corner_radius=10
        )
        desc_frame.place(x=400, y=130)

        desc_text = """Space Invaders: Galactic Defense is a modern reimagining of the iconic 1978 arcade game designed by Tomohiro Nishikado. Players command a laser cannon, sliding horizontally across the bottom of the screen, to fend off waves of relentless alien invaders descending from the cosmos. The objective is to shoot down all aliens before they reach the bottom of the screen or destroy the player’s cannon. With retro-inspired pixel-art visuals, a pulsating synth soundtrack, and updated mechanics like power-ups and boss battles, this game blends nostalgic charm with modern flair. Whether playing solo to achieve a high score or competing on leaderboards, Space Invaders: Galactic Defense challenges players’ reflexes and strategy in an epic battle to save Earth from an extraterrestrial threat."""

        desc_label = ctk.CTkLabel(
            master=desc_frame,
            text=desc_text,
            font=('Helvetica', 16),
            text_color=self.colors['text'],
            wraplength=780,
            justify='left'
        )
        desc_label.place(x=10, y=10)

        # Action buttons
        self.create_game_action_buttons(3, 150, 350)

    def create_tictactoe_details(self):
        # Game image
        game_img = tk.Label(
            master=self.main_frame,
            image=self.game_images['tictactoe'],
            bg=self.colors['bg']
        )
        game_img.place(x=50, y=80)

        # Game title
        title = ctk.CTkLabel(
            master=self.main_frame,
            text="Tic Tac Toe",
            font=('Helvetica', 28, 'bold'),
            text_color=self.colors['accent']
        )
        title.place(x=400, y=80)

        # Game description
        desc_frame = ctk.CTkFrame(
            master=self.main_frame,
            width=800,
            height=200,
            fg_color=self.colors['card'],
            corner_radius=10
        )
        desc_frame.place(x=400, y=130)

        desc_text = """Tic-Tac-Toe: Ultimate Showdown is a modern reimagining of the timeless two-player classic, where players compete to place three of their symbols (X or O) in a row on a 3x3 grid, either horizontally, vertically, or diagonally. Whether facing off against a friend in local multiplayer or challenging a cunning AI with adjustable difficulty levels, this game offers quick, strategic fun for all ages. With sleek visuals, engaging sound effects, and customizable game modes, Tic-Tac-Toe: Ultimate Showdown elevates the familiar pencil-and-paper game into a digital delight. Track your wins, unlock new themes, and test your wits in this battle of strategy and foresight!"""
        desc_label = ctk.CTkLabel(
            master=desc_frame,
            text=desc_text,
            font=('Helvetica', 16),
            text_color=self.colors['text'],
            wraplength=780,
            justify='left'
        )
        desc_label.place(x=10, y=10)

        # Action buttons
        self.create_game_action_buttons(4, 150, 350)

    def create_ludo_details(self):
        # Game image
        game_img = tk.Label(
            master=self.main_frame,
            image=self.game_images['ludo'],
            bg=self.colors['bg']
        )
        game_img.place(x=50, y=80)

        # Game title
        title = ctk.CTkLabel(
            master=self.main_frame,
            text="Ludo Game",
            font=('Helvetica', 28, 'bold'),
            text_color=self.colors['accent']
        )
        title.place(x=400, y=80)

        # Game description
        desc_frame = ctk.CTkFrame(
            master=self.main_frame,
            width=800,
            height=200,
            fg_color=self.colors['card'],
            corner_radius=10
        )
        desc_frame.place(x=400, y=130)

        desc_text = """Ludo Legends: Race to Victory is a vibrant, modern take on the classic board game Ludo, where 2–4 players compete to race their four pieces from their starting yard to the safety of their home triangle. Guided by the roll of a die, players strategize to advance their pieces, capture opponents’ pieces, and block rivals’ paths, all while navigating a colorful, dynamic board. With engaging multiplayer modes, charming pixel-art visuals, and lively sound effects, this game brings friends and family together for hours of fun, strategy, and friendly rivalry. Whether playing against AI or human opponents, Ludo Legends offers a timeless blend of luck and tactics, challenging players to outmaneuver their competitors and claim victory!"""
        desc_label = ctk.CTkLabel(
            master=desc_frame,
            text=desc_text,
            font=('Helvetica', 16),
            text_color=self.colors['text'],
            wraplength=780,
            justify='left'
        )
        desc_label.place(x=10, y=10)

        # Action buttons
        self.create_game_action_buttons(5, 150, 350)

    def create_8puzzle_details(self):
        # Game image
        game_img = tk.Label(
            master=self.main_frame,
            image=self.game_images['8puzzle'],
            bg=self.colors['bg']
        )
        game_img.place(x=50, y=80)

        # Game title
        title = ctk.CTkLabel(
            master=self.main_frame,
            text="8 Puzzle",
            font=('Helvetica', 28, 'bold'),
            text_color=self.colors['accent']
        )
        title.place(x=400, y=80)

        # Game description
        desc_frame = ctk.CTkFrame(
            master=self.main_frame,
            width=800,
            height=200,
            fg_color=self.colors['card'],
            corner_radius=10
        )
        desc_frame.place(x=400, y=130)

        desc_text = """8-Puzzle: Mind Matrix is a captivating sliding puzzle game that challenges players to rearrange eight numbered tiles on a 3x3 grid to match a target configuration, using the single empty space to slide tiles strategically. Inspired by the classic sliding puzzle, this modern take adds vibrant visuals, soothing audio, and varied difficulty modes to test your problem-solving prowess. Whether you’re a beginner tackling a simple scramble or a master solving complex configurations, the game offers endless brain-teasing fun. Track your moves, beat your best times, and compete on leaderboards in this timeless logic challenge that’s easy to learn but hard to master!"""
        desc_label = ctk.CTkLabel(
            master=desc_frame,
            text=desc_text,
            font=('Helvetica', 16),
            text_color=self.colors['text'],
            wraplength=780,
            justify='left'
        )
        desc_label.place(x=10, y=10)

        # Action buttons
        self.create_game_action_buttons(6, 150, 350)

    def create_quiz_details(self):
        # Game image
        game_img = tk.Label(
            master=self.main_frame,
            image=self.game_images['quiz'],
            bg=self.colors['bg']
        )
        game_img.place(x=50, y=80)

        # Game title
        title = ctk.CTkLabel(
            master=self.main_frame,
            text="Quiz Master",
            font=('Helvetica', 28, 'bold'),
            text_color=self.colors['accent']
        )
        title.place(x=400, y=80)

        # Game description
        desc_frame = ctk.CTkFrame(
            master=self.main_frame,
            width=800,
            height=200,
            fg_color=self.colors['card'],
            corner_radius=10
        )
        desc_frame.place(x=400, y=130)

        desc_text = """Quiz Master is an engaging trivia game that tests your knowledge across various topics. Answer 10 multiple-choice questions randomly selected from a 25-question bank. Use hints to assist with tough questions and track your progress with a detailed results dashboard showing your score, time taken, and more. Challenge yourself to become the ultimate quiz master!"""

        desc_label = ctk.CTkLabel(
            master=desc_frame,
            text=desc_text,
            font=('Helvetica', 14),
            text_color=self.colors['text'],
            wraplength=780,
            justify='left'
        )
        desc_label.place(x=10, y=10)

        # Action buttons
        self.create_game_action_buttons(7, 150, 350)

    def create_game_action_buttons(self, game_id, x_pos, y_pos):
        play_btn = ctk.CTkButton(
            master=self.main_frame,
            text="PLAY NOW",
            width=200,
            height=50,
            font=('Helvetica', 18, 'bold'),
            fg_color=self.colors['accent'],
            hover_color=self.colors['highlight'],
            command=lambda: self.play_game(game_id)
        )
        play_btn.place(x=x_pos, y=y_pos)

        how_to_btn = ctk.CTkButton(
            master=self.main_frame,
            text="HOW TO PLAY",
            width=150,
            height=40,
            font=('Helvetica', 14),
            fg_color='transparent',
            border_color=self.colors['accent'],
            border_width=2,
            hover_color=self.colors['divider'],
            command=lambda: self.show_how_to_play(game_id)
        )
        how_to_btn.place(x=x_pos + 220, y=y_pos + 5)

        rate_btn = ctk.CTkButton(
            master=self.main_frame,
            text="RATE GAME",
            width=150,
            height=40,
            font=('Helvetica', 14),
            fg_color='transparent',
            border_color=self.colors['accent'],
            border_width=2,
            hover_color=self.colors['divider'],
            command=lambda: self.rate_game(game_id)
        )
        rate_btn.place(x=x_pos + 390, y=y_pos + 5)

    def show_how_to_play(self, game_id):
        """Show how to play instructions for each game"""
        if game_id == 0:
            call(['python', 'How to play/how to play mario vs dragon game.py'])
        elif game_id == 1:
            call(['python', 'How to play/how to play shooter game.py'])
        elif game_id == 2:
            call(['python', 'How to play/how to play flappy bird.py'])
        elif game_id == 3:
            call(['python', 'How to play/how to play space invader.py'])
        elif game_id == 4:
            call(['python', 'How to play/how to play tictactoe.py'])
        elif game_id == 5:
            call(['python', 'How to play/how to play ludo.py'])
        elif game_id == 6:
            call(['python', 'How to play/how to play 8puzzle.py'])
        elif game_id == 7:
            call ( ['python' , 'How to play/how to play quiz.py'] )

    def show_profile(self):
        if not self.userName:
            messagebox.showinfo("Profile", "Please login to view your profile")
            return

        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Back button
        back_btn = ctk.CTkButton(
            master=self.main_frame,
            text="← Back to Home",
            font=('Helvetica', 14),
            fg_color='transparent',
            hover_color=self.colors['divider'],
            command=self.show_home_view
        )
        back_btn.place(x=20, y=20)

        # Profile content frame with shadow effect
        profile_frame = ctk.CTkFrame(
            master=self.main_frame,
            width=1200,
            height=640,
            fg_color=self.colors['card'],
            corner_radius=15,
            border_width=0
        )
        profile_frame.place(x=210, y=40)

        # Profile header with icon
        profile_header_frame = ctk.CTkFrame(
            master=profile_frame,
            width=1160,
            height=60,
            fg_color=self.colors['highlight'],
            corner_radius=10
        )
        profile_header_frame.place(x=20, y=20)

        # Try to load profile icon or use default
        try:
            profile_icon_img = Image.open("images/profile.png")
        except:
            # Create a simple placeholder if image not found
            profile_icon_img = Image.new('RGBA', (60, 60), (70, 70, 70))
            draw = ImageDraw.Draw(profile_icon_img)
            draw.ellipse((5, 5, 25, 25), fill=(100, 200, 255))

        profile_icon = ctk.CTkImage(
            light_image=profile_icon_img,
            size=(60, 60))
        profile_icon_label = ctk.CTkLabel(
            master=profile_header_frame,
            image=profile_icon,
            text=""
        )
        profile_icon_label.place(x=15, y=2)

        # Profile title
        profile_header = ctk.CTkLabel(
            master=profile_header_frame,
            text=f"{self.userName.upper()}'S PROFILE DASHBOARD",
            font=('Helvetica', 20, 'bold'),
            text_color=self.colors['text']
        )
        profile_header.place(x=80, y=15)

        # Profile picture section
        profile_pic_frame = ctk.CTkFrame(
            master=profile_frame,
            width=250,
            height=300,
            fg_color=self.colors['bg'],
            corner_radius=15
        )
        profile_pic_frame.place(x=30, y=100)

        # Load user data from database
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Suj@y935974',
                database='game'
            )
            cursor = conn.cursor()
            cursor.execute(
                f"SELECT profile_photo, email, mobile_no FROM create_account WHERE username='{self.userName}'"
            )
            user_data = cursor.fetchone()
            conn.close()

            profile_photo_path = user_data[0] if user_data else None
            email = user_data[1] if user_data else "N/A"
            mobile_no = user_data[2] if user_data else "N/A"
            if profile_photo_path and os.path.exists(profile_photo_path):
                profile_img = Image.open(profile_photo_path)
            else:
                profile_img = Image.open("images/profile.png") if os.path.exists(
                    "images/profile.png") else Image.new('RGBA', (200, 200), (70, 70, 70))
            self.profile_pic_img = ctk.CTkImage(profile_img, size=(200, 200))

            self.profile_pic = ctk.CTkButton(
                master=profile_pic_frame,
                text="",
                image=self.profile_img_large,
                width=210,
                height=210,
                fg_color='transparent',
                hover_color=self.colors['divider'],
                command=self.upload_profile_picture
            )
            self.profile_pic.place(x=20, y=20)
        except Exception as e:
            print(f"Error loading profile data: {e}")
            profile_img = Image.new('RGBA', (200, 200), (70, 70, 70))
            email = "N/A"

        profile_img = profile_img.resize((200, 200))

        # Upload button
        upload_btn = ctk.CTkButton(
            master=profile_pic_frame,
            text="Change Photo",
            width=180,
            height=30,
            fg_color=self.colors['accent'],
            hover_color=self.colors['highlight'],
            command=self.upload_profile_picture
        )
        upload_btn.place(x=35, y=240)

        # User info section
        info_frame = ctk.CTkFrame(
            master=profile_frame,
            width=250,
            height=200,
            fg_color=self.colors['bg'],
            corner_radius=15
        )
        info_frame.place(x=30, y=420)

        # Create icon placeholders if images don't exist
        def get_icon_or_placeholder(icon_name, default_color=(255, 255, 255)):
            try:
                return Image.open(f"images/{icon_name}")
            except:
                # Create a simple colored circle as placeholder
                img = Image.new('RGBA', (20, 20), (0, 0, 0, 0))
                draw = ImageDraw.Draw(img)
                draw.ellipse((0, 0, 19, 19), fill=default_color)
                return img

        # User info labels with icons or placeholders
        user_icon = ctk.CTkImage(
            light_image=get_icon_or_placeholder("user_icon.png", (100, 200, 255)),
            size=(20, 20))
        email_icon = ctk.CTkImage(
            light_image=get_icon_or_placeholder("email_icon.png", (255, 150, 100)),
            size=(20, 20))
        Mno_icon = ctk.CTkImage(
            light_image=get_icon_or_placeholder("Mno_icon.png", (2, 150, 100)),
            size=(20, 20))

        # Username
        user_label = ctk.CTkLabel(
            master=info_frame,
            text=" Username:",
            image=user_icon,
            compound="left",
            font=('Helvetica', 14, 'bold'),
            text_color=self.colors['text']
        )
        user_label.place(x=10, y=20)

        username_value = ctk.CTkLabel(
            master=info_frame,
            text=self.userName,
            font=('Helvetica', 14),
            text_color=self.colors['secondary_text']
        )
        username_value.place(x=40, y=50)

        # Email
        email_label = ctk.CTkLabel(
            master=info_frame,
            text=" Email:",
            image=email_icon,
            compound="left",
            font=('Helvetica', 14, 'bold'),
            text_color=self.colors['text']
        )
        email_label.place(x=10, y=80)

        email_value = ctk.CTkLabel(
            master=info_frame,
            text=email,
            font=('Helvetica', 14),
            text_color=self.colors['secondary_text'],
            wraplength=200
        )
        email_value.place(x=40, y=110)

        Mno_label = ctk.CTkLabel(
            master=info_frame,
            text=" Contact No.:",
            image=Mno_icon,
            compound="left",
            font=('Helvetica', 14, 'bold'),
            text_color=self.colors['text']
        )
        Mno_label.place(x=10, y=140)

        Mno_value = ctk.CTkLabel(
            master=info_frame,
            text=mobile_no,
            font=('Helvetica', 14),
            text_color=self.colors['secondary_text'],
            wraplength=200
        )
        Mno_value.place(x=40, y=170)

        # Stats section
        stats_frame = ctk.CTkFrame(
            master=profile_frame,
            width=870,
            height=500,
            fg_color=self.colors['bg'],
            corner_radius=15
        )
        stats_frame.place(x=300, y=100)

        # Stats header
        stats_header = ctk.CTkLabel(
            master=stats_frame,
            text="GAME STATISTICS",
            font=('Helvetica', 18, 'bold'),
            text_color=self.colors['accent']
        )
        stats_header.place(x=20, y=20)

        # Load and display game statistics
        self.load_user_stats(stats_frame)

    def load_user_stats(self, stats_frame):
        """Load and display user statistics from database with better UI"""
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Suj@y935974',
                database='game'
            )
            cursor = conn.cursor()

            # Updated query to include only the first four games
            cursor.execute(
                """SELECT score_mario, score_shooter, score_flappy, score_space, 
                   rating_mario, rating_shooter, rating_flappy, rating_space
                   FROM create_account WHERE username=%s""",
                (self.userName,)
            )
            stats = cursor.fetchone()
            conn.close()

            if stats:
                # Create placeholder icons if game icons don't exist
                def get_game_icon(game_name):
                    try:
                        return ctk.CTkImage(Image.open(f"images/{game_name}.png"), size=(100, 70))
                    except:
                        # Create a simple colored square as placeholder
                        colors = {
                            'mario': (255, 100, 100),
                            'shooter': (100, 255, 100),
                            'flappy': (100, 100, 255),
                            'space': (255, 255, 100)
                        }
                        color = colors.get(game_name, (200, 200, 200))
                        img = Image.new('RGBA', (40, 40), color)
                        return ctk.CTkImage(img)

                # Game stats for the first four games
                game_stats = [
                    {
                        "name": "Mario vs Dragon",
                        "score": stats[0],
                        "rating": stats[4],
                        "icon": get_game_icon("mario1")
                    },
                    {
                        "name": "Shooter Game",
                        "score": stats[1],
                        "rating": stats[5],
                        "icon": get_game_icon("bgimg")
                    },
                    {
                        "name": "Flappy Bird",
                        "score": stats[2],
                        "rating": stats[6],
                        "icon": get_game_icon("FALPPYBIRD LOGO1")
                    },
                    {
                        "name": "Space Invader",
                        "score": stats[3],
                        "rating": stats[7],
                        "icon": get_game_icon("space invader1")
                    }
                ]

                # Create stats cards
                for i, game in enumerate(game_stats):
                    row = i // 2
                    col = i % 2
                    x_pos = 20 + (col * 430)
                    y_pos = 60 + (row * 200)

                    # Game card frame
                    card = ctk.CTkFrame(
                        master=stats_frame,
                        width=410,
                        height=180,
                        fg_color=self.colors['card'],
                        corner_radius=12
                    )
                    card.place(x=x_pos, y=y_pos)

                    # Game icon and name
                    icon_label = ctk.CTkLabel(
                        master=card,
                        image=game['icon'],
                        text=""
                    )
                    icon_label.place(x=20, y=20)

                    name_label = ctk.CTkLabel(
                        master=card,
                        text=game['name'],
                        font=('Helvetica', 16, 'bold'),
                        text_color=self.colors['accent']
                    )
                    name_label.place(x=140, y=25)

                    # Score section
                    try:
                        score_icon_img = Image.open("images/medal1.png")
                    except:
                        score_icon_img = Image.new('RGBA', (25, 25), (0, 0, 0, 0))
                        draw = ImageDraw.Draw(score_icon_img)
                        draw.text((5, 5), "S", fill=(255, 255, 255))

                    score_icon = ctk.CTkImage(
                        light_image=score_icon_img,
                        size=(25, 25))
                    score_label = ctk.CTkLabel(
                        master=card,
                        text=" High Score:",
                        image=score_icon,
                        compound="left",
                        font=('Helvetica', 14),
                        text_color=self.colors['text']
                    )
                    score_label.place(x=20, y=100)

                    score_value = ctk.CTkLabel(
                        master=card,
                        text=f"{game['score'] if game['score'] is not None else 'N/A'}",
                        font=('Helvetica', 24, 'bold'),
                        text_color=self.colors['accent']
                    )
                    score_value.place(x=50, y=130)

                    # Rating section
                    try:
                        rating_icon_img = Image.open("images/starfill1.png")
                    except:
                        rating_icon_img = Image.new('RGBA', (25, 25), (0, 0, 0, 0))
                        draw = ImageDraw.Draw(rating_icon_img)
                        draw.text((5, 5), "★", fill=(255, 215, 0))

                    rating_icon = ctk.CTkImage(
                        light_image=rating_icon_img,
                        size=(25, 25))
                    rating_label = ctk.CTkLabel(
                        master=card,
                        text=" Your Rating:",
                        image=rating_icon,
                        compound="left",
                        font=('Helvetica', 14),
                        text_color=self.colors['text']
                    )
                    rating_label.place(x=190, y=90)
                    rating_value = ctk.CTkLabel(
                        master=card,
                        text=f"{game['rating'] if game['rating'] is not None else 'N/A'}",
                        font=('Helvetica', 18, 'bold'),
                        text_color=self.colors['accent']
                    )
                    rating_value.place(x=310, y=90)

                    # Play button for each game
                    play_btn = ctk.CTkButton(
                        master=card,
                        text="PLAY NOW",
                        width=100,
                        height=30,
                        fg_color=self.colors['accent'],
                        hover_color=self.colors['highlight'],
                        command=lambda gid=i: self.play_game(gid)
                    )
                    play_btn.place(x=280, y=140)
            else:
                # Handle case where no user data is found
                error_label = ctk.CTkLabel(
                    master=stats_frame,
                    text="No game statistics available",
                    font=('Helvetica', 16),
                    text_color="#FF5555"
                )
                error_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        except Exception as e:
            print(f"Error loading user stats: {e}")
            error_label = ctk.CTkLabel(
                master=stats_frame,
                text="Failed to load game statistics",
                font=('Helvetica', 16),
                text_color="#FF5555"
            )
            error_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def load_user_data(self):
        """Load user-specific data including recent games"""
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Suj@y935974',
                database='game'
            )
            cursor = conn.cursor()

            # Get both profile photo and recent games
            cursor.execute(
                f"SELECT profile_photo, Recently_played, played_time FROM create_account WHERE username='{self.userName}'"
            )
            user_data = cursor.fetchone()

            if user_data:
                # Update profile picture
                if user_data[0] and os.path.exists(user_data[0]):
                    profile_img = Image.open(user_data[0])
                    navbar_img = profile_img.resize((60, 60))
                    self.profile_img_navbar = ctk.CTkImage(navbar_img)
                    self.profile_btn.configure(image=self.profile_img_navbar)

                # Update recently played if available
                if user_data[1] is not None:
                    self.update_recently_played(user_data[1], user_data[2])
                else:
                    # Clear recent games if none exist
                    self.recent_content.configure(text="No recent games")

            conn.close()
        except Exception as e:
            print(f"Database error: {e}")
            messagebox.showerror("Error", "Failed to load user data")

    def update_recently_played(self, game_id, play_time):
        self.game_images1 = {
            'mario': self.load_and_process_image("images/mario1.png", (200, 100)),
            'shooter': self.load_and_process_image("images/bgimg.png", (200, 100)),
            'flappy': self.load_and_process_image("images/FALPPYBIRD LOGO1.png", (200, 100)),
            'space': self.load_and_process_image("images/space invader1.png", (200, 100)),
            'tictactoe': self.load_and_process_image("images/tictactoe.png", (200, 100)),
            'ludo': self.load_and_process_image("images/ludo.png", (200, 100)),
            '8puzzle': self.load_and_process_image("images/8 puzzle.png", (200, 100)),
            'quiz': self.load_and_process_image("images/quiz.png", (200, 100))
        }
        game_info = {
            0: {"name": "Mario vs Dragon", "image": self.game_images1['mario']},
            1: {"name": "Shooter Game", "image": self.game_images1['shooter']},
            2: {"name": "Flappy Bird", "image": self.game_images1['flappy']},
            3: {"name": "Space Invader", "image": self.game_images1['space']},
            4: {"name": "Tic Tac Toe", "image": self.game_images1['tictactoe']},
            5: {"name": "Ludo Game", "image": self.game_images1['ludo']},
            6: {"name": "8 Puzzle", "image": self.game_images1['8puzzle']},
            7: {"name": "quiz", "image": self.game_images1['quiz']}
        }

        if game_id in game_info:
            # Clear default content
            self.recent_content.destroy()

            # Game title
            game_title = ctk.CTkLabel(
                master=self.recent_frame,
                text=game_info[game_id]['name'],
                font=('Helvetica', 14, 'bold'),
                text_color=self.colors['text'],
                wraplength=160
            )
            game_title.place(x=20, y=80)

            # Game image
            game_image = tk.Label(
                master=self.recent_frame,
                image=game_info[game_id]['image'],
                bg=self.colors['card'],
            )
            game_image.place(x=6, y=110)

            # Play time
            time_label = ctk.CTkLabel(
                master=self.recent_frame,
                text=f"Played: {round(play_time / 60, 1)} mins",
                font=('arial', 12, 'bold'),
                text_color=self.colors['secondary_text']
            )
            time_label.place(x=20, y=240)

    def upload_profile_picture(self):
        """Handle profile picture upload with consistent sizing"""
        if not self.userName:
            return

        file_path = filedialog.askopenfilename(
            title="Select profile picture",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
        )

        if file_path:
            try:
                # Update database
                conn = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='Suj@y935974',
                    database='game'
                )
                cursor = conn.cursor()
                cursor.execute(
                    f"UPDATE create_account SET profile_photo = %s WHERE username = %s",
                    (file_path, self.userName)
                )
                conn.commit()
                conn.close()

                # Reload profile images
                self.load_profile_images()

                # Update UI elements
                self.profile_btn.configure(image=self.profile_img_navbar)
                if hasattr(self, 'profile_pic'):  # If in profile view
                    self.profile_pic.configure(image=self.profile_img_large)

                messagebox.showinfo("Success", "Profile picture updated!")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to update profile picture: {e}")

    def play_game(self, game_id):
        if not self.userName:
            messagebox.showerror("Login Required", "Please login to play games")
            return

        if game_id == 0:
            self.root.destroy()
            new_root = tk.Tk()
            import testing
            testing.Mario(new_root, self.userName, game_id)
        elif game_id == 1:
            self.root.destroy()
            import shooter_game
            new_root = tk.Tk()
            shooter_game.Shooter(new_root, self.userName, game_id)
        elif game_id == 2:
            import game
            game.Game(self.userName, game_id)
        elif game_id == 3:
            self.root.destroy()
            new_root = tk.Tk()
            import main
            main.Space(new_root, self.userName, game_id)
        elif game_id == 4:
            call(['python', 'TicTacToe.py',self.userName])


        elif game_id == 5:  # Assuming game_id 5 is for Ludo
            new_root = tk.Toplevel ( self.root )  # Use Toplevel instead of Tk
            new_root.geometry ( "1535x780+-7+0" )
            new_root.title ( "Play Ludo with Sam" )
            new_root.iconbitmap ( "Images/ludo_icon.ico" )
            new_root.resizable ( False , False )
            Ludo_game.Ludo ( new_root , self.userName )

        elif game_id == 6:
            call(['python', 'puzzle.py', self.userName])
        elif game_id == 7:
            call(['python', 'quiz game.py', self.userName])

    def rate_game(self, game_id):
        if not self.userName:
            messagebox.showerror("Login Required", "Please login to rate games")
            return

        self.root.destroy()
        new_root = tk.Tk()
        import rateus
        rateus.Rateus(new_root, self.userName, game_id)

    def login(self):
        self.root.destroy()
        from login import LogInPage
        login_root = tk.Tk()
        LogInPage(login_root, username_lg=self.userName)
        login_root.mainloop()

    def new_account(self):
        self.root.destroy()
        new_root = tk.Tk()
        import createAccount
        createAccount.SignInPage(new_root, username_lg=self.userName)

    def show_home_view(self):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Recreate game cards
        self.create_game_cards()

        # Recreate recently played section
        self.create_recently_played_section()

        # Reload user data to refresh recent games
        if self.userName:
            self.load_user_data()

        # Ensure navbar profile icon maintains correct size
        self.profile_btn.configure(image=self.profile_img_navbar)

if __name__ == '__main__':
    root = tk.Tk()
    app = Game(root, username_lg="")
    root.mainloop()