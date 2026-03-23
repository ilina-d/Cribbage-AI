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
Bug fixes and minor changes.

- Added gradient clipping to both trainers when `inflate_advantage == True`. The code is commented out for now.
- Fixed progress printing in both trainers not aligning each "column" properly.
- Removed all `DNT` (Discard Network Tests).
- Updated `TODO`.