from copy import deepcopy
from unittest.mock import patch

import pytest

from hangman.tests import STATE_MENU, STATE_IN_GAME
from hangman.src.uistate import (
    initial_state, start_game, input_letter, pass_screen)


# Initial state
def test_initial_state_current_screen_is_menu():
    assert "current_screen" in initial_state()
    assert "menu" == initial_state()["current_screen"]


# Start Game
def test_start_game_current_screen_is_game():
    assert "game" == start_game(STATE_MENU)["current_screen"]


def test_start_game_default_value():
    assert set() == start_game(STATE_MENU)["game"]["input_letters"]
    assert "main" == start_game(STATE_MENU)["game"]["mode"]


def test_start_game_choose_random_word():
    with patch("hangman.src.uistate.choice", side_effect=["boogie"]):
        assert start_game(STATE_MENU)["game"]["word"] == "boogie"


def test_start_game_choose_filled_default_state_with_nones():
    with patch("hangman.src.uistate.choice", side_effect=["boogie"]):
        assert start_game(STATE_MENU)["game"]["displayed_letters"] == [
            None, None, None, None, None, None]


# Input letter
@pytest.mark.parametrize("input_letters,letter,expected", [
    (set(), "o", [None, "o", "o", None, None, None]),
    ({"o"}, "i", [None, "o", "o", None, "i", None]),
    ({"b", "o", "g", "i"}, "e", ["b", "o", "o", "g", "i", "e"]),
])
def test_input_letter_displayed_letters(input_letters, letter, expected):
    state = deepcopy(STATE_IN_GAME)
    state["game"]["word"] = "boogie"
    state["game"]["input_letters"] = input_letters

    assert input_letter(state, letter)["game"]["displayed_letters"] == expected


def test_input_letter_add_letter():
    state = deepcopy(STATE_IN_GAME)
    state["game"]["input_letters"] = set()

    assert input_letter(state, "o")["game"]["input_letters"] == {"o"}


def test_input_letter_prefilled_set():
    state = deepcopy(STATE_IN_GAME)
    state["game"]["input_letters"] = {"b"}

    assert input_letter(state, "o")["game"]["input_letters"] == {"o", "b"}


@pytest.mark.parametrize("letter,initial_lives,expected", [
    ("b", 5, 5),
    ("r", 5, 4),
    ("a", 0, 0),
    ("b", 1, 1),
    ("o", 3, 3),
    ("x", 1, 0)
])
def test_input_letter_compute_remaining_lives(letter, initial_lives, expected):
    state = deepcopy(STATE_IN_GAME)
    state["game"]["lives"] = initial_lives

    assert input_letter(state, letter)["game"]["lives"] == expected


@pytest.mark.parametrize("remaining_lives,expected_mode", [
    (2, "main"),
    (1, "end_screen"),
])
def test_input_letter_end_of_lives(remaining_lives, expected_mode):
    state = deepcopy(STATE_IN_GAME)
    state["game"]["word"] = "boogie"
    state["game"]["lives"] = remaining_lives

    assert input_letter(state, "r")["game"]["mode"] == expected_mode


def test_input_letter_end_of_live_sentence():
    state = deepcopy(STATE_IN_GAME)
    state["game"]["word"] = "boogie"
    state["game"]["lives"] = 0

    assert input_letter(state, "r")["game"]["end_screen_sentence"] == "You loose! (Press any key to continue)"  # noqa


@pytest.mark.parametrize("inputed_letters, expected_mode", [
    ({"b", "o"}, "main"),
    ({"b", "o", "g", "i"}, "end_screen"),
])
def test_input_letter_word_was_wound(inputed_letters, expected_mode):
    state = deepcopy(STATE_IN_GAME)
    state["game"]["word"] = "boogie"
    state["game"]["input_letters"] = inputed_letters

    assert input_letter(state, "e")["game"]["mode"] == expected_mode


def test_pass_screen_to_menu():
    state = deepcopy(STATE_IN_GAME)
    state["game"]["mode"] = "end_screen"

    assert pass_screen(state)["current_screen"] == "menu"
