from war_probs.cards import Card


def calc_war_value(played_value: int, won_value: int, k: int = 2) -> float:
    """Base formula for calculating war metric score, given card played vs. card won."""
    margin = abs((won_value - played_value))
    score = won_value * (1 - margin / 13) ** k
    return score


def war_score(card_played: Card, card_won: Card) -> float:
    """Calculates _war_ metric score, given card played vs. card won.
    E.g., if card_played is a 10, and card_won is a 9, then score will be
    higher than if card_played is a 10 and card_won is a 2. But overall
    magnitude of card won is also considered, e.g., winning a queen (value=12)
    will have a higher score than winning a 2. Winning a king (value=13)
    with an Ace (value=14) will have the highest score."""
    return calc_war_value(card_played.value, card_won.value)
