import tkinter as tk
import random
import json
import os
import leaderboard as lb
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORDS_FILE = os.path.join(BASE_DIR, "emoji_data.json")

FALLBACK_RAW_WORDS = []
def load_word_data(path=WORDS_FILE):
    raw = None
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read().strip()
            if content:
                raw = json.loads(content)
                if not isinstance(raw, list) or not raw:
                    raw = None
        except (json.JSONDecodeError, OSError):
            raw = None
    if raw is None:
        print(f"Warning: could not load '{os.path.basename(path)}'. "
              f"Using built-in fallback word list instead.")
        raw = FALLBACK_RAW_WORDS
    grouped = {"easy": [], "medium": [], "hard": []}
    for item in raw:
        try:
            word = str(item["word"]).upper()
            emoji = str(item["emoji"])
            difficulty = str(item.get("difficulty", "Easy")).lower()
            if difficulty not in grouped:
                difficulty = "easy"
            grouped[difficulty].append({"emoji": emoji, "word": word})
        except (KeyError, TypeError):
            continue
    for key in grouped:
        if not grouped[key]:
            grouped[key] = [{"emoji": "❓", "word": "PYTHON"}]
    return grouped


WORD_DATA = load_word_data()
DIFFICULTY_PLAN = [("Easy", 5), ("Medium", 3), ("Hard", 2)]
TOTAL_WORDS_TO_WIN = sum(q for _, q in DIFFICULTY_PLAN)

TIME_PER_WORD = 10

BG_MAIN       = "#0B1120"
BG_CARD       = "#1E293B"
BG_CARD_ALT   = "#273449"
BG_INPUT      = "#0F172A"

TEXT_PRIMARY   = "#F8FAFC"
TEXT_SECONDARY = "#94A3B8"
TEXT_MUTED     = "#64748B"

ACCENT_PRIMARY   = "#3B82F6"
ACCENT_PRIMARY_H = "#2563EB"
ACCENT_SUCCESS   = "#10B981"
ACCENT_SUCCESS_H = "#059669"
ACCENT_WARNING   = "#F59E0B"
ACCENT_WARNING_H = "#D97706"
ACCENT_DANGER    = "#EF4444"
ACCENT_DANGER_H  = "#DC2626"
ACCENT_HINT      = "#8B5CF6"
ACCENT_HINT_H    = "#7C3AED"
ACCENT_GOLD      = "#FBBF24"

BORDER_SUBTLE = "#334155"

FB_SUCCESS = "#064E3B"
FB_DANGER  = "#7F1D1D"
FB_HINT    = "#4C1D95"

FONT_MENU_SUB    = ("Segoe UI", 10)
FONT_MENU_FOOT   = ("Segoe UI", 8)
FONT_HDR_TITLE   = ("Segoe UI", 16, "bold")
FONT_STAT_LABEL  = ("Segoe UI", 8, "bold")
FONT_STAT_VALUE  = ("Segoe UI", 16, "bold")
FONT_EMOJI       = ("Segoe UI Emoji", 52)
FONT_WORD        = ("Consolas", 30, "bold")
FONT_MSG         = ("Segoe UI", 11)
FONT_BTN         = ("Segoe UI", 10, "bold")
FONT_BTN_LARGE   = ("Segoe UI", 12, "bold")
FONT_WIN_TITLE   = ("Segoe UI", 24, "bold")
FONT_WIN_SUB     = ("Segoe UI", 12)
FONT_SECTION     = ("Segoe UI", 9, "bold")
ACHIEVEMENTS = [
    {"id": "first_win",   "name": "First Win",    "icon": "🏆",
     "desc": "Win your very first word."},
    {"id": "streak_5",    "name": "5 Streak",     "icon": "🔥",
     "desc": "Win 5 words in a row without losing a life."},
    {"id": "hint_master", "name": "Hint Master",  "icon": "💡",
     "desc": "Win a word right after using a hint."},
    {"id": "speed_solver","name": "Speed Solver", "icon": "⚡",
     "desc": "Solve a word in under 5 seconds."},
    {"id": "survivor",    "name": "Survivor",     "icon": "❤️",
     "desc": "Win a word with only 1 life remaining."},
    {"id": "champion",    "name": "Champion",     "icon": "👑",
     "desc": "Complete all 3 levels."},
]
class HangmanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Emoji Hangman — CSE 2216")
        self.root.geometry("780x680")
        self.root.configure(bg=BG_MAIN)
        self.root.resizable(False, False)

        self.player_name = "Player"
        self.timer_job = None
        self.timer_seconds_left = 0
        self.timer_running = False
        self.paused = False
        self.name_entry = None

     
        self.achievements = set()
        self.all_achievements = set()

        self.streak = 0
        self.round_start_time = None
        self.hint_used_this_round = False
        self.flash_job = None

        self.root.bind("<Escape>", lambda e: self._on_escape())
        self.root.bind("<space>",   lambda e: self._on_space())

        self.show_menu()

    # ═══════════════════════════════════════════════════════════
    #   HELPERS
    # ═══════════════════════════════════════════════════════════
    def clear_root(self):
        for w in self.root.winfo_children():
            w.destroy()
        self.name_entry = None

    def make_button(self, parent, text, command,
                    bg=ACCENT_PRIMARY, hover=ACCENT_PRIMARY_H,
                    fg=TEXT_PRIMARY, font=FONT_BTN, padx=16, pady=10):
        btn = tk.Button(parent, text=text, command=command,
                        font=font, bg=bg, fg=fg,
                        activebackground=hover, activeforeground=fg,
                        relief="flat", bd=0, padx=padx, pady=pady,
                        cursor="hand2", highlightthickness=0,
                        takefocus=0)
        btn.bind("<Enter>", lambda e: btn.config(bg=hover))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
        return btn

    def make_card(self, parent, bg=BG_CARD, border=BORDER_SUBTLE, **kwargs):
        return tk.Frame(parent, bg=bg, highlightbackground=border,
                        highlightthickness=1, **kwargs)

    def divider(self, parent, color=BORDER_SUBTLE, pady=0):
        f = tk.Frame(parent, bg=color, height=1)
        f.pack(fill="x", padx=24, pady=pady)
        return f

    # ═══════════════════════════════════════════════════════════
    #   KEYBOARD SHORTCUTS
    # ═══════════════════════════════════════════════════════════
    def _on_escape(self):
        if hasattr(self, "guess_entry") and self.guess_entry and \
                self.guess_entry.winfo_exists():
            self.go_to_menu()

    def _on_space(self):
        if hasattr(self, "pause_button") and self.pause_button and \
                self.pause_button.winfo_exists() and \
                not getattr(self, "game_over", True):
            self.toggle_pause()

    # ═══════════════════════════════════════════════════════════
    #   TIMER
    # ═══════════════════════════════════════════════════════════
    def cancel_timer(self):
        if self.timer_job is not None:
            try:
                self.root.after_cancel(self.timer_job)
            except Exception:
                pass
            self.timer_job = None
        self.timer_running = False
        self.paused = False

    def time_limit_for_current_level(self):
        return TIME_PER_WORD

    def start_timer(self):
        self.cancel_timer()
        self.timer_seconds_left = self.time_limit_for_current_level()
        self.timer_running = True
        self.paused = False
        self.round_start_time = time.time()
        self.update_timer_label()
        self.tick_timer()

    def tick_timer(self):
        if not self.timer_running or self.paused:
            return
        self.update_timer_label()
        if self.timer_seconds_left <= 0:
            self.timer_running = False
            self.on_time_up()
            return
        self.timer_seconds_left -= 1
        self.timer_job = self.root.after(1000, self.tick_timer)

    def update_timer_label(self):
        if not hasattr(self, "timer_label") or self.timer_label is None:
            return
        try:
            if not self.timer_label.winfo_exists():
                return
        except tk.TclError:
            return
        secs = max(self.timer_seconds_left, 0)
        limit = self.time_limit_for_current_level()
        if self.paused:
            self.timer_label.config(text="⏸", fg=ACCENT_HINT)
            return
        if secs > limit * 0.6:
            color = ACCENT_SUCCESS
        elif secs > limit * 0.3:
            color = ACCENT_WARNING
        else:
            color = ACCENT_DANGER
        self.timer_label.config(text=f"{secs}s", fg=color)

    def on_time_up(self):
        if self.game_over:
            return
        self.tries_left -= 1
        self.streak = 0
        self.update_stats()
        self.set_message(f"Time's up! The word was {self.word}",
                         ACCENT_DANGER, "⏱")
        self.flash(FB_DANGER)
        self.root.bell()
        if self.tries_left <= 0:
            self.game_over = True
            self.set_message(f"Game over. The word was {self.word}",
                             ACCENT_DANGER, "✕")
            self.flash(FB_DANGER)
            self.save_current_score(self.current_level_name())
            self.show_game_over_panel()
            return
        self.root.after(1400, self.new_round_ui)

    # ═══════════════════════════════════════════════════════════
    #   PAUSE
    # ═══════════════════════════════════════════════════════════
    def toggle_pause(self):
        if self.game_over:
            return
        if self.paused:
            self.paused = False
            self.pause_button.config(text="⏸  Pause",
                                     bg=ACCENT_WARNING,
                                     activebackground=ACCENT_WARNING_H)
            self.pause_button.bind("<Enter>",
                lambda e: self.pause_button.config(bg=ACCENT_WARNING_H))
            self.pause_button.bind("<Leave>",
                lambda e: self.pause_button.config(bg=ACCENT_WARNING))
            self.set_message("Resumed. Enter a letter.", ACCENT_PRIMARY, "▶")
            self.guess_entry.config(state="normal")
            self.guess_entry.focus()
            self.timer_running = True
            self.tick_timer()
        else:
            self.paused = True
            if self.timer_job is not None:
                try:
                    self.root.after_cancel(self.timer_job)
                except Exception:
                    pass
                self.timer_job = None
            self.pause_button.config(text="▶  Resume",
                                     bg=ACCENT_SUCCESS,
                                     activebackground=ACCENT_SUCCESS_H)
            self.pause_button.bind("<Enter>",
                lambda e: self.pause_button.config(bg=ACCENT_SUCCESS_H))
            self.pause_button.bind("<Leave>",
                lambda e: self.pause_button.config(bg=ACCENT_SUCCESS))
            self.set_message("Game paused — press Space or Resume.",
                             ACCENT_HINT, "⏸")
            self.guess_entry.config(state="disabled")
            self.update_timer_label()

    # ═══════════════════════════════════════════════════════════
    #   GAME OVER PANEL
    # ═══════════════════════════════════════════════════════════
    def show_game_over_panel(self):
        try:
            self.guess_entry.config(state="disabled")
        except tk.TclError:
            pass
        try:
            self.pause_button.config(state="disabled")
        except tk.TclError:
            pass
        try:
            self.puzzle_card.configure(highlightbackground=ACCENT_DANGER,
                                       highlightthickness=2)
        except tk.TclError:
            pass

        panel = self.make_card(self.root, border=ACCENT_DANGER)
        panel.pack(pady=(10, 10), padx=24, fill="x")

        top_row = tk.Frame(panel, bg=BG_CARD)
        top_row.pack(fill="x", pady=(16, 10), padx=20)
        tk.Label(top_row, text="✕", font=("Segoe UI", 26, "bold"),
                 bg=BG_CARD, fg=ACCENT_DANGER).pack(side="left", padx=(0, 14))
        text_col = tk.Frame(top_row, bg=BG_CARD)
        text_col.pack(side="left", fill="x", expand=True)
        tk.Label(text_col, text="GAME OVER", font=("Segoe UI", 16, "bold"),
                 bg=BG_CARD, fg=ACCENT_DANGER, anchor="w").pack(fill="x")
        tk.Label(text_col,
                 text=f"The word was {self.word}   •   Final score: {self.score}",
                 font=("Segoe UI", 10),
                 bg=BG_CARD, fg=TEXT_SECONDARY, anchor="w").pack(fill="x")

        self.divider(panel, pady=0)

        btn_row = tk.Frame(panel, bg=BG_CARD)
        btn_row.pack(fill="x", padx=20, pady=(14, 16))
        btn_row.columnconfigure(0, weight=1)
        btn_row.columnconfigure(1, weight=1)
        self.make_button(btn_row, "PLAY AGAIN", self.restart_game,
                         bg=ACCENT_SUCCESS, hover=ACCENT_SUCCESS_H,
                         font=FONT_BTN_LARGE, padx=14, pady=11).grid(
                         row=0, column=0, sticky="ew", padx=(0, 6))
        self.make_button(btn_row, "🏠  MENU", self.go_to_menu,
                         bg="#475569", hover="#334155",
                         font=FONT_BTN_LARGE, padx=14, pady=11).grid(
                         row=0, column=1, sticky="ew", padx=(6, 0))

    # ═══════════════════════════════════════════════════════════
    #   NAME CAPTURE
    # ═══════════════════════════════════════════════════════════
    def capture_name_from_menu(self):
        entry = getattr(self, "name_entry", None)
        if entry is None:
            return
        try:
            if not entry.winfo_exists():
                return
            typed = entry.get().strip()
        except tk.TclError:
            return
        self.player_name = typed[:20] if typed else "Player"

    def on_start_clicked(self):
        self.capture_name_from_menu()
        self.start_game()

    # ═══════════════════════════════════════════════════════════
    #   MENU  — full-screen layout like leaderboard
    # ═══════════════════════════════════════════════════════════
    def show_menu(self):
        self.cancel_timer()
        self.clear_root()
        self.root.configure(bg=BG_MAIN)
        self.root.geometry("780x680")

        # Top accent stripe
        stripe = tk.Frame(self.root, bg=BG_MAIN, height=4)
        stripe.pack(fill="x", side="top")
        colors = [ACCENT_PRIMARY, ACCENT_HINT, ACCENT_SUCCESS, ACCENT_GOLD]
        for i, c in enumerate(colors):
            seg = tk.Frame(stripe, bg=c, height=4)
            seg.place(relx=i/4, rely=0, relwidth=0.25, relheight=1)

        container = tk.Frame(self.root, bg=BG_MAIN)
        container.pack(fill="both", expand=True, padx=24, pady=14)

        # ── Header card ──
        header = self.make_card(container)
        header.pack(fill="x", pady=(0, 10))
        title_row = tk.Frame(header, bg=BG_CARD)
        title_row.pack(pady=(14, 4))
        tk.Label(title_row, text="EMOJI", font=("Segoe UI", 24, "bold"),
                 bg=BG_CARD, fg=TEXT_PRIMARY).pack(side="left")
        tk.Label(title_row, text="  HANGMAN", font=("Segoe UI", 24, "bold"),
                 bg=BG_CARD, fg=ACCENT_PRIMARY).pack(side="left")
        tk.Label(header, text="Software Development I  ·  CSE 2216",
                 font=FONT_MENU_SUB, bg=BG_CARD,
                 fg=TEXT_SECONDARY).pack(pady=(0, 14))

        # ── Name card ──
        name_card = self.make_card(container)
        name_card.pack(fill="x", pady=(0, 10))
        name_row = tk.Frame(name_card, bg=BG_CARD)
        name_row.pack(pady=10, padx=16, fill="x")
        tk.Label(name_row, text="PLAYER", font=FONT_SECTION,
                 bg=BG_CARD, fg=TEXT_MUTED).pack(side="left", padx=(0, 12))
        self.name_entry = tk.Entry(name_row, font=("Segoe UI", 11),
                                   bg=BG_INPUT, fg=TEXT_PRIMARY,
                                   insertbackground=TEXT_PRIMARY,
                                   relief="flat", bd=0,
                                   highlightthickness=1,
                                   highlightbackground=BORDER_SUBTLE,
                                   highlightcolor=ACCENT_PRIMARY)
        self.name_entry.pack(side="left", fill="x", expand=True, ipady=6)
        self.name_entry.insert(
            0, self.player_name if self.player_name != "Player" else "")

        # ── Progression card — expands to fill middle ──
        info = self.make_card(container)
        info.pack(fill="both", expand=True, pady=(0, 10))

        inner_info = tk.Frame(info, bg=BG_CARD)
        inner_info.pack(expand=True, fill="both")

        tk.Label(inner_info, text="GAME PROGRESSION", font=FONT_SECTION,
                 bg=BG_CARD, fg=ACCENT_PRIMARY).pack(pady=(18, 12))

        steps = [
            ("LEVEL 1", "Easy",   "5 words", ACCENT_SUCCESS),
            ("LEVEL 2", "Medium", "3 words", ACCENT_WARNING),
            ("LEVEL 3", "Hard",   "2 words", ACCENT_DANGER),
        ]
        for tag, name, quota, color in steps:
            row = tk.Frame(inner_info, bg=BG_CARD)
            row.pack(pady=4, padx=20, fill="x")
            dot = tk.Frame(row, bg=color, width=10, height=10)
            dot.pack(side="left", padx=(0, 12))
            dot.pack_propagate(False)
            tk.Label(row, text=tag, font=("Segoe UI", 10, "bold"),
                     bg=BG_CARD, fg=color, width=9,
                     anchor="w").pack(side="left")
            tk.Label(row, text=name, font=("Segoe UI", 11, "bold"),
                     bg=BG_CARD, fg=TEXT_PRIMARY, width=9,
                     anchor="w").pack(side="left")
            tk.Label(row, text=f"{quota}   ·   {TIME_PER_WORD}s / word",
                     font=("Segoe UI", 11),
                     bg=BG_CARD, fg=TEXT_SECONDARY,
                     anchor="w").pack(side="left")

        tk.Label(inner_info, text="Win all 10 words to become the Champion",
                 font=("Segoe UI", 10, "italic"),
                 bg=BG_CARD, fg=ACCENT_GOLD).pack(pady=(18, 18))

        # ── Buttons row ──
        btn_row = tk.Frame(container, bg=BG_MAIN)
        btn_row.pack(fill="x", pady=(0, 8))
        btn_row.columnconfigure(0, weight=1)
        btn_row.columnconfigure(1, weight=1)
        self.make_button(btn_row, "▶  START GAME", self.on_start_clicked,
                         bg=ACCENT_SUCCESS, hover=ACCENT_SUCCESS_H,
                         font=FONT_BTN_LARGE, padx=14, pady=13).grid(
                         row=0, column=0, sticky="ew", padx=(0, 5))
        self.make_button(btn_row, "🏆  LEADERBOARD", self.show_leaderboard,
                         bg=ACCENT_HINT, hover=ACCENT_HINT_H,
                         font=FONT_BTN_LARGE, padx=14, pady=13).grid(
                         row=0, column=1, sticky="ew", padx=(5, 0))

        btn_row2 = tk.Frame(container, bg=BG_MAIN)
        btn_row2.pack(fill="x", pady=(0, 10))
        btn_row2.columnconfigure(0, weight=1)
        btn_row2.columnconfigure(1, weight=1)
        # From the menu, show OVERALL achievements (this session)
        self.make_button(btn_row2, "🎖  ACHIEVEMENTS",
                         lambda: self.show_achievements(only_unlocked=False),
                         bg=ACCENT_WARNING, hover=ACCENT_WARNING_H,
                         font=FONT_BTN_LARGE, padx=14, pady=12).grid(
                         row=0, column=0, sticky="ew", padx=(0, 5))
        self.make_button(btn_row2, "EXIT", self.root.destroy,
                         bg="#475569", hover="#334155",
                         font=FONT_BTN_LARGE, padx=14, pady=12).grid(
                         row=0, column=1, sticky="ew", padx=(5, 0))

        tk.Label(container,
                 text="Northern University of Business & Technology, Khulna",
                 font=FONT_MENU_FOOT, bg=BG_MAIN,
                 fg=TEXT_MUTED).pack(side="bottom", pady=(6, 0))

    # ═══════════════════════════════════════════════════════════
    #   ACHIEVEMENTS SCREEN
    # ═══════════════════════════════════════════════════════════
    def show_achievements(self, only_unlocked=False):
        """
        Show the achievements screen.

        only_unlocked=False  → overall achievements (session-wide).
                               This is what the menu button shows.
        only_unlocked=True   → achievements unlocked this round only.
                               This is what the victory screen shows.
        """
        self.cancel_timer()
        self.clear_root()
        self.root.configure(bg=BG_MAIN)
        self.root.geometry("780x680")

        if only_unlocked:
            # Round-only view: use self.achievements (per-game set)
            source = self.achievements
            display_achievements = [a for a in ACHIEVEMENTS
                                    if a["id"] in source]
            title_text = "ROUND ACHIEVEMENTS"
            subtitle_text = f"Unlocked by {self.player_name} this round"
        else:
            # Overall view: use self.all_achievements (session-wide set)
            source = self.all_achievements
            display_achievements = ACHIEVEMENTS
            title_text = "ACHIEVEMENTS"
            subtitle_text = f"Player: {self.player_name}"

        container = tk.Frame(self.root, bg=BG_MAIN)
        container.pack(fill="both", expand=True, padx=24, pady=14)

        header = self.make_card(container)
        header.pack(fill="x", pady=(0, 10))
        tk.Label(header, text=f"🎖  {title_text}",
                 font=("Segoe UI", 18, "bold"),
                 bg=BG_CARD, fg=ACCENT_GOLD).pack(pady=(14, 2))
        tk.Label(header, text=subtitle_text,
                 font=FONT_MENU_SUB, bg=BG_CARD,
                 fg=TEXT_SECONDARY).pack(pady=(0, 12))

        board = self.make_card(container)
        board.pack(fill="both", expand=True, pady=(0, 10))

        if not only_unlocked:
            # Overall mode: show the session-wide player rating card
            unlocked = len(self.all_achievements)
            total = len(ACHIEVEMENTS)
            rating_card = tk.Frame(board, bg=BG_CARD_ALT,
                                   highlightbackground=BORDER_SUBTLE,
                                   highlightthickness=1)
            rating_card.pack(fill="x", padx=18, pady=(14, 10))
            tk.Label(rating_card, text="OVERALL PROGRESS",
                     font=FONT_SECTION,
                     bg=BG_CARD_ALT, fg=TEXT_MUTED).pack(pady=(10, 2))
            rating_title, rating_color = self.rating_title(unlocked, total)
            tk.Label(rating_card, text=rating_title,
                     font=("Segoe UI", 18, "bold"),
                     bg=BG_CARD_ALT, fg=rating_color).pack(pady=(0, 2))
            tk.Label(rating_card,
                     text=f"{unlocked} / {total} achievements unlocked in this session",
                     font=("Segoe UI", 9),
                     bg=BG_CARD_ALT,
                     fg=TEXT_SECONDARY).pack(pady=(0, 10))
        else:
            # Round-only mode: show a "Unlocked this round" summary card
            summary = tk.Frame(board, bg=BG_CARD_ALT,
                               highlightbackground=BORDER_SUBTLE,
                               highlightthickness=1)
            summary.pack(fill="x", padx=18, pady=(14, 10))
            count = len(display_achievements)
            tk.Label(summary, text="UNLOCKED THIS ROUND",
                     font=FONT_SECTION,
                     bg=BG_CARD_ALT, fg=TEXT_MUTED).pack(pady=(10, 2))
            if count > 0:
                tk.Label(summary,
                         text=f"{count} achievement{'s' if count != 1 else ''}",
                         font=("Segoe UI", 16, "bold"),
                         bg=BG_CARD_ALT,
                         fg=ACCENT_GOLD).pack(pady=(0, 10))
            else:
                tk.Label(summary, text="No achievements this round",
                         font=("Segoe UI", 13, "bold"),
                         bg=BG_CARD_ALT,
                         fg=TEXT_MUTED).pack(pady=(0, 10))

        list_frame = tk.Frame(board, bg=BG_CARD)
        list_frame.pack(fill="both", expand=True, padx=18, pady=(0, 12))

        if not display_achievements:
            tk.Label(list_frame, text="No achievements to show.",
                     font=("Segoe UI", 11, "italic"),
                     bg=BG_CARD, fg=TEXT_MUTED).pack(pady=30)
        else:
            for ach in display_achievements:
                # Unlocked = in the *overall* set (session) — this is correct
                # for both views because anything unlocked this round is also
                # added to all_achievements.
                unlocked_flag = ach["id"] in self.all_achievements
                row = tk.Frame(list_frame, bg=BG_CARD)
                row.pack(fill="x", pady=2)
                if unlocked_flag:
                    icon_color = ACCENT_GOLD
                    name_color = TEXT_PRIMARY
                    desc_color = TEXT_SECONDARY
                    badge = "✓"
                    badge_color = ACCENT_SUCCESS
                else:
                    icon_color = BORDER_SUBTLE
                    name_color = TEXT_MUTED
                    desc_color = BORDER_SUBTLE
                    badge = "🔒"
                    badge_color = TEXT_MUTED
                tk.Label(row, text=ach["icon"], font=("Segoe UI Emoji", 15),
                         bg=BG_CARD, fg=icon_color,
                         width=3).pack(side="left")
                text_col = tk.Frame(row, bg=BG_CARD)
                text_col.pack(side="left", fill="x", expand=True)
                tk.Label(text_col, text=ach["name"],
                         font=("Segoe UI", 10, "bold"),
                         bg=BG_CARD, fg=name_color,
                         anchor="w").pack(fill="x")
                tk.Label(text_col, text=ach["desc"],
                         font=("Segoe UI", 8),
                         bg=BG_CARD, fg=desc_color,
                         anchor="w").pack(fill="x")
                tk.Label(row, text=badge, font=("Segoe UI", 12, "bold"),
                         bg=BG_CARD, fg=badge_color,
                         width=3).pack(side="right")

        if only_unlocked:
            self.make_button(container, "↩   BACK TO RESULTS",
                             self.show_victory_screen,
                             bg="#475569", hover="#334155",
                             font=FONT_BTN_LARGE, padx=14,
                             pady=11).pack(fill="x")
        else:
            self.make_button(container, "🏠   BACK TO MENU", self.show_menu,
                             bg="#475569", hover="#334155",
                             font=FONT_BTN_LARGE, padx=14,
                             pady=11).pack(fill="x")

    def rating_title(self, unlocked, total):
        ratio = unlocked / total if total else 0
        if ratio >= 1.0:
            return "★  LEGEND", ACCENT_GOLD
        if ratio >= 0.83:
            return "★  GRANDMASTER", ACCENT_GOLD
        if ratio >= 0.66:
            return "★  MASTER", ACCENT_HINT
        if ratio >= 0.50:
            return "★  EXPERT", ACCENT_PRIMARY
        if ratio >= 0.33:
            return "★  SKILLED", ACCENT_SUCCESS
        if ratio >= 0.17:
            return "★  APPRENTICE", ACCENT_WARNING
        return "★  ROOKIE", TEXT_SECONDARY

    # ═══════════════════════════════════════════════════════════
    #   LEADERBOARD
    # ═══════════════════════════════════════════════════════════
    def show_leaderboard(self):
        self.cancel_timer()
        self.clear_root()
        self.root.configure(bg=BG_MAIN)
        self.root.geometry("780x680")

        container = tk.Frame(self.root, bg=BG_MAIN)
        container.pack(fill="both", expand=True, padx=24, pady=14)

        header = self.make_card(container)
        header.pack(fill="x", pady=(0, 10))
        tk.Label(header, text="🏆  LEADERBOARD",
                 font=("Segoe UI", 18, "bold"),
                 bg=BG_CARD, fg=ACCENT_GOLD).pack(pady=(14, 2))
        tk.Label(header, text="Top 10 Scores", font=FONT_MENU_SUB,
                 bg=BG_CARD, fg=TEXT_SECONDARY).pack(pady=(0, 12))

        board_card = self.make_card(container)
        board_card.pack(fill="both", expand=True, pady=(0, 10))

        top_scores = lb.get_top_scores(10)

        if not top_scores:
            empty = tk.Frame(board_card, bg=BG_CARD)
            empty.pack(fill="both", expand=True)
            tk.Label(empty, text="🏆", font=("Segoe UI Emoji", 40),
                     bg=BG_CARD, fg=BORDER_SUBTLE).pack(pady=(40, 8))
            tk.Label(empty, text="No scores yet — be the first to play!",
                     font=("Segoe UI", 11, "italic"),
                     bg=BG_CARD, fg=TEXT_SECONDARY).pack()
        else:
            hdr = tk.Frame(board_card, bg=BG_CARD)
            hdr.pack(fill="x", padx=20, pady=(14, 6))
            tk.Label(hdr, text="RANK", font=FONT_SECTION,
                     bg=BG_CARD, fg=TEXT_MUTED,
                     width=6, anchor="w").pack(side="left")
            tk.Label(hdr, text="NAME", font=FONT_SECTION,
                     bg=BG_CARD, fg=TEXT_MUTED,
                     width=16, anchor="w").pack(side="left")
            tk.Label(hdr, text="LEVEL", font=FONT_SECTION,
                     bg=BG_CARD, fg=TEXT_MUTED,
                     width=10, anchor="w").pack(side="left")
            tk.Label(hdr, text="SCORE", font=FONT_SECTION,
                     bg=BG_CARD, fg=TEXT_MUTED,
                     anchor="e").pack(side="right")

            tk.Frame(board_card, bg=BORDER_SUBTLE,
                     height=1).pack(fill="x", padx=20, pady=(0, 4))

            medal_colors = {0: ACCENT_GOLD, 1: "#CBD5E1", 2: "#D97706"}
            medal_icons = {0: "🥇", 1: "🥈", 2: "🥉"}
            for i, entry in enumerate(top_scores):
                row = tk.Frame(board_card, bg=BG_CARD)
                row.pack(fill="x", padx=20, pady=3)
                if i in medal_icons:
                    rank_text = medal_icons[i]
                else:
                    rank_text = f"#{i + 1}"
                tk.Label(row, text=rank_text,
                         font=("Segoe UI", 11, "bold"),
                         bg=BG_CARD,
                         fg=medal_colors.get(i, TEXT_PRIMARY),
                         width=6, anchor="w").pack(side="left")
                tk.Label(row, text=entry["name"][:14],
                         font=("Segoe UI", 10),
                         bg=BG_CARD, fg=TEXT_PRIMARY,
                         width=16, anchor="w").pack(side="left")
                tk.Label(row, text=entry["level"],
                         font=("Segoe UI", 10),
                         bg=BG_CARD, fg=TEXT_SECONDARY,
                         width=10, anchor="w").pack(side="left")
                tk.Label(row, text=str(entry["score"]),
                         font=("Segoe UI", 10, "bold"),
                         bg=BG_CARD, fg=ACCENT_SUCCESS,
                         anchor="e").pack(side="right")

            tk.Label(board_card, text="", bg=BG_CARD).pack(pady=4)

        btn_row = tk.Frame(container, bg=BG_MAIN)
        btn_row.pack(fill="x")
        btn_row.columnconfigure(0, weight=1)
        btn_row.columnconfigure(1, weight=1)
        self.make_button(btn_row, "🗑  CLEAR", self.clear_leaderboard,
                         bg=ACCENT_DANGER, hover=ACCENT_DANGER_H,
                         font=FONT_BTN_LARGE, padx=14, pady=12).grid(
                         row=0, column=0, sticky="ew", padx=(0, 5))
        self.make_button(btn_row, "🏠  MENU", self.show_menu,
                         bg="#475569", hover="#334155",
                         font=FONT_BTN_LARGE, padx=14, pady=12).grid(
                         row=0, column=1, sticky="ew", padx=(5, 0))

    # ═══════════════════════════════════════════════════════════
    #   CLEAR LEADERBOARD
    # ═══════════════════════════════════════════════════════════
    def clear_leaderboard(self):
        confirm = tk.Toplevel(self.root)
        confirm.title("Clear Leaderboard")
        confirm.configure(bg=BG_MAIN)
        confirm.resizable(False, False)
        confirm.transient(self.root)
        confirm.grab_set()

        self.root.update_idletasks()
        w, h = 400, 220
        px = self.root.winfo_x() + (self.root.winfo_width() - w) // 2
        py = self.root.winfo_y() + (self.root.winfo_height() - h) // 2
        confirm.geometry(f"{w}x{h}+{px}+{py}")

        card = self.make_card(confirm, border=ACCENT_DANGER)
        card.pack(fill="both", expand=True, padx=16, pady=16)

        tk.Label(card, text="⚠", font=("Segoe UI", 28, "bold"),
                 bg=BG_CARD, fg=ACCENT_WARNING).pack(pady=(16, 6))
        tk.Label(card, text="Clear the leaderboard?",
                 font=("Segoe UI", 14, "bold"),
                 bg=BG_CARD, fg=TEXT_PRIMARY).pack()
        tk.Label(card, text="All saved scores will be deleted permanently.",
                 font=("Segoe UI", 9),
                 bg=BG_CARD, fg=TEXT_SECONDARY).pack(pady=(4, 16))

        btn_row = tk.Frame(card, bg=BG_CARD)
        btn_row.pack(fill="x", padx=16, pady=(0, 16))
        btn_row.columnconfigure(0, weight=1)
        btn_row.columnconfigure(1, weight=1)

        def do_clear():
            try:
                if hasattr(lb, "clear_scores"):
                    lb.clear_scores()
                elif hasattr(lb, "clear_all"):
                    lb.clear_all()
                elif hasattr(lb, "reset"):
                    lb.reset()
                elif hasattr(lb, "SCORES_FILE"):
                    with open(lb.SCORES_FILE, "w", encoding="utf-8") as f:
                        json.dump([], f)
                elif hasattr(lb, "LEADERBOARD_FILE"):
                    with open(lb.LEADERBOARD_FILE, "w", encoding="utf-8") as f:
                        json.dump([], f)
                elif hasattr(lb, "FILE"):
                    with open(lb.FILE, "w", encoding="utf-8") as f:
                        json.dump([], f)
                else:
                    for name in ("leaderboard.json", "scores.json",
                                 "leaderboard_data.json"):
                        p = os.path.join(BASE_DIR, name)
                        if os.path.exists(p):
                            with open(p, "w", encoding="utf-8") as f:
                                json.dump([], f)
            except Exception as e:
                print(f"Could not clear leaderboard: {e}")
            confirm.destroy()
            self.show_leaderboard()

        self.make_button(btn_row, "Cancel", confirm.destroy,
                         bg="#475569", hover="#334155",
                         font=("Segoe UI", 11, "bold"),
                         padx=14, pady=9).grid(
                         row=0, column=0, sticky="ew", padx=(0, 6))
        self.make_button(btn_row, "Clear", do_clear,
                         bg=ACCENT_DANGER, hover=ACCENT_DANGER_H,
                         font=("Segoe UI", 11, "bold"),
                         padx=14, pady=9).grid(
                         row=0, column=1, sticky="ew", padx=(6, 0))

    # ═══════════════════════════════════════════════════════════
    #   GAME
    # ═══════════════════════════════════════════════════════════
    def start_game(self):
        self.cancel_timer()
        self.clear_root()
        self.root.configure(bg=BG_MAIN)
        self.root.geometry("780x680")

        self.score = 0
        self.max_tries = 5
        self.tries_left = self.max_tries
        self.game_over = False
        self.score_saved = False

        self.difficulty_index = 0
        self.words_won_in_level = 0
        self.total_words_won = 0
        self.used_words = set()
        self.hint_used = False

        # Reset the ROUND-ONLY achievements (used by the victory screen)
        self.achievements = set()
        # NOTE: self.all_achievements is intentionally NOT reset here so that
        # the menu's "overall achievements" view keeps growing across games.

        self.streak = 0
        self.round_start_time = None
        self.hint_used_this_round = False
        self.paused = False

        self.new_round()

        top = self.make_card(self.root)
        top.pack(pady=(14, 8), padx=24, fill="x")
        tk.Label(top, text="EMOJI HANGMAN", font=FONT_HDR_TITLE,
                 bg=BG_CARD, fg=TEXT_PRIMARY).pack(side="left",
                                                   padx=18, pady=12)
        self.level_label = tk.Label(top, text="",
                                    font=("Segoe UI", 10, "bold"),
                                    bg=BG_CARD, fg=ACCENT_PRIMARY)
        self.level_label.pack(side="right", padx=18)

        stats = tk.Frame(self.root, bg=BG_MAIN)
        stats.pack(pady=4, padx=24, fill="x")
        for i in range(4):
            stats.columnconfigure(i, weight=1)

        self.score_label = self._stat_tile(stats, 0, "SCORE", "0", ACCENT_SUCCESS)
        self.hearts_label = self._stat_tile(stats, 1, "LIVES", "", ACCENT_DANGER)
        self.won_label   = self._stat_tile(stats, 2, "WORDS", "0/10", ACCENT_WARNING)
        self.timer_label = self._stat_tile(stats, 3, "TIME",
                                            f"{TIME_PER_WORD}s",
                                            ACCENT_PRIMARY)

        self.puzzle_card = self.make_card(self.root)
        self.puzzle_card.pack(pady=12, padx=24, fill="x")

        self.emoji_label = tk.Label(self.puzzle_card, text=self.emoji,
                                    font=FONT_EMOJI, bg=BG_CARD,
                                    fg=TEXT_PRIMARY)
        self.emoji_label.pack(pady=(20, 6))

        self.word_label = tk.Label(self.puzzle_card,
                                   text=self.get_display_word(),
                                   font=FONT_WORD, bg=BG_CARD,
                                   fg=TEXT_PRIMARY)
        self.word_label.pack(pady=(4, 20))

        fb = tk.Frame(self.root, bg=BG_MAIN)
        fb.pack(pady=4, padx=24, fill="x")
        self.reaction_label = tk.Label(fb, text="",
                                       font=("Segoe UI", 18),
                                       bg=BG_MAIN, fg=TEXT_PRIMARY)
        self.reaction_label.pack(side="left", padx=(4, 8))
        self.message_label = tk.Label(fb, text="Enter a letter to begin",
                                      font=FONT_MSG, bg=BG_MAIN,
                                      fg=TEXT_SECONDARY)
        self.message_label.pack(side="left")

        inp = self.make_card(self.root)
        inp.pack(pady=10, padx=24, fill="x")
        inner = tk.Frame(inp, bg=BG_CARD)
        inner.pack(pady=12, padx=16)
        tk.Label(inner, text="YOUR GUESS", font=FONT_SECTION,
                 bg=BG_CARD, fg=TEXT_MUTED).pack(side="left", padx=(0, 12))
        self.guess_entry = tk.Entry(inner, width=3,
                                    font=("Segoe UI", 20, "bold"),
                                    justify="center", relief="flat", bd=0,
                                    bg=BG_INPUT, fg=TEXT_PRIMARY,
                                    insertbackground=TEXT_PRIMARY,
                                    highlightthickness=1,
                                    highlightbackground=BORDER_SUBTLE,
                                    highlightcolor=ACCENT_PRIMARY)
        self.guess_entry.pack(side="left", ipady=8, ipadx=6)
        self.guess_entry.bind("<Return>", lambda e: self.check_guess())
        self.make_button(inner, "GUESS", self.check_guess,
                         bg=ACCENT_PRIMARY, hover=ACCENT_PRIMARY_H,
                         font=FONT_BTN_LARGE,
                         padx=22, pady=10).pack(side="left", padx=(12, 0))

        actions = tk.Frame(self.root, bg=BG_MAIN)
        actions.pack(pady=(0, 12), padx=24, fill="x")
        self.make_button(actions, "💡  Hint", self.give_hint,
                         bg=ACCENT_HINT, hover=ACCENT_HINT_H,
                         padx=12, pady=10).pack(
                         side="left", expand=True, fill="x", padx=4)
        self.pause_button = self.make_button(
            actions, "⏸  Pause", self.toggle_pause,
            bg=ACCENT_WARNING, hover=ACCENT_WARNING_H, padx=12, pady=10)
        self.pause_button.pack(side="left", expand=True, fill="x", padx=4)
        self.make_button(actions, "↻  Restart", self.restart_game,
                         bg="#475569", hover="#334155",
                         padx=12, pady=10).pack(
                         side="left", expand=True, fill="x", padx=4)
        self.make_button(actions, "🏠  Menu", self.go_to_menu,
                         bg="#475569", hover="#334155",
                         padx=12, pady=10).pack(
                         side="left", expand=True, fill="x", padx=4)

        ach_wrap = tk.Frame(self.root, bg=BG_MAIN)
        ach_wrap.pack(pady=(0, 10), padx=24, fill="x")
        tk.Label(ach_wrap, text="ACHIEVEMENTS", font=FONT_SECTION,
                 bg=BG_MAIN, fg=TEXT_MUTED).pack(side="left",
                                                  padx=(0, 10))
        self.ach_bar = tk.Frame(ach_wrap, bg=BG_MAIN)
        self.ach_bar.pack(side="left", fill="x", expand=True)
        self.ach_labels = {}
        for ach in ACHIEVEMENTS:
            # If already unlocked overall in the session, show gold;
            # otherwise show dim (this round may still unlock it).
            already_overall = ach["id"] in self.all_achievements
            lbl = tk.Label(self.ach_bar, text=ach["icon"],
                           font=("Segoe UI Emoji", 14),
                           bg=BG_MAIN,
                           fg=ACCENT_GOLD if already_overall else BORDER_SUBTLE)
            lbl.pack(side="left", padx=4)
            self.ach_labels[ach["id"]] = lbl

        self.update_level_label()
        self.update_stats()
        self.guess_entry.focus()
        self.start_timer()

    def _stat_tile(self, parent, col, label, value, color):
        tile = self.make_card(parent)
        tile.grid(row=0, column=col, padx=5, sticky="nsew")
        tk.Label(tile, text=label, font=FONT_STAT_LABEL,
                 bg=BG_CARD, fg=TEXT_MUTED).pack(pady=(10, 2))
        val = tk.Label(tile, text=value, font=FONT_STAT_VALUE,
                       bg=BG_CARD, fg=color)
        val.pack(pady=(0, 10))
        return val

    # ═══════════════════════════════════════════════════════════
    #   GAME STATE
    # ═══════════════════════════════════════════════════════════
    def current_level_name(self):
        return DIFFICULTY_PLAN[self.difficulty_index][0]

    def current_level_quota(self):
        return DIFFICULTY_PLAN[self.difficulty_index][1]

    def update_level_label(self):
        name = self.current_level_name()
        quota = self.current_level_quota()
        self.level_label.config(
            text=f"{name.upper()}  ·  {self.words_won_in_level}/{quota}")

    def update_stats(self):
        self.score_label.config(text=str(self.score))
        self.hearts_label.config(text=self.hearts_text())
        self.won_label.config(
            text=f"{self.total_words_won}/{TOTAL_WORDS_TO_WIN}")

    def hearts_text(self):
        return "♥" * self.tries_left + "♡" * (self.max_tries - self.tries_left)

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
        self.hint_used_this_round = False
    def get_display_word(self):
        return " ".join(l if l in self.guessed_letters else "_"
                        for l in self.word)
    def check_guess(self):
        if self.paused:
            self.set_message("Game is paused. Press Space to resume.",
                             ACCENT_HINT, "⏸")
            return
        if self.game_over:
            self.set_message("Game over. Press Restart to play again.",
                             ACCENT_DANGER, "✕")
            return
        guess = self.guess_entry.get().upper().strip()
        self.guess_entry.delete(0, tk.END)
        if len(guess) != 1 or not guess.isalpha():
            self.set_message("Please enter a single letter.",
                             ACCENT_WARNING, "!")
            return
        if guess in self.guessed_letters:
            self.set_message(f"Already guessed '{guess}'.",
                             ACCENT_WARNING, "!")
            return
        self.guessed_letters.append(guess)
        if guess in self.word:
            self.set_message(f"'{guess}' is in the word.",
                             ACCENT_SUCCESS, "✓")
            self.flash(FB_SUCCESS)
            self.root.bell()
        else:
            self.tries_left -= 1
            self.streak = 0
            self.set_message(f"'{guess}' is not in the word.",
                             ACCENT_DANGER, "✕")
            self.flash(FB_DANGER)
            self.root.bell()
        self.word_label.config(text=self.get_display_word())
        self.update_stats()
        if all(l in self.guessed_letters for l in self.word):
            self.on_word_solved()
            return
        if self.tries_left <= 0:
            self.game_over = True
            self.cancel_timer()
            self.set_message(f"Game over. The word was {self.word}",
                             ACCENT_DANGER, "✕")
            self.flash(FB_DANGER)
            self.save_current_score(self.current_level_name())
            self.show_game_over_panel()
    def on_word_solved(self):
        self.cancel_timer()
        elapsed = (time.time() - self.round_start_time
                   if self.round_start_time else 99)
        self.score += 10
        self.words_won_in_level += 1
        self.total_words_won += 1
        self.streak += 1
        self.update_stats()
        self.set_message(f"Correct! The word was {self.word}",
                         ACCENT_SUCCESS, "★")
        self.flash(FB_SUCCESS)
        newly = []
        if "first_win" not in self.achievements:
            self.unlock_achievement("first_win")
            newly.append("first_win")
        if self.streak >= 5 and "streak_5" not in self.achievements:
            self.unlock_achievement("streak_5")
            newly.append("streak_5")
        if self.hint_used_this_round and "hint_master" not in self.achievements:
            self.unlock_achievement("hint_master")
            newly.append("hint_master")
        if elapsed < 5 and "speed_solver" not in self.achievements:
            self.unlock_achievement("speed_solver")
            newly.append("speed_solver")
        if self.tries_left == 1 and "survivor" not in self.achievements:
            self.unlock_achievement("survivor")
            newly.append("survivor")
        if (self.total_words_won >= TOTAL_WORDS_TO_WIN
                and "champion" not in self.achievements):
            self.unlock_achievement("champion")
            newly.append("champion")
        if newly:
            names = " ".join(
                next(a["icon"] for a in ACHIEVEMENTS if a["id"] == n)
                for n in newly)
            self.set_message(
                f"Correct! {self.word}  —  Unlocked: {names}",
                ACCENT_GOLD, "★")
        if self.total_words_won >= TOTAL_WORDS_TO_WIN:
            self.root.after(1400, self.show_victory_screen)
            return
        if self.words_won_in_level >= self.current_level_quota():
            if self.difficulty_index < len(DIFFICULTY_PLAN) - 1:
                self.difficulty_index += 1
                self.words_won_in_level = 0
                self.root.after(1300, self.announce_level_up)
                return
        self.root.after(1400, self.new_round_ui)
    def unlock_achievement(self, ach_id):
        self.achievements.add(ach_id)
        self.all_achievements.add(ach_id)
        lbl = self.ach_labels.get(ach_id)
        if lbl is not None:
            try:
                lbl.config(fg=ACCENT_GOLD)
            except tk.TclError:
                pass
        try:
            self.ach_bar.config(bg=FB_SUCCESS)
            self.root.after(260, lambda: self.ach_bar.config(bg=BG_MAIN))
        except tk.TclError:
            pass

    def announce_level_up(self):
        self.update_level_label()
        self.update_stats()
        self.set_message(
            f"Level up! Now on {self.current_level_name()}.",
            ACCENT_SUCCESS, "▲")
        self.flash(FB_SUCCESS)
        self.root.after(1300, self.new_round_ui)
    def give_hint(self):
        if self.paused:
            self.set_message("Game is paused. Press Space to resume.",
                             ACCENT_HINT, "⏸")
            return
        if self.game_over:
            self.set_message("Game is over. Press Restart to play again.",
                             ACCENT_DANGER, "✕")
            return
        if self.hint_used:
            self.set_message("Hint already used this round.",
                             ACCENT_WARNING, "!")
            return
        unrevealed = [l for l in self.word if l not in self.guessed_letters]
        if unrevealed:
            self.guessed_letters.append(unrevealed[0])
            self.hint_used = True
            self.hint_used_this_round = True
            self.score -= 10
            self.word_label.config(text=self.get_display_word())
            self.update_stats()
            self.set_message(
                f"Hint: revealed '{unrevealed[0]}'  (−10)",
                ACCENT_HINT, "?")
            self.flash(FB_HINT)
            if all(l in self.guessed_letters for l in self.word):
                self.on_word_solved()

    def new_round_ui(self):
        if self.game_over:
            return
        self.new_round()
        self.word_label.config(text=self.get_display_word())
        self.emoji_label.config(text=self.emoji)
        self.update_level_label()
        self.update_stats()
        self.set_message("New word. Enter a letter.",
                         ACCENT_PRIMARY, "")
        self.guess_entry.config(state="normal")
        self.guess_entry.focus()
        self.start_timer()

    def restart_game(self):
        self.cancel_timer()
        self.start_game()

    def go_to_menu(self):
        self.cancel_timer()
        self.show_menu()
    def set_message(self, text, color, icon):
        self.message_label.config(text=text, fg=color)
        self.reaction_label.config(text=icon, fg=color)
    def flash(self, target_bg, steps=12, delay=28):
        if self.flash_job is not None:
            try:
                self.root.after_cancel(self.flash_job)
            except Exception:
                pass
            self.flash_job = None

        def step(i):
            if i > steps * 2:
                try:
                    self.puzzle_card.config(bg=BG_CARD)
                    self.emoji_label.config(bg=BG_CARD)
                    self.word_label.config(bg=BG_CARD)
                except tk.TclError:
                    pass
                self.flash_job = None
                return
            if i <= steps:
                ratio = i / steps
                color = self._blend(target_bg, BG_CARD, ratio)
            else:
                ratio = (i - steps) / steps
                color = self._blend(BG_CARD, target_bg, ratio)
            try:
                self.puzzle_card.config(bg=color)
                self.emoji_label.config(bg=color)
                self.word_label.config(bg=color)
            except tk.TclError:
                return
            self.flash_job = self.root.after(delay, lambda: step(i + 1))
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
        return self._rgb_to_hex(
            tuple(int(a[i] + (b[i] - a[i]) * ratio) for i in range(3)))
    def save_current_score(self, level_reached):
        if not self.score_saved:
            lb.save_score(self.player_name, self.score, level_reached)
            self.score_saved = True
    #   VICTORY SCREEN
    def show_victory_screen(self):
        self.cancel_timer()
        self.save_current_score("Champion")
        self.clear_root()
        self.root.configure(bg=BG_MAIN)
        self.root.geometry("780x680")
        container = tk.Frame(self.root, bg=BG_MAIN)
        container.pack(fill="both", expand=True, padx=60, pady=24)
        card = self.make_card(container, border=ACCENT_GOLD)
        card.pack(fill="x")
        tk.Label(card, text="★", font=("Segoe UI", 46, "bold"),
                 bg=BG_CARD, fg=ACCENT_GOLD).pack(pady=(24, 4))
        tk.Label(card, text="YOU ARE THE CHAMPION",
                 font=FONT_WIN_TITLE,
                 bg=BG_CARD, fg=TEXT_PRIMARY).pack(pady=(0, 4))
        tk.Label(card, text="You completed all three levels",
                 font=FONT_WIN_SUB, bg=BG_CARD,
                 fg=TEXT_SECONDARY).pack(pady=(0, 16))
        self.divider(card, pady=4)
        stats = tk.Frame(card, bg=BG_CARD)
        stats.pack(pady=14, padx=32, fill="x")
        stats.columnconfigure(0, weight=1)
        stats.columnconfigure(1, weight=1)
        self._win_stat(stats, 0, "FINAL SCORE", str(self.score),
                       ACCENT_SUCCESS)
        self._win_stat(stats, 1, "WORDS WON",
                       str(self.total_words_won), ACCENT_WARNING)
        ach_frame = tk.Frame(card, bg=BG_CARD)
        ach_frame.pack(pady=(4, 10))
        unlocked_count = 0
        for ach in ACHIEVEMENTS:
            if ach["id"] in self.achievements:
                tk.Label(ach_frame, text=ach["icon"],
                         font=("Segoe UI Emoji", 18),
                         bg=BG_CARD,
                         fg=ACCENT_GOLD).pack(side="left", padx=4)
                unlocked_count += 1
        if unlocked_count == 0:
            tk.Label(ach_frame, text="No achievements this run",
                     font=("Segoe UI", 9, "italic"),
                     bg=BG_CARD, fg=TEXT_MUTED).pack()
        tk.Label(card, text="Well played.",
                 font=("Segoe UI", 10, "italic"),
                 bg=BG_CARD, fg=TEXT_MUTED).pack(pady=(0, 18))
        btn_row = tk.Frame(card, bg=BG_CARD)
        btn_row.pack(fill="x", padx=26, pady=(0, 20))
        btn_row.columnconfigure(0, weight=1)
        btn_row.columnconfigure(1, weight=1)
        self.make_button(btn_row, "PLAY AGAIN", self.start_game,
                         bg=ACCENT_SUCCESS, hover=ACCENT_SUCCESS_H,
                         font=("Segoe UI", 12, "bold"),
                         padx=12, pady=11).grid(
                         row=0, column=0, sticky="ew", padx=(0, 6))
        # Victory screen button → show ONLY this round's achievements
        self.make_button(btn_row, "🎖  ROUND ACHIEVEMENTS",
                         lambda: self.show_achievements(only_unlocked=True),
                         bg=ACCENT_WARNING, hover=ACCENT_WARNING_H,
                         font=("Segoe UI", 12, "bold"),
                         padx=12, pady=11).grid(
                         row=0, column=1, sticky="ew", padx=(6, 0))
        self.make_button(card, "🏠  BACK TO MENU", self.show_menu,
                         bg="#475569", hover="#334155",
                         font=("Segoe UI", 12, "bold"),
                         padx=12, pady=12).pack(
                         fill="x", padx=26, pady=(0, 24))
    def _win_stat(self, parent, col, label, value, color):
        parent.columnconfigure(col, weight=1)
        tile = tk.Frame(parent, bg=BG_CARD_ALT,
                        highlightbackground=BORDER_SUBTLE,
                        highlightthickness=1)
        tile.grid(row=0, column=col, padx=8, sticky="nsew")
        tk.Label(tile, text=label, font=FONT_SECTION,
                 bg=BG_CARD_ALT, fg=TEXT_MUTED).pack(pady=(12, 4))
        tk.Label(tile, text=value, font=("Segoe UI", 22, "bold"),
                 bg=BG_CARD_ALT, fg=color).pack(pady=(0, 12))
if __name__ == "__main__":
    root = tk.Tk()
    app = HangmanApp(root)
    root.mainloop()