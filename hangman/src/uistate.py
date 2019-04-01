from random import choice

WORDS = open("words", "r").read().splitlines()


def initial_state():
    return {
        "current_screen": "menu",
        "highscore": None
    }


# Events
def start_game(state):
    state["current_screen"] = "game"

    word = choice(WORDS).lower()

    state["game"] = {
        "mode": "main",
        "word": word,
        "input_letters": set(),
        "lives": 10,
        "score": 100
    }

    state = hide_letters_from_word(state)

    return state


def input_letter(state, letter):
    state["game"]["input_letters"].add(letter)
    state = compute_remaining_lives_and_score(state, letter)
    state = hide_letters_from_word(state)
    state = end_game_if_lives_too_low(state)
    state = end_game_if_word_found(state)
    return state


def pass_screen(state):
    state["current_screen"] = "menu"
    return state


# Complex state modifiers

def hide_letters_from_word(state):
    word = state["game"]["word"]
    if state["game"]["lives"] > 0:
        input_letters = state["game"]["input_letters"]
    else:
        input_letters = set(word)

    state["game"]["displayed_letters"] = (
        [(letter if letter in input_letters else None) for letter in word])

    return state


def compute_remaining_lives_and_score(state, letter):
    word = state["game"]["word"]
    current_lives = state["game"]["lives"]

    if letter not in word and current_lives > 0:
        state["game"]["lives"] -= 1
        state["game"]["score"] -= 20

    return state


def end_game_if_lives_too_low(state):
    if state["game"]["lives"] == 0:
        state = end_game(state, "You loose! (Press any key to continue)")
    return state


def end_game_if_word_found(state):
    word = state["game"]["word"]
    input_letters = state["game"]["input_letters"]

    if set(word).issubset(input_letters):
        state = end_game(state, "You win! (Press any key to continue)")
    return state


def end_game(state, sentence):
    state["game"]["mode"] = "end_screen"
    state["game"]["end_screen_sentence"] = sentence

    highscore = state["highscore"]
    score = state["game"]["score"]
    state["highscore"] = (
        max(highscore, score) if highscore is not None else score)

    return state
