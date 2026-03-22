import random
from ipycanvas import Canvas
import ipywidgets as widgets
from IPython.display import display, clear_output
from mastermind_class import Game

class MastermindGUI:
    def __init__(self, difficulty):
        if difficulty == 2:
            code_length = 4
            max_attempts = 8
            self.game = Game(code_length=code_length, max_attempts=max_attempts, difficulty=difficulty)
        elif difficulty == 3:
            code_length = 5
            max_attempts = 10
            self.game = Game(code_length=code_length, max_attempts=max_attempts, difficulty=difficulty)
        else:
            self.game = Game()
        self.background_color = "lightgray"
        self.title = 'MASTERMIND'
        self.color_map = {
            "R": "red",
            "G": "green",
            "B": "blue",
            "Y": "yellow",
            "O": "orange",
            "P": "purple",
            "W": "white",
            "S": "black"
        }
        self.width = 550
        self.height = 40 * (self.game.max_attempts + 5)
        self.selected_color = None
        self.current_guess = [""] * self.game.code_length

        self.canvas = Canvas(width=self.width, height=self.height)
        self.canvas.on_mouse_down(self.handle_click)

        self.output = widgets.Output()
        self.check_button = widgets.Button(description="Prüfen")
        self.reset_button = widgets.Button(description="Neues Spiel")
        self.check_button.on_click(self.check_guess)
        self.reset_button.on_click(self.reset_game)

        self.distance = 70
        self.y_current = self.height - 100
        self.x_current = self.width/2 - ((len(self.current_guess)-1) * self.distance)/2

        self.y_palette = self.height - 50
        self.x_palette = self.width/2 - ((len(self.game.colors)-1) * self.distance)/2

        display(self.canvas, self.check_button, self.reset_button, self.output)

        self.draw_board()

    def reset_game(self, b):
        # self.game = Game()
        self.game.reset()
        self.current_guess = [""] * self.game.code_length
        self.draw_board()
        with self.output:
            clear_output()
            print("Neues Spiel gestartet!")

    def draw_board(self):
        self.canvas.clear()
        self.canvas.fill_style = self.background_color
        self.canvas.fill_rect(0, 0, self.width, self.height)
        self.canvas.font = "35px Arial"
        self.canvas.text_align = "center"
        letter_distance = 25
        position = self.width/2 - ((len(self.title)-1) * letter_distance)/2

        for i in self.title:
            self.canvas.fill_style = random.choice(list(self.color_map.values()))
            self.canvas.fill_text(i, position, 30)
            position += letter_distance

        distance = self.distance
        y_palette = self.y_palette
        x_palette = self.x_palette
        for key in self.color_map.keys():
            if key in self.game.colors:
                self.canvas.fill_style = self.color_map[key]
                self.canvas.fill_circle(x_palette, y_palette, 20)
                self.canvas.font = "20px Arial"
                self.canvas.fill_style = "black"
                self.canvas.fill_text(key, x_palette, y_palette + 35)
                x_palette += distance
            
      
        y_current = self.y_current
        x_current = self.x_current
        for color in self.current_guess:
            self.canvas.stroke_circle(x_current, y_current, 20)
            if color:
                self.canvas.fill_style = self.color_map[color]
                self.canvas.fill_circle(x_current, y_current, 18)
            x_current += distance
      
        y_offset = self.distance
        for i, (guess, result) in enumerate(self.game.history):
            x = self.width/(self.game.code_length)
            for color in guess:
                self.canvas.fill_style = self.color_map[color]
                self.canvas.fill_circle(x, y_offset + i * 40, 15)
                x += 50
            self.canvas.fill_style = "black"
            self.canvas.fill_text(
                f"✔ {result[0]} | ? {result[1]}",
                self.width-self.width/(self.game.code_length),
                y_offset + i * 40 + 10
            )

  

    def handle_click(self, x, y):

        if self.game.attempts >= self.game.max_attempts:
            return
        if self.game.game_over:
            return
            
        distance = 70

        y_palette = self.y_palette
        x_pos = self.x_palette

        for key in self.color_map:
            if (x - x_pos) ** 2 + (y - y_palette) ** 2 <= 20 ** 2:
                self.selected_color = key
                return
            x_pos += 70

       
        y_current = self.y_current
        x_pos = self.x_current

        for i in range(len(self.current_guess)):
            if (x - x_pos) ** 2 + (y - y_current) ** 2 <= 20 ** 2:
                if self.selected_color:
                    self.current_guess[i] = self.selected_color
                    self.draw_board()
                return
            x_pos += 70

    

    def check_guess(self, b):
        if "" in self.current_guess:
            with self.output:
                clear_output()
                print("Bitte alle Kreise füllen!")
            return

        result = self.game.guess(self.current_guess)

        with self.output:
            clear_output()
            if result == "win":
                print("Gewonnen!")
                print("Code war:", " ".join(self.game.secret_code))
            elif result == "lose":
                print("Verloren!")
                print("Code war:", " ".join(self.game.secret_code))
            else:
                print(f"Versuche: {self.game.attempts}/{self.game.max_attempts}")

        self.current_guess = [""] * self.game.code_length
        self.draw_board()