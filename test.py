from interface import Interface
from player import Player
from table import Table
from deck import Deck
from card import Card
import constants
import methods


print("\n\n### Poker Bot Time! ###\n")

test_interface = Interface()
test_interface.play_hand()





























# ### TEST CASES FOR METHODS ###
# print("\n\n### Test cases for methods ###\n")

# #Test case: flush (s), straight 2-6
# sample_hand1 = [Card("2s"), Card("3s"), Card("4s"), Card("5s"), Card("6s"), Card("Ks"), Card("Qs")]
# #Test case: straight, 4-8
# sample_hand2 = [Card("2s"), Card("3c"), Card("4s"), Card("5s"), Card("6s"), Card("7h"), Card("8d")]
# #Test case: nothing
# sample_hand3 = [Card("2s"), Card("3c"), Card("4s"), Card("5s"), Card("7s"), Card("Qd"), Card("Kh")]
# #Test case: two straights, 3-7 & J-A
# sample_hand4 = [Card("3c"), Card("4s"), Card("5s"), Card("6c"), Card("7s"), Card("Tc"), Card("Jd"), Card("Qd"), Card("Kh"), Card("Ac")]
# #Test case: quads 
# sample_hand5 = [Card("2s"), Card("Kc"), Card("4s"), Card("5s"), Card("Ks"), Card("Kd"), Card("Kh")]
# #Test case: full house, K's and 5 pair
# sample_hand6 = [Card("2s"), Card("Kc"), Card("4s"), Card("5s"), Card("Ks"), Card("5d"), Card("Kh")]
# #Test case: two-pair, K's and 5's 8-high
# sample_hand7 = [Card("2s"), Card("Kc"), Card("4s"), Card("5s"), Card("Ks"), Card("5d"), Card("8h")]

# print(constants.hand_rankings_dict)
# print(methods.best_hand_calculator(sample_hand1))
# print(methods.best_hand_calculator(sample_hand2))
# print(methods.best_hand_calculator(sample_hand3))
# print(methods.best_hand_calculator(sample_hand4))
# print(methods.best_hand_calculator(sample_hand5))
# print(methods.best_hand_calculator(sample_hand6))
# print(methods.best_hand_calculator(sample_hand7))


### TEST CASES FOR INTERFACE ###
# print("\n\n### Poker Bot Time! ###\n")

# test_interface = Interface()
# test_interface.setup()
# test_interface.play_hand()
# test_interface.next_round()
# test_interface.next_round()
# test_interface.next_round()
# test_interface.next_round()


# ### TEST CASES FOR PLAYER ###
# print("\n\n### Test cases for player ###\n")

# test_deck = Deck(constants.suit_list, constants.rank_list) 
# test_player = Player((Card("As"), Card("7d")), 500, [])
# # print(test_player)
# # test_player.update_chips(-200)
# test_player.update_board([Card("Ah"), Card("Ac"), Card("Kh"), Card("5s"), Card("8d")])len(self.player1.peek_board())
# # test_player.new_hand((Card("Ks"), Card("Kd")))
# # print(test_player)

# test_best_hand = test_player.calculate_best_hand()

# ### TEST CASES FOR DECK ###
# print("\n\n### Test cases for deck ###\n")

# print(constants.rank_list)
# test_deck = Deck(constants.suit_list, constants.rank_list)
# test_deck.remove_card(Card("As"))
# print(test_deck)