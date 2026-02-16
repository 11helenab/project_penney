import os
#Emily was here

def create_deck() -> np.array:
    'return an array that represents a deck of cards'
    deck = np.repeat([0,1], [26, 26], axis=0)
    random.shuffle(deck)
    return deck
 
def save_deck(deck: np.array) -> None:
    'save the array to an output folder'
    folder = 'project_penney/data'
    file_path = os.path.join(folder, 'card_decks.npy')
    np.save(file_path, deck)
