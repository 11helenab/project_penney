Penney's Game is a coin flip game where the first player selects a sequence of heads or tails, and the second player selects their own sequence of the same length. The coin is flipped until its sequence matches one of the players, who wins the game.

The Humble-Nishiyama variations of Penney's Game are played with a deck of cards instead of a coin, and instead of selecting heads or tails, the players select a sequence of three black/red cards. To play both versions, cards are drawn until the color sequence matches either player's sequence. In one version of the game, points are earned for each card that is drawn before the sequence matches a player's. In another version, one point is earned for each set of cards drawn before the sequence matches the players, called a "trick". 

To run the code, run main.py. You will be prompted to enter the number of decks you want to be simulated. If you would like to view the npy files, run npy_reader.py. 

For scoring by tricks, the optimal strategy for player 2 is to take the opposite of player 1's middle selection, and then adding the first two selected from player 1's sequence to second and third places of player 2's selection.
