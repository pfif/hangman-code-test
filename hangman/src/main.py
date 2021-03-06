from time import sleep
from hangman.src import uistate
from hangman.src import cli as uiinterpreter


def main():
    with uiinterpreter.initialization() as window:
        state = uistate.initial_state()
        uiinterpreter.initialization()

        while(True):
            event = uiinterpreter.current_event(window, state)
            if event:
                event_name, event_args = event
                state = getattr(uistate, event_name)(state, *event_args)

            uiinterpreter.render(state, window)
            sleep(0.016)  # Limit the game to 60fps and prevents too many CPU operation


if __name__ == "__main__":
    main()
