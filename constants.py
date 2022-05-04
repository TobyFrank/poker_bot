suit_list = ("s", "c", "h", "d") # list of suits
rank_list = ("2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A")
rank_string = "23456789TJQKA" #string of all possible card values

suit_list_dict = {"s":1, "c":2, "h":3, "d":4} # list of suits
rank_value_dict = {"2":2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}

hand_rankings = ("Straight Flush", "Four of a Kind", "Full House", "Flush", "Straight", "Three of a Kind", "Two Pair", "Pair", "High Card") #ranking of all possible handsnds
hand_rankings_dict = {8: "Straight Flush", 7: "Four of a Kind", 6: "Full House", 5: "Flush", 4: "Straight", 3: "Three of a Kind", 2: "Two Pair", 1: "Pair", 0: "High Card"} #ranking of all possible hands
round_dict = {0: "pre-flop", 1: "flop", 2: "turn", 3: "river"}

positions_dict = {0: "Button", 1: "SB", 2: "BB", 3: "UTG", 4: "UTG+1", 5: "UTG+2", 6: "LJ", 7: "HJ", 8: "CO"}