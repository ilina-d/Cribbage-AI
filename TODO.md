# Project Structure
```
❌ | main.py
❌ | README.md
✅ | TODO.md
❌ | requirements.txt
⬛ |
🔄 | utils/
⬛ |-|
❌ |-| assets/ 
🔄 |-|-| __init__.py
🔄 |-|-| display.py
⬛ |-|
❌ |-| game/
🔄 |-|-| __init__.py
🔄 |-|-| game.py
⬛ |-|
❌ |-| helpers/
🔄 |-|-| __init__.py
🔄 |-|-| card_deck.py
🔄 |-|-| scoring.py
⬛ |-|
🔄 |-| players/
✅ |-|-| __init__.py
✅ |-|-| base_player.py
✅ |-|-| user_player.py
✅ |-|-| random_player.py
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
- Finish implementing the `visuals` toggle for `Game`:
  Add it as an argument in `Display` where the `print()` function would have a
  check for the `visuals` argument, instead of having multiple if-statements in
  `Game` for every time we print the game interface.
- Add a `clear` argument to `Display.print()` as to remove constant calls to
  `clear()` and `print()`.
- Clean up the code in Display and Game.
- Continue testing game flow.
- ...

---
# Notes & Ideas
...

---
# Latest Changes
Scoring fixes and Display updates.

- Fixed `Scoring.score_run()`.
- Fixed `Scoring.score_flush()`
- Updated `Display` to show `state['crib_sums']` of current playable crib.
- Updated `Display` to show a hat next to the dealer before the discard phase.
- Made input index based, instead of rank-suit format.
- Improved input for "GO".
- Updated `Display` to show the crib when it is being scored during the show phase. 
- Fixed `Display` issues when waiting for `UserPlayer` input.