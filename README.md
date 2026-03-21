Penney's Game is a coin flip game where the first player selects a sequence of heads or tails, and the second player selects their own sequence of the same length. The coin is flipped until its sequence matches one of the players', who wins the game.

The Humble-Nishiyama variations of Penney's Game are played with a deck of cards instead of a coin, and instead of selecting heads or tails, the players select a sequence of three black/red cards. To play both versions, cards are drawn until the color sequence matches either player's sequence. In one version of the game, points are earned for each card that is drawn before the sequence matches a player's. In another version, one point is earned for each set of cards drawn before the sequence matches the players, called a "trick". 

To run the code, run main.py. You will be prompted to enter the number of decks you want to be simulated and if you would like them to be scored. If you would like to view the npy files, run npy_reader.py with the name of the file. 

Player 1's strategy should be to avoid having their initial selection be "BBB" or "RRR" since those sequences make it likely that player 2 will win, when scored by both cards and tricks.

In general, for scoring by both tricks and cards, the optimal strategy for player 2 is to take the opposite of player 1's middle selection, and then adding the first two selected from player 1's sequence to second and third places of player 2's selection. An example of this is when scoring by tricks if player 1 chose the sequence "BRR", player 2 would chose "BBR" and would have an 88% chance of winning the trick. 

This method is more pronounced when scoring by cards, where there are some probabilities of player 2 winning that increase from 94% or 99% to 100% with the converged dataset. 

There are some exceptions to this strategy. When scoring by cards, if player 1 choses the sequences "BRB" and "RBR", the rule does not hold. Instead, player 2 must take the opposite of player 1's first selection and then add the second and third places of player 1's selection. For example, if player 1 chose "BRB", player 2 should chose "RRB" and would have a 92% chance of winning. 
