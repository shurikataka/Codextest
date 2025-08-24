import random
from dataclasses import dataclass
from typing import List, Optional

SUITS = ["♠", "♥", "♦", "♣"]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

@dataclass
class Card:
    rank: str
    suit: str

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"

def create_deck() -> List[Card]:
    """Create a standard 52-card deck."""
    return [Card(rank, suit) for suit in SUITS for rank in RANKS]


def print_board(board: List[Optional[Card]]):
    """Print the current state of the board with positions."""
    cols = 13
    for i, card in enumerate(board):
        if i % cols == 0:
            print()
        if card is None:
            cell = "   "
        else:
            cell = f"{i:02d}"  # show index for face-down cards
        print(cell, end=" ")
    print("\n")


def reveal_positions(board: List[Optional[Card]], positions: List[int]) -> List[Card]:
    """Reveal cards at the given positions."""
    cards = []
    for pos in positions:
        card = board[pos]
        if card is None:
            raise ValueError("Position already empty")
        cards.append(card)
    return cards


def remove_positions(board: List[Optional[Card]], positions: List[int]):
    for pos in positions:
        board[pos] = None


def all_same_rank(cards: List[Card]) -> bool:
    return len(set(c.rank for c in cards)) == 1 and len({c.suit for c in cards}) == 4


def play_game():
    deck = create_deck()
    random.shuffle(deck)
    board: List[Optional[Card]] = deck[:]
    num_players = 0
    while num_players < 1 or num_players > 6:
        try:
            num_players = int(input("How many players (1-6)? "))
        except ValueError:
            num_players = 0
    scores = [0] * num_players
    current = 0
    remaining_sets = len(RANKS)

    while remaining_sets > 0:
        print(f"\nPlayer {current + 1}'s turn")
        print_board(board)
        positions = []
        while len(positions) < 4:
            try:
                pos = int(input(f"Select position {len(positions)+1}: "))
                if pos < 0 or pos >= len(board) or board[pos] is None or pos in positions:
                    raise ValueError
                positions.append(pos)
            except ValueError:
                print("Invalid position. Try again.")

        revealed = reveal_positions(board, positions)
        print("Revealed:", " ".join(str(c) for c in revealed))
        if all_same_rank(revealed):
            print("Success! Removing cards.")
            remove_positions(board, positions)
            scores[current] += 1
            remaining_sets -= 1
            print_board(board)
            # player gets another turn
        else:
            print("Not a match.")
            current = (current + 1) % num_players

    max_score = max(scores)
    winners = [i + 1 for i, s in enumerate(scores) if s == max_score]
    print("Game over!")
    for i, s in enumerate(scores, 1):
        print(f"Player {i}: {s}")
    if len(winners) == 1:
        print(f"Winner is Player {winners[0]}!")
    else:
        print(f"It's a tie between players: {', '.join(map(str, winners))}")


if __name__ == "__main__":
    play_game()
