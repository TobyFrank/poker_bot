import Treys
import card


def treyseval(holecard1, holecard2, boardcards):
    evaluator = Treys.Evaluator()
    deck = Treys.Deck()
    player_hand = [Treys.Card.new(str(holecard1)),Treys.Card.new(str(holecard2))]
    board = []
    #print(boardcards)
    for i in boardcards:
        boardcard = card.Card.get_card(i)
        #print(boardcard)
        board.append(Treys.Card.new(boardcard))
    player_score = evaluator.evaluate(board, player_hand)
    rank = evaluator.evaluate(player_hand, board)
    rank_class = evaluator.get_rank_class(rank)
    class_string = evaluator.class_to_string(rank_class)
    percentage = 1.0 - evaluator.get_five_card_rank_percentage(rank)
    print("Player hand = {}, percentage rank among all hands = {}".format(class_string, percentage))
    if percentage >= 0.5:
        return print("Action suggested: bet/raise")
    else:
        return print("Action suggested: check/fold")
    


