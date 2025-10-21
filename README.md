# War Probs: Assorted Analytics for Card Game _War_

This repository is a collection of code snippets for simulating the card game _war_ and developing statistical metrics around the game.

While the game is incredibly simple and entirely luck based, and nearly deterministic based on the initial shuffle and deal, there are some interesting patterns that emerge when analyzing the game.

## Turn Value Metrics

... aka **war-score**.

```md
If you WIN:
    Turn Value = Card_won × (1 - margin/13)^k

If you LOSE:
    Turn Value = -(Card_lost × (1 + margin/13)^k)

Where:
- `margin` is the difference between the winning (or max value) card and the losing card
- `k` is a tuning parameter (maybe k=1 or k=2).
```


### Turn Values Score Matrix

![Turn Values Score Matrix](img/turn_values_score_matrix.png)
