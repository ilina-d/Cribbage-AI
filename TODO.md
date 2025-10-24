# Project Structure
```
❌ | main.py
❌ | README.md
✅ | TODO.md
❌ | requirements.txt
⬛ |
❌ | utils/
⬛ |-|
❌ |-| assets/ 
❌ |-|-| __init__.py
❌ |-|-| display.py
⬛ |-|
❌ |-| game/
❎ |-|-| __init__.py
❎ |-|-| game.py
❌ |-|-| ...
⬛ |-|
❌ |-| helpers/
❎ |-|-| __init__.py
❎ |-|-| card_deck.py
❎ |-|-| scoring.py
⬛ |-|
❌ |-| players/
❌ |-|-| __init__.py
❌ |-|-| base_player.py
❌ |-|-| user_player.py
❌ |-|-| ...
⬛ |-|
❌ |-| simulator/
❌ |-|-| __init__.py
❌ |-|-| ...
⬛ |
❌ | models/
❌ |-| ...
```

---
# TODO
- Implement BasePlayer.
- Implement RandomPlayer.
- Implement UserPlayer.
- Implement very basic Display.
- Test game flow.
- Improve Display.
- ...

---
# Notes & Ideas
...

---
# Latest Changes
Implemented scoring functionality and refactored the game state representation.

- Refactored the game state representation: 
  - Removed the `State` helper module.
  - Added a `state` dictionary to the `Game` module.
  - Moved `current_crib` variable from `Game` to `Game.state`.
  - Points are now stored in `BasePlayer`, rather than inside the state.
  - Added `check_win` function to `Game`.
  - Updated `Game` functions to work with the state representation changes.
  - Fixed errors in the `BasePlayer` module caused by the state representation changes. 
- Implemented missing `wait_after_move` functionality to the `Game` module.
- Added separate functions to the `CardDeck` module for unpacking a card's rank, suit, and worth.
- Added `Scoring` helper module for scoring different card combinations.
  - Updated `Game` class with new `Scoring` functionality.
- Minor changes to function names and docstrings.
- Updated TODO.