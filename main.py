import random
from enum import IntEnum, StrEnum
from typing import TypedDict

DECK_LENGTH: int = 52

NUM_PLAYERS = 3


class CardFamily(StrEnum):
    CLUBS = "clubs"
    DIAMONDS = "diamonds"
    HEARTS = "hearts"
    SPADES = "spades"


class CardNumber(IntEnum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NIN = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


class Card(TypedDict):
    number: int
    family: str


def load_cards(shuffle: bool = True) -> list[Card]:
    cards = []

    ## -- create numbered cards
    for number in CardNumber:
        for family in CardFamily:
            cards.append(Card(number=number.value, family=family.value))

    ## -- qa check !!!
    assert len(cards) == DECK_LENGTH

    ## -- shuffle step
    if shuffle:
        cards = random.sample(cards, k=len(cards))

    return cards


def display_card(card: Card) -> str:
    return f"[{card['number']} of {card['family']}]"


def distribute_cards_to_players(
    cards: list[Card], num_players: int = 2
) -> list[list[Card]]:
    ## -- qa checks
    assert (
        num_players > 1
    ), f"Game must have at least 2 players. Specified number of players '{num_players}' is not valid."
    assert (
        len(cards) == DECK_LENGTH
    ), f"Card deck must have exactly {DECK_LENGTH} cards, provided deck has {len(cards)} cards."

    cards_per_player = len(cards) // num_players
    remaining_cards = len(cards) % num_players

    players_hands: list[list[Card]] = []
    card_index: int = 0
    for player in range(num_players):
        if player < remaining_cards:
            num_cards = cards_per_player + 1
        else:
            num_cards = cards_per_player

        players_hands.append(cards[card_index : card_index + num_cards])
        card_index += num_cards

    return players_hands


def get_game_state(players_hands: list[list[Card]]) -> list[bool]:
    return [len(hand) > 0 for hand in players_hands]


def game_is_active(game_state: list[bool]) -> bool:
    return sum(game_state) > 1


PlayerNum = int
PrizeCards = list[Card]

PlayersHands = list[list[Card]]


class BattleResult(TypedDict):
    winning_player: PlayerNum
    prize_cards: list[tuple[PlayerNum, Card]]


class CardChange(TypedDict):
    origin_player: tuple[int, int]
    new_player: tuple[int, int]
    card: Card


CardValue = int
CardRanking = list[tuple[CardValue, list[PlayerNum]]]


def rank_cards(played_cards: list[Card]) -> CardRanking:
    played_card_numbers: dict[int, list[int]] = {}
    for player_num, played_card in enumerate(played_cards):
        if played_card["number"] in played_card_numbers:
            played_card_numbers[played_card["number"]].append(player_num)
        else:
            played_card_numbers[played_card["number"]] = [player_num]

    ## -- flatten and sort in reverse order
    ranked_results = sorted(played_card_numbers.items(), reverse=True)
    return ranked_results


def get_players_eligible_for_battle(
    players_hands: PlayersHands, required_num_cards: int
) -> list[bool]:
    return [len(hand) >= required_num_cards for hand in players_hands]


def play_round(
    players_hands: PlayersHands, battle_prize_card_reward: int = 3
) -> PlayersHands:
    players_in_battle = [
        player_num
        for player_num, player_hand in enumerate(players_hands)
        if len(player_hand) > 0
    ]

    in_battle_mode: bool = False
    prize_cards: list[Card] = []

    while True:
        if in_battle_mode:
            for player_num in players_in_battle:
                for _ in range(battle_prize_card_reward):
                    prize_cards.append(players_hands[player_num].pop(0))

        ## -- get next cards from each player
        played_cards: list[Card] = []
        for player_num in players_in_battle:
            played_cards.append(players_hands[player_num].pop(0))

        ## -- rank played cards
        ranked_results = rank_cards(played_cards)

        ## -- evaluate results
        if len(ranked_results[0][1]) == 1:
            ## -- easy case, we have a single winner
            winning_player_num = ranked_results[0][1][0]
            players_hands[winning_player_num].extend(played_cards)

            if len(prize_cards) > 0:
                players_hands[winning_player_num].extend(prize_cards)
            break

        else:
            ## -- !! battle !!
            prize_cards.extend(played_cards)

            players_in_battle = ranked_results[0][1]

            ## -- if players do not have enough cards for battle, they forfeit remaining cards to ultimate battle winner
            players_unable_to_continue_into_battle: list[PlayerNum] = []
            for player_num in players_in_battle:
                num_remaining_cards = len(players_hands[player_num])
                if num_remaining_cards <= battle_prize_card_reward:
                    ## -- player loses and forfeits cards to prize card deck
                    for _ in range(num_remaining_cards):
                        prize_cards.append(players_hands[player_num].pop(0))
                    players_unable_to_continue_into_battle.append(player_num)

            ## -- update players able to continue into battle
            players_in_battle = [
                player_num
                for player_num in players_in_battle
                if player_num not in players_unable_to_continue_into_battle
            ]

            if len(players_in_battle) > 1:
                in_battle_mode = True
            elif len(players_in_battle) == 0:
                raise ValueError("No players remaining battle. Game ends in tie.")
            else:
                last_standing_player = players_in_battle[0]
                players_hands[last_standing_player].extend(prize_cards)
                break

    return players_hands


def main():
    ## -- load shuffled deck of cards
    card_deck = load_cards(shuffle=True)

    ## -- distribute cards to players' hands
    players_hands = distribute_cards_to_players(card_deck, num_players=NUM_PLAYERS)

    game_state = get_game_state(players_hands)

    ## -- simulate war game
    _num_turns: int = 0
    _prev_players_hands: list[list[Card]] = []

    while game_is_active(game_state):
        ## -- increment stats
        _num_turns += 1
        _prev_players_hands = players_hands

        ## -- battle
        players_hands = play_round(players_hands)
        assert (
            sum([len(hand) for hand in players_hands]) == DECK_LENGTH
        ), f"Game entered invalid state at turn {_num_turns}.\nPrevious state: {_prev_players_hands}\n\nCurrent state: {players_hands}"

        ## -- update game state
        game_state = get_game_state(players_hands)

        if _num_turns > 5_000:
            print("Game exceeding 5000 turns...")
            break

    ## -- end game display
    print("---")
    print(f"> Game ended after {_num_turns} turns.")
    for player_num, player_hand in enumerate(players_hands):
        print(f"> Player {player_num} has {len(player_hand)} cards.")
    return


if __name__ == "__main__":
    main()
