import numpy as np

def trick_method(choice_a, choice_b, n_decks):
    ''' 
    placeholder function for the trick method
    '''
    return 0, 0, 0 # wins_a, wins_b, ties

def rons_method(deck: np.ndarray, choice_a: str, choice_b: str):
    '''
    Ron's scoring method:
    Player's win all upturned cards when their sequence appears
    Input:
        deck: 1D np.array of 0s and 1s representing cards
        choice_a: 3-bit string for Player 1
        choice_b: 3-bit string for Player 2 (the user)
    Returns:
        total scores for each player for the deck.
    '''
    deck = deck.tolist() # convert the deck to a list
    upturned = []
    score_a, score_b = 0, 0

    while len(deck) > 0:
        # flip a card
        card = deck.pop(0)
        upturned.append(str(card)) # ensure card is a string

        # only check once there are 3 cards
        if len(upturned) >= 3:
            last_three = ''.join(str(i) for i in upturned[-3:])
            if last_three == choice_a:
                score_a += len(upturned)
                upturned = []
            elif last_three == choice_b:
                score_b += len(upturned)
                upturned = []
    return score_a, score_b