import pygame
import asyncio
import platform
import random
import time
import numpy as np
import logging
import mysql.connector
import sys
from tkinter import messagebox

# Set up basic logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Pygame
pygame.init()

# Get display info for full-screen mode
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 102, 204)
GREEN = (0, 204, 102)
RED = (204, 0, 0)
DARK_GRAY = (30, 30, 30)
LIGHT_GRAY = (180, 180, 180)
GOLD = (255, 215, 0)
BACKGROUND = (20, 20, 40)
SHADOW = (15, 15, 25)

# Fonts
FONT_TITLE = pygame.font.SysFont('helvetica', 80, bold=True)
FONT = pygame.font.SysFont('helvetica', 36)
FONT_SMALL = pygame.font.SysFont('helvetica', 28)
FONT_XSMALL = pygame.font.SysFont('helvetica', 24)

# Expanded question bank (25 questions)
QUESTIONS = [
    {"question": "What is the capital of France?", "options": ["Paris", "London", "Berlin", "Madrid"],
     "answer": "Paris", "hint": "Known as the City of Light."},
    {"question": "Which planet is known as the Red Planet?", "options": ["Mars", "Jupiter", "Venus", "Mercury"],
     "answer": "Mars", "hint": "Named after a Roman god of war."},
    {"question": "What is 2 + 2?", "options": ["3", "4", "5", "6"], "answer": "4",
     "hint": "Sum of two even numbers less than 5."},
    {"question": "Who wrote 'Romeo and Juliet'?", "options": ["Shakespeare", "Dickens", "Austen", "Hemingway"],
     "answer": "Shakespeare", "hint": "An Elizabethan playwright."},
    {"question": "What is the largest ocean?", "options": ["Atlantic", "Indian", "Arctic", "Pacific"],
     "answer": "Pacific", "hint": "The largest body of water on Earth."},
    {"question": "What is the chemical symbol for Gold?", "options": ["Au", "Ag", "Fe", "Cu"], "answer": "Au",
     "hint": "Derived from the Latin word 'Aurum'."},
    {"question": "Which country hosted the 2016 Summer Olympics?", "options": ["China", "Brazil", "Japan", "UK"],
     "answer": "Brazil", "hint": "Held in Rio de Janeiro."},
    {"question": "What is the tallest mountain in the world?",
     "options": ["K2", "Kangchenjunga", "Everest", "Lhotse"], "answer": "Everest",
     "hint": "Located in the Himalayas."},
    {"question": "Who painted the Mona Lisa?", "options": ["Van Gogh", "Da Vinci", "Picasso", "Monet"],
     "answer": "Da Vinci", "hint": "A Renaissance genius."},
    {"question": "What is the smallest prime number?", "options": ["0", "1", "2", "3"], "answer": "2",
     "hint": "The only even prime number."},
    {"question": "Which gas is most abundant in Earth's atmosphere?",
     "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Helium"], "answer": "Nitrogen",
     "hint": "Makes up about 78% of the air."},
    {"question": "What is the currency of Japan?", "options": ["Yuan", "Yen", "Won", "Ringgit"], "answer": "Yen",
     "hint": "Used in the land of the rising sun."},
    {"question": "Who discovered penicillin?", "options": ["Fleming", "Pasteur", "Jenner", "Koch"],
     "answer": "Fleming", "hint": "Discovered by accident in 1928."},
    {"question": "What is the longest river in the world?",
     "options": ["Amazon", "Nile", "Yangtze", "Mississippi"], "answer": "Nile", "hint": "Flows through Egypt."},
    {"question": "Which element has the atomic number 1?",
     "options": ["Helium", "Hydrogen", "Lithium", "Beryllium"], "answer": "Hydrogen",
     "hint": "The lightest element."},
    {"question": "What is the capital of Australia?", "options": ["Sydney", "Melbourne", "Canberra", "Perth"],
     "answer": "Canberra", "hint": "A planned city."},
    {"question": "Which animal is known as the 'King of the Jungle'?",
     "options": ["Tiger", "Lion", "Elephant", "Gorilla"], "answer": "Lion", "hint": "Has a majestic mane."},
    {"question": "What is the largest planet in our solar system?",
     "options": ["Earth", "Mars", "Jupiter", "Saturn"], "answer": "Jupiter",
     "hint": "Known for its Great Red Spot."},
    {"question": "Who wrote 'Pride and Prejudice'?", "options": ["Brontë", "Austen", "Woolf", "Eliot"],
     "answer": "Austen", "hint": "A classic Regency novel."},
    {"question": "What is the speed of light in a vacuum?",
     "options": ["300,000 km/s", "150,000 km/s", "450,000 km/s", "600,000 km/s"], "answer": "300,000 km/s",
     "hint": "A universal constant."},
    {"question": "Which country is known as the Land of the Midnight Sun?",
     "options": ["Sweden", "Norway", "Finland", "Iceland"], "answer": "Norway",
     "hint": "Experiences 24-hour daylight in summer."},
    {"question": "What is the main ingredient in guacamole?", "options": ["Tomato", "Avocado", "Onion", "Pepper"],
     "answer": "Avocado", "hint": "A creamy green fruit."},
    {"question": "Which scientist proposed the theory of relativity?",
     "options": ["Newton", "Einstein", "Galileo", "Tesla"], "answer": "Einstein", "hint": "Famous for E=mc²."},
    {"question": "What is the capital of Brazil?",
     "options": ["Rio de Janeiro", "São Paulo", "Brasília", "Salvador"], "answer": "Brasília",
     "hint": "A planned capital city."},
    {"question": "Which bird is the fastest flyer?", "options": ["Eagle", "Falcon", "Hawk", "Ostrich"],
     "answer": "Falcon", "hint": "Known for its diving speed."}
]

# Sound effect (using numpy array for compatibility with Pyodide)
def create_click_sound():
    sample_rate = 44100
    duration = 0.1
    frequency = 440
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    audio = np.sin(2 * np.pi * frequency * t) * 32767
    audio = np.clip(audio, -32767, 32767).astype(np.int16)
    audio_2d = np.column_stack((audio, audio))  # Stereo
    return pygame.sndarray.make_sound(audio_2d)

CLICK_SOUND = create_click_sound()

# Game state
class QuizGame:
    def __init__(self, username=""):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("Quiz Master")
        self.clock = pygame.time.Clock()
        self.state = "start"
        self.current_question = 0
        self.score = 0
        self.start_time = time.time()  # Record start time
        self.hints_used = 0
        self.selected_option = None
        self.show_hint = False
        self.total_questions = 10
        self.randomized_questions = random.sample(QUESTIONS, self.total_questions)
        self.end_time = 0
        self.correct_answers = []
        self.username = username  # Store username for database
        self.game_name = 7  # Identifier for the game
        logging.debug("Game initialized with username: %s", self.username)

    def draw_text(self, text, font, color, x, y, center=False, max_width=None):
        try:
            if max_width:
                words = text.split(' ')
                lines = []
                current_line = []
                current_width = 0
                for word in words:
                    test_line = ' '.join(current_line + [word])
                    text_surface = font.render(test_line, True, color)
                    if text_surface.get_width() <= max_width:
                        current_line.append(word)
                        current_width = text_surface.get_width()
                    else:
                        lines.append(' '.join(current_line))
                        current_line = [word]
                lines.append(' '.join(current_line))
                for i, line in enumerate(lines):
                    text_surface = font.render(line, True, color)
                    text_rect = text_surface.get_rect()
                    if center:
                        text_rect.center = (x, y + i * font.get_height())
                    else:
                        text_rect.topleft = (x, y + i * font.get_height())
                    self.screen.blit(text_surface, text_rect)
                return len(lines) * font.get_height()
            else:
                text_surface = font.render(text, True, color)
                text_rect = text_surface.get_rect()
                if center:
                    text_rect.center = (x, y)
                else:
                    text_rect.topleft = (x, y)
                self.screen.blit(text_surface, text_rect)
                return font.get_height()
        except Exception as e:
            logging.error(f"Error in draw_text: {e}")
            return 0

    def draw_button(self, text, x, y, w, h, color, hover_color, action=None):
        try:
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            button_rect = pygame.Rect(x, y, w, h)
            # Draw shadow
            shadow_rect = pygame.Rect(x + 5, y + 5, w, h)
            pygame.draw.rect(self.screen, SHADOW, shadow_rect, border_radius=12)
            # Draw button
            if button_rect.collidepoint(mouse):
                pygame.draw.rect(self.screen, hover_color, button_rect, border_radius=12)
                if click[0] == 1 and action:
                    CLICK_SOUND.play()
                    action()
            else:
                pygame.draw.rect(self.screen, color, button_rect, border_radius=12)
            self.draw_text(text, FONT_SMALL, WHITE, x + w // 2, y + h // 2, center=True)
            return button_rect
        except Exception as e:
            logging.error(f"Error in draw_button: {e}")
            return None

    def draw_progress_bar(self, x, y, w, h, progress):
        try:
            pygame.draw.rect(self.screen, LIGHT_GRAY, (x, y, w, h), border_radius=10)
            progress_width = (w - 4) * progress
            pygame.draw.rect(self.screen, GREEN, (x + 2, y + 2, progress_width, h - 4), border_radius=8)
        except Exception as e:
            logging.error(f"Error in draw_progress_bar: {e}")

    def start_screen(self):
        try:
            self.screen.fill(BACKGROUND)
            # Gradient background
            for i in range(HEIGHT):
                color = (20, 20, 40 + int(20 * (i / HEIGHT)))
                pygame.draw.line(self.screen, color, (0, i), (WIDTH, i))
            self.draw_text("Quiz Master", FONT_TITLE, GOLD, WIDTH // 2, HEIGHT // 4, center=True)
            self.draw_text("Challenge Your Mind!", FONT, WHITE, WIDTH // 2, HEIGHT // 3, center=True)
            self.draw_button("Start Quiz", WIDTH // 2 - 200, HEIGHT // 2, 400, 80, BLUE, GREEN, self.start_quiz)
            self.draw_button("Exit", WIDTH // 2 - 200, HEIGHT // 2 + 120, 400, 80, RED, LIGHT_GRAY, self.exit_game)
        except Exception as e:
            logging.error(f"Error in start_screen: {e}")

    def start_quiz(self):
        try:
            self.state = "quiz"
            self.current_question = 0
            self.score = 0
            self.start_time = time.time()  # Reset start time when quiz starts
            self.hints_used = 0
            self.show_hint = False
            self.selected_option = None
            self.correct_answers = []
            self.randomized_questions = random.sample(QUESTIONS, self.total_questions)
            self.end_time = 0
            logging.debug("Quiz started")
        except Exception as e:
            logging.error(f"Error in start_quiz: {e}")

    def quiz_screen(self):
        try:
            self.screen.fill(BACKGROUND)
            # Gradient background
            for i in range(HEIGHT):
                color = (20, 20, 40 + int(20 * (i / HEIGHT)))
                pygame.draw.line(self.screen, color, (0, i), (WIDTH, i))

            question = self.randomized_questions[self.current_question]
            progress = (self.current_question + 1) / self.total_questions
            self.draw_progress_bar(WIDTH // 2 - 300, 50, 600, 20, progress)
            self.draw_text(f"Question {self.current_question + 1}/{self.total_questions}", FONT_SMALL, WHITE,
                           WIDTH // 2, 90, center=True)
            self.draw_text(question["question"], FONT, WHITE, WIDTH // 2, 140, center=True, max_width=WIDTH - 100)

            # Draw options
            for i, option in enumerate(question["options"]):
                y = 250 + i * 100
                color = GREEN if self.selected_option == i else BLUE
                hover_color = LIGHT_GRAY if self.selected_option == i else GREEN
                self.draw_button(option, WIDTH // 2 - 450, y, 900, 80, color, hover_color,
                                 lambda opt=i: self.select_option(opt))

            # Hint button
            self.draw_button("Show Hint", WIDTH // 2 - 150, HEIGHT - 200, 300, 60, BLUE, GREEN, self.toggle_hint)
            if self.show_hint:
                self.draw_text("AI Hint: " + question["hint"], FONT_XSMALL, LIGHT_GRAY, WIDTH // 2, HEIGHT - 120,
                               center=True, max_width=WIDTH - 100)

            # Submit button
            if self.selected_option is not None:
                self.draw_button("Submit", WIDTH // 2 - 150, HEIGHT - 60, 300, 60, BLUE, GREEN, self.submit_answer)
        except Exception as e:
            logging.error(f"Error in quiz_screen: {e}")

    def select_option(self, option):
        try:
            self.selected_option = option
        except Exception as e:
            logging.error(f"Error in select_option: {e}")

    def toggle_hint(self):
        try:
            self.show_hint = not self.show_hint
            if self.show_hint:
                self.hints_used += 1
        except Exception as e:
            logging.error(f"Error in toggle_hint: {e}")

    def submit_answer(self):
        try:
            if self.selected_option is None:
                logging.warning("No option selected")
                return
            question = self.randomized_questions[self.current_question]
            is_correct = question["options"][self.selected_option] == question["answer"]
            self.correct_answers.append(is_correct)
            if is_correct:
                self.score += 1
            self.current_question += 1
            self.selected_option = None
            self.show_hint = False
            if self.current_question >= self.total_questions:
                self.end_time = time.time()
                self.state = "results"
                logging.debug(f"Transitioning to results: score={self.score}, correct_answers={len(self.correct_answers)}")
            time.sleep(0.1)  # Brief delay to ensure state update
        except Exception as e:
            logging.error(f"Error in submit_answer: {e}")

    def results_screen(self):
        try:
            if not self.correct_answers or self.end_time == 0:
                logging.error("Results screen called with invalid state: correct_answers=%s, end_time=%s",
                              self.correct_answers, self.end_time)
                self.state = "start"  # Fallback to start screen
                return

            self.screen.fill(BACKGROUND)
            # Gradient background
            for i in range(HEIGHT):
                color = (20, 20, 40 + int(20 * (i / HEIGHT)))
                pygame.draw.line(self.screen, color, (0, i), (WIDTH, i))

            self.draw_text("Quiz Result", FONT_TITLE, GOLD, WIDTH // 2, HEIGHT // 8, center=True)

            total_questions = self.total_questions
            percentage = (self.score / total_questions) * 100 if total_questions > 0 else 0
            time_taken = int(self.end_time - self.start_time) if self.end_time > self.start_time else 0

            # Progress bar for score
            self.draw_text(f"Score: {self.score}/{total_questions} ({percentage:.1f}%)", FONT, WHITE, WIDTH // 2,
                           HEIGHT // 5, center=True)
            self.draw_progress_bar(WIDTH // 2 - 300, HEIGHT // 5 + 50, 600, 30, self.score / total_questions)

            # Detailed stats
            stats = [
                f"Correct Answers: {self.score}/{total_questions}",
                f"Percentage: {percentage:.1f}%",
                f"Hints Used: {self.hints_used}",
                f"Time Taken: {time_taken} seconds",
                f"Average Time per Question: {(time_taken / total_questions):.1f} seconds" if total_questions > 0 else "N/A"
            ]

            for i, stat in enumerate(stats):
                self.draw_text(stat, FONT, WHITE, WIDTH // 2, HEIGHT // 3 + i * 50, center=True)

            # Performance message and feedback
            if percentage >= 80:
                message = "Outstanding Performance!"
                color = GREEN
                feedback = "You're a quiz master! Keep shining!"
            elif percentage >= 50:
                message = "Great Job!"
                color = BLUE
                feedback = "Solid effort! Try for a perfect score next time!"
            else:
                message = "Keep Practicing!"
                color = RED
                feedback = "Review the questions and try again!"
            self.draw_text(message, FONT, color, WIDTH // 2, HEIGHT // 3 + 300, center=True)
            self.draw_text(feedback, FONT_XSMALL, LIGHT_GRAY, WIDTH // 2, HEIGHT // 3 + 350, center=True)

            self.draw_button("Play Again", WIDTH // 2 - 200, HEIGHT - 200, 400, 80, BLUE, GREEN, self.start_quiz)
            self.draw_button("Exit", WIDTH // 2 - 200, HEIGHT - 100, 400, 80, RED, LIGHT_GRAY, self.exit_game)
            logging.debug("Results screen rendered")
        except Exception as e:
            logging.error(f"Error in results_screen: {e}")
            self.state = "start"  # Fallback to start screen on error

    def exit_game(self):
        try:
            self.state = "exit"
            self.end_time = time.time()  # Record end time
            time_taken = int(self.end_time - self.start_time)  # Calculate time spent
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
                values = (time_taken, self.game_name, self.username)
                cursor.execute(query, values)
                conn.commit()
                cursor.close()
                conn.close()
                logging.debug(f"Played time {time_taken} seconds saved for user {self.username}")
            except mysql.connector.Error as e:
                logging.error(f"Database error: {e}")
                # Use pygame to display error message since tkinter may not work in Pyodide
                self.draw_text("Failed to save game time to database.", FONT_XSMALL, RED, WIDTH // 2, HEIGHT - 50, center=True)
                pygame.display.flip()
                time.sleep(1)  # Brief delay to show error message
            logging.debug("Exiting game")
        except Exception as e:
            logging.error(f"Error in exit_game: {e}")

    async def main(self):
        try:
            self.setup()
            while self.state != "exit":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.exit_game()  # Call exit_game to save time before quitting
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.exit_game()  # Call exit_game to save time before quitting

                if self.state == "start":
                    self.start_screen()
                elif self.state == "quiz":
                    self.quiz_screen()
                elif self.state == "results":
                    self.results_screen()

                pygame.display.flip()
                self.clock.tick(FPS)
                await asyncio.sleep(0)
        except Exception as e:
            logging.error(f"Error in main loop: {e}")
        finally:
            pygame.quit()
            logging.debug("Pygame quit")

    def setup(self):
        pass  # Initialization already handled in __init__

if platform.system() == "Emscripten":
    asyncio.ensure_future(QuizGame(username="").main())
else:
    if __name__ == "__main__":
        try:
            username = sys.argv[1] if len ( sys.argv ) > 1 else None
            if not username:
                raise ValueError ( "Username must be provided" )
            asyncio.run(QuizGame(username=username).main())
        except Exception as e:
            logging.error(f"Error running game: {e}")
