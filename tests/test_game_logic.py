from logic_utils import check_guess, parse_guess, get_range_for_difficulty


# --- Existing starter tests ---------------------------------------------
# NOTE: check_guess returns a tuple (outcome, message), which is the contract
# app.py uses ("outcome, message = check_guess(...)"). The starter versions
# compared the whole result to a bare string, so they were updated to check
# the outcome element, result[0].

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _message = check_guess(40, 50)
    assert outcome == "Too Low"


# --- New tests targeting the Bug 1 fix (high/low hint flip) --------------
# The old code cast the secret to a str on even attempts, so check_guess
# compared int vs str and produced a wrong/flipping hint (e.g. "9" > "100"
# is True as strings). These pin the correct integer behaviour.

def test_low_guess_against_high_secret_says_too_low():
    # Reproduces the reflection scenario: guess 2, secret 100 -> always too low
    outcome, _message = check_guess(2, 100)
    assert outcome == "Too Low"


def test_hint_message_points_the_right_direction():
    # A too-low guess must tell the player to go HIGHER, and a too-high guess
    # must tell them to go LOWER (the messages used to be swapped).
    _outcome_low, msg_low = check_guess(2, 50)
    assert "HIGHER" in msg_low
    _outcome_high, msg_high = check_guess(88, 50)
    assert "LOWER" in msg_high

def test_hint_is_consistent_for_repeated_guess():
    # Same guess/secret must give the same outcome every time (no flipping)
    first = check_guess(2, 100)
    second = check_guess(2, 100)
    assert first == second

def test_two_digit_vs_three_digit_not_string_compared():
    # As strings, "9" > "100" is True. As ints, 9 < 100 -> Too Low.
    outcome, _message = check_guess(9, 100)
    assert outcome == "Too Low"


# --- A couple of supporting logic tests ---------------------------------

def test_parse_guess_rejects_non_number():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert err == "That is not a number."

def test_parse_guess_accepts_integer_text():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_hard_range_is_smaller_than_normal():
    # Documents the (intentional starter) range design per difficulty.
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 100)
    assert get_range_for_difficulty("Hard") == (1, 50)
