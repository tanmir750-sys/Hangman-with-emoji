import random
from score_manager import ScoreManager

word_list = [
    {"emoji": "📚✏️🎓", "word": "STUDENT", "difficulty": "Easy"},
    {"emoji": "🎬🍿🎥", "word": "MOVIE", "difficulty": "Easy"},
    {"emoji": "🏏🏃🏆", "word": "CRICKET", "difficulty": "Hard"},
    {"emoji": "🎮🕹️🏆", "word": "GAMER", "difficulty": "Medium"},
    {"emoji": "🚀🌕⭐", "word": "ROCKET", "difficulty": "Medium"},
    {"emoji": "📱💬📞", "word": "MOBILE", "difficulty": "Easy"},
    {"emoji": "💻⌨️🖱️", "word": "COMPUTER", "difficulty": "Easy"},
    {"emoji": "🌧️☁️💧", "word": "WEATHER", "difficulty": "Medium"},
    {"emoji": "🔥🍳👨‍🍳", "word": "COOKING", "difficulty": "Hard"},
    {"emoji": "🎸🎵🎤", "word": "MUSIC", "difficulty": "Easy"},
    {"emoji": "📷🌄📸", "word": "PHOTOGRAPHY", "difficulty": "Hard"},
    {"emoji": "🏃💪🥇", "word": "ATHLETE", "difficulty": "Easy"},
    {"emoji": "👑🏰⚔️", "word": "KINGDOM", "difficulty": "Medium"},
    {"emoji": "🌍✈️🧳", "word": "TRAVELER", "difficulty": "Medium"},
    {"emoji": "🚗🛣️⛽", "word": "DRIVING", "difficulty": "Medium"},
    {"emoji": "🏥💉👨‍⚕️", "word": "DOCTOR", "difficulty": "Medium"},
    {"emoji": "⚖️📜🏛️", "word": "JUSTICE", "difficulty": "Medium"},
    {"emoji": "🌳🌱💧", "word": "NATURE", "difficulty": "Easy"},
    {"emoji": "🎨🖌️🖼️", "word": "ARTIST", "difficulty": "Medium"},
    {"emoji": "🔍🕵️📄", "word": "DETECTIVE", "difficulty": "Medium"},
    {"emoji": "📖🧠💡", "word": "KNOWLEDGE", "difficulty": "Medium"},
    {"emoji": "🏠🏗️🔨", "word": "BUILDING", "difficulty": "Medium"},
    {"emoji": "🍔🍟🥤", "word": "FASTFOOD", "difficulty": "Easy"},
    {"emoji": "📚🏫📝", "word": "HOMEWORK", "difficulty": "Easy"},
    {"emoji": "🚓🚨👮", "word": "POLICE", "difficulty": "Easy"},
    {"emoji": "🧪🔬⚗️", "word": "SCIENCE", "difficulty": "Hard"},
    {"emoji": "🎭🎬⭐", "word": "ACTOR", "difficulty": "Medium"},
    {"emoji": "📺🎤📰", "word": "REPORTER", "difficulty": "Medium"},
    {"emoji": "🌙⭐🌌", "word": "GALAXY", "difficulty": "Medium"},
    {"emoji": "⚡🔋🚗", "word": "ELECTRIC", "difficulty": "Hard"},
    {"emoji": "🗺️📍🌍", "word": "JOURNEY", "difficulty": "Medium"},
    {"emoji": "🏟️⚽🥅", "word": "FOOTBALL", "difficulty": "Medium"},
    {"emoji": "🍫🍬🍭", "word": "CANDY", "difficulty": "Easy"},
    {"emoji": "🛒🏬💳", "word": "SHOPPING", "difficulty": "Medium"},
    {"emoji": "🎹🎼🎵", "word": "PIANIST", "difficulty": "Medium"},
    {"emoji": "🐘🌿🌳", "word": "WILDLIFE", "difficulty": "Medium"},
    {"emoji": "✉️📬📨", "word": "MESSAGE", "difficulty": "Medium"},
    {"emoji": "🏆🥇🎖️", "word": "CHAMPION", "difficulty": "Medium"},
    {"emoji": "🎤🎶🎧", "word": "SINGER", "difficulty": "Hard"},
    {"emoji": "🧑‍💻💻☕", "word": "CODING", "difficulty": "Hard"},
    {"emoji": "📡🛰️🌍", "word": "NETWORK", "difficulty": "Hard"},
    {"emoji": "🕰️⏳⌛", "word": "TIMING", "difficulty": "Medium"},
    {"emoji": "🚲🏞️🌤️", "word": "CYCLING", "difficulty": "Hard"},
    {"emoji": "🍎🥗💪", "word": "HEALTHY", "difficulty": "Hard"},
    {"emoji": "🌋🔥🌍", "word": "VOLCANO", "difficulty": "Medium"},
    {"emoji": "🎓📖🏫", "word": "EDUCATION", "difficulty": "Medium"},
    {"emoji": "🔐💻🛡️", "word": "SECURITY", "difficulty": "Hard"},
    {"emoji": "🎂🎉🎁", "word": "BIRTHDAY", "difficulty": "Medium"},
    {"emoji": "🌊⛵🐟", "word": "OCEAN", "difficulty": "Medium"},
    {"emoji": "💰🏦📈", "word": "BANKING", "difficulty": "Hard"}
]


def show_progress(word, guessed_letters):
    display = ""

    for letter in word:
        if letter in guessed_letters:
            display += letter + " "
        else:
            display += "_ "

    return display.strip()


def get_words(difficulty, number):
    """Get random words from a specific difficulty."""

    available_words = [
        item for item in word_list
        if item["difficulty"] == difficulty
    ]

    random.shuffle(available_words)

    return available_words[:number]


def play_word(chosen_word, score_manager, lives):

    word = chosen_word["word"]
    emoji = chosen_word["emoji"]
    difficulty = chosen_word["difficulty"]

    guessed_letters = []

    print("\n" + "=" * 40)
    print(f"Difficulty: {difficulty}")
    print(f"Emoji Hint: {emoji}")
    print(f"The word has {len(word)} letters.")
    print("=" * 40)

    while lives > 0:

        print("\nWord:", show_progress(word, guessed_letters))
        print(f"❤️ Lives left: {lives}")
        print(f"⭐ Score: {score_manager.score}/10")

        guess = input("Guess a letter: ").upper().strip()

        if len(guess) != 1 or not guess.isalpha():
            print("Please enter only ONE letter.")
            continue
            
        if guess in guessed_letters:
            print("You already guessed that letter.")
            continue

        guessed_letters.append(guess)
        
        if guess in word:
            print(f"✅ Good guess! '{guess}' is correct.")

        else:
            lives -= 1
            print(f"❌ Wrong guess! '{guess}' is not in the word.")

        if all(letter in guessed_letters for letter in word):

            print("\n🎉 CORRECT!")
            print(f"The word was: {word}")

            score_manager.correct_word()

            print(f"⭐ You earned 1 point!")
            print(f"⭐ Current Score: {score_manager.score}/10")

            return lives, True

    print("\n💀 No lives left!")
    print(f"The word was: {word}")

    return lives, False


def play_game():

    score_manager = ScoreManager()
    lives = 5

    print("\n" + "=" * 45)
    print("       WELCOME TO HANGMAN WITH EMOJIS")
    print("=" * 45)
    print("\nGAME RULES")
    print("❤️ You have 5 wrong guesses in total.")
    print("🟢 Easy Level   = 5 words")
    print("🟡 Medium Level = 3 words")
    print("🔴 Hard Level   = 2 words")
    print("⭐ 10 points = WINNER")
    print("=" * 45)

    print("\n🟢 EASY LEVEL STARTED!")

    easy_words = get_words("Easy", 5)

    for chosen_word in easy_words:

        lives, success = play_word(
            chosen_word,
            score_manager,
            lives
        )
        if not success:
            print("\nGAME OVER!")
            print(f"Final Score: {score_manager.score}/10")
            return

    print("\n🎉 EASY LEVEL COMPLETED!")

    print("\n🟡 MEDIUM LEVEL STARTED!")

    medium_words = get_words("Medium", 3)

    for chosen_word in medium_words:

        lives, success = play_word(
            chosen_word,
            score_manager,
            lives
        )
        if not success:
            print("\nGAME OVER!")
            print(f"Final Score: {score_manager.score}/10")
            return

    print("\n🎉 MEDIUM LEVEL COMPLETED!")

    print("\n🔴 HARD LEVEL STARTED!")

    hard_words = get_words("Hard", 2)

    for chosen_word in hard_words:

        lives, success = play_word(
            chosen_word,
            score_manager,
            lives
        )

        if not success:
            print("\nGAME OVER!")
            print(f"Final Score: {score_manager.score}/10")
            return

    print("\n" + "=" * 45)
    print("🏆 CONGRATULATIONS!")
    print("🏆 YOU COMPLETED ALL 10 WORDS!")
    print(f"⭐ FINAL SCORE: {score_manager.score}/10")
    print("🎉 YOU ARE THE WINNER!")
    print("=" * 45)

if __name__ == "__main__":
    play_game()
