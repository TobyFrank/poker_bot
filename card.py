import constants

# Card class is one card in the deck
# - properties: suit, value

class Card:
    # "Class stores all suit values and rank values of a card"
    #Takes in strings in format: "Ah", "Tc", "8d"

    def __init__(self, card_string):
        # "Initializes a card with a suit and a rank"
        if card_string[0] == "1":
            self.rank, self.suit = card_string[0:2], card_string[2]
        else:
            self.rank, self.suit = card_string[0], card_string[1]
        self.rank_index = constants.rank_value_dict[self.rank]
        self.suit_index = constants.suit_list_dict[self.suit]

    def __eq__(self, other) -> bool:
        # "Checkes if two cards are identical"
        if self is None:
            return other is None
        elif other is None:
            return False
        return self.rank == other.rank and self.suit == other.suit

    def get_rank(self):
        return self.rank

    def get_suit(self):
        return self.suit
    
    def get_card(self):
        return self.rank + self.suit

    def get_rank_index(self):
        return self.rank_index

    def get_suit_index(self):
        return self.suit_index
    
    def __str__(self):
        return repr(self.rank + self.suit)

    def __repr__(self):
        return repr(self.rank + self.suit)