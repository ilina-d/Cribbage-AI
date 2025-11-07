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
- Fix `Scoring.score_run()` sometimes finding runs where there aren't any.
- Finish implementing the `visuals` toggle for `Game`:
  Add it as an argument in `Display` where the `print()` function would have a
  check for the `visuals` argument, instead of having multiple if-statements in
  `Game` for every time we print the game interface.
- Add a `clear` argument to `Display.print()` as to remove constant calls to
  `clear()` and `print()`.
- Fix `Display` issues when waiting for `UserPlayer` input.
- Update `Display` to show the crib when it is being scored during the show phase.
- Update `Display` to show `state['crib_sums']`.
- Update `Display` to show a hat next to the dealer before the discard phase.
- Clean up the code in Display and Game.
- Continue testing game flow.
- ...

---
# Notes & Ideas
...

---
# Latest Changes
Minor adjustments and fixes, mainly to `Display`.

- Adjustments and bug fixes to `Display`:
  - Fixed positions for cards in the players' hands.
  - Adjusted positions for other interface elements.
  - Fixed game interface blinking issue.
  - Fixed position of played cards when a new round starts.
  - Fixed game interface not showing points properly.
  - Fixed program crashing when attempting to draw the last played card.
- Added missing `Display` function calls in `Game`.
- Fixed some scoring issues in `Game`.
- Added hints to `UserPlayer` when waiting for input.
- Updated TODO.