import os
import numpy as np
from src.scoring import rons_method

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
    '''
    save the win probabilities to an output folder
    '''
    folder = 'data'
    file_path = os.path.join(folder, str)

    if not os.path.exists(folder):
        os.mkdir(folder)

    if os.path.exists(file_path):
        raise FileExistsError(f'File {filename} already exists')
    
    np.save(file_path, win_a_prob)
    np.save(file_path, win_b_prob)
    np.save(file_path, ties_prob)