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

# Create figure and subplots (12 games * 2 plots per game = 24 subplots)
fig, axs = plt.subplots(nrows=6, ncols=4, figsize=(20, 20))
axs = axs.flatten()  # Flatten the axes array for easy iteration

# Iterate over each game
for idx, game in enumerate(game_names):
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

    colors = plt.get_cmap('tab10').colors

    # Plotting for 'avg' case in the corresponding subplot
    ax_avg = axs[2*idx]
    for method_idx, (label, data) in enumerate(data_dict_avg.items()):
        ax_avg.plot(data['step'], data['exp'], label=label, color=colors[method_idx % len(colors)])
    ax_avg.set_yscale('log')
    ax_avg.set_ylim(10**-18, 10**0)
    ax_avg.set_title(f'{game_names_show[idx]} - Avg', fontsize=16, fontweight='bold' )
    ax_avg.grid(True, which="major", linestyle="-")
    
    # Plotting for 'last' case in the corresponding subplot
    ax_last = axs[2*idx+1]
    for method_idx, (label, data) in enumerate(data_dict_last.items()):
        ax_last.plot(data['step'], data['exp'], label=label, color=colors[method_idx % len(colors)])
    ax_last.set_yscale('log')
    ax_last.set_ylim(10**-18, 10**0)
    ax_last.set_title(f'{game_names_show[idx]} - Last', fontsize=16, fontweight='bold')
    ax_last.grid(True, which="major", linestyle="-")

# Adjusting the font size for axis labels and ticks
for ax in axs:
    ax.xaxis.label.set_size(16)  # X轴标签字体大小
    ax.yaxis.label.set_size(16)  # Y轴标签字体大小
    ax.tick_params(axis='both', which='major', labelsize=14)  # 主刻度标签字体大小
    ax.tick_params(axis='both', which='minor', labelsize=12)  # 次刻度标签字体大小
# Set labels (only on the first subplot)
fig.text(0.5, 0.02, 'Step', ha='center', fontsize=18, fontweight='bold')
fig.text(0.02, 0.5, 'Exploitability', va='center', rotation='vertical', fontsize=18, fontweight='bold')

# Set a single legend outside of all subplots
handles, labels = axs[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 1.02), fontsize=18, ncol=len(labels), frameon=True, borderaxespad=0.3)

# Adjust layout to make room for the legend
plt.tight_layout(rect=[0.03, 0.03, 0.95, 1])

# Save the plot as a vector image
output_dir = './pic'
os.makedirs(output_dir, exist_ok=True)
plt.savefig(os.path.join(output_dir, 'full.pdf'), format='pdf', bbox_inches='tight')

# Close the figure to free memory
plt.close(fig)
