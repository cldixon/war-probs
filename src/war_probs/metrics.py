import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from war_probs.cards import Card, get_suit


def calc_war_value(played_value: int, won_value: int, k: int = 2) -> float:
    """Base formula for calculating war metric score, given card played vs. card won."""
    margin = abs((won_value - played_value))
    score = won_value * (1 - margin / 13) ** k
    return score


def war_score(card_played: Card, card_won: Card) -> float:
    return calc_war_value(card_played.value, card_won.value)


def _calculate_turn_value(a_value: int, b_value: int, k: int = 2) -> float:
    if a_value > b_value:
        # player a wins
        margin = a_value - b_value
        return b_value * (1 - margin / 13) ** k
    elif b_value > a_value:
        # player b wins
        margin = b_value - a_value
        return -(a_value * (1 - margin / 13) ** k)
    else:
        # Tie (war scenario) - could return 0 or handle separately
        return 0


def turn_value(your_card: Card, opp_card: Card, k: int = 2) -> float:
    """
    Calculates _war_ metric score, given card played vs. card won.
    E.g., if card_played is a 10, and card_won is a 9, then score will be
    higher than if card_played is a 10 and card_won is a 2. But overall
    magnitude of card won is also considered, e.g., winning a queen (value=12)
    will have a higher score than winning a 2. Winning a king (value=13)
    with an Ace (value=14) will have the highest score.
    """
    return _calculate_turn_value(your_card.value, opp_card.value, k)


def turn_values_matrix() -> np.ndarray:
    ## -- get list of cards with all distinct ranks
    cards = get_suit(suit="clubs")

    # Create the confusion matrix
    num_ranks = len(cards)
    score_matrix = np.zeros((num_ranks, num_ranks))

    for i, your_card in enumerate(cards):
        for j, opp_card in enumerate(cards):
            score_matrix[i, j] = turn_value(your_card, opp_card)

    return score_matrix


def turn_values_matrix_plot(
    score_matrix: np.ndarray | None = None,
    figsize: tuple[int, int] = (12, 10),
    _war_annotation: str = "*WAR",
) -> plt.Figure:  # type: ignore
    ## -- generate score matrix if not provided
    score_matrix = score_matrix or turn_values_matrix()

    ## -- get name of card ranks
    single_suit_cards = get_suit(suit="clubs")
    num_ranks = len(single_suit_cards)
    rank_names = [card.rank for card in single_suit_cards]

    # Create custom annotations with "WAR" on diagonal
    annot_matrix = np.empty((num_ranks, num_ranks), dtype=object)

    for i in range(num_ranks):
        for j in range(num_ranks):
            if i == j:
                annot_matrix[i, j] = _war_annotation
            else:
                annot_matrix[i, j] = f"{score_matrix[i, j]:.1f}"

    ## -- initialize plot objects
    fig, ax = plt.subplots(figsize=figsize)

    ## -- create the heatmap
    sns.heatmap(
        score_matrix,
        xticklabels=rank_names,
        yticklabels=rank_names,
        cmap="RdYlGn",  # Red for losses, Green for wins
        center=0,  # Center colormap at 0
        annot=annot_matrix,  # Use custom annotations
        fmt="",  # Empty format since we're using strings
        cbar_kws={"label": "Turn Value"},
    )

    ax.set_xlabel("Opponent's Card", fontsize=12)
    ax.set_ylabel("Your Card", fontsize=12)
    ax.set_title(
        "War Card Game: Turn Value Matrix\n(Green = Win, Red = Loss, White = War)",
        fontsize=14,
        pad=20,
    )

    fig.tight_layout()

    return fig
