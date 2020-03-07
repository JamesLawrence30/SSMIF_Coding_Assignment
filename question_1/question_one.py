import math
import datetime as dt
from pandas_datareader import data


def Daily_Returns(df):

	# Obtain specified row from df and convert to list
	closeList = df["Adj Close"].tolist()
	
	# Declare some place holders
	prevPrice = closeList[0] # Initialized with first close price
	dailyReturns = [] # List to hold daily returns

	# Perform calculation
	for currentPrice in closeList[1:]: # Skip the first price since it is already set to prevPrice
		priceChange = round(currentPrice-prevPrice, 2) # Sig figs->prices have 2 decimals. (otherwise 1-0.8=.199999)
		theReturn = priceChange/prevPrice # Change in price as percentage
		dailyReturns.append(theReturn*100)  # Returns x 100% added to list
		prevPrice = currentPrice # Set PRICE(t) to PRICE(t-1) and advance to PRICE(t+1)

	return dailyReturns


def Monthly_VaR(ticker, CI=0.05): # Default value of 0.05

	# Obtain a dataframe of stock prices
	df = data.DataReader(ticker, start='2019-1-1', end='2019-12-31', data_source='yahoo')

	# Obtain list of daily returns given the dataframe
	dailyReturns = Daily_Returns(df)

	# Calculate Value at Risk
	ascendingReturns = sorted(dailyReturns) # Sort daily returns from highest loss to most profit
	num = CI * len(ascendingReturns) # Acceptible risk level based on confidence interval
	oneDayVaR = ascendingReturns[round(num-1)] # Starting at index of 0, so subtract 1
	monthVaR = math.sqrt(20) * oneDayVaR # Assuming 20 business days in a month

	return round(monthVaR, 2)


def Monthly_CVar(ticker, CI=0.05): # Default value of 0.05
	
	# Obtain a dataframe of stock prices
	df = data.DataReader(ticker, start='2019-1-1', end='2019-12-31', data_source='yahoo')

	# Obtain list of daily returns given the dataframe
	dailyReturns = Daily_Returns(df)

	# Calculate Conditional Value at Risk
	ascendingReturns = sorted(dailyReturns) # Sort daily returns from highest loss to most profit
	num = CI * len(ascendingReturns) # Acceptible risk level based on confidence interval
	sumReturns = sum(ascendingReturns[0:round(num-1)])

	oneDayCVaR = (1/num)*sumReturns # conditional value at return calculation
	monthCVaR = math.sqrt(20) * oneDayCVaR # Assuming 20 business days in a month

	return round(monthCVaR, 2)


def Monthly_Volatility(ticker):
	
	# Obtain a dataframe of stock prices
	df = data.DataReader(ticker, start='2019-1-1', end='2019-12-31', data_source='yahoo')

	# Obtain list of daily returns given the dataframe
	dailyReturns = Daily_Returns(df)

	# Obtain variance of returns
	mean = sum(dailyReturns) / len(dailyReturns) # Computed average
	variance = sum((oneDayReturn - mean) ** 2 for oneDayReturn in dailyReturns) / len(dailyReturns) # Difference in value and mean squared for all values

	# Obtain volatility
	oneDayVolatility = math.sqrt(variance) # Volatility ==> Standard Deviation = square root of variance
	monthVolatility = math.sqrt(20) * oneDayVolatility # Assuming 20 business days in a month

	return round(monthVolatility, 2)


def main():

	ticker = "AAPL" # Specify stock here
	CI = 0.05 # Specify optional Confidence Interval here

	value_at_risk = Monthly_VaR(ticker, CI) # Pass in a ticker (can add confidence interval if you choose)
	conditional_value_at_risk = Monthly_CVar(ticker, CI) # Pass in a ticker and a confidence interval
	volatility = Monthly_Volatility(ticker) # Pass in a ticker only

	print("VaR: ", value_at_risk, "%")
	print("CVaR: ", conditional_value_at_risk, "%")
	print("Volatility: ", volatility, "%")


#Tell python to call main function first
if __name__ == "__main__":
    main()
