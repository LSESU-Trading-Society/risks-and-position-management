import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns 
import yfinance as yf 
from datetime import datetime 

data = pd.DataFrame() 
ticker_list = ['TSLA', 'SQ', 'ATVI', 'MSFT', 'MARA'] 

for i in ticker_list: 
    query = yf.Ticker(i) 
    td = query.history(start=datetime(2020,5,1), end=datetime(2021, 1, 10))
    #excluding March to smooth out volatility/returns calculation 
    data[i] = td['Close'] 
data = data.dropna() 
print(data) 

def portfolio_annualised_perf(weights, mean_returns, cov_maxtrix): 
    returns = np.sum(mean_returns * weights) * 252 
    #compounding returns? 
    std = np.sqrt(np.dot(weights.T, np.dot(cov_maxtrix, weights))) * np.sqrt(252) #tranposition to fit shape 
    return returns, std 

def random_portfolio(num_portfolios, mean_returns, cov_matrix, rfr): 
    results = np.zeros((3, num_portfolios)) 
    #dataframe > array 
    #print(results) 
    #three col: returns, std, sharpe ratio 
    #x rows on simulation
    w_combo = [] 
    for i in range(num_portfolios): 
        weights = np.random.random(len(ticker_list)) #long only // what about shorting? 
        #np.random.random -> [0, 1) 
        weights /= np.sum(weights) 
        w_combo.append(weights)
        portfolio_returns, portfolio_std = portfolio_annualised_perf(weights,mean_returns, cov_matrix)      
        results[0, i] = portfolio_std 
        results[1, i] = portfolio_returns 
        results[2, i] = (portfolio_returns - rfr) / portfolio_std 
        #index [1] array -> std 
        #index [2] array -> returns... 
    return results, w_combo
#run-time? 

def show_frontier(mean_returns, cov_matrix, num_portfolios, rfr): 
    results, weights = random_portfolio(num_portfolios, mean_returns, cov_matrix, rfr) 
    #max sharpe 
    #.max() -> y / column 
    #.argmac() -> x / row 
    #most important part here for the data is matching the index --> can you generate allocation without having to transpose the data 
    max_sharpe_idx = np.argmax(results[2]) 
    sd, r = results[0, max_sharpe_idx], results[1, max_sharpe_idx] 
    max_sharpe_allocation = pd.DataFrame(weights[max_sharpe_idx], index=data.columns, columns=['allocation'])
    max_sharpe_allocation['allocation'] = [round(i, 5) for i in max_sharpe_allocation.allocation] 
    max_sharpe_allocation = max_sharpe_allocation.T
    print(max_sharpe_allocation) 

    min_vol_idx = np.argmin(results[0]) 
    sd_vol, r_vol = results[0, min_vol_idx], results[1, min_vol_idx] 
    min_vol_allocation = pd.DataFrame(weights[min_vol_idx], index=data.columns, columns = ['allocation']) 
    min_vol_allocation['allocation'] = [round(i, 5) for i in min_vol_allocation.allocation]
    min_vol_allocation = min_vol_allocation.T
    print(min_vol_allocation) 

    print('-'*80) 
    print("Maximum Sharpe Ratio Portfolio Allocation\n")
    print("Annualised Return:", r)
    print("Annualised Volatility:", sd)
    print('\n') 
    print(max_sharpe_allocation) 


    print('-'*80) 
    print('Minimum Volatility Ratio Portfolio Allocation\n') 
    print("Annualised Return:", r_vol) 
    print("Annualised Volatility:", sd_vol) 
    print('\n') 
    print(min_vol_allocation) 

    sns.set() 
    plt.figure(figsize = (10,7)) 
    plt.scatter(results[0,:], results[1,:], c=results[2,:], cmap='viridis', marker='o', s=19, alpha=0.2) 
    plt.colorbar() 
    plt.scatter(sd, r, marker='o', color='r', s=500, label='Maximum Sharpe Ratio') 
    plt.scatter(sd_vol, r_vol, marker='o', color='g', s=500, label='Minimum Volatility') 
    plt.title('Simulated Portoflio Optimisation based on Efficient Frontier') 
    plt.xlabel('Annualised Volatility') 
    plt.ylabel('Annualised Returns') 
    plt.legend(labelspacing = 0.8) 
    plt.show()

#show_frontier(mean_returns, cov_matrix, num_portfolios, rfr)

returns = np.log(data/data.shift(1)) 
mean_returns = returns.mean() 
cov_matrix = returns.cov()
n_portfolio = 75000 
rfr = 0.014 

show_frontier(mean_returns, cov_matrix, n_portfolio, rfr) 