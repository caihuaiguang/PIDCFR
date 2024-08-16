import os
import pandas as pd
import matplotlib.pyplot as plt
import scienceplots

# Activate SciencePlots style
plt.style.use(['science', 'no-latex'])

# List of game names
game_names = [
    "KuhnPoker",
    "LiarsDice4",
    "LiarsDice5",
    "GoofSpiel4",
    "GoofSpiel5",
    "GoofSpielImp4",
    "GoofSpielImp5",
    "Battleship_22_3",
    "Battleship_32_3",
    "LeducPokerIso",
    "Subgame3",
    "Subgame4",
    # "SmallMatrix",
]

game_names_show = [
    "Kuhn Poker",
    "Liar's Dice (4)",
    "Liar's Dice (5)",
    "GoofSpiel (4)",
    "GoofSpiel (5)",
    "GoofSpielImp (4)",
    "GoofSpielImp (5)",
    "Battleship (2)",
    "Battleship (3)",
    "Leduc Poker",
    "HUNL Subgame (3)",
    "HUNL Subgame (4)",
]

# List of methods
methods = [
    "CFR",
    "CFRPlus",
    "LinearCFR",
    "DCFR",
    "DCFRPlus",
    "PCFRPlus",
    "PDCFRPlus",
    # "PIDCFR",
]

# Base directory
base_dir = './results'

# Iterate over each game
for idx_, game in enumerate(game_names):
    game_dir = os.path.join(base_dir, game)
    
    # Check if the game directory exists
    if not os.path.exists(game_dir):
        print(f"Directory for game {game} does not exist.")
        continue

    # Create dictionaries to store data for each method with different suffixes
    data_dict_last = {}
    data_dict_avg = {}

    # Iterate over each method
    for method in methods:
        method_dir = os.path.join(game_dir, method)
        
        # Check if the method directory exists
        if not os.path.exists(method_dir):
            print(f"Directory for method {method} in game {game} does not exist.")
            continue
        
        # Read the data.csv file for the 'last' case (38-2)
        csv_file_last = os.path.join(method_dir, '38-2/data.csv')
        if os.path.exists(csv_file_last):
            data_last = pd.read_csv(csv_file_last)
            data_dict_last[method] = data_last
        
        # Read the data.csv file for the 'avg' case (38-1)
        csv_file_avg = os.path.join(method_dir, '38-1/data.csv')
        if os.path.exists(csv_file_avg):
            data_avg = pd.read_csv(csv_file_avg)
            data_dict_avg[method] = data_avg

    # Use a bright color palette
    colors = plt.get_cmap('tab10').colors

    # Plotting for 'last' case
    fig, ax1 = plt.subplots(figsize=(8, 6))

    # Iterate over the data and plot each line for 'last'
    for idx, (label, data) in enumerate(data_dict_last.items()):
        ax1.plot(data['step'], data['exp'], label=label, color=colors[idx % len(colors)])

    # Customize the plot
    # ax1.set_yscale('linear')
    # ax1.set_ylim(0, 10**0)
    ax1.set_yscale('log')
    ax1.set_ylim(10**-18, 10**0)
    ax1.set_ylabel('Exploitability')
    # ax1.set_xlabel('Step')
    ax1.legend()
    ax1.grid(True, which="major", linestyle="-")  # Simplified grid with solid lines for major grid

    # Create output directory if it doesn't exist
    output_dir = './pic'
    os.makedirs(output_dir, exist_ok=True)

    # Save the plot as a vector image
    plt.savefig(os.path.join(output_dir, f'{game_names_show[idx_]}_last.pdf'), format='pdf')

    # Close the figure to free memory
    plt.close(fig)

    # Plotting for 'avg' case
    fig, ax1 = plt.subplots(figsize=(8, 6))

    # Iterate over the data and plot each line for 'avg'
    for idx, (label, data) in enumerate(data_dict_avg.items()):
        ax1.plot(data['step'], data['exp'], label=label, color=colors[idx % len(colors)])

    # Customize the plot
    
    # ax1.set_yscale('linear')
    # ax1.set_ylim(0, 10**0)
    ax1.set_yscale('log')
    ax1.set_ylim(10**-18, 10**0)
    ax1.set_ylabel('Exploitability')
    # ax1.set_xlabel('Step')
    ax1.legend()
    ax1.grid(True, which="major", linestyle="-")  # Simplified grid with solid lines for major grid

    # Save the plot as a vector image
    plt.savefig(os.path.join(output_dir, f'{game_names_show[idx_]}_avg.pdf'), format='pdf')

    # Close the figure to free memory
    plt.close(fig)