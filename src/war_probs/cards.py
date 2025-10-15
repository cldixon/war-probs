import random
from enum import IntEnum, StrEnum
from typing import TypedDict

import polars as pl

DECK_LENGTH: int = 52


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


class CardIndex(TypedDict):
    name: str
    value: int
    family: CardFamily
    player: int
    index: int


def convert_hands_to_table(players_hands: list[list[Card]]) -> pl.DataFrame:
    master_card_index = []
    for player_num, player_hand in enumerate(players_hands):
        for idx, card in enumerate(player_hand):
            master_card_index.append(
                CardIndex(
                    **{
                        "name": f"{card['number']}_of_{card['family']}",
                        "value": card["number"],
                        "family": card["family"],
                        "player": player_num,
                        "index": idx,
                    }
                )
            )
    return pl.DataFrame(master_card_index)
