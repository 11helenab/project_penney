import numpy as np

def trick_method(choice_a, choice_b, n_decks):
    ''' 
    placeholder function for the trick method
    '''
    return

def rons_method(deck: np.ndarray, choice_a: str, choice_b: str):
    '''
    Ron's scoring method:
    Player's win all upturned cards when their sequence appears
    '''
    deck = list(deck)
    upturned = []
    rscore_a = 0
    rscore_b = 0

    while len(deck) > 0:
        # flip a card
        card = deck.pop(0)
        upturned.append(card)

        # only check once there are 3 cards
        if len(upturned) >= 3:
            last_three = ''.join(str(i) for i in upturned[-3:])
            if last_three == choice_a:
                rscore_a += len(upturned)
                upturned = []
            elif last_three == choice_b:
                rscore_b += len(upturned)
                upturned = []
    return rscore_a, rscore_b