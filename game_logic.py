"""                    Hangman with Emojis
Core Game Logic (CLI Version) a simple terminal-based Hangman game """
import random
word_list = [
    {"emoji": "📚", "word": "books"},
    {"emoji": "🍿", "word": "popcorn"},
    {"emoji": "🚀", "word": "rocket"},
    {"emoji": "📱", "word": "mobile"},
    {"emoji": "💪", "word": "strong"},
    {"emoji": "⚔️", "word": "swords"},
    {"emoji": "🌍️", "word": "plane"},
    {"emoji": "🚗", "word": "car"},
    {"emoji": "💉️", "word": "injection"},
    {"emoji": "⚖️", "word": "law"},
    {"emoji": "⭐", "word": "star"},
    {"emoji": "📰", "word": "newspaper"},
    {"emoji": "✉️", "word": "mail"},
    {"emoji": "🏆", "word": "trophy"},
    {"emoji": "🎧", "word": "headset",},
    {"emoji": "🎂", "word": "cake"},
    {"emoji": "🎁", "word": "gift"},
]
def choose_word():
    return random.choice(word_list)

def show_progress(word, guessed_letters):
    display = ""
    for letter in word:
        if letter in guessed_letters:
            display += letter + " "
        else:
            display += "_ "
    return display.strip()
def play_game():
    chosen = choose_word()
    word = chosen["word"]
    emoji = chosen["emoji"]
    guessed_letters = []
    max_tries = 6
    tries_left = max_tries

    print("WELCOME TO HANGMAN WITH EMOJIS")
    print("=" * 40)
    print(f"\nHint emoji: {emoji}")
    print(f"The word has {len(word)} letters.\n")
    while tries_left > 0:
        print("Word: ", show_progress(word, guessed_letters))
        print(f"Tries left: {tries_left}")
        guess = input("Guess a letter: ").lower().strip()

        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single letter.\n")
            continue

        if guess in guessed_letters:
            print("You already guessed that letter.\n")
            continue
        guessed_letters.append(guess)

        if guess in word:
            print(f"Good guess! '{guess}' is in the word.\n")
        else:
            tries_left -= 1
            print(f"Wrong guess. '{guess}' is not in the word.\n")

        if all(letter in guessed_letters for letter in word):

            print(f"YOU WIN! The word was: {emoji} {word} ")
            print("=" * 40)
            return
    print(f"GAME OVER! The word was:  {emoji} {word}")
    print("=" * 40)
if __name__ == "__main__":
    play_game()