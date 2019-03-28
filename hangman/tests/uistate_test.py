import pytest

from hangman.src.uistate import (
    initial_state, start_game, hide_letters_from_word, input_letter)


# Initial state
def test_initial_state_current_screen_is_menu():
    assert "current_screen" in initial_state()
    assert "menu" == initial_state()["current_screen"]


# Hide letters from word
@pytest.mark.parametrize("word,foundletters,expected", [
    ("boogie", [], [None for i in range(8)]),
    ("boogie", ["o"], [None, "o", "o", None, None, None]),
    ("boogie", ["o", "i"], [None, "o", "o", None, "i", None]),
    ("boogie", ["b", "o", "g", "i", "e"], ["b", "o", "o", "g", "i", "e"]),
])
def hide_letters_from_word_tests(word, foundletters, expected):
    assert hide_letters_from_word(word, foundletters) == expected


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


# Input letter
def test_input_letter_empty_input_set():
    state = {
        "game": {
            "word": "boogie",
            "displayed_letters": [None, None, None, None, None, None],
            "input_letters": set()
        }
    }

    assert input_letter(state, "o")["game"]["input_letters"] == {"o"}


def test_input_letter_prefilled_set():
    state = {
        "game": {
            "word": "boogie",
            "displayed_letters": ["b", None, None, None, None, None],
            "input_letters": {"b"}
        }
    }

    assert input_letter(state, "o")["game"]["input_letters"] == {"o", "b"}


def test_input_letter_set_change_displayed_letters():
    state = {
        "game": {
            "word": "boogie",
            "displayed_letters": ["b", None, None, None, None, None],
            "input_letters": {"b"}
        }
    }

    assert input_letter(state, "o")["game"]["displayed_letters"] == [
        "b", "o", "o", None, None, None]
