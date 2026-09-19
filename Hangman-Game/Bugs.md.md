# BUGS.md — Bug Log for Emoji Hangman

**Project:** Emoji Hangman (CSE 2216)
**Maintainer:** <Your Name>
**Format:** `[ID] | Status | Severity | Description | Fix commit`

---

## Legend
- **Status:** `OPEN`, `FIXED`, `WONTFIX`, `DUPLICATE`
- **Severity:** `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, `COSMETIC`

---

## Bug Log

| ID  | Status | Severity | Description | Root Cause | Fix |
|-----|--------|----------|-------------|------------|-----|
| B001 | FIXED | HIGH | Timer kept running after game over | `cancel_timer()` not called on `tries_left <= 0` | Call `cancel_timer()` before `show_game_over_panel()` |
| B002 | FIXED | HIGH | Empty guess input accepted silently | No length/alpha validation | Added `len(guess) != 1 or not guess.isalpha()` check |
| B003 | FIXED | MEDIUM | Repeated letters scored twice | `guessed_letters` didn't guard duplicates | Added `if guess in self.guessed_letters: return` |
| B004 | FIXED | MEDIUM | Hint could reveal a letter already revealed | Hint picked `unrevealed[0]` but if list was empty it crashed | Guard `if unrevealed:` before use |
| B005 | FIXED | MEDIUM | Negative score after using hint at 0 points | No floor on score | (Design decision: allowed; shows player penalty) |
| B006 | FIXED | LOW | Same word repeated in a session | `used_words` not updated on level change | Reset pool per level; fallback re-uses when exhausted |
| B007 | FIXED | LOW | Achievement bar not reset between games | `self.achievements` was only reset in some paths | Always reset in `start_game()` |
| B008 | FIXED | LOW | Leaderboard row misaligned for long names | No truncation | Truncate name to 14 chars in list view |
| B009 | FIXED | LOW | Clear-leaderboard dialog could open twice | Button had no disabled state | Used `grab_set()` on Toplevel |
| B010 | FIXED | COSMETIC | Menu buttons overflowed on smaller screens | Fixed padding 110px | Switched to grid with column weights |
| B011 | FIXED | COSMETIC | Emoji rendering differed on macOS/Linux | Font hardcoded to `Segoe UI Emoji` | Left as-is (Windows target) — noted in README |
| B012 | FIXED | MEDIUM | Corrupted scores.json crashed the leaderboard screen | No try/except around JSON load | Added `_load_raw()` with `_backup_corrupted()` |
| B013 | FIXED | HIGH | Timer could fire after switching to menu | `after_cancel()` was called on stale job id | Track `self.timer_job` and always cancel in `cancel_timer()` |
| B014 | FIXED | MEDIUM | Space bar triggered pause even when typing in Entry | Global bind caught all spaces | Scoped to only fire when game is active |
| B015 | FIXED | LOW | `restart_game` didn't reset `hint_used_this_round` | Forgot to reset flag | Reset in `start_game()` |

---

## Peer Testing Feedback (Round 1 — 3 testers)

| Tester | Device | Issue Reported | Result |
|--------|--------|----------------|--------|
| A | Windows 11 | "Hint button does nothing on second use" | B004 — FIXED |
| A | Windows 11 | "Score went negative" | B005 — WONTFIX (intended) |
| B | Windows 10 | "Leaderboard didn't save when I closed with X" | Not a bug — file saved on game over only |
| B | Windows 10 | "Pause button text stayed red after resume" | Cosmetic tweak applied |
| C | Windows 11 | "Emoji didn't show on last word" | Font fallback — not reproducible |

---

## Regression Test Checklist (run after each fix)

- [x] Start a new game with empty name → default "Player"
- [x] Start a new game with 50-char name → truncated to 20
- [x] Guess a correct letter → score increases by 10
- [x] Guess a wrong letter → life lost, hearts update
- [x] Use hint → letter revealed, −10 score
- [x] Use hint twice in one round → blocked
- [x] Let timer run out → life lost
- [x] Lose all 5 lives → game-over panel
- [x] Win 10 words → victory screen
- [x] Achievements unlock and appear in both views
- [x] Leaderboard displays top 10 with medals
- [x] Clear leaderboard → confirmation → empty list
- [x] Delete scores.json → game still plays, no crash
- [x] Corrupt scores.json with garbage → backup created, no crash
- [x] Press Escape during game → returns to menu
- [x] Press Space during game → pause/unpause
- [x] Pause button reflects state correctly
- [x] Achievement screen fits fully in 780×680