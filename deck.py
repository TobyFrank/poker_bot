from typing import List
import random
import constants
from card import Card

class Deck: 
    "Class stores a list of shuffled Cards and can deal cards to various locations on the table"

    def __init__(self, deck_suits, deck_ranks):
        "Initializes a deck with given rank/suit possibilities"
        self.deck_suits: List[str] = deck_suits
        self.deck_suits_index: List[int] = [constants.suit_list_dict[suit] for suit in deck_suits]
        self.deck_ranks: List[str] = deck_ranks
        self.deck_ranks_index: List[int] = [constants.rank_value_dict[rank] for rank in deck_ranks]
        self.setup()

    def setup(self):
        "Initializes a list of Card classes for a decklist"
        self.decklist: List[Card] = [Card(rank + suit) for suit in self.deck_suits for rank in self.deck_ranks]
        # random.shuffle(self.decklist)
        self.dealt_cards: List[Card] = []

    def peek_deck_size(self):
        "Returns the length of cards not in play"
        return len(self.decklist)


    def remove_card(self, card: Card):
        "Removes a card from decklist and adds it to the dealt_cards"
        if card in self.decklist:
            self.decklist.remove(card)
            self.dealt_cards.append(card)
            # print((card.rank, card.suit))
        else:
            print(f'Sorry, {card} is not in the deck!')

    def __str__(self):
        "Prints all cards not dealt"
        return f"Deck: {([(card.rank, card.suit) for card in self.decklist])}"

    def __repr__(self):
        "Prints all cards not dealt"
        return f"Deck: {([(card.rank, card.suit) for card in self.decklist])}"