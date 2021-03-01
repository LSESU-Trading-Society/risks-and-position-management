from datetime import date,datetime,timedelta
import random

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


stocks = ['PEP', 'GME', 'AAPL', 'F', 'AMZN', 'NVDA', 'BP', 'MSFT']

first_day = datetime(2014, 1, 1)
last_day = datetime(2021, 2, 2)

# pd.set_option('display.max_rows', 1000)
# pd.set_option('display.max_columns', 1000)


def rand_generate_portfolios(num: int, stocks: list): #Random generator of  portfolios (a portfolio is identified by the weights assigned to each element of the list stocks)
    returns = yf.Tickers(stocks).history(interval = '1wk', start=first_day, end=last_day).Close.pct_change(1).dropna() #Download from yf, Take the close price, Calc the percentage change, Drop the first row
    for i in range(num): 
        weights = np.random.uniform(-1,1,len(stocks))
        weights = weights/sum(weights) # Standardization to sum to 1

        returns['Portfolio'] = np.dot(returns[stocks],weights)

        if (returns['Portfolio'].mean()) < 0 or (returns['Portfolio'].std() > 1): continue

        yield weights, returns['Portfolio'].mean(), returns['Portfolio'].std()

def rand_efficient_frontier(num, stocks:list, precision):
    weights = []
    exps = []
    stds = []
    for weight, exp, std in rand_generate_portfolios(num, stocks):
        exp = round(exp, precision)
        std = round(std, precision)
        if exp in exps:
            index = exps.index(exp)
            if std < stds[index]:
                weights[index] = weight
                exps[index] = exp
                stds[index] = std
        else:
            weights.append(weight)
            exps.append(exp)
            stds.append(std)
    
    portfolios = pd.DataFrame()
    portfolios['weights'] = weights
    portfolios['exps'] = exps
    portfolios['stds'] = stds

    return portfolios

def rand_plot_portfolios(num, stocks:list, precision = 2, filter_efficient = False):
    plt.title("Random Portfolios")

    colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#f032e6', '#9a6324', '#000000']

    # color_names = ['Red','Green','Yellow','Blue','Orange','Purple', 'Magenta','Brown', 'Black']

    if type(stocks[0]) != list:
        possibilities = [stocks]
    elif len(stocks) > len(colors):
        return "You need more colors to perform this"
    else: 
        possibilities = stocks
    
    for stocks,color,i in zip(possibilities, colors, range(len(possibilities))):
        if not filter_efficient:
            for _, exp, std in rand_generate_portfolios(num, stocks):
                plt.scatter(std,exp)
        else:
            efficient_pfl = rand_efficient_frontier(num, stocks, precision)
            plt.scatter(efficient_pfl.stds, efficient_pfl.exps, s = 10, c = color, label = i+1)

    plt.xlabel("Portfolio return standard deviation (weekly)")
    plt.ylabel("Portfolio return mean (weekly)")
    plt.legend()
    plt.show()


# rand_plot_portfolios(1000, stocks, 3, filter_efficient = True)




#You can even give it a list of different stock groups and it will plot them with different colors (this way we can see how having more options affect our frontier)

stocks1 = ['PEP', 'GME', 'AAPL', 'F', 'AMZN', 'NVDA', 'BP', 'MSFT', 'TATT', 'JNJ']
stocks2 = ['CNK','RDNT','DAO','FNKO','UTL','SCHR','EPP','PFSI','NUMG','ECPG']
stocks3 = ['GJH','FDHY','GLIBP','IJK','SSYS','CTZ','UJUN','GLDD','NPA','UUU']
stocks4 = ['GRX','EVF','FSFG','PBEE','LDEM','GDV','BRPA','IDN','DT','NFLX']

stocks = ['PEP', 'GME', 'AAPL', 'F', 'AMZN', 'NVDA', 'BP', 'MSFT', 'TATT', 'JNJ','CNK','RDNT','DAO','FNKO','UTL','SCHR','EPP','PFSI','NUMG','ECPG','GJH','FDHY','GLIBP','IJK','SSYS','CTZ','UJUN','GLDD','NPA','UUU','GRX','EVF','FSFG','PBEE','LDEM','GDV','BRPA','IDN','DT','NFLX']

possibilities  = [stocks1, stocks2, stocks3, stocks4]

rand_plot_portfolios(10000, [stocks,stocks4], 3, filter_efficient = True)



# The rest is to be completed if possible. The three functions above are based on
# random portfolio weights combinations which can leave us wondering, did we miss any amazing
# opportunity? By completing the rest, we should expect to go through all possibilities (obviously
# with some restrictions such as limiting the individual weights to 1 or 2 or 3 OR the depth of
# precision we want to dive into, assigning weights in increment of 0.1 or 0.05 or 0.01)

def det_generate_portfolios(stocks, returns, step = 0.1, max_weight = 1, min_weight = -1): #Deterministic generator of  portfolios (modifying the weights)
    # possible_weights = 
    for x in range(num): 
        weights = np.random.uniform(-1,1,len(stocks)) #change it to not random here
        weights = weights/sum(weights) # Standardization to sum to 1

        returns['Portfolio'] = np.dot(returns[stocks],weights)
        if returns['Portfolio'].mean() < 0: continue

        yield weights, returns['Portfolio'].mean(), returns['Portfolio'].std()