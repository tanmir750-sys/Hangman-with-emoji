import tkinter as tk
import random
import json
import sys
import os
EMOJI_DATA_JSON = r"""
{
  "easy": [
    {"emoji": "📚✏️🎓", "word": "STUDENT"},
    {"emoji": "🎬🍿🎥", "word": "MOVIE"},
    {"emoji": "🏏🏃🏆", "word": "CRICKET"},
    {"emoji": "🎮🕹️🏆", "word": "GAMER"},
    {"emoji": "🚀🌕⭐", "word": "ROCKET"},
    {"emoji": "📱💬📞", "word": "MOBILE"},
    {"emoji": "🌧️☁️💧", "word": "WEATHER"},
    {"emoji": "🏃💪🥇", "word": "ATHLETE"},
    {"emoji": "👑🏰⚔️", "word": "KINGDOM"},
    {"emoji": "🚗🛣️⛽", "word": "DRIVING"},
    {"emoji": "🌳🌱💧", "word": "NATURE"},
    {"emoji": "🎨🖌️🖼️", "word": "ARTIST"},
    {"emoji": "🍔🍟🥤", "word": "FASTFOOD"},
    {"emoji": "🚓🚨👮", "word": "POLICE"},
    {"emoji": "🎭🎬⭐", "word": "ACTOR"},
    {"emoji": "🌙⭐🌌", "word": "GALAXY"},
    {"emoji": "🍫🍬🍭", "word": "CANDY"},
    {"emoji": "🎹🎼🎵", "word": "PIANIST"},
    {"emoji": "🎤🎶🎧", "word": "SINGER"},
    {"emoji": "🕰️⏳⌛", "word": "TIMING"},
    {"emoji": "🍎🥗💪", "word": "HEALTHY"},
    {"emoji": "🎂🎉🎁", "word": "BIRTHDAY"},
    {"emoji": "🌊⛵🐟", "word": "OCEAN"},
    {"emoji": "💰🏦📈", "word": "BANKING"},
    {"emoji": "🎓📖🏫", "word": "EDUCATION"}
  ],
  "medium": [
    {"emoji": "💻⌨️🖱️", "word": "COMPUTER"},
    {"emoji": "🔥🍳👨‍🍳", "word": "COOKING"},
    {"emoji": "🎸🎵🎤", "word": "MUSICIAN"},
    {"emoji": "🌍✈️🧳", "word": "TRAVELER"},
    {"emoji": "🏥💉👨‍⚕️", "word": "DOCTOR"},
    {"emoji": "⚖️📜🏛️", "word": "JUSTICE"},
    {"emoji": "🔍🕵️📄", "word": "DETECTIVE"},
    {"emoji": "🏠🏗️🔨", "word": "BUILDING"},
    {"emoji": "📚🏫📝", "word": "HOMEWORK"},
    {"emoji": "🧪🔬⚗️", "word": "SCIENCE"},
    {"emoji": "📺🎤📰", "word": "REPORTER"},
    {"emoji": "⚡🔋🚗", "word": "ELECTRIC"},
    {"emoji": "🗺️📍🌍", "word": "JOURNEY"},
    {"emoji": "🏟️⚽🥅", "word": "FOOTBALL"},
    {"emoji": "🛒🏬💳", "word": "SHOPPING"},
    {"emoji": "🐘🌿🌳", "word": "WILDLIFE"},
    {"emoji": "✉️📬📨", "word": "MESSAGE"},
    {"emoji": "🏆🥇🎖️", "word": "CHAMPION"},
    {"emoji": "📡🛰️🌍", "word": "NETWORK"},
    {"emoji": "🚲🏞️🌤️", "word": "CYCLING"},
    {"emoji": "🌋🔥🌍", "word": "VOLCANO"},
    {"emoji": "🎬🍿🎥", "word": "CINEMA"},
    {"emoji": "🎯🎪🎨", "word": "CARNIVAL"}
  ],
  "hard": [
    {"emoji": "📷🌄📸", "word": "PHOTOGRAPHY"},
    {"emoji": "📖🧠💡", "word": "KNOWLEDGE"},
    {"emoji": "🧑‍💻💻☕", "word": "PROGRAMMING"},
    {"emoji": "🔐💻🛡️", "word": "CYBERSECURITY"},
    {"emoji": "🎓📖🏫", "word": "UNIVERSITY"},
    {"emoji": "🌌🔭🪐", "word": "ASTRONOMY"},
    {"emoji": "🧬🔬🧪", "word": "BIOTECHNOLOGY"},
    {"emoji": "🏛️⚖️📜", "word": "CONSTITUTION"},
    {"emoji": "🌍🌡️🌊", "word": "ENVIRONMENT"},
    {"emoji": "💊🧪🏥", "word": "PHARMACEUTICAL"}
  ]
}
"""
try:
    WORD_DATA = json.loads(EMOJI_DATA_JSON)
except json.JSONDecodeError as e:
    print(f"ERROR: Embedded JSON is invalid: {e}")
    sys.exit(1)

DIFFICULTY_PLAN = [("Easy", 5), ("Medium", 3), ("Hard", 2)]
TOTAL_WORDS_TO_WIN = sum(q for _, q in DIFFICULTY_PLAN)

BG_MAIN       = "#0F172A"
BG_CARD       = "#4c4672"
BG_INPUT      = "#334155"

TEXT_PRIMARY   = "#F1F5F9"
TEXT_SECONDARY = "#94A3B8"
TEXT_MUTED     = "#94A3B8"

ACCENT_PRIMARY   = "#3B82F6"
ACCENT_PRIMARY_H = "#2563EB"
ACCENT_SUCCESS   = "#10B981"
ACCENT_SUCCESS_H = "#059669"
ACCENT_WARNING   = "#F59E0B"
ACCENT_DANGER    = "#EF4444"
ACCENT_HINT      = "#8B5CF6"
ACCENT_GOLD      = "#FBBF24"

FB_SUCCESS = "#064E3B"
FB_DANGER  = "#7F1D1D"
FB_INFO    = "#1E3A8A"
FB_HINT    = "#4C1D95"

FONT_MENU_TITLE  = ("Segoe UI", 30, "bold")
FONT_MENU_SUB    = ("Segoe UI", 12)
FONT_MENU_BTN    = ("Segoe UI", 14, "bold")
FONT_MENU_FOOT   = ("Segoe UI", 9)

FONT_HDR_TITLE   = ("Segoe UI", 18, "bold")
FONT_STAT_LABEL  = ("Segoe UI", 9)
FONT_STAT_VALUE  = ("Segoe UI", 14, "bold")
FONT_EMOJI       = ("Segoe UI Emoji", 36)
FONT_WORD        = ("Consolas", 26, "bold")
FONT_MSG         = ("Segoe UI", 11)
FONT_BTN         = ("Segoe UI", 10, "bold")
FONT_WIN_TITLE   = ("Segoe UI", 26, "bold")
FONT_WIN_SUB     = ("Segoe UI", 13)

class HangmanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Emoji Hangman — CSE 2216")
        self.root.geometry("600x720")
        self.root.configure(bg=BG_MAIN)
        self.root.resizable(False, False)
        self.show_menu()

    def clear_root(self):
        for w in self.root.winfo_children():
            w.destroy()

    def make_button(self, parent, text, command,
                    bg=ACCENT_PRIMARY, hover=ACCENT_PRIMARY_H,
                    fg=TEXT_PRIMARY, font=FONT_BTN, padx=14, pady=8):
        btn = tk.Button(parent, text=text, command=command,
                        font=font, bg=bg, fg=fg,
                        activebackground=hover, activeforeground=fg,
                        relief="flat", bd=0, padx=padx, pady=pady,
                        cursor="hand2", highlightthickness=0)
        btn.bind("<Enter>", lambda e: btn.config(bg=hover))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
        return btn

    def make_card(self, parent, **kwargs):
        return tk.Frame(parent, bg=BG_CARD, highlightbackground="#334155",
                        highlightthickness=1, **kwargs)

    def show_menu(self):
        self.clear_root()
        self.root.configure(bg=BG_MAIN)
        self.root.geometry("600x720")

        header = self.make_card(self.root)
        header.pack(pady=(50, 15), padx=40, fill="x")

        tk.Label(header, text="EMOJI HANGMAN", font=FONT_MENU_TITLE,
                 bg=BG_CARD, fg=TEXT_PRIMARY).pack(pady=(24, 4))
        tk.Label(header, text="Software Development I — CSE 2216",
                 font=FONT_MENU_SUB, bg=BG_CARD, fg=TEXT_SECONDARY).pack(pady=(0, 24))

        info = self.make_card(self.root)
        info.pack(pady=(0, 20), padx=40, fill="x")

        tk.Label(info, text="GAME PROGRESSION", font=("Segoe UI", 10, "bold"),
                 bg=BG_CARD, fg=ACCENT_PRIMARY).pack(pady=(16, 8))

        steps = [
            ("LEVEL 1", "Easy",   "5 words", ACCENT_SUCCESS),
            ("LEVEL 2", "Medium", "3 words", ACCENT_WARNING),
            ("LEVEL 3", "Hard",   "2 words", ACCENT_DANGER),
        ]
        for tag, name, quota, color in steps:
            row = tk.Frame(info, bg=BG_CARD)
            row.pack(pady=3, padx=20, fill="x")
            tk.Label(row, text=tag, font=("Segoe UI", 9, "bold"),
                     bg=BG_CARD, fg=color, width=9, anchor="w").pack(side="left")
            tk.Label(row, text=name, font=("Segoe UI", 10, "bold"),
                     bg=BG_CARD, fg=TEXT_PRIMARY, width=9, anchor="w").pack(side="left")
            tk.Label(row, text=quota, font=("Segoe UI", 10),
                     bg=BG_CARD, fg=TEXT_SECONDARY, anchor="w").pack(side="left")

        tk.Label(info, text="Win all 10 words to become the Champion",
                 font=("Segoe UI", 9, "italic"),
                 bg=BG_CARD, fg=ACCENT_GOLD).pack(pady=(10, 16))

        self.make_button(self.root, "START GAME", self.start_game,
                         bg=ACCENT_SUCCESS, hover=ACCENT_SUCCESS_H,
                         font=FONT_MENU_BTN, padx=20, pady=14).pack(
                         fill="x", padx=110, pady=(0, 10))

        self.make_button(self.root, "Exit", self.root.destroy,
                         bg="#475569", hover="#334155",
                         font=FONT_MENU_BTN, padx=20, pady=12).pack(
                         fill="x", padx=110)

        tk.Label(self.root,
                 text="Northern University of Business & Technology, Khulna",
                 font=FONT_MENU_FOOT, bg=BG_MAIN, fg=TEXT_MUTED).pack(
                 side="bottom", pady=16)

    def start_game(self):
        self.clear_root()
        self.root.configure(bg=BG_MAIN)
        self.root.geometry("600x720")

        self.score = 0
        self.max_tries = 5
        self.tries_left = self.max_tries
        self.game_over = False

        self.difficulty_index = 0
        self.words_won_in_level = 0
        self.total_words_won = 0
        self.used_words = set()
        self.hint_used = False

        self.new_round()

        # Top bar
        top = self.make_card(self.root)
        top.pack(pady=(15, 8), padx=20, fill="x")

        tk.Label(top, text="EMOJI HANGMAN", font=FONT_HDR_TITLE,
                 bg=BG_CARD, fg=TEXT_PRIMARY).pack(side="left", padx=16, pady=12)

        self.level_label = tk.Label(top, text="", font=("Segoe UI", 10, "bold"),
                                    bg=BG_CARD, fg=ACCENT_PRIMARY)
        self.level_label.pack(side="right", padx=16)

        # Stats row
        stats = tk.Frame(self.root, bg=BG_MAIN)
        stats.pack(pady=6, padx=20, fill="x")
        stats.columnconfigure(0, weight=1)
        stats.columnconfigure(1, weight=1)
        stats.columnconfigure(2, weight=1)

        self.score_label = self._stat_tile(stats, 0, "SCORE", "0", ACCENT_SUCCESS)
        self.hearts_label = self._stat_tile(stats, 1, "LIVES", "", ACCENT_DANGER)
        self.won_label   = self._stat_tile(stats, 2, "WORDS WON", "0/10", ACCENT_WARNING)

        self.puzzle_card = self.make_card(self.root)
        self.puzzle_card.pack(pady=12, padx=20, fill="x")
        self.puzzle_card.configure(highlightbackground="#334155")

        self.emoji_label = tk.Label(self.puzzle_card, text=self.emoji,
                                    font=FONT_EMOJI, bg=BG_CARD, fg=TEXT_PRIMARY)
        self.emoji_label.pack(pady=(22, 6))

        self.word_label = tk.Label(self.puzzle_card, text=self.get_display_word(),
                                   font=FONT_WORD, bg=BG_CARD, fg=TEXT_PRIMARY)
        self.word_label.pack(pady=(4, 22))

        fb = tk.Frame(self.root, bg=BG_MAIN)
        fb.pack(pady=6, padx=20, fill="x")

        self.reaction_label = tk.Label(fb, text="", font=("Segoe UI", 18),
                                       bg=BG_MAIN, fg=TEXT_PRIMARY)
        self.reaction_label.pack(side="left", padx=(4, 6))

        self.message_label = tk.Label(fb, text="Enter a letter to begin",
                                      font=FONT_MSG, bg=BG_MAIN, fg=TEXT_SECONDARY)
        self.message_label.pack(side="left")

        inp = self.make_card(self.root)
        inp.pack(pady=12, padx=20, fill="x")

        inner = tk.Frame(inp, bg=BG_CARD)
        inner.pack(pady=14, padx=14)

        tk.Label(inner, text="Your guess:", font=("Segoe UI", 10),
                 bg=BG_CARD, fg=TEXT_SECONDARY).pack(side="left", padx=(0, 8))

        self.guess_entry = tk.Entry(inner, width=4, font=("Segoe UI", 16, "bold"),
                                    justify="center", relief="flat", bd=0,
                                    bg=BG_INPUT, fg=TEXT_PRIMARY,
                                    insertbackground=TEXT_PRIMARY,
                                    highlightthickness=1,
                                    highlightbackground="#475569",
                                    highlightcolor=ACCENT_PRIMARY)
        self.guess_entry.pack(side="left", ipady=6)
        self.guess_entry.bind("<Return>", lambda e: self.check_guess())

        self.make_button(inner, "GUESS", self.check_guess,
                         bg=ACCENT_PRIMARY, hover=ACCENT_PRIMARY_H,
                         padx=18, pady=8).pack(side="left", padx=(10, 0))

        actions = tk.Frame(self.root, bg=BG_MAIN)
        actions.pack(pady=(0, 14), padx=20, fill="x")

        self.make_button(actions, "Hint", self.give_hint,
                         bg=ACCENT_HINT, hover="#7C3AED").pack(
                         side="left", expand=True, fill="x", padx=4)
        self.make_button(actions, "Restart", self.restart_game,
                         bg="#475569", hover="#334155").pack(
                         side="left", expand=True, fill="x", padx=4)
        self.make_button(actions, "Menu", self.show_menu,
                         bg="#475569", hover="#334155").pack(
                         side="left", expand=True, fill="x", padx=4)

        self.update_level_label()
        self.update_stats()
        self.guess_entry.focus()

    def _stat_tile(self, parent, col, label, value, color):
        tile = tk.Frame(parent, bg=BG_CARD, highlightbackground="#334155",
                        highlightthickness=1)
        tile.grid(row=0, column=col, padx=5, sticky="nsew")
        tk.Label(tile, text=label, font=FONT_STAT_LABEL,
                 bg=BG_CARD, fg=TEXT_MUTED).pack(pady=(10, 0))
        val = tk.Label(tile, text=value, font=FONT_STAT_VALUE,
                       bg=BG_CARD, fg=color)
        val.pack(pady=(0, 10))
        return val

    def current_level_name(self):
        return DIFFICULTY_PLAN[self.difficulty_index][0]

    def current_level_quota(self):
        return DIFFICULTY_PLAN[self.difficulty_index][1]

    def update_level_label(self):
        name = self.current_level_name()
        quota = self.current_level_quota()
        self.level_label.config(text=f"{name.upper()}  •  {self.words_won_in_level}/{quota}")

    def update_stats(self):
        self.score_label.config(text=str(self.score))
        self.hearts_label.config(text=self.hearts_text())
        self.won_label.config(text=f"{self.total_words_won}/{TOTAL_WORDS_TO_WIN}")

    def hearts_text(self):
        return "♥ " * self.tries_left + "♡ " * (self.max_tries - self.tries_left)

    def new_round(self):
        key = self.current_level_name().lower()
        pool = WORD_DATA.get(key, [])
        available = [w for w in pool if w["word"] not in self.used_words]
        if not available:
            self.used_words = {w for w in self.used_words
                               if w not in [x["word"] for x in pool]}
            available = pool
        chosen = random.choice(available)
        self.word = chosen["word"]
        self.emoji = chosen["emoji"]
        self.used_words.add(self.word)
        self.guessed_letters = []
        self.hint_used = False

    def get_display_word(self):
        return " ".join(l if l in self.guessed_letters else "_" for l in self.word)

    def check_guess(self):
        if self.game_over:
            self.set_message("Game is over. Press Restart to play again.", ACCENT_DANGER, "✕")
            return

        guess = self.guess_entry.get().upper().strip()
        self.guess_entry.delete(0, tk.END)

        if len(guess) != 1 or not guess.isalpha():
            self.set_message("Please enter a single letter.", ACCENT_WARNING, "!")
            return

        if guess in self.guessed_letters:
            self.set_message(f"Already guessed '{guess}'.", ACCENT_WARNING, "!")
            return

        self.guessed_letters.append(guess)

        if guess in self.word:
            self.set_message(f"'{guess}' is in the word.", ACCENT_SUCCESS, "✓")
            self.flash(FB_SUCCESS)
            self.root.bell()
        else:
            self.tries_left -= 1
            self.set_message(f"'{guess}' is not in the word.", ACCENT_DANGER, "✕")
            self.flash(FB_DANGER)
            self.root.bell()

        self.word_label.config(text=self.get_display_word())
        self.update_stats()

        if all(l in self.guessed_letters for l in self.word):
            self.score += 10
            self.words_won_in_level += 1
            self.total_words_won += 1
            self.update_stats()
            self.set_message(f"Correct! The word was {self.word}", ACCENT_SUCCESS, "★")
            self.flash(FB_SUCCESS)

            if self.total_words_won >= TOTAL_WORDS_TO_WIN:
                self.root.after(1200, self.show_victory_screen)
                return

            if self.words_won_in_level >= self.current_level_quota():
                if self.difficulty_index < len(DIFFICULTY_PLAN) - 1:
                    self.difficulty_index += 1
                    self.words_won_in_level = 0
                    self.root.after(1200, self.announce_level_up)
                    return

            self.root.after(1400, self.new_round_ui)
            return
        if self.tries_left <= 0:
            self.game_over = True
            self.set_message(f"Game over. The word was {self.word}.", ACCENT_DANGER, "✕")
            self.flash(FB_DANGER)

    def announce_level_up(self):
        self.update_level_label()
        self.update_stats()
        self.set_message(f"Level up! Now on {self.current_level_name()}.", ACCENT_SUCCESS, "▲")
        self.flash(FB_SUCCESS)
        self.root.after(1300, self.new_round_ui)

    def give_hint(self):
        if self.game_over:
            self.set_message("Game is over. Press Restart to play again.", ACCENT_DANGER, "✕")
            return

        if self.hint_used:
            self.set_message("Hint already used this round.", ACCENT_WARNING, "!")
            return

        unrevealed = [l for l in self.word if l not in self.guessed_letters]
        if unrevealed:
            self.guessed_letters.append(unrevealed[0])
            self.hint_used = True
            self.score -= 10
            self.word_label.config(text=self.get_display_word())
            self.update_stats()
            self.set_message(f"Hint: revealed '{unrevealed[0]}'  (−10)", ACCENT_HINT, "?")
            self.flash(FB_HINT)

            if all(l in self.guessed_letters for l in self.word):
                self.score += 10
                self.words_won_in_level += 1
                self.total_words_won += 1
                self.update_stats()
                self.set_message(f"Correct! The word was {self.word}", ACCENT_SUCCESS, "★")
                self.flash(FB_SUCCESS)

                if self.total_words_won >= TOTAL_WORDS_TO_WIN:
                    self.root.after(1200, self.show_victory_screen)
                    return

                if self.words_won_in_level >= self.current_level_quota():
                    if self.difficulty_index < len(DIFFICULTY_PLAN) - 1:
                        self.difficulty_index += 1
                        self.words_won_in_level = 0
                        self.root.after(1200, self.announce_level_up)
                        return

                self.root.after(1400, self.new_round_ui)

    def new_round_ui(self):
        self.new_round()
        self.word_label.config(text=self.get_display_word())
        self.emoji_label.config(text=self.emoji)
        self.update_level_label()
        self.update_stats()
        self.set_message("New word. Enter a letter.", ACCENT_PRIMARY, "")
        self.guess_entry.focus()

    def restart_game(self):
        self.start_game()

    def set_message(self, text, color, icon):
        self.message_label.config(text=text, fg=color)
        self.reaction_label.config(text=icon, fg=color)

    def flash(self, target_bg, steps=14, delay=30):
        def step(i):
            if i > steps * 2:
                self.puzzle_card.config(bg=BG_CARD)
                self.emoji_label.config(bg=BG_CARD)
                self.word_label.config(bg=BG_CARD)
                return
            if i <= steps:
                ratio = i / steps
                color = self._blend(target_bg, BG_CARD, ratio)
            else:
                ratio = (i - steps) / steps
                color = self._blend(BG_CARD, target_bg, ratio)
            self.puzzle_card.config(bg=color)
            self.emoji_label.config(bg=color)
            self.word_label.config(bg=color)
            self.root.after(delay, lambda: step(i + 1))
        step(0)

    @staticmethod
    def _hex_to_rgb(h):
        h = h.lstrip("#")
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

    @staticmethod
    def _rgb_to_hex(rgb):
        return "#%02x%02x%02x" % rgb

    def _blend(self, c1, c2, ratio):
        a = self._hex_to_rgb(c1)
        b = self._hex_to_rgb(c2)
        return self._rgb_to_hex(tuple(int(a[i] + (b[i] - a[i]) * ratio) for i in range(3)))

    def show_victory_screen(self):
        self.clear_root()
        self.root.configure(bg=BG_MAIN)
        self.root.geometry("600x720")

        card = self.make_card(self.root)
        card.pack(pady=(70, 20), padx=50, fill="x")

        tk.Label(card, text="★", font=("Segoe UI", 48, "bold"),
                 bg=BG_CARD, fg=ACCENT_GOLD).pack(pady=(28, 6))

        tk.Label(card, text="YOU ARE THE CHAMPION", font=FONT_WIN_TITLE,
                 bg=BG_CARD, fg=TEXT_PRIMARY).pack(pady=(0, 6))

        tk.Label(card, text="You completed all three levels",
                 font=FONT_WIN_SUB, bg=BG_CARD, fg=TEXT_SECONDARY).pack(pady=(0, 20))

        tk.Frame(card, bg="#334155", height=1).pack(fill="x", padx=30, pady=6)

        stats = tk.Frame(card, bg=BG_CARD)
        stats.pack(pady=18, padx=30, fill="x")

        self._win_stat(stats, 0, "FINAL SCORE", str(self.score), ACCENT_SUCCESS)
        self._win_stat(stats, 1, "WORDS WON", str(self.total_words_won), ACCENT_WARNING)

        tk.Label(card, text="Well played.", font=("Segoe UI", 11, "italic"),
                 bg=BG_CARD, fg=TEXT_MUTED).pack(pady=(0, 24))
        self.make_button(self.root, "PLAY AGAIN", self.start_game,
                         bg=ACCENT_SUCCESS, hover=ACCENT_SUCCESS_H,
                         font=FONT_MENU_BTN, padx=20, pady=13).pack(
                         fill="x", padx=110, pady=(0, 10))

        self.make_button(self.root, "MAIN MENU", self.show_menu,
                         bg="#475569", hover="#334155",
                         font=FONT_MENU_BTN, padx=20, pady=12).pack(
                         fill="x", padx=110)
    def _win_stat(self, parent, col, label, value, color):
        parent.columnconfigure(col, weight=1)
        tile = tk.Frame(parent, bg=BG_MAIN, highlightbackground="#334155",
                        highlightthickness=1)
        tile.grid(row=0, column=col, padx=6, sticky="nsew")
        tk.Label(tile, text=label, font=("Segoe UI", 9, "bold"),
                 bg=BG_MAIN, fg=TEXT_MUTED).pack(pady=(12, 2))
        tk.Label(tile, text=value, font=("Segoe UI", 22, "bold"),
                 bg=BG_MAIN, fg=color).pack(pady=(0, 12))

if __name__ == "__main__":
    root = tk.Tk()
    app = HangmanApp(root)
    root.mainloop()