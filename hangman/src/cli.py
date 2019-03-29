from contextlib import contextmanager
import curses


@contextmanager
def initialization():
    try:
        # Initialize curses
        stdscr = curses.initscr()

        # Setup input
        curses.noecho()
        curses.cbreak()
        stdscr.nodelay(1)
        stdscr.keypad(1)

        yield stdscr
    finally:
        # Set everything back to normal
        if 'stdscr' in locals():
            stdscr.keypad(0)
            curses.echo()
            curses.nocbreak()
            curses.endwin()


# Input
def current_event(stdsrc, state):
    try:
        key = stdsrc.getkey()
    except curses.error:
        pass
    else:
        return event(key, state)


def event(key, state):
    if state["current_screen"] == "menu":
        return event_menu(key)

    if state["current_screen"] == "game":
        return event_game(key)


def event_menu(key):
    return ("start_game", ())


def event_game(key):
    if key in "abcdefghijklmnopqrstuvwxyz1234567890":
        return ("input_letter", (key,))


# GUI
def render(state, stdscr):
    stdscr.erase()

    if state["current_screen"] == "menu":
        render_menu(stdscr)

    if state["current_screen"] == "game":
        render_game(stdscr, state["game"])

    stdscr.refresh()


def render_menu(stdscr):
    stdscr.addstr(0, 0, "Darkest Prisoner")
    stdscr.addstr(2, 0, "Press any key to start")


def render_game(stdscr, state):
    stdscr.addstr(0, 0, 'Guess this word')
    render_game_displayed_letters(stdscr, state)
    render_game_remaining_lives(stdscr, state, 80)
    render_game_guessed_letters(stdscr, state)


def render_game_displayed_letters(stdscr, state):
    stdscr.addstr(2, 0, " ".join(
        [(letter if letter is not None else "_")
         for letter in state["displayed_letters"]]))


def render_game_guessed_letters(stdscr, state):
    stdscr.addstr(4, 0, "Guessed letters: " + ", ".join(
        sorted(state["input_letters"])))


def render_game_remaining_lives(stdsrc, state, width):
    lives_string = "Remaining lives: " + " ".join(["|"] * state["lives"])

    stdsrc.addstr(0, width - len(lives_string), lives_string)
