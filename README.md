# Bet Simulation and Analysis

This Python script allows you to simulate and analyze sports betting outcomes using historical data from a CSV file. It simulates a specified number of betting sessions and provides insights into your potential bankroll growth or decline based on the bets placed and their associated odds. It was initially made as a tool for my friend griffy to analyze his betting history and determine whether he was making profitable bets, who is a gambling sharp.

## Prerequisites

Before using this script, ensure you have the following:

- Python installed (version 3.x recommended)
- Required Python libraries: pandas, matplotlib, numpy

You can install the necessary libraries using pip.

```bash
pip install pandas matplotlib numpy
```

## Usage

1. **Data Preparation:**

   - To use you own bets, make sure you have a csv containing your historical betting data. Make sure the file includes columns like 'odds,' 'clv,' 'stake,' 'potential_payout,' and 'bet_type.'
   - The script assumes that your CSV contains a 'bet_type' column with the values 'positive_ev' to identify bets with positive expected value.
   - Replace the `BET_HISTORY_FILE` variable in the script with the path to your CSV file.

2. **Command-line Arguments:**

   - You can run the script from the command line with the following optional arguments:
     - `s`: Number of simulations to run (default: 2500)
     - `r`: Number of times the bet history is repeated to simulate a longer period (default: 5)

Example command to run the script with custom parameters:

```bash
python griffy_sharps.py --s 5000 --r 10
```

3. **Simulation Results:**

   - The script simulates betting outcomes based on your historical data and the specified parameters.
   - It calculates statistics like the break-even percentage, mean bankroll, and more.
   - The script generates and displays three plots:
     1. Bankroll by Bet Number: A line plot showing the bankroll's evolution during the simulation.
     2. Bankroll Distribution: A histogram of bankroll outcomes.
     3. Plot of Bankrolls: A box plot summarizing bankroll statistics.

4. **Interpreting Results:**

   - The `Break Even Percentage` represents the percentage of simulations where your bankroll remained positive.
   - The `Number of Bets` is the total number of bets considered in the simulation (including repetitions).

5. **Adjusting Simulation Parameters:**
   - You can customize the number of simulations and repetitions by modifying the `DEFAULT_NUM_SIMS` and `DEFAULT_NUM_TIMES_BETS_REPEATED` variables in the script, or the number of line plots and histograms by modifying the `NUM_INDIVIDUAL_PLOTS` variable.

## Example

Here's an example command to run the script with custom parameters.

```bash
python bet_simulation.py --s 5000 --r 10
```

This will run 5000 simulations with the bet history repeated 10 times to simulate an extended period.

## Disclaimer

This script is for educational and analytical purposes only. It does not guarantee or predict actual betting outcomes. Use it responsibly and make informed decisions when placing bets.

## Author

Created by JAke Flynn
