import pandas as pd
import csv
import random
import matplotlib.pyplot as plt
import numpy as np

NUM_SIMS = 1000
CSV_FILE = '4-6-2023.csv'
NUM_PLOTS = 10
NUM_TIMES_SIM = 10

def main():
    bets = []
    with open (CSV_FILE, 'r') as f:
        csvreader = csv.reader(f)
        next(csvreader)
        for row in csvreader:
            try:
                bets.append({'odds': float(row[8]), 'clv': float(row[9]), 'stake': float(row[10]), 'payout': float(row[11]), 'bet_type': row[13]})
            except ValueError:
                pass
    bankrolls = []
    bankrolls_sim = []
    sim_nums = []
    bet_nums = []
    num_positive_outcomes = 0
    num_bets = len(bets)
    for i in range(NUM_SIMS):
        print(i)
        bankroll, data = sim(bets, i)
        bankrolls.append(bankroll)
        if bankroll > 0:
            num_positive_outcomes += 1
        for bet in data:
            sim_nums.append(bet['sim'])
            bet_nums.append(bet['bet_num'])
            bankrolls_sim.append(bet['bankroll'])

    break_even_per = num_positive_outcomes / NUM_SIMS

    bet_data = pd.DataFrame({'sim': sim_nums, 'bet_num': bet_nums, 'bankroll': bankrolls_sim})

    bet_data = bet_data[bet_data['sim'] < NUM_PLOTS]
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3)

    #bet_data.set_index('bet_num').groupby('sim')['bankroll'].plot(ax = ax1)
    

    mean = np.mean(bankrolls)
    median = np.median(bankrolls)

    griffy = pd.DataFrame(bankrolls)
    griffy.plot.hist(ax = ax2, bins = 100, orientation = 'horizontal', legend = False)

    ax1.set_title('Bankroll by Bet Number')
    ax1.set_xlabel('Bet Number')
    ax1.set_ylabel('Bankroll')

    ax2.set_title(f'Bankroll Distribution (Mean: {mean:.2f})')
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

    fig.suptitle(f'Break Even Percentage: {(break_even_per * 100):.2f}%\nNumber of Bets: {num_bets * NUM_TIMES_SIM}')

    plt.show()

def american_to_percent (american):
    if american > 0:
        return 100 / (100 + american)
    else:
        return -american / (100 - american)

def sim(bets, sim_index):
    bankroll = 0
    datas = []
    for i in range(NUM_TIMES_SIM):
        for bet_index, bet in enumerate(bets):
            if bet['bet_type'] != "positive_ev":
                continue
            try:
                prob = american_to_percent(float(bet['clv']))
            except ValueError:
                continue
            rand = random.random()
            if rand < prob:
                bankroll += float(bet['payout']) - float(bet['stake'])
            else:
                bankroll -= float(bet['stake'])
            datas.append({'sim': sim_index, 'bet_num': bet_index,'bankroll': bankroll})
    return bankroll, datas

if __name__ == "__main__":
    main()