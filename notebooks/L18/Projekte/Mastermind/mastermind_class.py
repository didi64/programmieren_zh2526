import random


class Game:
    def __init__(self, code_length=4, max_attempts=10, difficulty=1):
        self.colors = ["R", "G", "B", "Y", "O", "P", "W", "S"]
        self.code_length = code_length
        self.max_attempts = max_attempts
        self.difficulty = difficulty
        self.reset()


    def reset(self):
        if self.difficulty == 1:
            self.colors = ["R", "G", "B", "Y", "O", "P"]
        elif self.difficulty == 2:
            self.colors = ["R", "G", "B", "Y", "O", "P", "W", "S"]
        elif self.difficulty == 3:
            self.colors = ["R", "G", "B", "Y", "O", "P", "W", "S"]
        self.secret_code = [random.choice(self.colors) for _ in range(self.code_length)]
        self.attempts = 0
        self.history = []
        self.game_over = False

    def guess(self, guess):
        if self.game_over:
            return None

        correct_position = 0
        correct_color = 0

        secret_copy = []
        guess_copy = []

        for i in range(len(guess)):
            if guess[i] == self.secret_code[i]:
                correct_position += 1
            else:
                secret_copy.append(self.secret_code[i])
                guess_copy.append(guess[i])

        for color in guess_copy:
            if color in secret_copy:
                correct_color += 1
                secret_copy.remove(color)
        

        self.attempts += 1
        self.history.append((guess, (correct_position, correct_color)))

        if correct_position == self.code_length:
            self.game_over = True
            return "win"

        if self.attempts >= self.max_attempts:
            self.game_over = True
            return "lose"

        return correct_position, correct_color, secret_copy, guess_copy, self.secret_code, guess

game = Game()
print(game.guess(game.secret_code))