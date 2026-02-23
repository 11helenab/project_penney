import os
import numpy as np
from src.generatedeck import create_deck, save_deck
from src.scoring import rons_method


def main() -> None:
    print("Ron's Version of the H-N Game")
    n_decks = int(input("How many decks of cards do you want to run project penney on?"))

    # Generate the decks
    decks = create_deck(n_decks)

    # Save decks
    save_deck(decks)

    # Placeholder choices (later all 8 combos will be looped over)
    choice_a = "010"
    choice_b = "101"

    # INSERT TRICK SIMULATION
    # ron's simulation
    rwins_a, rwins_b, rties = rons_method(decks, choice_a, choice_b)

    print(f"For {n_decks} deck of cards:")
    print(f"Player 1 wins: {rwins_a}")
    print(f"Player 2 wins: {rwins_b}")
    print(f"Ties: {rties}")
    # make_heatmap(data, 'test_heatmap.svg') # uncomment when we have heatmap function


if __name__ == "__main__":
    main()