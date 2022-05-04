import constants
from card import Card

# Calculating best hand from a list of cards

#potential source: https://www.codingthewheel.com/archives/poker-hand-evaluator-roundup/  

def best_hand_calculator(card_list):
    ranks = sorted(card.get_rank_index() for card in card_list)
    suits = [card.get_suit_index() for card in card_list]
    rank_map = build_rank_map(card_list)
    suit_map = build_suit_map(card_list)
    
    flush = has_flush(suit_map, rank_map)
    # print(f"Has flush: {flush}")
    straight = has_straight(rank_map, ranks, suits)
    # print(f"Has straight: {straight}")
    full_house = has_full_house(suit_map, rank_map, card_list)
    # print(f"Has full house: {full_house}")
    quads = has_quads(suit_map, rank_map, card_list)
    # print(f"Has quads: {quads}")
    trips = has_trips(suit_map, rank_map, card_list)
    # print(f"Has trips: {trips}")
    two_pair = has_two_pair(suit_map, rank_map, card_list)
    # print(f"Has two-pair: {two_pair}")
    pair = has_pair(suit_map, rank_map, card_list)
    # print(f"Has pair: {pair} \n")
    high_card = has_high_card(card_list)


    # Conditions for straight and flush
    if flush[0] and straight[0]:
        return straight[1]
    elif quads[0]:
        return quads[1]
    elif full_house[0]:
        return full_house[1]
    elif flush[0]:
        return flush[1]
    elif straight[0]:
        return straight[1]
    elif trips[0]:
        return trips[1]
    elif two_pair[0]:
        return two_pair[1]
    elif pair[0]:
        return pair[1]
    else:
        return high_card[1]
    

def has_flush(suit_map, rank_map):
    for key in suit_map:
        if len(suit_map[key]) >= 5:
            flush_cards = suit_map[key]
            # print(flush_cards)
            return True, get_n_highest_cards(5, flush_cards)
    return False, None
    
def has_quads(suit_map, rank_map, card_list):
    for key in rank_map:
        if len(rank_map[key]) == 4:
            return True, rank_map[key] + get_n_highest_cards(min(1, len(card_list)-2), diff_cards(card_list, rank_map[key]))
    return False, None

def has_straight(rank_map, ranks, suits):
    hand = []
    for i in reversed(range(min(ranks), max(ranks) + 1)):
        if all(rank in ranks for rank in reversed(list(range(i-4, i+1)))):
            for j in reversed(range(i-4, i+1)):
                hand.append(rank_map[j][0])
            return True, hand
    return False, None

def has_full_house(suit_map, rank_map, card_list):
# check if 3-of-a-kind, then if pair with remaining cards
    trips = has_trips(suit_map, rank_map, card_list)
    if trips[0]:
        diff = diff_cards(card_list, trips[1][0:3])
        pair = has_pair(suit_map, rank_map, diff)
        if pair[0]:
            return True, trips[1][0:3] + pair[1][0:2]
    return False, None

def has_trips(suit_map, rank_map, card_list):
    for key in rank_map:
        if len(rank_map[key]) == 3:
            diff =  diff_cards(card_list, rank_map[key])
            return True, rank_map[key] + get_n_highest_cards(min(2, len(card_list)-2), diff)
    return False, None

def has_two_pair(suit_map, rank_map, card_list):
    pair1 = has_pair(suit_map, rank_map, card_list)
    if pair1[0]:
        diff = diff_cards(card_list, pair1[1][0:2])
        suit_map2pair = build_suit_map(diff)
        rank_map2pair = build_rank_map(diff)
        pair2 = has_pair(suit_map2pair, rank_map2pair, diff)
        if pair2[0]:
            return True, pair1[1][0:2] + pair2[1][0:2] + get_n_highest_cards(min(1, len(card_list)-2), diff_cards(diff, pair2[1][0:2]))
    return False, None

def has_pair(suit_map, rank_map, card_list):
    for key in rank_map:
        if len(rank_map[key]) == 2:
            return True, rank_map[key] + get_n_highest_cards(min(3, len(card_list)-2), diff_cards(card_list, rank_map[key]))
    return False, None

def has_high_card(card_list):
    return True, get_n_highest_cards(min(5, len(card_list)), card_list)

def get_n_highest_cards(n, possible_cards):
    highest_cards = []
    cards = possible_cards
    for i in range(0, n):
        max_card = cards[0]
        for card in cards:
            if (max_card.get_rank_index() <= card.get_rank_index()):
                max_card = card
        highest_cards.append(max_card)
        cards.remove(max_card)
    return highest_cards

def build_suit_map(card_list):
    suit_map = {}
    for suit in range(1,5):
        suit_map[suit] = []
    for card in card_list:
        suit_map[card.get_suit_index()].append(card)
    return suit_map
    
def build_rank_map(card_list):
    rank_map = {}
    for rank in range(2,15):
        rank_map[rank] = []
    
    for card in card_list:
        rank_map[card.get_rank_index()].append(card)
    return rank_map

# Taken from https://www.geeksforgeeks.org/python-difference-two-lists/
def diff_cards(li1, li2):
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li_dif