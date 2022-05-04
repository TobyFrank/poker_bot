import constants
from card import Card

# Table class keeps track of the table order, blinds, and pots
# - properties: num_players, position, small_blind, big_blind, round, pot_size

class Table:
    "Class stores number of players, order of user at table, size of small blind, size of ante, size of pot, current round"
    
    def __init__(self, num_players, pos, sb, round, round_index, pot_size: int = 0):
        self.num_players = num_players
        self.position = pos
        self.small_blind = sb
        self.big_blind = sb * 2
        self.round = round
        self.round_index = round_index
        self.pot_size = pot_size

    ### METHODS TO RETURN VALUES ###

    def peek_players(self):
        return self.num_players

    def peek_pos(self):
        return self.position

    def peek_sb(self):
        return self.small_blind

    def peek_round(self):
        return self.round, self.round_index

    def peek_pot(self):
        return self.pot_size

    ### METHODS TO CHANGE VALUES ###

    def next_hand(self, blind_increase: bool = False):
        self.position = (self.position - 1) % self.num_players
        if blind_increase:
            self.small_blind *= 2
            self.big_blind *= 2
        self.round = "pre-flop"
        self.round_index = 0
        self.pot_size = 0
        # print(f"Position: {self.position}, round: {self.round}, blinds: {self.small_blind}")

    def eliminate_player(self, player_index):
        self.num_players -= 1
        if player_index == self.position:
            print("Bad beat. Better luck next time!")
        if player_index < self.position:
            self.position -= 1
        print(f"Player count: {self.num_players}, position: {self.position}")
        
    def register_bet(self, bet_size):
        self.pot_size += bet_size

    def next_round(self):
        self.round_index = (self.round_index + 1) % 4
        self.round = constants.round_dict[self.round_index]

    def __str__(self):
        return f"Table: {self.num_players}-player game with {self.small_blind}/{self.big_blind} blinds. Round: {self.round} with {self.pot_size} pot. Player is {constants.positions_dict[self.position]}"

### TEST CASE ###
# num_players = int(input("Enter number of players:"))
# hole_cards = input("Enter hole cards: (eg: (\"As\", \"Ah\"))")
# position = int(input("What index are you at? (dealer is index 0, turn order)")) # TODO: make this more user-friendly
# blind_size = int(input("What is the small blind size?"))
# round = input("Where in turn are you? [pre-flop, flop, turn, river]")

# test_table = Table(num_players, position, blind_size, round)
# test_table.next_hand()
# test_table.eliminate_player(0)