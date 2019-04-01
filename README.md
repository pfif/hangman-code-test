# Hangman (a code test)
[![CircleCI](https://circleci.com/gh/pfif/hangman-code-test.svg?style=svg)](https://circleci.com/gh/pfif/hangman-code-test)

This is a hangman game that I built for a code test.

To run it, place yourself in the root directory of the repository and execute

`python -m hangman.src.main`

## Short explanation of the architecture

This program is in two parts:

- The UI Server (`hangman/src/uiserver.py`) : it provides a state of what
  should be displayed on screen. It can react to events.
- An interpreter (`hangman/src/cli.py`) : renders the UI state and read input to
  provide events to the UI server

`hangman/src/main.py` is responsible for tying them together.

One reason to split the UI server from the interpreter is that it makes it
possible to have several interpreters. For instance, there could be a CLI one and a
GUI one, or we could imagine shipping two versions of an otherwise whitelabeled
hangman.

There are unittests in the folder `hangman/test`.

