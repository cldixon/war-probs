from src.war_probs.cards import Card, distribute_cards_to_players, load_cards

NUM_PLAYERS = 2


def get_game_state(players_hands: list[list[Card]]) -> list[bool]:
    return [len(hand) > 0 for hand in players_hands]


def game_is_active(game_state: list[bool]) -> bool:
    return sum(game_state) > 1


PlayerNum = int
PrizeCards = list[Card]

PlayersHands = list[list[Card]]


def conduct_battle(players_hands: PlayersHands) -> PlayersHands:
    ## -- get battle cards
    battle_cards: list[Card] = []
    for hand in players_hands:
        played_card = hand.pop(0)
        battle_cards.append(played_card)

    # battle_cards = [hand[0] for hand in players_hands]

    played_card_numbers: dict[int, list[int]] = {}
    for player_num, played_card in enumerate(battle_cards):
        if played_card["number"] in played_card_numbers:
            played_card_numbers[played_card["number"]].append(player_num)
        else:
            played_card_numbers[played_card["number"]] = [player_num]

    ## -- flatten and sort in reverse order
    ranked_results = sorted(played_card_numbers.items(), reverse=True)

    if len(ranked_results[0][1]) == 1:
        ## -- single first place winner
        winning_player_num = ranked_results[0][1][0]
        prize_cards = battle_cards
    else:
        ## -- !! battle
        raise NotImplementedError(
            f"Reached a **BATTLE** scenario with players {ranked_results[0][1]} submitting a card with value {ranked_results[0][0]}."
        )

    ## -- update winning player's hand
    players_hands[winning_player_num].extend(prize_cards)
    return players_hands


def main():
    ## -- load shuffled deck of cards
    card_deck = load_cards(shuffle=True)

    ## -- distribute cards to players' hands
    players_hands = distribute_cards_to_players(card_deck, num_players=NUM_PLAYERS)

    game_state = get_game_state(players_hands)

    ## -- simulate war game
    while game_is_active(game_state):
        ## -- battle
        players_hands = conduct_battle(players_hands)

        ## -- update game state
        game_state = get_game_state(players_hands)

    ## -- end game display
    for player_num, player_hand in enumerate(players_hands):
        print(f"> Player {player_num} has {len(player_hand)} cards.")
    return


if __name__ == "__main__":
    main()
