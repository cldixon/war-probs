import math
import time
from collections import deque
from typing import Deque, Literal, TypedDict
from uuid import uuid4

from war_probs.cards import DECK_LENGTH, Card, load_cards

PlayerNum = int
PrizeCards = list[Card]

PlayersHandLists = list[list[Card]]
PlayersHandDeques = list[Deque[Card]]

CardValue = int
CardRanking = list[tuple[CardValue, list[PlayerNum]]]


def distribute_cards_to_players(
    cards: list[Card], num_players: int = 2
) -> PlayersHandDeques:
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

    return [deque(hand) for hand in players_hands]


def get_game_state(players_hands: PlayersHandDeques) -> list[bool]:
    return [len(hand) > 0 for hand in players_hands]


def game_is_active(game_state: list[bool]) -> bool:
    return sum(game_state) > 1


def rank_cards(played_cards: list[Card]) -> CardRanking:
    played_card_numbers: dict[int, list[int]] = {}
    for player_num, played_card in enumerate(played_cards):
        if played_card.value in played_card_numbers:
            played_card_numbers[played_card.value].append(player_num)
        else:
            played_card_numbers[played_card.value] = [player_num]

    ## -- flatten and sort in reverse order
    ranked_results = sorted(played_card_numbers.items(), reverse=True)
    return ranked_results


class PlayedCardScoring(TypedDict):
    outcome: Literal["winner", "war"]
    ranking: CardRanking
    winning_player: PlayerNum | None
    winning_value: CardValue | None


def score_played_cards(played_cards: list[Card]) -> PlayedCardScoring:
    ranking = rank_cards(played_cards)

    if len(ranking[0][1]) == 1:
        ## -- easy case, we have a single winner
        return PlayedCardScoring(
            outcome="winner",
            ranking=ranking,
            winning_player=ranking[0][1][0],
            winning_value=ranking[0][0],
        )

    else:
        return PlayedCardScoring(
            outcome="war",
            ranking=ranking,
            winning_player=None,
            winning_value=None,
        )


def get_players_eligible_for_battle(
    players_hands: PlayersHandLists, required_num_cards: int
) -> list[bool]:
    return [len(hand) >= required_num_cards for hand in players_hands]


def play_turn(
    players_hands: PlayersHandDeques, battle_prize_card_reward: int = 3
) -> PlayersHandDeques:
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
                    prize_card = players_hands[player_num].popleft()
                    prize_cards.append(prize_card)

        ## -- get next cards from each player
        played_cards: list[Card] = []
        for player_num in players_in_battle:
            players_card = players_hands[player_num].popleft()
            played_cards.append(players_card)

        ## -- rank played cards
        # ranked_results = rank_cards(played_cards)
        result = score_played_cards(played_cards)

        ## -- evaluate results
        # if len(ranked_results[0][1]) == 1:
        if result["winning_player"] is not None:
            ## -- easy case, we have a single winner
            winning_player_num = result["winning_player"]
            players_hands[winning_player_num].extend(played_cards)

            if len(prize_cards) > 0:
                players_hands[winning_player_num].extend(prize_cards)
            break

        else:
            ## -- !! war !!
            prize_cards.extend(played_cards)

            players_in_battle = result["ranking"][0][1]

            ## -- if players do not have enough cards for war, they forfeit remaining cards to ultimate war winner
            players_with_insufficient_cards_for_battle: list[PlayerNum] = []
            for player_num in players_in_battle:
                num_remaining_cards = len(players_hands[player_num])
                if num_remaining_cards <= battle_prize_card_reward:
                    ## -- player loses and forfeits cards to prize card deck
                    for _ in range(num_remaining_cards):
                        prize_card = players_hands[player_num].popleft()
                        prize_cards.append(prize_card)
                    players_with_insufficient_cards_for_battle.append(player_num)

            ## -- update players able to continue into battle
            players_in_battle = [
                player_num
                for player_num in players_in_battle
                if player_num not in players_with_insufficient_cards_for_battle
            ]

            if len(players_in_battle) > 1:
                in_battle_mode = True
            elif len(players_in_battle) == 0:
                raise ValueError("No players remaining battle. Game ends in tie.")
            else:
                last_standing_player = players_in_battle[0]
                players_hands[last_standing_player].extend(prize_cards)
                break

    ## -- create turn metrics
    # turn_metrics = TurnMetrics(
    #    played_cards=played_cards,
    #    winning_card=result[],
    #    war_scores=war_scores,
    # )

    return players_hands


class GameResult(TypedDict):
    id: str
    completed_turns: int
    total_time: float
    starting_hands: list[list[Card]]
    ending_hands: list[list[Card]]
    player_scores: list[int]
    end_status: Literal["winner", "draw"]


class Game:
    def __init__(
        self,
        num_players: int = 2,
        cards: list[Card] | None = None,
        max_turns: int = 5_000,
    ) -> None:
        self.num_players = num_players
        self.cards = cards or load_cards()
        self.max_turns = max_turns
        self.id = str(uuid4())

    def play(self) -> GameResult:
        ## -- start timer
        start_time = time.perf_counter()

        ## -- distribute cards to players
        players_hands = distribute_cards_to_players(self.cards)

        ## -- keep record of starting game state
        _starting_players_hands = players_hands

        ## -- initiate game
        game_state = get_game_state(players_hands)

        ## -- simulate war game
        _num_turns: int = 0

        while game_is_active(game_state):
            ## -- increment stats
            _num_turns += 1

            ## -- battle
            players_hands = play_turn(players_hands)
            assert (
                sum([len(hand) for hand in players_hands]) == DECK_LENGTH
            ), f"Game entered invalid state at turn {_num_turns}. Current state: {players_hands}"

            ## -- update game state
            game_state = get_game_state(players_hands)

            if _num_turns > self.max_turns:
                print("Game exceeding 5000 turns...")
                break

        ## -- return game results
        end_time = time.perf_counter()
        duration_seconds = end_time - start_time
        duration_milliseconds = duration_seconds * 1000

        player_scores = [len(hand) for hand in players_hands]

        ## -- temporary way to get winner or draw status
        if math.prod(player_scores) != 0:
            end_status = "draw"
        else:
            end_status = "winner"

        return GameResult(
            id=self.id,
            completed_turns=_num_turns,
            total_time=duration_milliseconds,
            starting_hands=[list(hand) for hand in _starting_players_hands],
            ending_hands=[list(hand) for hand in players_hands],
            player_scores=player_scores,
            end_status=end_status,
        )
