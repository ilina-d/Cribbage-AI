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
❎ |-|-| state.py
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
- Implement Scoring helper class.
- Update Game with Scoring.
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
Implemented game flow logic and helper modules.

- Implemented `Game` logic.
- Added `CardDeck` helper module for cards logic.
- Added `State` helper module for representation of game states.
- Implemented shell of `BasePlayer` class.