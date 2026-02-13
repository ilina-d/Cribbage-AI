# Project Structure
```
❌ | main.py
❌ | README.md
✅ | TODO.md
❌ | requirements.txt
⬛ |
🔄 | utils/
⬛ |-|
✅ |-| assets/ 
✅ |-|-| __init__.py
✅ |-|-| display.py
⬛ |-|
✅ |-| game/
✅ |-|-| __init__.py
✅ |-|-| game.py
⬛ |-|
❌ |-| helpers/
🔄 |-|-| __init__.py
✅ |-|-| card_deck.py
✅ |-|-| scoring.py
✅ |-|-| discard_evaluator.py
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
- Implement an AI player with a neural network.
- Beautify scoring info when displayed in the terminal.

---
# Notes & Ideas
- Internal state representation for neural networks:
  - Card: [
      rank (1 - 13),
      suit (0001, 0010, 0100, 1000),
      worth (1 - 10)
    ]
  - State: [
      points (int, int),
      dealer (01, 10),  <-- may not be necessary
      starter_card (Card),
      crib (Card, Card, ...)  <-- only the current crib may be enough
    ]
- Neural network outputs:
  - For discarding cards, outputs a confidence percentage for all 52 cards in the deck.
    Afterwards, take the two cards with the highest value that are valid to discard.
  - For playing cards, outputs a confidence percentage for all 52 cards in the deck.
    Afterwards, take the card with the highest value that is valid to play.
    For "GO", the move is made automatically when there are no other valid cards to play.
    However, saying "GO" is also a move that needs to be rewarded/penalized.
- Neural network training:
  - For discarding cards, use a statistical coach.
  - For playing cards, penalize or reward all moves during the game depending on whether the agent lost or won.

---
# Latest Changes
Implemented evaluation for discarding cards, visual updates, and minor fixes.

- Added a `clear` argument to `Display.print()` for clearing the terminal display before printing.
- Finished implementing the `visuals` toggle for `Game` and `Display`.
- Added `DiscardEvaluator` to `utils/helpers/` for choosing which cards to discard based on statistical probability.
- Added missing `__all__` variable to `RandomPlayer`.
- Updated TODO.