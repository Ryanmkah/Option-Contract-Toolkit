import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import requests
import time
import yfinance as yf
from scipy.stats import norm


ALPHA_API = 'Enter Your Key Here'



# --- Risk-Free Rate ---
url = f'https://www.alphavantage.co/query?function=TREASURY_YIELD&interval=daily&maturity=10y&apikey={ALPHA_API}'
response = requests.get(url)
data = response.json()
latest_data = data.get('data', [])[0]
r = float(latest_data['value'] if latest_data else '4.25') / 100  # convert % to decimal
print(f'Latest 10-Year Treasury Yield: {r * 100:.2f} %')


# --- Stock Data ---
symbol = input('Enter stock symbol: ').upper()
url = "https://www.alphavantage.co/query"
params = {
    "function": "GLOBAL_QUOTE",
    "symbol": symbol,
    "apikey": ALPHA_API
}

response = requests.get(url, params=params)
data = response.json()

try:
    s = float(data["Global Quote"]["05. price"])
    print(f"\nCurrent price of {symbol}: ${s:.2f}")
except:
    print("\nError retrieving price. Response:")
    print(data)






#Handles Different User Input
alias_map = {
    # Protective Put
    'pp': 'protective put',
    'protective': 'protective put',
    'protective put': 'protective put',

    # Covered Call
    'cc': 'covered call',
    'covered': 'covered call',
    'covered call': 'covered call',

    # Straddle
    'straddle': 'straddle',

    # Collar
    'collar': 'collar',

    # Bull Call Spread
    'bull call': 'bull call spread',
    'bull call spread': 'bull call spread',

    # Bear Put Spread
    'bear put': 'bear put spread',
    'bear put spread': 'bear put spread',

    # Bull Put Spread
    'bull put': 'bull put spread',
    'bull put spread': 'bull put spread',

    # Bear Call Spread
    'bear call': 'bear call spread',
    'bear call spread': 'bear call spread',

    # Long Butterfly Spread
    'lbf': 'long butterfly spread',
    'long butterfly': 'long butterfly spread',
    'long butterfly spread': 'long butterfly spread',
    'lb': 'long butterfly spread',

    # Short Butterfly Spread
    'sbf': 'short butterfly spread',
    'short butterfly': 'short butterfly spread',
    'short butterfly spread': 'short butterfly spread',
    'sb': 'short butterfly spread',

    # --- BASIC OPTION CONTRACTS ---
    'bc': 'bc',
    'buy call': 'bc',
    'buying call': 'bc',
    'buying the call': 'bc',

    'sc': 'sc',
    'sell call': 'sc',
    'selling call': 'sc',
    'selling the call': 'sc',

    'bp': 'bp',
    'buy put': 'bp',
    'buying put': 'bp',
    'buying the put': 'bp',

    'sp': 'sp',
    'sell put': 'sp',
    'selling put': 'sp',
    'selling the put': 'sp',
    
    'black scholes': 'black scholes',
    'bls': 'black scholes',
    'blackscholes': 'black scholes'
}





basic_contracts = {'bc', 'bp', 'sc', 'sp'}

strategies = {
    'protective put', 'covered call', 'straddle', 'collar',
    'bull call spread', 'bear put spread', 'bull put spread',
    'bear call spread', 'long butterfly spread', 'short butterfly spread'
}

black_scholes = {'black scholes'}




input_labels = {
    'bc': 'Buying the Call',
    'sc': 'Selling the Call',
    'bp': 'Buying the Put',
    'sp': 'Selling the Put',
    'bcls': 'Buying the Call Low Strike',
    'bchs': 'Buying the Call High Strike',
    'scls': 'Selling the Call Low Strike',
    'schs': 'Selling the Call High Strike'
}



def Welcome():
    
    user_input = input("Welcome to Ryan's Option Calculator! Would you like to Calculate?\n")
    option_type  = alias_map.get(user_input)
    
    if option_type in basic_contracts:
        
        x , p = parameters(option_type)
        payoff, profit = option_calc(option_type, x, p, s)
        payoff = float(payoff)
        profit = float(profit)
        print(f'Your option contract payoff is: ${payoff:,.2f}')
        print(f'Your option contract profit is: ${profit:,.2f}')
        
        x_range = get_x_range(s)
        
        y_range = get_y_range(x_range, option_type, x, p, s)
        plot(x_range, y_range)

        
    elif option_type in strategies:
         
        strat_type = alias_map.get(user_input)
        option_strat(strat_type)
    
    elif option_type in black_scholes:
        
        call_or_put = input('Is this a Call Option or a Put Option?\n').strip().lower()
    
        if call_or_put in ['call', 'call option']:
            
            x = float(input('What is the Strike Price of the Call Option\n'))
            time = float(input('What is the time to expiration in days?\n'))
            sigma_input = input("Enter volatility (e.g., 25 for 25%): ")
            sigma = float(sigma_input) / 100

            
            call_option = black_scholes_calc(call_or_put, x, time, s, sigma)
            
            print(f"Black-Scholes estimated price for the call option is: ${call_option:,.2f}")
            
            heatmap(call_or_put, x, time, s, sigma)
            
            
        elif call_or_put in ['put', 'put option']:
            
            x = float(input('What is the Strike Price of the Put Option\n'))
            time = float(input('What is the time to expiration in days?\n'))
            sigma_input = input("Enter volatility (e.g., 25 for 25%): ")
            sigma = float(sigma_input) / 100

            
            put_option = black_scholes_calc(call_or_put, x, time, s, sigma)
            
            print(f'Black-Scholes estimated price for the put option is: ${put_option:,.2f}')
            
            heatmap(call_or_put, x, time, s, sigma)
            
            
            
            
            
#Handles Option Type
def parameters(option_type):
    
    label = input_labels.get(option_type)
    
    if label:
        
        return get_inputs(label)
    
    else:
        print('Error')
        
#Gets User Input
def get_inputs(label):
    
    x = float(input(f'What is the Strike Price of the Option Contract for {label}?\n'))
    p = float(input(f'What is the Premium Per Share for the Option Contract for {label}?\n'))
    p = p * 100
    return x,p

#Gets the option Profit
def get_option(option_type, s):
            
    x , p = parameters(option_type)
    payoff, profit = option_calc(option_type, x, p, s)
    profit = float(profit)
            
    return profit



#Gets the Range of X values for Basic Option Contract
def get_x_range(s):
    
    percent = .5
    points = 10
    
    if points % 2 == 0:
        points += 1
        
    lower = (s) * (1 - percent)
    upper = (s) *(1 + percent)

    x_range = np.linspace(lower, upper, points)
    
    return x_range
    
#Gets the Range of Y values for Basic Option Contract   
def get_y_range(x_range, option_type, x, p, s):
    
    y_range = []
    
    for i in x_range:
    
        s = i
        payoff, profit = (option_calc(option_type, x ,p, s))
        profit = float(profit/100)
        y_range.append(profit)
        
    return y_range
    
    
#Plots the Profit of the Option Contract
def plot(x_range, y_range):
    
    x = x_range
    y = y_range
    
    plt.plot(x, y, '-o', color = '#1f77b4')
    plt.xlabel('Stock Price')
    plt.ylabel('Profit')
    plt.title('Profit vs. Stock Price')
    plt.grid(True, linestyle = '--', color = 'gray')
    plt.show()

#Calculates The Values for the Option Contract
def option_calc(option_type, x ,p, s):

    
    if option_type in ['bc', 'bchs', 'bcls']:
        
        payoff = max(s - x, 0) * 100
        profit = payoff - p
        
        return payoff, profit
        
    elif option_type in ['sc', 'schs', 'scls']:
        
        payoff = min(x - s, 0) * 100
        profit = payoff + p
        
        return payoff, profit
    
        

    elif option_type == 'bp':
        
        payoff = max(x - s, 0) * 100
        profit = payoff - p
        
        return payoff, profit

    elif option_type == 'sp':
        
        payoff = min(s - x, 0) * 100
        profit = payoff + p
        
        return payoff, profit

    else:
        print('Error')



#Calculates the Profit and Loss for Option Strats
def option_strat(strat_type):

#Protective Put

    if strat_type == 'protective put':
        
        #Calculates the P&L from the shares in time today
        contract_amount = float(input('How many option contracts would you like to purchase? Each contract is quoted per 100 shares\n'))
        cost_of_shares = float(input('What was the total cost of the shares purchased?\n'))
        num_of_shares = contract_amount * 100
        total_share_value = s * num_of_shares
        pl = total_share_value - cost_of_shares
        
        #Calculates the profit of the contact
        option_type = 'bp'
        pl2 = get_option(option_type, s)

        #Calculates the total P&L of the Protective Put
        PL = float(pl + (pl2 * contract_amount))

#Covered Call
    
    elif strat_type == 'covered call':
    
        #Calculates the P&L from the shares in time today
        contract_amount = float(input('How many option contracts would you like to purchase? Each contract is quoted per 100 shares\n'))
        cost_of_shares = float(input('What was the total cost of the shares purchased?\n'))
        num_of_shares = contract_amount * 100
        total_share_value = s * num_of_shares
        pl = total_share_value - cost_of_shares
        
        #Calculates the profit of the contact
        option_type = 'sc'
        pl2 = get_option(option_type, s)

        #Calculates the total P&L of the Covered Call
        PL = float(pl + (pl2 * contract_amount))

#Straddle

    elif strat_type == 'straddle':
        
        #Calculates the P&L for buying the call
        option_type = 'bc'
        PL = get_option(option_type, s)
        
        #Calculates the P&L for buying the put
        option_type = 'bp'
        PL += get_option(option_type, s)
        
#Collar

    elif strat_type == 'collar':
        
        #Calculates the P&L for buying the put
        option_type = 'bp'
        PL = get_option(option_type, s)
        
        
        #Calculates the P&L for selling the call
        option_type = 'sc'
        PL += get_option(option_type, s)
        
#Bull Call Spread

    elif strat_type == 'bull call spread':
        
        
        #Buy the Call
        option_type = 'bc'
        PL = get_option(option_type, s)
        
        #Sell the Call
        option_type = 'sc'
        PL += get_option(option_type, s)  

#Bear Put Spread
    
    elif strat_type == 'bear put spread':
        
        #Buy a Put
        option_type = 'bp'
        PL = get_option(option_type, s)
        
        
        
        #Sell a Put
        option_type = 'sp'
        PL += get_option(option_type, s)
        
#Bull Put Spread
    
    elif strat_type == 'bull put spread':
        
        #Sell a Put
        option_type = 'sp'
        PL = get_option(option_type, s)
        
        #Buy a Put
        option_type = 'bp'
        PL += get_option(option_type, s)

#Bear Call Spread
    
    elif strat_type == 'bear call spread':
        
        #Sell the Call
        option_type = 'sc'
        PL = get_option(option_type, s)
        
         #Buy the Call
        option_type = 'bc'
        PL += get_option(option_type, s)    
        
#Long Butterfly Spread
        
    elif strat_type == 'long butterfly spread':
            
        #Buy the Call Low Strike
        option_type = 'bcls'
        PL = get_option(option_type, s)
        
        #Sell 2 Call
        option_type = 'sc'
        PL += (get_option(option_type, s) * 2)

        #Buy the Call High Strike
        option_type = 'bchs'
        PL += get_option(option_type, s)  
            
#Short Butterfly Spread
            
    elif strat_type == 'short butterfly spread':
        
        #Sell the Call Low Strike
        option_type = 'scls'
        PL = get_option(option_type, s)
        
        #Buy 2 Calls
        option_type = 'bc'
        PL += (get_option(option_type, s) * 2)

        #Sell the Call High Strike
        option_type = 'schs'
        PL += get_option(option_type, s)
        
    else:
        print('Error')

    print(f'Your P&L for this {strat_type} is: ${PL:,.2f}')



#Black Scholes Calculator
def black_scholes_calc(call_or_put, x, time, s, sigma):
    
    if call_or_put in ['call', 'call option']:
        
        t = float(time / 365)
        
        d1 = (np.log(s / x) + (r + 0.5 * sigma**2) * t) / (sigma * np.sqrt(t))

        d2 = d1 - sigma * np.sqrt(t)

        call_option = (s* norm.cdf(d1)) - x * np.exp(-1* r * t) * norm.cdf(d2)
        
        return call_option

        
    elif call_or_put in ['put', 'put option']:
        
        t = float(time / 365)
        
        d1 = (np.log(s / x) + (r + 0.5 * sigma**2) * t) / (sigma * np.sqrt(t))

        d2 = d1 - sigma * np.sqrt(t)

        put_option = (x * np.exp(-1* r * t)) * norm.cdf(-1*d2) - s * norm.cdf(d1 * -1)
        
        return put_option
    
    
#Gets the Upper and Lower Bounds of the Stocks Volatility by +- 30%
def get_vol_range(sigma):
    
    percent = .30
    points = 10
        
    lower = (sigma) * (1 - percent)
    upper = (sigma) *(1 + percent)

    y_range = np.linspace(lower, upper, points)
    
    return (y_range)


#Gets the Upper and Lower Bounds of the Stocks Price by +- 30%
def get_price_range(s):
    
    percent = .30
    points = 10
    
    lower = (s) * (1 - percent)
    upper = (s) *(1 + percent)

    x_range = np.linspace(lower, upper, points)
    
    return (x_range)


#Creates the list of Option Premium Vaules 
def heat_map_inputs(call_or_put, x, time, s, sigma):
    
    value = []
    
    y_axis = get_vol_range(sigma)
    
    x_axis = get_price_range(s)
    
    for i in y_axis:
        
        sigma = i
        
        for _ in x_axis:
            
            s = _
            
            output = float(black_scholes_calc(call_or_put, x, time, s, sigma))

            value.append(output)
                
    return y_axis, x_axis, value
    

#Creates the Heatmap
def heatmap(call_or_put, x, time, s, sigma):
    
    y_axis, x_axis, value = heat_map_inputs(call_or_put, x, time, s, sigma)

    x_axis = np.round(np.array(x_axis))

    y_axis = np.round(np.array(y_axis), 3)

    z_array = np.reshape(value, (10, 10))

    df = pd.DataFrame(z_array, index = y_axis, columns = x_axis)
    df = df.round(2)
    df.index = df.index * 100
    df.index = ['{:.1f}'.format(v) for v in df.index]
    print(df)
    
    sns.heatmap(df, annot=True,fmt='.2f', linewidths = .4, linecolor='black', cmap='RdYlGn_r', annot_kws={'size':8})
    plt.xlabel('Stock Price')
    plt.ylabel('Volatility %')
    plt.title('Black-Scholes Option Premium in $')
    plt.xticks(rotation=0, fontsize=8)
    plt.yticks(rotation=90, fontsize=8)
    plt.show()




Welcome()