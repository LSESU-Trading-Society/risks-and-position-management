from euro_options_pricing import EuroCall, EuroPut
import numpy as np 
#long call - price above strike 
#long put - price below strike 

#call option - buy tsla at 142 below current 
#delta usually between 0.1 and 0.15

#gamma - measure of stability (aka rate of change) change of delta 
long = EuroCall(543, .53, 545, 30/365, .015) #1000 
long_price = long.price
long_delta = long.delta 
long_gamma = long.gamma 
long_vega = long.vega 
print(long_price, long_delta, long_gamma, long_vega) 

option_a = EuroCall(543, .53, 550, 30/365, .015) 
a_price = option_a.price 
a_delta = option_a.delta 
a_gamma = option_a.gamma 
a_vega = option_a.vega 

option_b = EuroCall(543, .53, 555, 30/365, .015) 
b_price = option_b.price 
b_delta = option_b.delta 
b_gamma = option_b.gamma 
b_vega = option_b.vega 

#creating matrices for new options's greeks + portfolio greeks 
greeks = np.array([[a_gamma, b_gamma], [a_vega, b_vega]])
p_greeks = np.array([[long_gamma*-1000], [long_vega*-1000]]) 

#round matrix 
inv = np.linalg.inv(np.round(greeks, 2)) 
print(inv) 

#using dot product, find weights 
w = np.dot(inv, p_greeks) 
print(w)

#check for neutralisation 
a = np.round(greeks, 2) 
b = w 
check = np.round(np.dot(a, b) - p_greeks) 
print(check) 

#accounting for delta 
greeks = np.array([[a_delta, b_delta], [a_gamma, b_gamma], [a_vega, b_vega]]) 

p_greeks = np.array([[long_delta*1000], [long_gamma*1000], [long_vega*1000]]) 
#figure out why this is (+/-) of above m

c = np.round(greeks, 2) 
net_delta_position = np.round(np.dot(c, w) + p_greeks) 
print(net_delta_position)