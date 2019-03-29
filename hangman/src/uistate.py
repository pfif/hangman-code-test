from random import choice

WORDS = ["3dhubs", "marvin", "print", "filament", "order", "layer"]


def initial_state():
    return {
        "current_screen": "menu",
    }


# Events
def start_game(state):
    state["current_screen"] = "game"

    word = choice(WORDS)

    state["game"] = {
        "mode": "main",
        "word": word,
        "input_letters": set(),
        "lives": 5
    }

    state = hide_letters_from_word(state)

    return state


def input_letter(state, letter):
    state["game"]["input_letters"].add(letter)
    state = hide_letters_from_word(state)
    state = compute_remaining_lives(state, letter)
    state = end_game_if_lives_too_low(state)
    state = end_game_if_word_found(state)
    return state


def pass_screen(state):
    pass


# Complex state modifiers

def hide_letters_from_word(state):
    word = state["game"]["word"]
    input_letters = state["game"]["input_letters"]

    state["game"]["displayed_letters"] = (
        [(letter if letter in input_letters else None) for letter in word])

    return state


def compute_remaining_lives(state, letter):
    word = state["game"]["word"]
    current_lives = state["game"]["lives"]

    if letter not in word and current_lives > 0:
        state["game"]["lives"] -= 1

    return state


def end_game_if_lives_too_low(state):
    if state["game"]["lives"] == 0:
        state["game"]["mode"] = "end_screen"
        state["game"]["end_screen_sentence"] = "You loose! (Press any key to continue)"  # noqa
    return state


def end_game_if_word_found(state):
    if None not in state["game"]["displayed_letters"]:
        state["game"]["mode"] = "end_screen"
        state["game"]["end_screen_sentence"] = "You win! (Press any key to continue)"  # noqa
    return state
