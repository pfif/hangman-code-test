from hangman.src.uistate import initial_state, start_game


# Initial state
def test_initial_state_current_screen_is_menu():
    assert "current_screen" in initial_state()
    assert "menu" == initial_state()["current_screen"]


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
