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
✅ |-|-| scoring.py
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
- Fix the Display.
- Test game flow.
- ...

---
# Notes & Ideas
...

---
# Latest Changes
Implemented player modules and started working on the game visuals.

- Implemented missing `BasePlayer` functionality and docstrings.
- Implemented `UserPlayer` class.
- Implemented `RandomPlayer` class.
- Started implementation of the `Display` class.
- Updated the `Game` class with display and player logic.
- Updated TODO.