from copy import deepcopy
from unittest.mock import MagicMock

import pytest

from hangman.src.cli import event, render
from hangman.tests import STATE_MENU, STATE_IN_GAME


# Testing event()
def test_menu_press_e_key():
    assert event("e", STATE_MENU) == ("start_game", ())


def test_menu_press_key_left():
    state = deepcopy(STATE_MENU)
    assert event("KEY_LEFT", state) == ("start_game", ())


def test_game_press_key_e():
    state = deepcopy(STATE_IN_GAME)
    state["game"]["mode"] = "main"
    assert event("e", state) == ("input_letter", ("e",))


def test_game_press_key_three():
    state = deepcopy(STATE_IN_GAME)
    state["game"]["mode"] = "main"
    assert event("3", state) == ("input_letter", ("3",))


def test_game_press_key_left():
    state = deepcopy(STATE_IN_GAME)
    state["game"]["mode"] = "main"
    assert event("KEY_LEFT", state) is None


def test_game_end_screen_mode_press_e():
    state = deepcopy(STATE_IN_GAME)
    state["game"]["mode"] = "end_screen"
    assert event("e", state) == ("pass_screen", ())


def test_game_end_screen_mode_press_key_left():
    state = deepcopy(STATE_IN_GAME)
    state["game"]["mode"] = "end_screen"
    assert event("KEY_LEFT", state) == ("pass_screen", ())


# Testing render()
@pytest.mark.parametrize("displayed_letter,expected_string", [
    ([None, None, None], "_ _ _"),
    ([None, "i", None], "_ i _"),
    (["a", "i", None], "a i _"),
    (["a", "i", "g"], "a i g")
])
def test_render_word(displayed_letter, expected_string):
    stdscr = MagicMock()

    state = deepcopy(STATE_IN_GAME)
    state["game"]["displayed_letters"] = displayed_letter

    render(state, stdscr)
    stdscr.addstr.assert_any_call(2, 0, expected_string)


@pytest.mark.parametrize("input_letters,expected_string", [
    ({}, ""),
    ({"a", "e", "p"}, "a, e, p")
])
def test_render_guessed_letters(input_letters, expected_string):
    stdscr = MagicMock()

    state = deepcopy(STATE_IN_GAME)
    state["game"]["input_letters"] = input_letters

    render(state, stdscr)
    stdscr.addstr.assert_any_call(4, 0, "Guessed letters: " + expected_string)


@pytest.mark.parametrize("lives,position,string", [
    (5, 54, "| | | | |"),
    (4, 56, "| | | |"),
    (3, 58, "| | |"),
    (2, 60, "| |"),
    (1, 62, "|")
])
def test_render_game_remaining_lives(lives, position, string):
    stdscr = MagicMock()

    state = deepcopy(STATE_IN_GAME)
    state["game"]["lives"] = lives

    render(state, stdscr)

    stdscr.addstr.assert_any_call(0, position, "Remaining lives: " + string)


def test_print_score():
    stdscr = MagicMock()

    state = deepcopy(STATE_IN_GAME)
    state["game"]["score"] = 40

    render(state, stdscr)

    stdscr.addstr.assert_any_call(0, 0, "Score: 40")
