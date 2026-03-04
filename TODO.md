# TODO
- Continue implementing `PeggingTrainer`.
- Implement early stopping in `DiscardTrainer` if needed.
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
# Things to Consider
- `DiscardTrainer`: As it is now, the network makes decisions randomly from time to time due to using multinomial on its
  output distribution. If the network becomes very confident early on, the random exploration of other actions will stop.
  It might be worth adding an entropy bonus to the loss gradient.
- `DiscardTrainer`: Check difference in using Adam(W) and SGD.

---
# Latest Changes
DiscardTrainer updates to batched loss propagation, on-policy exploration, and fixes.

- `DiscardTrainer` changes:
  - Implemented on-policy exploration. Trainer now pulls from a set of predefined states every batch, ensuring that
    some states are observed multiple times before changing the policy.
  - Fixed loss being propagated after every batch-iteration instead of after the entire batch.
  - Fixed `play_style` causing an error if left as None.
  - Fixed `alpha_step` causing an error if set to 0.
- Minor `Simulator` fixes and changes.
- Updated TODO.
