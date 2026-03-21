# import statements
import numpy as np

def scoring(deck: np.ndarray, choice_a: str, choice_b: str):
    """
    Ron's scoring method:
    Players win all upturned cards when their sequence appears
    Trick scoring method:
    Players win one point when their sequence appears.
    Input:
        - deck: 1D np.array of 0s and 1s representing cards
        - choice_a: 3-bit string for Player 1
        - choice_b: 3-bit string for Player 2 (the user)
    Returns:
        - total card scores and trick scores for each player for the deck.
    """
    deck = deck.tolist() # convert the deck to a list
    upturned = [] # initialize empty list
    # initialize P1 and P2 scores at 0
    cards_a, cards_b = 0, 0
    tricks_a, tricks_b = 0,0

    while len(deck) > 0: # while there are still cards in deck
        card = deck.pop(0) # flip a card
        upturned.append(str(card)) # ensure card is a string

        # only look for sequence once there are 3 cards
        if len(upturned) >= 3:
            last_three = ''.join(str(i) for i in upturned[-3:]) # combine last 3 cards into one string
            if last_three == choice_a: # if sequence a is found in last 3 cards
                cards_a += len(upturned) # add the number of upturned card to P1 card score
                tricks_a += 1 # add 1 trick won to P1 trick score
                upturned = [] # reset upturned to empty list
            elif last_three == choice_b: # if sequence b is found in last 3 cards
                cards_b += len(upturned) # add the number of upturned card to P2 card score
                tricks_b += 1 # add 1 trick won to P2 trick score
                upturned = [] # reset upturned to empty list
            # keep flipping cards if neither sequence is found
    return cards_a, tricks_a, cards_b, tricks_b # return trick and card scores for P1 and P2