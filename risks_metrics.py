import numpy as np 
import seaborn as sns 
import matplotlib.pyplot as plt
from scipy.stats import norm 

class Risks: 
    def __init__(self, data): 
        self.data = data 
        self.sigma = 0 
        self.mu = 0 

    def volatility(self, price): 
        vol = self.data[price].std(ddof=1) 

        print('Volatility: ', vol)
    
    def distribution(self, price): 
        self.data['LogReturns'] = np.log(self.data[price]) - np.log(self.data[price].shift(1))
        self.mu = self.data['LogReturns'].mean() 
        self.sigma = self.data['LogReturns'].std(ddof=1) 

        #visualising distribution with a histogram 
        sns.set() 
        self.data['LogReturns'].hist(bins=50, figsize=(15,8)) 
        plt.show() 
        
        return self.data 
    
    def calculate_prob_daily(self, returns): 
        prob_return = norm.cdf(returns, self.mu, self.sigma) 

        print('The Probability is ', prob_return) 

    def calculate_prob_period(self, returns, period): 
        prob_return = norm.cdf(returns, self.mu*period, (self.sigma*period**0.5))

        print('The Probability of ' + str(returns) + ' per cent returns in ' + str(period) + ' days is ', prob_return) 

    
    def var_daily(self, quantile): 
        var = norm.ppf(quantile, self.mu, self.sigma) 

        print("VaR at " + str(quantile) + ' confidence interval is ', var) 
