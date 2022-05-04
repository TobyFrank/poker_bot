import constants
from card import Card
from player import Player
from table import Table
from deck import Deck
from renderer import Renderer
import treysevaluator

# Interface class keeps track of all player inputs and makes changes to the state classes based on inputs
# parameters: player1, table, current_bet, players_in
# TODO: Implement keeping track of bets and players in the hand still

CARD_POSITIONS = {
    "board": [(235, 160), (265, 160), (295, 160), (325, 160), (355, 160)], 
    0: [(185, 240), (215, 240)],
    1: [(80, 190), (110, 190)], 
    2: [(80, 130), (110, 130)], 
    3: [(185, 80), (215, 80)], 
    4: [(280, 80), (310, 80)], 
    5: [(375, 80), (405, 80)],
    6: [(480, 130), (510, 130)],
    7: [(480, 190), (510, 190)],
    8: [(375, 240), (405, 240)]
    }


class Interface:
    def __init__(self):
        manual_input = input("Manual or automatic param eval? (M/A)")
        manual = True if manual_input == "M" else False
        if manual:
            num_players = int(input("Enter number of players:"))
            hole_card1 = input("Enter first hole card: eg:As")
            hole_card2 = input("Enter second hole card: eg:Ac")
            position = int(input("What index are you at? (dealer is index 0, turn order)")) # TODO: make this more user-friendly
            blind_size = int(input("What is the small blind size?"))
            stack_size = int(input("How many chips do you have?"))
            round = input("Where in turn are you? [pre-flop, flop, turn, river]")
            self.setup(num_players, hole_card1, hole_card2, position, blind_size, stack_size, round)
        else:
            self.setup()

    def setup(self, num_players: int = 6, hole_card1: str = "Ah", hole_card2: str = "As", position: int = 0, blind_size: int = 25, stack_size: int = 500, round: str = "pre-flop"):
        self.players_in_round = [x for x in range(num_players)]
        self.players_in = [[x, 0] for x in range(num_players)]
        self.players_in[1][1] = blind_size
        self.players_in[2][1] = 2*blind_size
        self.players_in = self.players_in[3:] + self.players_in[0:3]
        self.current_bet = 2*blind_size
        hole_cards = (Card(hole_card1), Card(hole_card2))
        self.deck = Deck(constants.suit_list, constants.rank_list)
        for hole_card in hole_cards:
            self.deck.remove_card(hole_card)
        if round == "pre-flop":
            round_index = 0
            self.player1 = Player(hole_cards, stack_size, [])
            self.table = Table(num_players, position, blind_size, round, round_index)
        else:
            board_cards = input("Enter board cards: (eg: Ks, Ah, Ad)")
            round_index = len(board_cards) - 2
            pot_size = int(input("What is the current pot size?"))
            board = [Card(params) for params in board_cards.split(", ")]
            for board_card in board:
                self.deck.remove_card(board_card)
            self.player1 = Player(hole_cards, stack_size, board)
            self.table = Table(num_players, position, blind_size, round, round_index, pot_size)
        dealer_pos = (0 - self.table.peek_pos())%self.table.peek_players()
        self.renderer = Renderer([card.get_card() for card in hole_cards], num_players, dealer_pos)
        lookup_for_renderer = [pos[0] for pos in self.players_in]
        self.renderer.update_pot(str(blind_size), (num_players-2-lookup_for_renderer.index(self.table.peek_pos()))%num_players, "chip")
        self.renderer.update_pot(str(2*blind_size), (num_players-1-lookup_for_renderer.index(self.table.peek_pos()))%num_players, "chip")
        self.print_stats()                                                                                                                                                                                      

    def print_stats(self):
        print(f"Current round: {self.table.peek_round()}", self.player1, self.table, sep="\n")          

    ### METHODS FOR DISPLAYING CONTENT ###

    
    
    
    ### METHODS FOR INCREMENTING THE ROUND / STARTING A NEW HAND ###

    def next_round(self):
        if self.table.peek_round()[0] == "river":
            self.new_hand()
        else:
            self.table.next_round()
            self.current_bet = 0
            players_in_temp = [player[0] for player in self.players_in]
            players_in_temp.sort()
            if players_in_temp[0] == 0:
                players_in_temp = players_in_temp[1:] + [players_in_temp[0]]
            self.players_in = [[player, 0] for player in players_in_temp]
            self.players_in_round = [player[0] for player in self.players_in]
            self.renderer.setup([card.get_card() for card in self.player1.peek_cards()], len(self.players_in_round), self.renderer.peek_dealer_pos(), False)
            self.renderer.update_pot(str(self.table.peek_pot()), "pot", "pot")
            self.deal_board_cards()
            self.print_stats()
        self.play_hand()

    def deal_board_cards(self):
        new_board_input = input("Enter new board cards: (eg: Ks, Ac, Ad)")
        new_board = [Card(params) for params in new_board_input.split(", ")]
        self.player1.update_board(new_board)
        for i in range(len(self.player1.peek_board())):
            # self.deck.remove_card(new_board[i])
            card_str = self.player1.peek_board()[i].get_card()
            round = CARD_POSITIONS["board"][i]
            self.renderer.load_card(card_str, round)

    def new_hand(self):
        blind_change_input = input("Did the blinds change? (Y/N)")
        blind_change = True if blind_change_input == "Y" else False
        win_pot_input = input("Did you win the pot? (Y/N)")
        win_pot = True if win_pot_input == "Y" else False
        self.deck.setup()
        self.resolve_pot(win_pot)
        self.check_eliminate_player()
        self.table.next_hand(blind_change)
        self.deal_hole_cards()
        self.player1.board = []
        self.players_in = [[x, 0] for x in range(self.table.peek_players())]
        self.players_in[1][1] = self.table.peek_sb()
        self.players_in[2][1] = 2*self.table.peek_sb()
        self.players_in = self.players_in[3:] + self.players_in[0:3]
        self.players_in_round = [player[0] for player in self.players_in]
        self.current_bet = 2*self.table.peek_sb()
        dealer_pos = (0 - self.table.peek_pos())%self.table.peek_players()
        self.renderer.setup([card.get_card() for card in self.player1.peek_cards()], len(self.players_in), dealer_pos)
        lookup_for_renderer = [pos[0] for pos in self.players_in]
        self.renderer.update_pot(str(self.table.peek_sb()), (self.table.peek_players()-2-lookup_for_renderer.index(self.table.peek_pos()))%self.table.peek_players(), "chip")
        self.renderer.update_pot(str(2*self.table.peek_sb()), (self.table.peek_players()-1-lookup_for_renderer.index(self.table.peek_pos()))%self.table.peek_players(), "chip")
        print(f"New Hand: You are {constants.positions_dict[self.table.peek_pos()]}")
        self.print_stats()


    def resolve_pot(self, win_pot):
        if win_pot:
            self.player1.update_chips(self.table.peek_pot())

    def check_eliminate_player(self):
        player_elim_input = int(input("How many players were eliminated?"))
        player_elim = True if player_elim_input > 0 else False
        if player_elim:
            for i in range(player_elim_input):
                player_elim_index = int(input("What index (dealer = 0) was the player eliminated at?"))
                self.table.eliminate_player(player_elim_index)

    def deal_hole_cards(self):
        hole_card1_input = input("What is your first hole card? (eg: Ah)")
        hole_card2_input = input("What is your second hole card? (eg: As)")
        hole_card1 = Card(hole_card1_input)
        hole_card2 = Card(hole_card2_input)
        self.player1.new_hand((hole_card1, hole_card2))
        for card in [hole_card1, hole_card2]:
            self.deck.remove_card(card)

    ### METHODS FOR BETTING ###

    def play_hand(self):
            player_queue = [player for player in self.players_in]
            while len(player_queue) != 0:
                # print(player_queue)
                player_info = player_queue[0]
                player_index = player_info[0]
                player_bet = player_info[1]
                if self.table.peek_round()[0] == "pre-flop":
                    index_port = (self.renderer.peek_dealer_pos() + self.players_in_round.index(player_index))%len(self.players_in_round)
                else:
                    index_port = (self.renderer.peek_dealer_pos() + self.players_in_round.index(player_index)+1)%len(self.players_in_round)
                # print(index_port)
                if player_index == self.table.peek_pos():
                    # call evaluator for action
                    cards = self.player1.peek_cards()
                    hole_card1, hole_card2 = self.player1.treyscards()
                    board = self.player1.peek_board()
                    # treysboard = self.player1.treysboard()
                    if board != []:
                        treysevaluator.treyseval(hole_card1, hole_card2, board)
                    print(f"You ({constants.positions_dict[player_index]}) are playing. Your best hand is: {self.player1.calculate_best_hand()}. {self.current_bet - player_bet} to call")
                    player_action_input = input("What did you do? (check, call, bet, fold)")
                else:
                    print(f"{constants.positions_dict[player_index]} is playing. {self.current_bet - player_bet} to call")
                    player_action_input = input("What did the player do? (check, call, bet, fold)")
                if player_action_input == "check":
                    pass
                elif player_action_input == "call":
                    self.update_player_bet(player_info, self.current_bet)
                    self.renderer.update_pot(str(self.current_bet), index_port, "chip")
                elif player_action_input == "bet":
                    player_bet_input = int(input(f"How much did player {player_index} bet?"))
                    self.change_call_bet(player_bet_input)
                    self.update_player_bet(player_info, self.current_bet)
                    self.renderer.update_pot(str(self.current_bet), index_port, "chip")
                    # Update the queue so that other players have a chance to bet
                    player_position = self.players_in.index([player_index, self.current_bet])
                    player_queue += self.players_in[:player_position]
                else:
                    if player_index == self.table.peek_pos():
                        print("You folded! Next hand")
                        self.new_hand()
                        self.play_hand()
                    else:
                        self.renderer.update_pot("", index_port, "chip")
                        self.player_folds(player_info)

                player_queue.pop(0)
            for player in self.players_in:
                self.table.register_bet(player[1])
            if len(self.players_in) <= 1:
                if len(self.players_in) == 0:
                    print("\n\n### No players left in hand, something went wrong ###\n\n")
                print(f"Player {self.players_in[0][0]} wins the hand!")
                self.new_hand()
                self.play_hand()
            else:   
                self.next_round()

    def change_call_bet(self, bet):
        self.current_bet = bet

    def player_folds(self, player_info):
        index_players_in = self.players_in.index(player_info)
        self.table.register_bet(self.players_in[index_players_in][1])
        self.players_in.remove(player_info)

    def update_player_bet(self, player_info, bet):
        index_players_in = self.players_in.index(player_info)
        self.players_in[index_players_in][1] = bet
