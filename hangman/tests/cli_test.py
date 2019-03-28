from hangman.src.cli import event


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
