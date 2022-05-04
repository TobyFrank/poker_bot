import constants
import methods
from card import Card
from deck import Deck

# Player class keeps track of all information secret to the user
# - properties: hand (List of Cards), chips (int), board cards (List of Cards)

class Player:
    def __init__(self, hand, chips, board):
        self.card1 = hand[0]
        self.card2 = hand[1]
        self.chips = chips
        self.board = board     

    ### METHODS TO RETURN VALUES ###

    def peek_cards(self):
        return self.card1, self.card2

    def peek_chips(self):
        return self.chips

    def peek_board(self):
        return self.board

    ### METHODS TO CHANGE VALUES ###

    def new_hand(self, hand):
        self.card1 = hand[0]
        self.card2 = hand[1]
    
    def update_chips(self, delta):
        self.chips += delta
    
    def update_board(self, card_list):
        self.board += card_list

    ### OTHER METHODS ###

    def treyscards(self):
        card1 = Card.get_card(self.card1)
        card2 = Card.get_card(self.card2)
        return card1, card2

    def treysboard(self):
        cards = []
        for i in self.board:
            card = Card.get_card(i)
            cards += card
        return cards

    def calculate_best_hand(self):
        hand = [self.card1, self.card2]
        all_cards = hand + self.board
        return methods.best_hand_calculator(all_cards)

    def __str__(self):
        return f"Player: {(repr(self.card1), repr(self.card2))} hole cards, {self.chips} chips, {[repr(card) for card in self.board]} on the board"