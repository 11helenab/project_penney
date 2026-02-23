import os
import random
import itertools
import numpy as np

# bring in deck(s) of cards
def generate_deck(n_decks):
    deck = []
    for _ in range(n_decks):
        deck += [0]*26 + [1]*26
    random.shuffle(deck) # should we use a seed?
    return deck

# create all possible sequence combinations
N_BITS = 3
x = list(range(2**3)) #all 3 card combinations of 2 choices (8)
choices = [f'{xi:b}'.zfill(3) for xi in range(2**N_BITS)] #0s and 1s 

combinations = list(itertools.product(choices, choices))
combinations = list(map(list, combinations))

def rons_method(choice_a, choice_b, n_decks):
    deck = generate_deck(n_decks)
    upturned = []
    score_a = 0
    score_b = 0

    while len(deck) > 0:
        # flip a card
        card = deck.pop(0)
        upturned.append(card)

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

def win_probability(choice_a, choice_b, n_decks, N=5000):
    wins_a = 0
    wins_b = 0
    ties = 0

    for _ in range(N):
        score_a, score_b = rons_method(choice_a, choice_b, n_decks)

        if score_a > score_b:
            wins_a += 1
        elif score_b > score_a:
            wins_b += 1
        else: ties += 1
        win_a_prob = wins_a/N
        win_b_prob = wins_b/N
        ties_prob = ties/N
    return win_a_prob, win_b_prob, ties_prob

def save_scores(win_a_prob: float, win_b_prob: float, 
                ties_prob: float, filename: str) -> None:
    'save the win probabilities to an output folder'
    folder = 'data'
    file_path = os.path.join(folder, str)

    if not os.path.exists(folder):
        os.mkdir(folder)

    if os.path.exists(file_path):
        raise FileExistsError(f'File {filename} already exists')
    
    np.save(file_path, win_a_prob)
    np.save(file_path, win_b_prob)
    np.save(file_path, ties_prob)