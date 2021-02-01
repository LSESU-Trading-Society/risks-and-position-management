import yfinance as yf 
import numpy as np 
from datetime import datetime
import pandas as pd

ticker = 'tsla' 
query = yf.Ticker(ticker) 
df = query.history(start=datetime(2020, 1, 1), end = datetime.today())
print(df) 

#STOP LOSSES -----

#create range 
perc_range = np.arange(1, 11, 1) #extend the range as large as you want 

#loop through range - risk calculation table 
entry_price = df.iloc[-1, 3] 

risk_table_sl = pd.DataFrame() 
risk_table_sl['Loss Levels'] = perc_range

risk_table_tp = pd.DataFrame() 
risk_table_tp['Profit Levels'] = perc_range 

stop_losses=[]
take_profit = [] 

for i in perc_range: 
    sl = entry_price - (entry_price*i/100)
    stop_losses.append(sl) 
    tp = entry_price + (entry_price*i/100) 
    take_profit.append(tp) 
risk_table_sl['Stop Losses'] = stop_losses 
risk_table_tp['Take Profits'] = take_profit 


risk_table_sl = risk_table_sl.set_index('Loss Levels')
risk_table_tp = risk_table_tp.set_index('Profit Levels')
print(risk_table_sl) 
print(risk_table_tp) 

#POSITION SIZING -----
#account details 
acc_total = 20000
acc_risk = .01 
trade_risk = 5 #user input 

#formula for position size : account risk / trade risk 
#print(risk_table_sl.iloc[(trade_risk-1), 0]) 
position_size = (acc_total * acc_risk) / risk_table_sl.iloc[(trade_risk-1), 0]
print(position_size) 

#trade details
commission = 6 #when ure trading uk equities, usually in pence (adjust) 
total_cost = position_size * entry_price + commission
breakeven = total_cost / position_size 

print('SUMMARY') 
print('-'*30) 
print('Position Size: ' + str(position_size)) 
print('Total Cost (with commission): ' + str(total_cost)) 
print('Breakeven at ' + str(breakeven) + ' per share') 

#CONTINUE next week: performance test the position size and sl levels on different trades 

