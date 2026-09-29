from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    is_guess_in_range,
    parse_guess,
    update_score,
)


def test_difficulty_ranges():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 50)
    assert get_range_for_difficulty("Hard") == (1, 100)


def test_parse_guess():
    assert parse_guess(" 42 ") == (True, 42, None)
    assert parse_guess("") == (False, None, "Enter a guess.")
    assert parse_guess("9.8")[0] is False


def test_guess_range_is_inclusive():
    assert is_guess_in_range(1, 1, 20)
    assert is_guess_in_range(20, 1, 20)
    assert not is_guess_in_range(0, 1, 20)
    assert not is_guess_in_range(21, 1, 20)

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


def test_score_decreases_by_twenty_per_attempt():
    assert update_score(0, "Win", 1) == 100
    assert update_score(0, "Win", 2) == 80
    assert update_score(0, "Win", 3) == 60


def test_incorrect_guess_does_not_change_score():
    assert update_score(25, "Too High", 2) == 25
    assert update_score(25, "Too Low", 3) == 25
