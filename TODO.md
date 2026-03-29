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
Added discard training datasets.

- Added datasets for training discard networks.
- Added a `Sigmoid()` layer to some discard networks for testing.
- Minor fix in `DiscardTrainerPreLoaded` logs.