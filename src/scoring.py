import os
import random
import itertools
import numpy as np

PATH_DATA = 'data'

def load_data(filename: str) -> np.ndarray:
    '''
    Loads deck data from an .npy file located in the default data directory.
    '''
    return np.load(os.path.join(PATH_DATA, filename))

# create all possible sequence combinations
N_BITS = 3
x = list(range(2**3)) #all 3 card combinations of 2 choices (8)
choices = [f'{xi:b}'.zfill(3) for xi in range(2**N_BITS)] #0s and 1s 

combinations = list(itertools.product(choices, choices))
combinations = list(map(list, combinations))

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

def win_probability(choice_a, choice_b, n_decks, N=5000):
    rwins_a = 0
    rwins_b = 0
    rties = 0

    for _ in range(N):
        rscore_a, rscore_b = rons_method(choice_a, choice_b, n_decks)

        if rscore_a > rscore_b:
            rwins_a += 1
        elif rscore_b > rscore_a:
            rwins_b += 1
        else: rties += 1
        rwin_a_prob = rwins_a/N
        rwin_b_prob = rwins_b/N
        rties_prob = rties/N
    return rwin_a_prob, rwin_b_prob, rties_prob

def save_scores(rwin_a_prob: float, rwin_b_prob: float, 
                rties_prob: float, filename: str) -> None:
    '''
    save the win probabilities to an output folder
    '''
    folder = 'data'
    file_path = os.path.join(folder, str)

    if not os.path.exists(folder):
        os.mkdir(folder)

    if os.path.exists(file_path):
        raise FileExistsError(f'File {filename} already exists')
    
    np.save(file_path, rwin_a_prob)
    np.save(file_path, rwin_b_prob)
    np.save(file_path, rties_prob)