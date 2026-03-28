# TODO
- Optimize `PeggingTrainer` with the same method used in `DiscardTrainer`.
- Implement `PeggingTrainerPreLoaded`.
- Beautify scoring info when displayed in the terminal.

---
# Notes & Ideas
- Player agents that use neural nets expect a network with preloaded weights.

---
# Things to Consider
- `DiscardTrainer`: As it is now, the network makes decisions randomly from time to time due to using multinomial on its
  output distribution. If the network becomes very confident early on, the random exploration of other actions will stop.
  It might be worth adding an entropy bonus to the loss gradient.
- Change opponent half-way through training (or when the net reaches a satisfactory point) to Scripted opponent or the net itself.

---
# Latest Changes
Implemented new discard trainer that works with pre-generated states and other small changes.

- Implemented `DiscardTrainerPreLoaded` for training on pre-generated states.
- Changed how `DiscardTrainer` calculates reward and advantage.
- Removed card normalization in `SimpleStateEncoder`.
- Removed `SeededDiscardTrainer`.
- Minor changes in `DNT_DeepSeluSlim` and `DNT_DeepSeluWide` for testing purposes.
- Updated TODO.
