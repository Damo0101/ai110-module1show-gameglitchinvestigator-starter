# FIX: Refactored core game logic out of app.py into logic_utils.py so the
# UI (Streamlit) and the rules are separated and the logic can be unit-tested.
# Done with the AI assistant in agent mode; each function below was reviewed
# against the original app.py version before accepting the edit.


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    # FIX: high/low bug. The secret is always compared as an int now, and the
    # old `except TypeError` band-aid (which fell back to broken string
    # comparison, e.g. "9" > "100" -> True) was removed.
    if guess == secret:
        return "Win", "🎉 Correct!"

    # FIX: the hint messages were swapped. A guess that is too HIGH must tell
    # the player to go LOWER, and a guess that is too LOW must tell them to go
    # HIGHER. (The outcome labels were already correct; only the text/arrow
    # shown to the player was inverted.)
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
