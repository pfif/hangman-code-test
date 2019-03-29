import pytest


from hangman.src.uistate import (
    initial_state, start_game, hide_letters_from_word, input_letter,
    compute_remaining_lives, end_game_if_lives_too_low)


# Initial state
def test_initial_state_current_screen_is_menu():
    assert "current_screen" in initial_state()
    assert "menu" == initial_state()["current_screen"]


# Hide letters from word
@pytest.mark.parametrize("word,foundletters,expected", [
    ("boogie", [], [None for i in range(6)]),
    ("boogie", ["o"], [None, "o", "o", None, None, None]),
    ("boogie", ["o", "i"], [None, "o", "o", None, "i", None]),
    ("boogie", ["b", "o", "g", "i", "e"], ["b", "o", "o", "g", "i", "e"]),
])
def test_hide_letters_from_word_tests(word, foundletters, expected):
    state = {
        "game": {
            "word": word,
            "input_letters": foundletters
        }
    }
    assert hide_letters_from_word(state)["game"]["displayed_letters"] == (
        expected)


# Start Game
def test_start_game_current_screen_is_game():
    state = {
        "current_screen": "menu"
    }
    assert "game" == start_game(state)["current_screen"]


def test_start_game_keeps_state_intact():
    state = {
        "current_screen": "menu",
        "other": "value"
    }
    assert "value" == start_game(state)["other"]


def test_start_game_add_game_state():
    state = {
        "current_screen": "menu",
    }
    assert "word" in start_game(state)["game"]
    assert "displayed_letters" in start_game(state)["game"]
    assert set() == start_game(state)["game"]["input_letters"]
    assert "main" == start_game(state)["game"]["mode"]


# Input letter
def test_input_letter_empty_input_set():
    state = {
        "game": {
            "word": "boogie",
            "displayed_letters": [None, None, None, None, None, None],
            "input_letters": set(),
            "lives": 5
        }
    }

    assert input_letter(state, "o")["game"]["input_letters"] == {"o"}


def test_input_letter_prefilled_set():
    state = {
        "game": {
            "word": "boogie",
            "displayed_letters": ["b", None, None, None, None, None],
            "input_letters": {"b"},
            "lives": 5
        }
    }

    assert input_letter(state, "o")["game"]["input_letters"] == {"o", "b"}


@pytest.mark.parametrize("letter,initial_lives,expected", [
    ("b", 5, 5),
    ("r", 5, 4),
    ("a", 0, 0),
    ("b", 1, 1),
    ("o", 3, 3),
    ("x", 1, 0)
])
def test_compute_remaining_lives(letter, initial_lives, expected):
    state = {
        "game": {
            "word": "boogie",
            "lives": initial_lives
        }
    }

    assert compute_remaining_lives(state, letter)["game"]["lives"] == expected


@pytest.mark.parametrize("remaining_lives,expected_mode", [
    (1, "main"),
    (0, "end_screen"),
])
def test_end_game_if_lives_too_low_setting_mode(
        remaining_lives, expected_mode):
    state = {
        "game": {
            "mode": "main",
            "lives": remaining_lives,
        }
    }

    assert end_game_if_lives_too_low(state)["game"]["mode"] == expected_mode
