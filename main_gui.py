"""
Hangman with Emojis
Week 6 - GUI Prototype (Tkinter)
"""
import tkinter as tk
import random
word_list = [
    {"emoji": "📚✏️🎓", "word": "STUDENT"},
    {"emoji": "🎬🍿🎥", "word": "MOVIE"},
    {"emoji": "🏏🏃🏆", "word": "CRICKET"},
    {"emoji": "🎮🕹️🏆", "word": "GAMER"},
    {"emoji": "🚀🌕⭐", "word": "ROCKET"},
    {"emoji": "📱💬📞", "word": "MOBILE"},
    {"emoji": "💻⌨️🖱️", "word": "COMPUTER"},
    {"emoji": "🌧️☁️💧", "word": "WEATHER"},
    {"emoji": "🔥🍳👨‍🍳", "word": "COOKING"},
    {"emoji": "🎸🎵🎤", "word": "MUSICIAN"},
]
class HangmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman with Emojis")
        self.root.geometry("500x420")
        self.root.resizable(False, False)
        self.score = 0
        self.max_tries = 5
        self.hint_used = False
        self.new_round()

        tk.Label(root, text="🎯 Hangman with Emojis", font=("Arial", 18, "bold")).pack(pady=10)
        stats_frame = tk.Frame(root)
        stats_frame.pack(pady=5)

        self.score_label = tk.Label(stats_frame, text=f"Score: {self.score}", font=("Arial", 12))
        self.score_label.grid(row=0, column=0, padx=20)

        self.lives_label = tk.Label(stats_frame, text=f"Lives: {self.tries_left}", font=("Arial", 12))
        self.lives_label.grid(row=0, column=1, padx=20)

        self.emoji_label = tk.Label(root, text=self.emoji, font=("Arial", 32))
        self.emoji_label.pack(pady=10)

        self.word_label = tk.Label(root, text=self.get_display_word(), font=("Consolas", 22))
        self.word_label.pack(pady=10)

        self.message_label = tk.Label(root, text="Guess a letter to start!", font=("Arial", 11), fg="blue")
        self.message_label.pack(pady=5)

        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)

        self.guess_entry = tk.Entry(input_frame, width=5, font=("Arial", 14), justify="center")
        self.guess_entry.grid(row=0, column=0, padx=5)
        self.guess_entry.bind("<Return>", lambda event: self.check_guess())

        tk.Button(input_frame, text="Guess", command=self.check_guess, width=8).grid(row=0, column=1, padx=5)

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="💡 Hint", command=self.give_hint, width=10).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="🔄 Restart", command=self.restart_game, width=10).grid(row=0, column=1, padx=5)

    def new_round(self):
        chosen = random.choice(word_list)
        self.word = chosen["word"]
        self.emoji = chosen["emoji"]
        self.guessed_letters = []
        self.tries_left = self.max_tries
        self.hint_used = False

    def get_display_word(self):
        return " ".join(letter if letter in self.guessed_letters else "_" for letter in self.word)

    def check_guess(self):
        guess = self.guess_entry.get().upper().strip()
        self.guess_entry.delete(0, tk.END)

        if len(guess) != 1 or not guess.isalpha():
            self.message_label.config(text="Please enter a single letter.", fg="orange")
            return

        if guess in self.guessed_letters:
            self.message_label.config(text=f"You already guessed '{guess}'.", fg="orange")
            return

        self.guessed_letters.append(guess)

        if guess in self.word:
            self.message_label.config(text=f"Good guess! '{guess}' is in the word.", fg="green")
        else:
            self.tries_left -= 1
            self.message_label.config(text=f"Wrong guess. '{guess}' is not in the word.", fg="red")

        self.word_label.config(text=self.get_display_word())
        self.lives_label.config(text=f"Lives: {self.tries_left}")

        if all(letter in self.guessed_letters for letter in self.word):
            self.score += 10
            self.score_label.config(text=f"Score: {self.score}")
            self.message_label.config(text=f"🎉 YOU WIN! The word was {self.word}", fg="green")
            self.root.after(1500, self.new_round_ui)
            return

        if self.tries_left <= 0:
            self.message_label.config(text=f"💀 GAME OVER! The word was {self.word}", fg="red")
            self.root.after(1500, self.new_round_ui)

    def give_hint(self):
        if self.hint_used:
            self.message_label.config(text="Hint already used this round.", fg="orange")
            return

        unrevealed = [l for l in self.word if l not in self.guessed_letters]
        if unrevealed:
            self.guessed_letters.append(unrevealed[0])
            self.hint_used = True
            self.word_label.config(text=self.get_display_word())
            self.message_label.config(text=f"Hint: revealed '{unrevealed[0]}'", fg="purple")

    def new_round_ui(self):
        self.new_round()
        self.word_label.config(text=self.get_display_word())
        self.emoji_label.config(text=self.emoji)
        self.lives_label.config(text=f"Lives: {self.tries_left}")
        self.message_label.config(text="New word! Guess a letter.", fg="blue")

    def restart_game(self):
        self.score = 0
        self.score_label.config(text=f"Score: {self.score}")
        self.new_round_ui()

if __name__ == "__main__":
    root = tk.Tk()
    app = HangmanGUI(root)
    root.mainloop()
