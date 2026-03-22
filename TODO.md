# TODO
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
Trainer updates and Simulator fixes.

- Adjusted time estimate in Simulator.
- Added handling of zombie processes. 
- Improved supervised training and the way imitation loss is interpreted.
- Added supervised training option for `PeggingTrainer`.
- Fixed gradient updates in trainers and added option for accumulating loss per batch.
- Added option to inflate the advantage when training.
- Added `get_card_confidence` function to `BasePeggingNet`.
- Removed manual changes to `num_workers` in the trainers.
- Altered the distribution of the state pool for the `PeggingTrainer`.
- Removed the option for `early_stop` in both trainers.
- Updated `TODO`.