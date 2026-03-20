# import statements
import numpy as np
import os
import itertools
import pandas as pd
import shutil

# import functions from other .py files in src folder
from src.generatedeck import create_deck
from src.scoring import scoring

# paths for accessing and saving data
DATA_PATH_SCORED = "data/scored" # scored folder
DATA_PATH_UNSCORED = "data/unscored" # unscored folder
DATA_PATH = "data" # data folder
PATH_SEED = os.path.join(DATA_PATH, 'next_seed.txt') # seed number .txt file
RESULTS_FILE = os.path.join(DATA_PATH, "combined_results.npy") # results .npy file
CSV_FILE = os.path.join(DATA_PATH, "heatmap_data.csv") # same as results file but in .csv format for heatmaps

# max decks per file (chunk size)
MAX_DECKS = 1000

# make data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

def get_seed() -> int:
    """
    Return the number stored in PATH_SEED.
    This is the next seed to be used in random array generation.
    """
    if os.path.exists(PATH_SEED): # check if file exists
        with open(PATH_SEED, 'r', encoding='utf-8') as f: # open in read-only mode
            seed = int(f.read().split()[0]) # splits and extracts first token then converts it to an int
    else:
        seed = 0 # if file empty, seed is 0
    return seed

def update_seed(new_seed: int) -> None:
    """
    Update the number stored in PATH_SEED to new_seed.
    Inputs:
        - next seed number (old seed + 1)
    Returns:
        - None
    """
    with open(PATH_SEED, 'w', encoding='utf-8') as f:
        f.write(str(new_seed))
    return None

def generate_sequences() -> list:
    '''
    Generate all 3-bit sequence combinations of cards as strings.
    Returns:
        - List of 8 sequences (ex: ['000',...,'111'])
    '''
    N_BITS = 3 # define length of binary string
    choices = [f'{xi:b}'.zfill(3) for xi in range(2**N_BITS)] # convert int into binary string
                                                              # and pad string with leading zeros
                                                              # to always be 3 characters long
    return choices # return list of 8 (2**3) choices of three-card sequences

def initialize_results() -> dict:
    """
    Stores win/tie counts for Player 2.
    Probability of wins/ties will be calculated later in the heatmap scripts.
    """
    # initialize an 8x8 array for each win/tie variable and save total_deck number
    return {
        "card_wins_p2": np.zeros((8, 8), dtype=int),
        "card_ties": np.zeros((8, 8), dtype=int),
        "trick_wins_p2": np.zeros((8, 8), dtype=int),
        "trick_ties": np.zeros((8, 8), dtype=int),
        "total_decks": 0
    }

def load_results() -> dict:
    """
    Load previous results if they exist.
    If not, create empty results dictionary.
    """
    if os.path.exists(RESULTS_FILE):
        # access former game results if they exist
        return np.load(RESULTS_FILE, allow_pickle=True).item()
    else:
        return initialize_results()

def save_results(results: dict) -> None:
    """
    Save combined old and new results.
    """
    np.save(RESULTS_FILE, results) # appends results to RESULTS_FILE

def save_deck_chunks(decks: list, seed: int) -> None:
    """
    Save one chunk of 1,000 decks to its own file.
    """
    # unique file names generated using seed number
    filename = os.path.join(DATA_PATH_UNSCORED, f"rawdeck_{seed}.npy")
    # save decks as arrays
    np.save(filename, np.array(decks, dtype=np.int8)) 

def save_heatmap_csv(results: dict, sequences: list) -> None:
    """
    Saves win data in a CSV containing:
        - seq_a and seq_b
        - card_wins_p2 and card_ties_p2
        - trick_wins_p2 and trick_ties_p2
    """

    rows = [] # initialize list

    # set i as index and seq_a as the current val of P1's choice
    for i, seq_a in enumerate(sequences):
        # set j as index and seq_b as the current val of P2's choice (user)
        for j, seq_b in enumerate(sequences):

            # wins and ties from perspective of P2, 
            # save in respective spot in results based on index
            card_wins = results["card_wins_p2"][i, j]
            card_ties = results["card_ties"][i, j]

            trick_wins = results["trick_wins_p2"][i, j]
            trick_ties = results["trick_ties"][i, j]

            # append current sequence of P1 and P2 and P2 wins/ties to list rows
            rows.append({
                "seq_a": seq_a,
                "seq_b": seq_b,

                "card_wins_p2": card_wins,
                "card_ties_p2": card_ties,

                "trick_wins_p2": trick_wins,
                "trick_ties_p2": trick_ties
            })

    # convert list rows into dataframe
    df = pd.DataFrame(rows)
    # convert dataframe to csv file for easier heatmap plotting
    df.to_csv(CSV_FILE, index=False)


def deck_gen(n_decks: int) -> None:
    """
    Generate and save chunks of decks based on user-inputted integer.
    Increment the seed by 1 for every chunk of 1,000 decks saved.
    """
    # number of decks left to generate
    remaining = n_decks

    while remaining > 0: # if there are more decks to generate
        seed = get_seed() # get the current seed number
        np.random.seed(seed) # set seed to that seed number

        # chunk_size is 1,000 unless there is <1,000 decks remaining, 
        # then save chunk as number of remaining decks
        chunk_size = min(MAX_DECKS, remaining) # picks smaller number
        decks_chunk = [] # initialize empty list

        for _ in range(chunk_size): # Increments through numbers 0-999 (or less if fewer decks left)

            deck = create_deck() # create current deck number
            decks_chunk.append(deck) # append deck to the current chunk of decks

        # save this chunk of decks using current seed as file name
        save_deck_chunks(decks_chunk, seed)

        # increment seed by 1
        update_seed(seed + 1)

        # subtract the most recent number of decks created (chunk_size) from number of decks left to create
        remaining -= chunk_size

def scoring_new() -> dict:
    """
    Score all unscored deck files by iterating through and evaluating every sequence matchup.
        - Loads unscored deck chunks
        - Computes card and trick results for all sequence pairs
        - Updates total results and moves files to scored directory
        - Saves results dictionary and heatmap CSV
    Returns:
        dict: Updated results dictionary
    """
    sequences = generate_sequences() # run generating sequences function
    results = load_results() # run load_results function

    for filename in os.listdir(DATA_PATH_UNSCORED): # accessed unscored decks
        file_path = os.path.join(DATA_PATH_UNSCORED, filename) # file name is the path of the unscored folder + current file name
    
        data = np.load(file_path) # load in unscored decks from a file

        # set i as index and seq_a as the current val of P1's choice
        for i, seq_a in enumerate(sequences):
            # set j as index and seq_b as the current val of P2's choice
            for j, seq_b in enumerate(sequences):
                for deck in data: # define deck as one of the arrays in the chunk 
                    deck_copy = deck.copy() # create a copy of the deck
                            
                    # running both methods at the same time
                    cards_a, tricks_a, cards_b, tricks_b = scoring(deck_copy, seq_a, seq_b) # access scoring function from src.scoring

                    # Ron's method: score by number of cards won
                    # (we do not care about P1 results)
                    if cards_b > cards_a: # if P2 has more cards than P1 after the deck has been played
                        results["card_wins_p2"][i, j] += 1 # add 1 to P2's number of card wins
                    elif cards_b == cards_a: # if P2 and P1 have the same number of cards after deck has been played
                        results["card_ties"][i, j] += 1 # add 1 to number of card ties
                            
                    # Trick method: score by number of tricks won
                    if tricks_b > tricks_a: # if P2 has more tricks won than P1 after the deck has been played
                        results["trick_wins_p2"][i, j] += 1 # add 1 to P2's number of trick wins
                    elif tricks_b == tricks_a: # if P2 and P1 have the same number of tricks won after deck has been played
                        results["trick_ties"][i, j] += 1 # add 1 to number of trick ties

        # for each deck scored, add 1 to the count of number of decks
        for deck in data: 
            results["total_decks"] += 1

        # move the file from the unscored folder to the scored folder
        new_path = f'{DATA_PATH_SCORED}/{filename}' # define new scored folder path
        shutil.move(file_path, new_path) # moves file to new scored folder path
    
    # save combined results
    save_results(results)

    # save CSV for heatmaps
    save_heatmap_csv(results, sequences)

    return results