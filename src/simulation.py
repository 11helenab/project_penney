import numpy as np
import os
import itertools
from src.generatedeck import create_deck
from src.scoring import rons_method, trick_method

DATA_PATH = os.path("data")
os.makedirs(DATA_PATH, exist_ok=True)

def generate_sequences():
    '''
    Generate all 3-bit sequence combinations as strings.
    Returns:
        List of 8 sequences (ex: ['000',...,'111'])
    '''
    N_BITS = 3
    x = list(range(2**3)) #all 3 card combinations of 2 choices (8)
    choices = [f'{xi:b}'.zfill(3) for xi in range(2**N_BITS)] #0s and 1s 

    combinations = list(itertools.product(choices, choices))
    combinations = list(map(list, combinations))
    return combinations

def initialize_result_dict():
    '''
    Create a dictionary of 3 8x8 arrays holding the results of all possible combinations.
    '''
    return {
        "wins_a": np.zeros((8, 8), dtype=int),
        "wins_b": np.zeros((8, 8), dtype=int),
        "ties": np.zeros((8, 8), dtype=int),
        "total_decks": 0
    }

def load_results(method_name: str):
    '''
    Load previous results if they exist.
    If not, create empty results dictionary.
    '''
    os.makedirs(DATA_PATH, exist_ok=True)
    file_path = os.path.join(DATA_PATH, f"{method_name}_results.npy")

    if os.path.exists(file_path):
        return np.load(file_path).item()
    else:
        return initialize_result_dict()

def save_results(results: dict, method_name: str):
    """
    Save combined old and new results.
    """
    file_path = os.path.join(DATA_PATH, f"{method_name}_results.npy")
    np.save(file_path, results)

def run_simulation(n_decks: int, method: str = "ron"):
    '''
    Run simulation for specified method "ron" or "tricks".
    Default is set to "ron"
    '''
    sequences = generate_sequences()
    results = load_results(method)

    for _ in range(n_decks):
        deck = create_deck()

        for i, seq_a in enumerate(sequences):
            for j, seq_b in enumerate(sequences):

                if method == "ron":
                    score_a, score_b = rons_method(deck, seq_a, seq_b)
                elif method == "trick":
                    score_a, score_b = trick_method(deck, seq_a, seq_b)
                else:
                    raise ValueError("Unknown method.")

                # update results
                if score_a > score_b:
                    results["wins_a"][i, j] += 1
                elif score_b > score_a:
                    results["wins_b"][i, j] += 1
                else:
                    results["ties"][i, j] += 1

        results["total_decks"] += 1

    save_results(results, method)
    return results, sequences