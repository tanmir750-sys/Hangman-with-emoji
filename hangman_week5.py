import random
EASY_WORDS = [
    {"word": "MOVIE", "emoji": "🎬🍿🎥"},
    {"word": "GAMER", "emoji": "🎮🕹️🏆"},
    {"word": "MOBILE", "emoji": "📱💬📞"},
    {"word": "OCEAN", "emoji": "🌊⛵🐟"},
    {"word": "CANDY", "emoji": "🍫🍬🍭"},
]

MEDIUM_WORDS = [
    {"word": "CRICKET", "emoji": "🏏🏃🏆"},
    {"word": "COMPUTER", "emoji": "💻⌨️🖱️"},
    {"word": "WEATHER", "emoji": "🌧️☁️💧"},
]

HARD_WORDS = [
    {"word": "PHOTOGRAPHY", "emoji": "📷🌄📸"},
    {"word": "KNOWLEDGE", "emoji": "📖🧠💡"},
]
DIFFICULTY_SETTINGS = {
    "EASY":   {"words": EASY_WORDS,   "count": 5, "max_tries": 8, "hint_penalty": 3,  "word_bonus": 10},
    "MEDIUM": {"words": MEDIUM_WORDS, "count": 3, "max_tries": 6, "hint_penalty": 5,  "word_bonus": 20},
    "HARD":   {"words": HARD_WORDS,   "count": 2, "max_tries": 5, "hint_penalty": 8,  "word_bonus": 30},
}

MAX_HINTS_PER_WORD = 3
TOTAL_WORDS = 10


def show_progress(word, guessed_letters):
    """Show the word as blanks, revealing only guessed letters."""
    return " ".join(letter if letter in guessed_letters else "_" for letter in word)


def play_round(word_data, tier, settings, total_score):
    word = word_data["word"]
    emoji = word_data["emoji"]

    guessed_letters = []
    tries_left = settings["max_tries"]
    hints_used = 0

    print("-" * 45)
    print(f"[{tier}] New word! Hint emoji: {emoji}")
    print(f"Word length: {len(word)} letters | Lives: {tries_left} | Hints available: {MAX_HINTS_PER_WORD}")

    while tries_left > 0:
        print("\nWord: ", show_progress(word, guessed_letters))
        print(f"Lives: {tries_left} | Hints left: {MAX_HINTS_PER_WORD - hints_used} | Score: {total_score}")

        guess = input("Guess a letter (or type HINT): ").upper().strip()
        if guess == "HINT":
            if hints_used >= MAX_HINTS_PER_WORD:
                print("No hints left for this word!")
                continue
            unrevealed = [l for l in word if l not in guessed_letters]
            if not unrevealed:
                print("Nothing left to hint!")
                continue
            reveal = unrevealed[0]
            guessed_letters.append(reveal)
            hints_used += 1
            total_score -= settings["hint_penalty"]
            print(f"💡 Hint used! Revealed '{reveal}'. -{settings['hint_penalty']} points.")

            if all(letter in guessed_letters for letter in word):
                total_score += settings["word_bonus"]
                print(f"\n🎉 WORD COMPLETE: {word} {emoji}  (+{settings['word_bonus']} points)")
                return total_score, True
            continue
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single letter, or type HINT.")
            continue

        if guess in guessed_letters:
            print("You already guessed that letter.")
            continue

        guessed_letters.append(guess)

        if guess in word:
            print(f"Good guess! '{guess}' is in the word.")
        else:
            tries_left -= 1
            print(f"Wrong guess. '{guess}' is not in the word.")

        if all(letter in guessed_letters for letter in word):
            total_score += settings["word_bonus"]
            print(f"\n🎉 WORD COMPLETE: {word} {emoji}  (+{settings['word_bonus']} points)")
            return total_score, True
    print(f"\n💀 OUT OF LIVES! The word was: {word} {emoji}")
    return total_score, False

def play_game():
    print("=" * 45)
    print("   HANGMAN WITH EMOJIS - Week 5 Demo")
    print("   Hint System + Adaptive Difficulty")
    print("=" * 45)

    total_score = 0
    words_completed = 0

    for tier in ["EASY", "MEDIUM", "HARD"]:
        settings = DIFFICULTY_SETTINGS[tier]
        round_words = random.sample(settings["words"], settings["count"])

        print(f"\n{'#' * 45}")
        print(f"# DIFFICULTY LEVEL: {tier}  "
              f"(tries: {settings['max_tries']}, word bonus: {settings['word_bonus']})")
        print(f"{'#' * 45}")

        for word_data in round_words:
            total_score, survived = play_round(word_data, tier, settings, total_score)
            words_completed += 1
            status = "cleared" if survived else "missed"
            print(f"Progress: {words_completed}/{TOTAL_WORDS} words {status} | Total score: {total_score}")

    print("\n" + "=" * 45)
    print(f"🏆 YOU COMPLETED ALL {TOTAL_WORDS} WORDS! YOU ARE A WINNER! 🏆")
    print(f"Final Score: {total_score}")
    print("=" * 45)
if __name__ == "__main__":
    play_game()
