class ScoreManager:

    def __init__(self):
        self.score = 0
        self.streak = 0

    def correct_word(self):
        self.score += 1
        self.streak += 1

        if self.streak >= 3:
            print("🔥 Streak bonus!")

        if self.score > 10:
            self.score = 10

    def wrong_word(self):
        self.streak = 0

    def show_score(self):
         print(f"Score: {self.score}/10")