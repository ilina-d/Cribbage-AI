# TODO
- Add `net.train()` to both trainers.
- Update trainers to not change `num_workers` since `multiprocessing.Pool` already handles load balancing.
- Change state pool distribution in `PeggingTrainer`.
  Currently `recommended` is best, with `aggressive` and maybe `sure_bet` close behind.
- Change how `imitation_loss` works:
  ```python
  rely_on_coach = random.choices([True, False], [alpha, 1 - alpha], k = 1)
  distribution = discard_network.get_distribution_policy(...)
  
  if rely_on_coach:
      card1, card2 = state['best_cards']
      confidence = discard_network.get_combo_confidence(...)
  else:
      log_probs = torch.stack([combo[2] for combo in distribution])
      probs = torch.exp(log_probs)

      chosen_combo = distribution[torch.multinomial(probs, 1).item()]
      card1, card2, confidence = chosen_combo[0], chosen_combo[1], chosen_combo[2]
  
  hand_score = ...
  crib_score = ...
  reward = hand_score + crib_score if is_dealer else hand_score - crib_score
  baseline = state['baseline']
  advantage = reward - baseline

  loss = -confidence * advantage
  ...
  ```
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
Added multiprocessing to Simulator and option to choose first dealer in Game.

- Added option to choose the initial dealer in `Game`.
- Implemented `Simulator` multiprocessing.