# TODO
- Change state pool distribution in `PeggingTrainer`.
  Currently `recommended` is best, with `aggressive` and maybe `sure_bet` close behind.
- Implement early stopping if needed.
- Implement different neural network structures and player agents.
- Beautify scoring info when displayed in the terminal.

---
# Notes & Ideas
- Player agents that use neural nets expect a network with preloaded weights.

---
# Things to Consider
- `DiscardTrainer`: As it is now, the network makes decisions randomly from time to time due to using multinomial on its
  output distribution. If the network becomes very confident early on, the random exploration of other actions will stop.
  It might be worth adding an entropy bonus to the loss gradient.
- `DiscardTrainer`: Check difference in using Adam(W) and SGD.
- Change distribution half-way through training to something like: 50% aggressive, 50% recommended discards (Pegging net).
- Change opponent half-way through training (or when the net reaches a satisfactory point) to Scripted opponent or the net itself.

---
# Latest Changes
Prepared code for testing of DiscardNets and training methods.

- Reorganized `utils/neural_nets/`.
- Removed `is_dealer` and `starter_card` from state encoding for `PeggingNets`.
- Added various `DiscardNets` and `DiscardTrainers` for testing neural network structures and training methods.
- Removed debug argument in `DiscardTrainer`.