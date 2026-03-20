# import statements
import os
import numpy as np
import matplotlib.pyplot as plt
from src.simulation import load_results
from src.data_viz import create_heatmap
from src.simulation import deck_gen, scoring_new

# create directory for all figures
FIGURES_PATH = os.path.join("figures")
os.makedirs(FIGURES_PATH, exist_ok=True)

def main() -> None:
    '''
    Main function that accesses src functions to run the simulation, 
    generate decks, scores decks, and creates figure.
    Returns: None
    '''
    print("The Humble-Nishiyama Randomness Game Simulation!")

    # load previous results (old runs)
    results = load_results()
    total_decks = results["total_decks"] # access the current number of total decks

    print(f"You have {total_decks:,} generated and scored:") # show user current number of decks

    # get number of decks to generate
    try:
        n_decks = int(input("How many new decks do you want to generate?")) # user input number of decks to generate
    # raise an error if the input is not a valid integer
    except ValueError:
        print("Invalid input")
        exit()
    
    # raise an error if the input is a negative number
    if n_decks < 0:
        print("Cannot generate a negative number of decks.")
        exit()

    # ask user to confirm number of decks that will be generated
    print(f'\nYou are going to generate {n_decks}:')
    confirm = input("Would you like to proceed? (y/n): ").lower() # remove case-sensitivity

    # cancel simulation if user types anytihng but 'y'
    if confirm != "y":
        print("Simulation Cancelled")
        exit()
    
    # generate n decks
    deck_gen(n_decks) # access deck_gen function from src.simulation

    # ask user if unscored decks should be scored
    print(f'would you like to score the decks?')
    confirm = input("Would you like to proceed? (y/n): ").lower() # remove case-sensitivity

    # cancel simulation if user types anytihng but 'y'
    if confirm != "y":
        print("Simulation Cancelled")
        exit()

    # score all unscored decks
    results = scoring_new() # access scoring_new function from src.simulation
    # tell user simulation is done and print number of decks scored
    print(f"Simulation complete! Total decks simulated: {results['total_decks']:,}")

    # create tricks and cards heatmaps with the scored decks
    create_heatmap('tricks', results['total_decks']) # access create_heatmap function from src.data_viz
    create_heatmap('cards', results['total_decks'])

    # tell user simulation is complete and finished
    print("Heatmaps updated successfully!")
    print("Simulation done!")

if __name__ == "__main__":
    main()