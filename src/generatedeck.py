# import statements
import numpy as np
import matplotlib 
import random
import os

def create_deck() -> np.array:
    """
    Uses 0s and 1s to represent black and red cards.
    Returns:
    - A 1D array (shape 52) of shuffled 0s and 1s
    """
    deck = np.repeat([0,1], [26, 26], axis=0) # np array of 26 0s followed by 26 1s
    random.shuffle(deck) # randomize the order of the 52 cards in-place
    return deck

def save_deck(deck: np.array, filename: str) -> None:
    """
    Save the deck array with to specified folder. In simulation.py script this is 
    defined as the unscored folder.
    """
    folder = 'data'
    # join preferred folder and filename to create file path
    file_path = os.path.join(folder, filename)

    # make the data folder if it doesn't exist
    if not os.path.exists(folder):
        os.mkdir(folder)

    # do not save file if the path already exists
    if os.path.exists(file_path):
        raise FileExistsError(f'File {filename} already exists')
    
    np.save(file_path, deck) # save the deck