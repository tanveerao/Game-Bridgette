"""Core game logic for Bridgette: deck building, trick dealing, and scoring.

Pure Python, no Streamlit imports — everything here is unit-testable.
"""

import random

SUITS = ["♠", "♥", "♦", "♣"]  # ♠ ♥ ♦ ♣
RED_SUITS = {"♥", "♦"}  # ♥ ♦
ALL_RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

CARD_COUNTS = [6, 8, 10, 12, 13]
TRICK_SIZE = 4

DIFFICULTIES = {
    "Easy": {"duration": 7, "visible": "all"},
    "Medium": {"duration": 5, "visible": "previous"},
    "Hard": {"duration": 3, "visible": "current"},
}


def build_deck(card_count):
    """The deck: the smallest `card_count` ranks (A, 2, 3, ...) in each of the 4 suits."""
    ranks = ALL_RANKS[:card_count]
    return [(rank, suit) for suit in SUITS for rank in ranks]


def deal_trick(deck, last_suit):
    """Deal one trick of 4 cards from the remaining deck.

    Returns (trick_cards, primary_suit). primary_suit is None when the trick
    was filled fully at random (deck nearly exhausted).

    Rules:
    - Prefer a random suit that still has >= 4 cards and wasn't the previous
      trick's suit; draw 4 random ranks from it.
    - If no such suit exists, pick a random non-previous suit that still has
      cards, take everything it has, and fill the rest of the trick at random
      from whatever else remains (any suit, including the previous one).
    - If only the previous trick's suit has cards left (or nothing qualifies),
      fill the whole trick at random, ignoring the no-repeat-suit rule.
    """
    by_suit = {s: [c for c in deck if c[1] == s] for s in SUITS}

    full_suits = [s for s in SUITS if len(by_suit[s]) >= TRICK_SIZE and s != last_suit]
    if full_suits:
        suit = random.choice(full_suits)
        return random.sample(by_suit[suit], TRICK_SIZE), suit

    short_suits = [s for s in SUITS if 0 < len(by_suit[s]) < TRICK_SIZE and s != last_suit]
    if short_suits:
        suit = random.choice(short_suits)
        trick = list(by_suit[suit])
        rest = [c for c in deck if c[1] != suit]
        trick += random.sample(rest, min(TRICK_SIZE - len(trick), len(rest)))
        return trick, suit

    return random.sample(deck, min(TRICK_SIZE, len(deck))), None


def score_first_guess(marked, correct):
    """Score the first Check of a round on accuracy of the marked set.

    1.0  -> every marked card was actually played (100% accuracy)
    0.5  -> at least half the marked cards were actually played
    0.0  -> fewer than half were
    """
    marked = set(marked)
    if not marked:
        return 0.0
    accuracy = len(marked & set(correct)) / len(marked)
    if accuracy == 1.0:
        return 1.0
    if accuracy >= 0.5:
        return 0.5
    return 0.0
