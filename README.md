# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Describe the game's purpose.** It's a Streamlit number-guessing game. The app picks a secret number within a range that depends on the chosen difficulty (Easy 1–20, Normal 1–100, Hard 1–50), and the player guesses until they either find it or run out of attempts. After each guess the game gives a "Too High" / "Too Low" hint, tracks a score and a history of guesses, and ends on a win or when attempts run out.

- [x] **Detail which bugs you found.**
  1. **Flipping hints (state bug).** The secret was cast to a string on every even-numbered attempt, so `check_guess` compared an int to a string and fell into a hidden `except TypeError` branch that did string comparison. The same guess could say "higher" one time and "lower" the next.
  2. **Backwards hint messages.** Even once the flipping was fixed, the "Go HIGHER / Go LOWER" text was swapped — a too-low guess told the player to go *lower*, and a too-high guess told them to go *higher*.
  3. **New Game button dead after game over.** Clicking "New Game" never reset the game's `status`, so after a win or loss the `status != "playing"` guard kept calling `st.stop()` and the only way to restart was reloading the page.

- [x] **Explain what fixes you applied.**
  1. Removed the `str(secret)` cast so the secret is always compared as an int, and deleted the dead `except TypeError` band-aid in `check_guess`.
  2. Swapped the two hint messages (and their 📈/📉 arrows) so "Too High" → "Go LOWER!" and "Too Low" → "Go HIGHER!".
  3. Made the "New Game" handler reset `status` back to `"playing"` (and also reset score/history and draw the new secret from the selected difficulty's range).
  4. Refactored the four logic functions out of `app.py` into `logic_utils.py` and imported them, then added regression tests in `tests/test_game_logic.py`.

## 📸 Demo Walkthrough

A text-based record of a full sample game so anyone can follow how the fixed game behaves end-to-end without running it. (Difficulty: **Normal**, range **1–100**, **8** attempts. For this example the secret is **63**, which you can confirm in the "Developer Debug Info" expander.)

1. The app loads in Normal difficulty. The banner shows the range and attempts left, and "Developer Debug Info" reveals the secret (63).
2. User enters a guess of **40** and clicks "Submit Guess 🚀" → game returns **"Too Low" → "📈 Go HIGHER!"** (the hint now points the correct direction).
3. User enters a guess of **70** → game returns **"Too High" → "📉 Go LOWER!"**.
4. The score and the guess history update after each submission, and "Attempts left" counts down — the secret stays **63** across submissions (it no longer changes on every click).
5. User enters **63** → game returns **"🎉 Correct!"**, shows balloons, reveals the secret and the final score, and marks the game as won.
6. User clicks **"New Game 🔁"** → the game restarts in place (no page reload needed): a new secret is drawn from the current difficulty's range, and score, history, and attempts reset.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

Challenge 1 (Advanced Edge-Case Testing) — `python -m pytest tests/ -v`:

```
============================= test session starts =============================
platform win32 -- Python 3.13.7, pytest-9.1.1, pluggy-1.6.0 -- C:\Python313\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Damin\Downloads\ai110-module1show-gameglitchinvestigator-starter-main\ai110-module1show-gameglitchinvestigator-starter-main
plugins: anyio-4.14.0
collecting ... collected 10 items

tests/test_game_logic.py::test_winning_guess PASSED                      [ 10%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 20%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 30%]
tests/test_game_logic.py::test_low_guess_against_high_secret_says_too_low PASSED [ 40%]
tests/test_game_logic.py::test_hint_message_points_the_right_direction PASSED [ 50%]
tests/test_game_logic.py::test_hint_is_consistent_for_repeated_guess PASSED [ 60%]
tests/test_game_logic.py::test_two_digit_vs_three_digit_not_string_compared PASSED [ 70%]
tests/test_game_logic.py::test_parse_guess_rejects_non_number PASSED     [ 80%]
tests/test_game_logic.py::test_parse_guess_accepts_integer_text PASSED   [ 90%]
tests/test_game_logic.py::test_hard_range_is_smaller_than_normal PASSED  [100%]

============================= 10 passed in 0.07s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
