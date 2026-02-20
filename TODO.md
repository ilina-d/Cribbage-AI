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
- Implement early stopping in `DiscardTrainer`.
- Implement progress printing in `DiscardTrainer`.
- Implement different neural network structures and player agents.
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
  
- Player agents that use neural nets expect a network with preloaded weights.

---
# Latest Changes
Began implementing neural network agents.

- Added `StateEncoder` for encoding game states in a format recognizable for neural networks.
- Added a `neural_nets` module.
  - Added a `BaseDiscardNet` from which all discard policy nets will inherit.
  - Added `DiscardNetV1`.
  - Added `DiscardTrainer` for training different discard policy nets.
- Added `DNPRPlayer` that uses the first version of the discard net.
- Altered `DiscardEvaluator` to return all combinations of card pairs, sorted by their criteria.
- Updated `requirements.txt`.
- Minor variable name and docstring changes.
- Updated TODO.