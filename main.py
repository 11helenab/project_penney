import os
import numpy as np
import matplotlib.pyplot as plt
from src.simulation import run_simulation

FIGURES_PATH = os.path.join("figures")
os.makedirs(FIGURES_PATH, exist_ok=True)

def main() -> None:
    print("The Humble-Nishiyama Randomness Game Simulation!")
    n_decks = int(input("How many new decks do you want to simulate? "))

    results = run_simulation(n_decks)
    print(f"Simulation complete! Total decks simulated: {results['total_decks']}")

    # make_heatmap(data, 'test_heatmap.svg') # uncomment when we have heatmap function

if __name__ == "__main__":
    main()