from war_probs.cards import load_cards
from war_probs.game import Game

NUM_PLAYERS: int = 2


def main():
    ## -- load shuffled deck of cards
    card_deck = load_cards(shuffle=True)

    ## -- set up game
    game = Game(num_players=NUM_PLAYERS, cards=card_deck)

    ## -- play game
    result = game.play()

    ## -- end game display
    print("---")
    print(
        f"> Game ended with a '{result['end_status']}' in {round(result['total_time'], 3)}ms after {result['completed_turns']} turns."
    )
    for player_num, player_hand in enumerate(result["ending_hands"]):
        print(f"> Player {player_num} has {len(player_hand)} cards.")
    return


if __name__ == "__main__":
    main()
