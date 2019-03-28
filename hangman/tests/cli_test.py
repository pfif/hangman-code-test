from unittest.mock import MagicMock

import pytest

from hangman.src.cli import event, render


# Testing event()
def test_menu_press_e_key():
    state = {
        "current_screen": "menu"
    }
    assert event("e", state) == "start_game"


def test_menu_press_key_left():
    state = {
        "current_screen": "menu"
    }
    assert event("KEY_LEFT", state) == "start_game"


# Testing render
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
            "displayed_letters": displayed_letter
        }
    }

    render(state, stdscr)

    stdscr.addstr.assert_called_with(2, 0, expected_string)
