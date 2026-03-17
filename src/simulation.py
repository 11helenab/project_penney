import numpy as np
import os
import itertools
import pandas as pd
import shutil

from src.generatedeck import create_deck, save_deck
from src.scoring import scoring

# paths for accessing and saving data
DATA_PATH_SCORED = "data/scored"
DATA_PATH_UNSCORED = "data/unscored"
DATA_PATH = "data"
PATH_SEED = os.path.join(DATA_PATH, 'next_seed.txt')
#RAW_DECK_FILE = os.path.join(DATA_PATH, "all_decks.npy")
#TEST_DECK_FILE = os.path.join(DATA_PATH, "test_deck2.npy")
RESULTS_FILE = os.path.join(DATA_PATH, "combined_results.npy")
CSV_FILE = os.path.join(DATA_PATH, "heatmap_data.csv")

# max decks per file
MAX_DECKS = 1000

os.makedirs("data", exist_ok=True)

def get_seed() -> int:
    '''
    Return the number stored in PATH_SEED.
    This is the next seed to be used in
    random array generation.
    '''
    if os.path.exists(PATH_SEED):
        with open(PATH_SEED, 'r', encoding='utf-8') as f:
            seed = int(f.read().split()[0])
    else:
        seed = 0
    return seed

def update_seed(new_seed: int) -> None:
    '''
    Update the number stored in PATH_SEED to new_seed.
    '''
    with open(PATH_SEED, 'w', encoding='utf-8') as f:
        f.write(str(new_seed))
    return None

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
    return choices

def initialize_results():
    '''
    Stores win/tie counts for Player 2.
    Probability of wins/ties will be calculated later in the heatmap scripts.
    '''
    return {
        "card_wins_p2": np.zeros((8, 8), dtype=int),
        "card_ties": np.zeros((8, 8), dtype=int),
        "trick_wins_p2": np.zeros((8, 8), dtype=int),
        "trick_ties": np.zeros((8, 8), dtype=int),
        "total_decks": 0
    }

def load_results():
    '''
    Load previous results if they exist.
    If not, create empty results dictionary.
    '''
    if os.path.exists(RESULTS_FILE):
        # access former game results if they exist
        return np.load(RESULTS_FILE, allow_pickle=True).item()
    else:
        return initialize_results()

def save_results(results: dict):
    """
    Save combined old and new results.
    """
    np.save(RESULTS_FILE, results)

def save_decks(new_decks):
    #THIS CAN BE DELETED EVENTUALLY
    '''
    Append new decks to existing all_decks.npy.
    Store decks at int8 for size safety - ask Ron about this.
    '''
    new_decks = np.array(new_decks, dtype=np.int8)

    if os.path.exists(RAW_DECK_FILE):
        old_decks = np.load(RAW_DECK_FILE, allow_pickle=True)
        combined = np.vstack((old_decks, new_decks)) # vertically stacks arrays
    else:
        combined = new_decks
    
    np.save(RAW_DECK_FILE, combined)

def save_deck_chunks(decks: list, seed: int):
    '''
    Save one chunk of decks to its own file.
    '''
    filename = os.path.join(DATA_PATH_UNSCORED, f"rawdeck_{seed}.npy")
    np.save(filename, np.array(decks, dtype=np.int8)) 

def save_heatmap_csv(results, sequences):
    '''
    Saves win data in a CSV containing:
        - seq_a and seq_b
        - card_wins_p2 and card_ties_p2
        - trick_wins_p2 and trick_ties_p2
    '''

    rows = []
    total = results["total_decks"]

    for i, seq_a in enumerate(sequences):
        for j, seq_b in enumerate(sequences):

            card_wins = results["card_wins_p2"][i, j]
            card_ties = results["card_ties"][i, j]

            trick_wins = results["trick_wins_p2"][i, j]
            trick_ties = results["trick_ties"][i, j]

            rows.append({
                "seq_a": seq_a,
                "seq_b": seq_b,

                "card_wins_p2": card_wins,
                "card_ties_p2": card_ties,

                "trick_wins_p2": trick_wins,
                "trick_ties_p2": trick_ties
            })

    df = pd.DataFrame(rows)
    df.to_csv(CSV_FILE, index=False)


def deck_gen(n_decks: int):
    '''
    Run simulation for both "ron" and "tricks" methods.
    Update win/tie counts for player 2.
    Returns:
        - All decks
        - Raw results (.npy)
        - Heatmap CSV data
    '''
    new_decks = []
    remaining = n_decks

    while remaining > 0:
        seed = get_seed()
        np.random.seed(seed)

        # if there is less than # max decks left -> pick remaining deck number
        chunk_size = min(MAX_DECKS, remaining)
        decks_chunk = []

        for _ in range(chunk_size):

            deck = create_deck()
            decks_chunk.append(deck)

        # save this chunk of decks
        save_deck_chunks(decks_chunk, seed)

        # increment seed
        update_seed(seed + 1)

        remaining -= chunk_size



def scoring_new()-> list:
    sequences = generate_sequences()
    results = load_results()

    #this function needs to read in everything from the unscored folder, score it and move it to the scored folder

    for filename in os.listdir(DATA_PATH_UNSCORED):
        file_path = os.path.join(DATA_PATH_UNSCORED, filename)
    
        data = np.load(file_path)

        for i, seq_a in enumerate(sequences):
            for j, seq_b in enumerate(sequences):
                for deck in data:
                    deck_copy = deck.copy()
                            
                    # running both methods at the same time
                    cards_a, tricks_a, cards_b, tricks_b = scoring(deck_copy, seq_a, seq_b)

                    # Ron's method
                    if cards_b > cards_a:
                        results["card_wins_p2"][i, j] += 1
                    elif cards_b == cards_a:
                        results["card_ties"][i, j] += 1
                            
                    # Trick method
                        if tricks_b > tricks_a:
                            results["trick_wins_p2"][i, j] += 1
                        elif tricks_b == tricks_a:
                            results["trick_ties"][i, j] += 1

                    results["total_decks"] += 1
                    #END OF FOR LOOP

        #move the file to the scored folder
        new_path = f'{DATA_PATH_SCORED}/{filename}'
        shutil.move(file_path, new_path)
    
    # save combined results
    save_results(results)

    # save CSV for heatmaps
    save_heatmap_csv(results, sequences)

    return results

def run_simulation(n_decks: int):
    #CAN DELETE THIS EVENTUALLY
    '''
    Run simulation for both "ron" and "tricks" methods.
    Update win/tie counts for player 2.
    Returns:
        - All decks
        - Raw results (.npy)
        - Heatmap CSV data
    '''

    sequences = generate_sequences()
    results = load_results()

    new_decks = []
    remaining = n_decks

    while remaining > 0:
        seed = get_seed()
        np.random.seed(seed)

        # if there is less than # max decks left -> pick remaining deck number
        chunk_size = min(MAX_DECKS, remaining)
        decks_chunk = []

        for _ in range(chunk_size):

            deck = create_deck()
            decks_chunk.append(deck)

            for i, seq_a in enumerate(sequences):
                for j, seq_b in enumerate(sequences):
                    deck_copy = deck.copy()
                    
                    # running both methods at the same time
                    cards_a, tricks_a, cards_b, tricks_b = scoring(deck_copy, seq_a, seq_b)

                    # Ron's method
                    if cards_b > cards_a:
                        results["card_wins_p2"][i, j] += 1
                    elif cards_b == cards_a:
                        results["card_ties"][i, j] += 1
                    
                    # Trick method
                    if tricks_b > tricks_a:
                        results["trick_wins_p2"][i, j] += 1
                    elif tricks_b == tricks_a:
                        results["trick_ties"][i, j] += 1

            results["total_decks"] += 1
            #END OF FOR LOOP

        # save this chunk of decks
        save_deck_chunks(decks_chunk, seed)

        # increment seed
        update_seed(seed + 1)

        remaining -= chunk_size
    
    # save combined results
    save_results(results)

    # save CSV for heatmaps
    save_heatmap_csv(results, sequences)

    return results