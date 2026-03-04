import os
import numpy as np
import matplotlib.pyplot as plt
from src.simulation import run_simulation, load_results
from src.data_viz import create_heatmap

FIGURES_PATH = os.path.join("figures")
os.makedirs(FIGURES_PATH, exist_ok=True)

def main() -> None:
    print("The Humble-Nishiyama Randomness Game Simulation!")

    #n_decks = int(input("How many new decks do you want to simulate? "))

    results = load_results()
    total_decks = results["total_decks"]

    print(f"You have {total_decks:,} generated and scored:")
    print()

    try:
        n_decks = int(input("How many new decks do you want to generate?"))
    except ValueError:
        print("Invalid input")
        exit()
    
    if n_decks < 0:
        print("Cannot generate a negative number of decks.")
        exit()

    print("\nYou are going to:")
    print(f"Generate {n_decks:,} new decks, update all win/tie totals, and regenerate heatmaps and CSV data")

    confirm = input("Would you like to proceed? (y/n): ").lower()

    if confirm != "y":
        print("Simulation Cancelled")
        exit()

    results = run_simulation(n_decks)
    print(f"Simulation complete! Total decks simulated: {results['total_decks']:,}")

    create_heatmap('tricks', results['total_decks'])
    create_heatmap('cards', results['total_decks'])

    print("Heatmaps updated successfully!")
    print("Simulation done!")

if __name__ == "__main__":
    main()