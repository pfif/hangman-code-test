from unittest.mock import MagicMock

import pytest

from hangman.src.cli import (
    event, render_game_displayed_letters,
    sentence_guessed_letters, render_game_remaining_lives)


# Testing event()
def test_menu_press_e_key():
    state = {
        "current_screen": "menu"
    }
    assert event("e", state) == ("start_game", ())


def test_menu_press_key_left():
    state = {
        "current_screen": "menu",
        "game": {
            "mode": "main"
        }
    }
    assert event("KEY_LEFT", state) == ("start_game", ())


def test_game_press_key_e():
    state = {
        "current_screen": "game",
        "game": {
            "mode": "main"
        }
    }
    assert event("e", state) == ("input_letter", ("e",))


def test_game_press_key_three():
    state = {
        "current_screen": "game",
        "game": {
            "mode": "main"
        }
    }
    assert event("3", state) == ("input_letter", ("3",))


def test_game_press_key_left():
    state = {
        "current_screen": "game",
        "game": {
            "mode": "main"
        }
    }
    assert event("KEY_LEFT", state) is None


def test_game_end_screen_mode_press_e():
    state = {
        "current_screen": "game",
        "game": {
            "mode": "end_screen"
        }
    }
    assert event("KEY_LEFT", state) is None


# Testing render()
@pytest.mark.parametrize("displayed_letter,expected_string", [
    ([None, None, None], "_ _ _"),
    ([None, "i", None], "_ i _"),
    (["a", "i", None], "a i _"),
    (["a", "i", "g"], "a i g")
])
def test_render_word(displayed_letter, expected_string):
    stdscr = MagicMock()
    state = {
        "displayed_letters": displayed_letter,
    }

    render_game_displayed_letters(stdscr, state)

    stdscr.addstr.assert_called_with(2, 0, expected_string)


@pytest.mark.parametrize("input_letters,expected_string", [
    ({}, ""),
    ({"a", "e", "p"}, "a, e, p")
])
def test_render_guessed_letters(input_letters, expected_string):
    state = {
        "input_letters": input_letters
    }
    assert sentence_guessed_letters(state) == (
        "Guessed letters: " + expected_string)


@pytest.mark.parametrize("lives,position,string", [
    (5, 54, "| | | | |"),
    (4, 56, "| | | |"),
    (3, 58, "| | |"),
    (2, 60, "| |"),
    (1, 62, "|")
])
def test_render_game_remaining_lives(lives, position, string):
    stdscr = MagicMock()
    state = {
        "lives": lives
    }

    render_game_remaining_lives(stdscr, state, 80)

    stdscr.addstr.assert_called_with(
        0, position, "Remaining lives: " + string)
