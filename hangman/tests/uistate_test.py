from copy import deepcopy
from unittest.mock import patch

import pytest

from hangman.tests import STATE_MENU, STATE_IN_GAME
from hangman.src.uistate import (
    initial_state, start_game, input_letter, pass_screen)


# Initial state
def test_initial_state_current_screen_is_menu():
    assert "menu" == initial_state()["current_screen"]
    assert initial_state()["highscore"] is None


# Start Game
def test_start_game_current_screen_is_game():
    assert "game" == start_game(STATE_MENU)["current_screen"]


def test_start_game_default_value():
    assert set() == start_game(STATE_MENU)["game"]["input_letters"]
    assert "main" == start_game(STATE_MENU)["game"]["mode"]
    assert 100 == start_game(STATE_MENU)["game"]["score"]


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
    state["game"]["lives"] = 1

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


@pytest.mark.parametrize("current_score,letter,expected_new_score", [
    (100, "r", 80),
    (100, "o", 100),
    (20, "r", 0),
])
def test_compute_new_score(current_score, letter, expected_new_score):
    state = deepcopy(STATE_IN_GAME)
    state["game"]["word"] = "boogie"
    state["game"]["score"] = current_score

    assert input_letter(state, letter)["game"]["score"] == expected_new_score


@pytest.mark.parametrize("current_highscore,current_score,new_highscore", [
    (None, 80, 80),
    (None, 100, 100),
    (None, 0, 0),
    (100, 80, 100),
    (50, 100, 100),
])
def test_input_letter_change_highscore(
        current_highscore, current_score, new_highscore):
    state = deepcopy(STATE_IN_GAME)
    # The player is about to win
    state["game"]["word"] = "boogie"
    state["game"]["input_letters"] = {"b", "o", "g", "i"}

    state["game"]["score"] = current_score
    state["highscore"] = current_highscore

    assert input_letter(state, "e")["highscore"] == new_highscore


def test_input_letter_keep_highscore():
    state = deepcopy(STATE_IN_GAME)
    # The player is not about to win
    state["game"]["word"] = "boogie"
    state["game"]["input_letters"] = {"b", "o", "g"}

    state["game"]["score"] = "100"
    state["highscore"] = "20"

    assert input_letter(state, "e")["highscore"] == "20"


@pytest.mark.parametrize("remaining_lives, displayed_letters", [
    (1, ["b", "o", "o", "g", "i", "e"]),
    (3, ["b", "o", "o", "g", None, None])
])
def test_input_letter_show_letters_when_loosing(
        remaining_lives, displayed_letters):
    state = deepcopy(STATE_IN_GAME)

    # The player is about to loose
    state["game"]["word"] = "boogie"
    state["game"]["displayed_letters"] = ["b", "o", "o", "g", None, None]
    state["game"]["input_letters"] = {"b", "o", "g"}
    state["game"]["lives"] = remaining_lives

    assert input_letter(state, "r")["game"]["displayed_letters"] == (
        displayed_letters)


# Pass screen
def test_pass_screen_to_menu():
    state = deepcopy(STATE_IN_GAME)
    state["game"]["mode"] = "end_screen"

    assert pass_screen(state)["current_screen"] == "menu"
