from random import choice

WORDS = ["3dhubs", "marvin", "print", "filament", "order", "layer"]


def initial_state():
    return {
        "current_screen": "menu",
    }


def start_game(state):
    state["current_screen"] = "game"

    word = choice(WORDS)

    state["game"] = {
        "word": word,
        "displayed_letters": hide_letters_from_word(word, [])
    }

    return state


def hide_letters_from_word(word, foundletters):
    return [(letter if letter in foundletters else None) for letter in word]
