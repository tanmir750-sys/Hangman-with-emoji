"""Hangman with Emojis Core Game Logic (CLI Version) a simple terminal-based Hangman game """
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
        {"emoji": "📷🌄📸", "word": "PHOTOGRAPHY"},
        {"emoji": "🏃💪🥇", "word": "ATHLETE"},
        {"emoji": "👑🏰⚔️", "word": "KINGDOM"},
        {"emoji": "🌍✈️🧳", "word": "TRAVELER"},
        {"emoji": "🚗🛣️⛽", "word": "DRIVING"},
        {"emoji": "🏥💉👨‍⚕️", "word": "DOCTOR"},
        {"emoji": "⚖️📜🏛️", "word": "JUSTICE"},
        {"emoji": "🌳🌱💧", "word": "NATURE"},
        {"emoji": "🎨🖌️🖼️", "word": "ARTIST"},
        {"emoji": "🔍🕵️📄", "word": "DETECTIVE"},
        {"emoji": "📖🧠💡", "word": "KNOWLEDGE"},
        {"emoji": "🏠🏗️🔨", "word": "BUILDING"},
        {"emoji": "🍔🍟🥤", "word": "FASTFOOD"},
        {"emoji": "📚🏫📝", "word": "HOMEWORK"},
        {"emoji": "🚓🚨👮", "word": "POLICE"},
        {"emoji": "🧪🔬⚗️", "word": "SCIENCE"},
        {"emoji": "🎭🎬⭐", "word": "ACTOR"},
        {"emoji": "📺🎤📰", "word": "REPORTER"},
        {"emoji": "🌙⭐🌌", "word": "GALAXY"},
        {"emoji": "⚡🔋🚗", "word": "ELECTRIC"},
        {"emoji": "🗺️📍🌍", "word": "JOURNEY"},
        {"emoji": "🏟️⚽🥅", "word": "FOOTBALL"},
        {"emoji": "🍫🍬🍭", "word": "CANDY"},
        {"emoji": "🛒🏬💳", "word": "SHOPPING"},
        {"emoji": "🎹🎼🎵", "word": "PIANIST"},
        {"emoji": "🐘🌿🌳", "word": "WILDLIFE"},
        {"emoji": "✉️📬📨", "word": "MESSAGE"},
        {"emoji": "🏆🥇🎖️", "word": "CHAMPION"},
        {"emoji": "🎤🎶🎧", "word": "SINGER"},
        {"emoji": "🧑‍💻💻☕", "word": "CODING"},
        {"emoji": "📡🛰️🌍", "word": "NETWORK"},
        {"emoji": "🕰️⏳⌛", "word": "TIMING"},
        {"emoji": "🚲🏞️🌤️", "word": "CYCLING"},
        {"emoji": "🍎🥗💪", "word": "HEALTHY"},
        {"emoji": "🌋🔥🌍", "word": "VOLCANO"},
        {"emoji": "🎓📖🏫", "word": "EDUCATION"},
        {"emoji": "🔐💻🛡️", "word": "SECURITY"},
        {"emoji": "🎂🎉🎁", "word": "BIRTHDAY"},
        {"emoji": "🌊⛵🐟", "word": "OCEAN"},
        {"emoji": "💰🏦📈", "word": "BANKING"}]
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
        guess = input("Guess a letter: ").upper().strip()

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
            print(f"YOU WIN! The word was: {word} {emoji}")
            print("=" * 40)
            return
    print(f"GAME OVER! The word was: {word} {emoji}")
    print("=" * 40)

if __name__ == "__main__":
    play_game()
