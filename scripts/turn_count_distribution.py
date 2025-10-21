import matplotlib.pyplot as plt

from war_probs.distributions import turn_count_distribution_histogram
from war_probs.game import Game

NUM_SIMULATIONS: int = 25_000

## NOTE: t
MAX_TURNS: int = 5_000
OUTPUT_HISTOGRAM_PATH: str = "img/turn_count_histogram.png"


def main():
    ## ---- simulate many games and collect results
    print(f"> Simulated {NUM_SIMULATIONS} games of war...")

    completed_games: list = []
    draw_games: list = []

    for _ in range(NUM_SIMULATIONS):
        ## -- initialize a game
        game = Game(max_turns=MAX_TURNS)

        ## -- simulate game
        results = game.play()

        if results["completed_turns"] < MAX_TURNS:
            completed_games.append(results)
        else:
            draw_games.append(results)

    ## ---- compare number of completed vs. draw games
    print(
        f"> {len(completed_games):,} games ended with a winner. {len(draw_games)} ended in a draw."
    )

    ## ---- get number of turns from all completed games
    all_num_turns = [result["completed_turns"] for result in completed_games]

    ## -- create histogram of game turn counts
    turn_count_histogram = turn_count_distribution_histogram(all_num_turns)

    ## -- save to disk
    turn_count_histogram.savefig(OUTPUT_HISTOGRAM_PATH, dpi=300, bbox_inches="tight")

    plt.show()


if __name__ == "__main__":
    main()
