# TODO
- Optimize `PeggingTrainer` with the same method used in `DiscardTrainer`.
- Implement different neural network structures and player agents.
- Beautify scoring info when displayed in the terminal.

---
# Notes & Ideas
- Player agents that use neural nets expect a network with preloaded weights.
- Selu needs additional settings changed to the linear layers.

---
# Things to Consider
- `DiscardTrainer`: As it is now, the network makes decisions randomly from time to time due to using multinomial on its
  output distribution. If the network becomes very confident early on, the random exploration of other actions will stop.
  It might be worth adding an entropy bonus to the loss gradient.
- Change opponent half-way through training (or when the net reaches a satisfactory point) to Scripted opponent or the net itself.

---
# Latest Changes
Major bug fix, optimizations, and testing additions.

- Fixed a major oversight in both `DiscardTrainer` and `PeggingTrainer` always choosing to `rely_on_coach`.
- Optimized the `DiscardTrainer` by simultaneously training and generating state pools.
- Added 20 Discard neural network structures for testing.
- Added `SeededDiscardTrainer` for testing.
- Normalized card values in `SimpleStateEncoder` for testing. May need to revert the encoding back.
- Updated TODO.