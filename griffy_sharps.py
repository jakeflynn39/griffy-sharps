import pandas as pd
import random
import matplotlib.pyplot as plt
import numpy as np
import argparse

NUM_INDIVIDUAL_PLOTS = 10
DEFAULT_NUM_SIMS = 2500
DEFAULT_NUM_TIMES_BETS_REPEATED = 5
CSV_FILE = 'griffy_bet_history.csv'

def main():
    parser = argparse.ArgumentParser(description="Simulate sports betting outcomes.")
    parser.add_argument("--s", type=int, default=DEFAULT_NUM_SIMS, help="Number of simulations to run")
    parser.add_argument("--r", type=int, default=DEFAULT_NUM_TIMES_BETS_REPEATED, help="Number of times the bet history is repeated to simulate a longer period")

    args = parser.parse_args()
    num_sims = args.s
    num_times_bets_repeated = args.r
        
    '''
    num_sims: number of simulations to run
    num_times_bets_repeated: number of times the bet history is repeated to simulate a longer period of time
    '''

    bets_csv = pd.read_csv(CSV_FILE)
    bets_placed_df = bets_csv[['odds', 'clv', 'stake', 'potential_payout', 'bet_type']]
    bets_placed_df = bets_placed_df[bets_placed_df['bet_type'] == "positive_ev"]
    bets_placed_df = bets_placed_df[bets_placed_df["clv"].apply(lambda x: isinstance(x, float))]
    bets_placed_df['clv'] = bets_placed_df['clv'].apply(american_to_percent)

    num_positive_outcomes = 0
    num_bets = len(bets_placed_df)

    all_sims_df = pd.DataFrame(index=range(num_sims), columns=['sim_index', 'bankroll', 'sim_bankroll_history'])

    for i in range(num_sims):
        print(f"--{i} sims completed out of {num_sims}", end='\r')
        individual_sim_df = simulate_bet_history(bets_placed_df, i, NUM_INDIVIDUAL_PLOTS, num_times_bets_repeated)
        all_sims_df.loc[i] = individual_sim_df

    all_sims_df["sim_bankroll_history"]

    bankrolls = all_sims_df['bankroll']

    num_positive_outcomes = len(all_sims_df[all_sims_df['bankroll'] > 0])
    mean_bankroll = bankrolls.mean()
    max_bankroll = bankrolls.max()
    min_bankroll = bankrolls.min()
    break_even_percent = num_positive_outcomes / num_sims

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3)

    all_sims_df[all_sims_df['sim_index'] < NUM_INDIVIDUAL_PLOTS].set_index('sim_index')['sim_bankroll_history'].apply(pd.Series).T.plot(ax = ax1, legend = False)


    ax2.hist(bankrolls, bins = 100, orientation = 'horizontal')

    ax1.set_title('Bankroll by Bet Number')
    ax1.set_xlabel('Bet Number')
    ax1.set_ylabel('Bankroll')

    ax2.set_title(f'Bankroll Distribution (Mean: {mean_bankroll:.2f})')
    ax2.set_xlabel('Bankroll')
    ax2.set_ylabel('Frequency')

    ax2.axhline(y=0, color='r', linestyle='-')

    ax3.set_title('Plot of Bankrolls')
    ax3.set_xlabel('Bankroll')
    ax3.set_ylabel('Frequency')

    ax3.boxplot(bankrolls, vert = True, showfliers=False, labels=['Bankrolls'])
    quartiles = np.quantile(bankrolls, [0.25, 0.5, 0.75])
    for quartile in quartiles:
        ax3.text(1.1, quartile, f'${quartile:.2f}', horizontalalignment='left', size='medium', color='black', weight='semibold')

    min_bankroll = min(bankrolls)
    max_bankroll = max(bankrolls)
    ax1.set_ylim(min_bankroll, max_bankroll)
    ax2.set_ylim(min_bankroll, max_bankroll)
    ax3.set_ylim(min_bankroll, max_bankroll)

    fig.set_size_inches(18.5, 10.5)

    fig.suptitle(f'Break Even Percentage: {(break_even_percent * 100):.2f}%\nNumber of Bets: {num_bets * num_times_bets_repeated}')

    plt.show()

def american_to_percent (american):
    if american > 0:
        return 100 / (100 + american)
    else:
        return -american / (100 - american)

def simulate_bet_history(bets, sim_index, NUM_PLOTS, NUM_TIMES_SIM):
    bankroll = 0
    bankroll_history = []

    # if the random win probability is less than the clv, then the bet was a win
    for _ in range(NUM_TIMES_SIM):
        # for when need to track bankroll history for plotting
        if sim_index < NUM_PLOTS:
            for bet in bets.itertuples():
                random_win_prob = random.random()
                if random_win_prob < bet.clv:
                    bankroll += bet.potential_payout 
                bankroll -= bet.stake

                bankroll_history.append(bankroll)

        # for when only tracking bankroll at the end of each simulation is needed (faster)
        else:
            random_win_probs = np.random.rand(len(bets))
            win_mask = random_win_probs < bets['clv']

            # only add the payout if the bet was a win
            bankroll += (win_mask * (bets['potential_payout']) -  bets['stake']).sum()

    sims_df_row = {'sim_index': sim_index, 'bankroll': bankroll, 'sim_bankroll_history': bankroll_history}

    return sims_df_row

if __name__ == "__main__":
    main()
