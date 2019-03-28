def initial_state():
    return {
        "current_screen": "menu",
    }


def start_game(state):
    state["current_screen"] = "game"
    return state
