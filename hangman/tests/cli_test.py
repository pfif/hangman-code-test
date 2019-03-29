from unittest.mock import MagicMock

import pytest

from hangman.src.cli import event, render


# Testing event()
def test_menu_press_e_key():
    state = {
        "current_screen": "menu"
    }
    assert event("e", state) == ("start_game", ())


def test_menu_press_key_left():
    state = {
        "current_screen": "menu"
    }
    assert event("KEY_LEFT", state) == ("start_game", ())


def test_game_press_key_e():
    state = {
        "current_screen": "game"
    }
    assert event("e", state) == ("input_letter", ("e",))


def test_game_press_key_three():
    state = {
        "current_screen": "game"
    }
    assert event("3", state) == ("input_letter", ("3",))


def test_game_press_key_left():
    state = {
        "current_screen": "game"
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
        "current_screen": "game",
        "game": {
            "displayed_letters": displayed_letter,
            "input_letters": {}
        }
    }

    render(state, stdscr)

    stdscr.addstr.assert_any_call(2, 0, expected_string)


@pytest.mark.parametrize("input_letters,expected_string", [
    ({}, ""),
    ({"a", "e", "p"}, "a, e, p")
])
def test_render_guessed_letters(input_letters, expected_string):
    stdscr = MagicMock()
    state = {
        "current_screen": "game",
        "game": {
            "displayed_letters": [],
            "input_letters": input_letters
        }
    }
    render(state, stdscr)
    stdscr.addstr.assert_any_call(
        4, 0, "Guessed letters: " + expected_string)
