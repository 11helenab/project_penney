import numpy as np

def scoring(deck: np.ndarray, choice_a: str, choice_b: str):
    '''
    Ron's scoring method:
    Players win all upturned cards when their sequence appears
    Trick scoring method:
    Players win one point when their sequence appears.
    Input:
        deck: 1D np.array of 0s and 1s representing cards
        choice_a: 3-bit string for Player 1
        choice_b: 3-bit string for Player 2 (the user)
    Returns:
        total card scores and trick scores for each player for the deck.
    '''
    deck = deck.tolist() # convert the deck to a list
    upturned = []
    # initialize scores
    cards_a, cards_b = 0, 0
    tricks_a, tricks_b = 0,0

    while len(deck) > 0:
        # flip a card
        card = deck.pop(0)
        upturned.append(str(card)) # ensure card is a string

        # only check once there are 3 cards
        if len(upturned) >= 3:
            last_three = ''.join(str(i) for i in upturned[-3:])
            if last_three == choice_a:
                cards_a += len(upturned)
                tricks_a += 1
                upturned = []
            elif last_three == choice_b:
                cards_b += len(upturned)
                tricks_b += 1
                upturned = []
    return cards_a, tricks_a, cards_b, tricks_b