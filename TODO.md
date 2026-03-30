# TODO
- Add the best neural networks once all testing is done.
- Beautify scoring info when displayed in the terminal.

---
# Notes & Ideas
- Player agents that use neural nets expect a network with preloaded weights.
- Try training the previously best networks with simple normalized encoder.
- Try training the previously best networks with the original encoder plus added card worth.

---
# Things to Consider
- `DiscardTrainer`: As it is now, the network makes decisions randomly from time to time due to using multinomial on its
  output distribution. If the network becomes very confident early on, the random exploration of other actions will stop.
  It might be worth adding an entropy bonus to the loss gradient.
- Change opponent half-way through training (or when the net reaches a satisfactory point) to Scripted opponent or the net itself.
- Pegging networks should be RNNs perhaps.

---
# Latest Changes
Added greedy discarding players and pegging trainer fixes.

- Added `DGPNPlayer` and `DGPRPlayer` for faster evaluation of pegging neural networks.
- Fixed both `PeggingTrainer` and `PeggingTrainerPreLoaded` 
- Fixed `DAPNPlayer.play_card()` passing too many arguments to the neural network.
- Removed `pegging_net_v1` and `pegging_net_v2`.
- Minor doc-string changes.
- Updated TODO.
