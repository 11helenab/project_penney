import numpy as np
import matplotlib 
import random
import os
#Emily was here

def create_deck() -> np.array:
    'return an array that represents the black and red cards in a deck of cards'
    deck = np.repeat([0,1], [26, 26], axis=0)
    random.shuffle(deck)
    return deck

def save_deck(deck: np.array, filename: str) -> None:
    'save the array to an output folder'
    folder = 'data'
    file_path = os.path.join(folder, str)

    if not os.path.exists(folder):
        os.mkdir(folder)

    if os.path.exists(file_path):
        raise FileExistsError(f'File {filename} already exists')
    
    np.save(file_path, deck)

number_decks = int(input("How many decks of cards do you want to run project penney on?"))
for _ in range(number_decks):
    print(create_deck())