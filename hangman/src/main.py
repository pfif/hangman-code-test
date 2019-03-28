from hangman.src import uistate
from hangman.src import cli as uiinterpreter


def main():
    with uiinterpreter.initialization() as window:
        state = uistate.initial_state()
        uiinterpreter.initialization()

        while(True):
            event = uiinterpreter.current_event()
            if event:
                state = getattr(uistate, event)(state)

            uiinterpreter.render(state, window)


if __name__ == "__main__":
    main()
