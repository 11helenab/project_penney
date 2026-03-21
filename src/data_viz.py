# import statements
import pandas as pd
import numpy as np
import random
import itertools
import matplotlib.pyplot as plt
import seaborn as sns

# define the basic heatmap function shown in class: 

FIG_SIZE_SQUARE = (8, 8) # pre-set figure size

# Ron's method: 
def heatmap(data: pd.DataFrame | np.ndarray,
            cmap: str,
            vmin: float, # specify so seaborn doesn't scale color to max and min
            vmax: float,
            annot: np.ndarray | str = None,
            x_label: str = None,
            y_label: str = None,
            title: str = None,
            figsize: tuple = FIG_SIZE_SQUARE,
            cbar: bool = True,
            **kwargs
           ):
    """
    Create a seaborn heatmap with custom annotations.

    Returns fig, ax objects for further customization.
    
    Required Inputs:
        data: A pandas DataFrame, or numpy array, or similar
        cmap: Name of a matplotlib colormap
        vmin: Minimum color value
        vmax: Maximum color value
        
    Note that it is best practice to explicity define vmin and vmax.
    If you really want them to be determined automatically, pass None for each.

    Optional Inputs:
        annot:    An array of the same shape as the data to be used
                  as annotations, or a format specifier such as .2f
        x_label:  Optional x-axis label. Blank if omitted.
        y_label:  Optional y-axis label. Blank if omitted.
        cbar:     Whether or not to show the colorbar. Defaults to True.
                  Discouraged if showing annotations.
        **kwargs: Any keyword arguments accepted by sns.heatmap()
    """

    kwargs = kwargs or {}

    if annot is not None:
        if type(annot) == str:
            fmt = annot
            annot = True
        else:
            fmt='' # this is required to make it work 

    fig, ax = plt.subplots(1, 1, figsize=figsize)
    sns.heatmap(data=data,
                ax=ax,
                annot=annot,
                fmt=fmt,
                cmap=cmap,
                cbar=cbar,
                vmin=vmin,
                vmax=vmax,
                **kwargs
               )
    
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    if title:
        ax.set_title(title)
    return fig, ax

def get_data(method: str, score: str, games: int) -> pd.DataFrame: 
    """
    Load heatmap data from CSV and compute percentage values for wins and ties.
    Inputs:
        - method: 'tricks' or 'cards'
        - score: 'wins' or 'ties'
        - games: total number of simulated games
    
    Returns:
        - data frame of pivoted table of percentage values
    """

    # set the datatypes so python reads in the seq as text to keep leading 0s 
    data_types = {
        'seq_a': str,
        'seq_b': str,
        'trick_wins_p2': int,
        'trick_ties_p2': int,
        'card_wins_p2': int,
        'card_ties_p2': int
    }

    # read in heatmap data
    data = pd.read_csv('data/heatmap_data.csv', dtype = data_types) 
    
    # calculate percent for given method and win/tie
    # pct = round((results/games)*100)
    if method == 'tricks' and score == 'wins':
        score_vals = 'trick_wins_p2'
    elif method == 'tricks' and score == 'ties':
        score_vals = 'trick_ties_p2'
    elif method == 'cards' and score == 'wins':
        score_vals = 'card_wins_p2'
    else: 
        score_vals = 'card_ties_p2'

    data_proc = data.loc[:, ['seq_a', 'seq_b', score_vals]]

    data_proc = pd.pivot_table(data_proc, 
                        index = 'seq_a', #rows
                        columns = 'seq_b', #columns
                        values = score_vals #values
                       )
    data_proc = ((data_proc / games) * 100).round(0).astype(int)
    
    return data_proc

def create_annotations(scoring: str, games: int) -> np.ndarray: 
    """
    Creates annotations to be used in heatmaps

    input: scoring method (so we know what data to use)
    output: annotation array to be entered into heatmap
    """
    
    if scoring == 'tricks':
        # use wins and ties df for tricks
        wins = get_data('tricks', 'wins', games)
        ties = get_data('tricks', 'ties', games)
    else:
        # use wins and ties df for cards
        wins = get_data('cards', 'wins', games)
        ties = get_data('cards', 'ties', games)
    
    annot = np.full(shape=wins.shape, fill_value='', dtype='<U10') #create the annotation array
    for i in range(annot.shape[0]):
        for j in range(annot.shape[1]):
            # fill in each value with the corresponding text from the wins and ties dfs
            annot[i, j] = f'{wins.iloc[i,j]} ({ties.iloc[i,j]})' 
    return annot

def create_heatmap(scoring: str, deck_count: int) -> None: 
    """
    Uses the heatmap function to create heatmaps to display results 
    
    Input: Takes in a string that determines the type of scoring used 
    Output: prints the generated heatmap to the screeen (SHOULD WE SAVE IT?)
    """

    if scoring == 'tricks':
        annot = create_annotations('tricks', deck_count)
        wins = get_data('tricks', 'wins', deck_count) #use by tricks wins info
    elif scoring == 'cards': 
        annot = create_annotations('cards', deck_count)
        wins = get_data('cards', 'wins', deck_count) #use by cards wins info

    # create mask to "grey out" the diagonals
    mask = mask = np.eye(len(wins), dtype=bool) #this is the same for both maps
    # create the labels for the heatmap: 
    choices = [f'{xi:b}'.zfill(3).replace('0','B').replace('1','R') for xi in range(2**3)] #Bs and Rs

    fig, ax = heatmap(wins, # Data we want to visualize 
                      cmap = 'Blues', # color scheme
                      vmin = 0, # we want 0% wins to have the lightest color 
                      vmax = 100, # 100% wins has darkest color
                      annot = annot, # set annotations we created
                      cbar = False, # we do not want the color bar
                      linewidths = 0.5, # spaces between squares
                      square = True, # make the boxes actual squares
                      mask=mask, # apply the mask 
                      title = f'My Chance of Win(Draw)\nby {scoring}\nN={deck_count}' # set title
                     )
    ax.set_xticklabels(choices) # x labels are our choices
    ax.set_yticklabels(choices, rotation = 0) # y labels are our choices but rotated to be horizontal
    ax.set_facecolor('lightgrey') # color of masked cells is light grey
    ax.set_xlabel("My Choice") # set x axis label
    ax.set_ylabel("Opponent Choice") # set y axis label
    plt.rcParams['font.weight'] = 'light' # make font weight lighter across the plot 
    # plt.show() # optional display plot 
    fig.savefig(f'figures/{scoring}.svg', bbox_inches='tight')
    
    return