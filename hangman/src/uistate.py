from random import choice

WORDS = ["3dhubs", "marvin", "print", "filament", "order", "layer"]


# Events
def initial_state():
    return {
        "current_screen": "menu",
    }


def start_game(state):
    state["current_screen"] = "game"

    word = choice(WORDS)

    state["game"] = {
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
    return state


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
"b"
