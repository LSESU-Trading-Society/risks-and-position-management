import math 
from scipy.stats import norm 

class EuroCall: 
    def calc_delta(self, price: int, vol: int, strike:int, expiry, rfr:float): 
        #price = price now 
        # volatility = implied volatility on asset 
        # strike price = strike price 
        #exp is days till exp /365 
        #rfr = CB's rfr     
        b = math.exp(-rfr * expiry) 
        x1 = math.log(price/(b*strike)) + .5*(vol*vol)*expiry 
        x1 = x1/(vol*(expiry**.5)) 
        z1 = norm.cdf(x1) 
        return z1 
    
    def calc_gamma(self, price, vol, strike, expiry, rfr): 
        b = math.exp(-rfr*expiry) 
        x1 = math.log(price/(b*strike)) + .5*(vol*vol)*expiry 
        x1 = x1/(vol*(expiry**.5)) 
        z1 = norm.cdf(x1) 
        z2 = z1/(price*vol*math.sqrt(expiry)) 
        return z2 

    def calc_vega(self, price, vol, strike, expiry, rfr): 
        b = math.exp(-rfr*expiry) 
        x1 = math.log(price/(b*strike)) + .5*(vol*vol)*expiry 
        x1 = x1/(vol*(expiry**.5)) 
        z1 = norm.cdf(x1) 
        z2 = price * z1 * math.sqrt(expiry) 
        return z2/100 

    def calc_price(self, price, vol, strike, expiry, rfr): 
        b = math.exp(-rfr*expiry)
        x1 = math.log(price/(b*strike)) + .5*(vol*vol)*expiry
        x1 = x1/(vol*(expiry**.5))
        z1 = norm.cdf(x1)
        z1 = z1*price
        
        x2 = math.log(price/(b*strike)) - .5*(vol*vol)*expiry
        x2 = x2/(vol*(expiry**.5))
        z2 = norm.cdf(x2)
        z2 = b*strike*z2

        return z1-z2 
    
    def __init__ (self, price, vol, strike, expiry, rfr): 
        self.price = price 
        self.vol = vol 
        self.strike = strike
        self.expiry = expiry 
        self.rfr = rfr 

        self.price = self.calc_price(price, vol, strike, expiry, rfr) 
        self.delta = self.calc_delta(price, vol, strike, expiry, rfr) 
        self.gamma = self.calc_gamma(price, vol, strike, expiry, rfr) 
        self.vega = self.calc_vega(price, vol, strike, expiry, rfr) 

class EuroPut: 
    def calc_delta(self, price, vol, strike, expiry, rfr): 
        b = math.exp(-rfr * expiry) 
        x1 = math.log(price/(b*strike)) + .5*(vol*vol)*expiry 
        x1 = x1/(vol*(expiry**.5)) 
        z1 = norm.cdf(x1) 
        return z1 - 1 
    
    def calc_gamma(self, price, vol, strike, expiry, rfr): 
        b = math.exp(-rfr*expiry) 
        x1 = math.log(price/(b*strike)) + .5*(vol*vol)*expiry 
        x1 = x1/(vol*(expiry**.5)) 
        z1 = norm.cdf(x1) 
        z2 = z1/(price*vol*math.sqrt(expiry)) 
        return z2 
    
    def calc_vega(self, price, vol, strike, expiry, rfr): 
        b = math.exp(-rfr*expiry) 
        x1 = math.log(price/(b*strike)) + .5*(vol*vol)*expiry 
        x1 = x1/(vol*(expiry**.5)) 
        z1 = norm.cdf(x1) 
        z2 = price * z1 * math.sqrt(expiry) 
        return z2/100 
    
    def calc_price(self, price, vol, strike, expiry, rfr): 
        b = math.exp(-rfr*expiry)
        x1 = math.log((b*strike)/price) + .5*(vol*vol)*expiry
        x1 = x1/(vol*(expiry**.5))
        z1 = norm.cdf(x1)
        z1 = b*strike*z1

        x2 = math.log((b*strike)/price) - .5*(vol*vol)*expiry
        x2 = x2/(vol*(expiry**.5))
        z2 = norm.cdf(x2)
        z2 = price*z2

        return z1-z2 

    def __init__ (self, price, vol, strike, expiry, rfr): 
        self.price = price 
        self.vol = vol 
        self.strike = strike
        self.expiry = expiry 
        self.rfr = rfr 

        self.price = self.calc_price(price, vol, strike, expiry, rfr) 
        self.delta = self.calc_delta(price, vol, strike, expiry, rfr) 
        self.gamma = self.calc_gamma(price, vol, strike, expiry, rfr) 
        self.vega = self.calc_vega(price, vol, strike, expiry, rfr) 
    
