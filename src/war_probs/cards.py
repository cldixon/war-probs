import random
from collections import namedtuple
from enum import IntEnum, StrEnum
from typing import Literal

DECK_LENGTH: int = 52

NUM_PLAYERS = 3

_VALID_SUITS: list[str] = ["clubs", "diamonds", "hearts", "spades"]


class Suit(StrEnum):
    CLUBS = "clubs"
    DIAMONDS = "diamonds"
    HEARTS = "hearts"
    SPADES = "spades"


SuitType = Literal["clubs", "diamonds", "hearts", "spades"]


class Rank(StrEnum):
    TWO = "two"
    THREE = "three"
    FOUR = "four"
    FIVE = "five"
    SIX = "six"
    SEVEN = "seven"
    EIGHT = "eight"
    NINE = "nine"
    TEN = "ten"
    JACK = "jack"
    QUEEN = "queen"
    KING = "king"
    ACE = "ace"


RankType = Literal[
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "jack",
    "queen",
    "king",
    "ace",
]


class Value(IntEnum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


_RANK_TO_VALUE_MAP: dict[str, int] = {
    "two": Value.TWO.value,
    "three": Value.THREE.value,
    "four": Value.FOUR.value,
    "five": Value.FIVE.value,
    "six": Value.SIX.value,
    "seven": Value.SEVEN.value,
    "eight": Value.EIGHT.value,
    "nine": Value.NINE.value,
    "ten": Value.TEN.value,
    "jack": Value.JACK.value,
    "queen": Value.QUEEN.value,
    "king": Value.KING.value,
    "ace": Value.ACE.value,
}


def map_rank_to_value(rank: RankType) -> int:
    return _RANK_TO_VALUE_MAP[rank.lower()]


## ------------------------------------------------- ##
## ---- PLAYING CARD REPRESENTED AS NAMED TUPLE ---- ##
## ------------------------------------------------- ##

Card = namedtuple("Card", ["rank", "suit", "value"])


def display_card(card: Card) -> str:
    return f"[{card.rank} of {card.suit}]"


def get_card(rank: RankType, suit: SuitType) -> Card:
    assert suit.lower() in _VALID_SUITS, f"Invalid suit: {suit}"
    return Card(rank=rank.lower(), suit=suit.lower(), value=map_rank_to_value(rank))


def get_suit(suit: SuitType) -> list[Card]:
    assert suit.lower() in _VALID_SUITS, f"Invalid suit: {suit}"
    return [
        Card(rank=rank.lower(), suit=suit.lower(), value=map_rank_to_value(rank.value))
        for rank in Rank
    ]


## ------------------------------------------------- ##
## ---- FUNCTION TO INITIALIZE DECK OF CARDS ------- ##
## ---------- E.G., LIST OF NAMED-TUPLES ----------- ##
## ------------------------------------------------- ##


def load_cards(shuffle: bool = True) -> list[Card]:
    cards: list[Card] = []

    ## -- create numbered cards
    for rank, value in zip(Rank, Value):
        for suit in Suit:
            cards.append(Card(rank=rank.value, suit=suit.value, value=value.value))

    ## -- qa check !!!
    assert len(cards) == DECK_LENGTH

    ## -- shuffle step
    if shuffle:
        cards = random.sample(cards, k=len(cards))

    return cards
