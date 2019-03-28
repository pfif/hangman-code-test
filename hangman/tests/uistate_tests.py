from hangman.src.uistate import initial_state


# Initial state
def test_initial_state_current_screen_is_menu():
    assert "current_screen" in initial_state()
    assert "menu" == initial_state()["current_screen"]
