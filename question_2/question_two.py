import math
import sqlite3
from datetime import datetime
from pandas_datareader import data


def Make_Database():

	# Main block
	try:
		# Open a connection to the local database
		conn = sqlite3.connect('SSMIF.db')
		print("Opened connection.")

		# Cursor used to execute SQL queries
		c = conn.cursor()

		# Create a table to hold times and prices
		c.execute("""CREATE TABLE "Stock_Data" (
		"Timestamp" INTEGER NOT NULL,
		"Open" DECIMAL(10, 2),
		"High" DECIMAL(10, 2),
		"Low" DECIMAL(10, 2),
		"Close" DECIMAL(10, 2),
		"Adj_Close" DECIMAL(10, 2)
		);""")

		# Save changes to database
		conn.commit()

	# Check for errors in SQL execute
	except sqlite3.Error as e:
		print("SQLite error:")
		print(e.args[0])

	# Catch general exceptions
	except Exception:
		print("Caught error:")
		print(Exception)

	# ALWAYS close connections to database
	finally:
		conn.close
		print("Closed connection.")


def Fill_Table(ticker):

	# Obtain a dataframe of stock prices
	df = data.DataReader(ticker, start='2019-1-1', end='2019-12-31', data_source='yahoo')

	# Create the database
	Make_Database()

	try:

		# Open a connection to the local database
		conn = sqlite3.connect('SSMIF.db')
		print("Opened connection.")

		# Cursor used to execute SQL queries
		c = conn.cursor()

		# Get data from the dataframe, row by row
		for row in df.iterrows():
			date = datetime.date(row[0]) # Get timestamp and drop min and sec
			dateInt = int(str(date).replace("-","")) # Convert the date to integer
			openPrice = row[1]["Open"]
			highPrice = row[1]["High"]
			lowPrice = row[1]["Low"]
			closePrice = row[1]["Close"]
			adjClosePrice = row[1]["Adj Close"]

			# Add a row to the table
			c.execute("""INSERT INTO Stock_Data VALUES (
				{},{},{},{},{},{});""".format(
				dateInt,
				openPrice,
				highPrice,
				lowPrice,
				closePrice,
				adjClosePrice
				))

			# Save change for each row to database
			conn.commit()

	# Check for errors in SQL execute
	except sqlite3.Error as e:
		print("SQLite error:")
		print(e.args[0])

	# Catch general exceptions
	except Exception:
		print("Caught error:")
		print(Exception)

	# ALWAYS close connections to database
	finally:
		conn.close
		print("Closed connection.")


def Daily_Returns(closeList):
	
	# Declare some place holders
	prevPrice = closeList[0][0] # Initialized with first close price (SELECT returns list of prices inside a tuple)
	dailyReturns = [] # List to hold daily returns

	# Perform calculation
	for currentPrice in closeList[1:]: # Skip the first price since it is already set to prevPrice
		priceChange = round(currentPrice[0]-prevPrice, 2) # Sig figs->prices have 2 decimals. (otherwise 1-0.8=.199999)
		theReturn = priceChange/prevPrice # Change in price as percentage
		dailyReturns.append(theReturn*100)  # Returns x 100% added to list
		prevPrice = currentPrice[0] # Set PRICE(t) to PRICE(t-1) and advance to PRICE(t+1)

	return dailyReturns


def Monthly_VaR(CI=0.05): # Default value of 0.05
	try:

		# Open a connection to the local database
		conn = sqlite3.connect('SSMIF.db')
		print("Opened connection.")

		# Cursor used to execute SQL queries
		c = conn.cursor()

		# Obtain a list of adjusted close prices
		closeData = c.execute("SELECT Adj_Close FROM Stock_Data;")
		closeList = closeData.fetchall()

	# Check for errors in SQL execute
	except sqlite3.Error as e:
		print("SQLite error:")
		print(e.args[0])

	# Catch general exceptions
	except Exception:
		print("Caught error:")
		print(Exception)

	# ALWAYS close connections to database
	finally:
		conn.close
		print("Closed connection.")

	# Obtain list of tuples of daily returns from the database
	dailyReturns = Daily_Returns(closeList)

	# Calculate Value at Risk
	ascendingReturns = sorted(dailyReturns) # Sort daily returns from highest loss to most profit
	num = CI * len(ascendingReturns) # Acceptible risk level based on confidence interval
	oneDayVaR = ascendingReturns[round(num-1)] # Starting at index of 0, so subtract 1
	monthVaR = math.sqrt(20) * oneDayVaR # Assuming 20 business days in a month

	return round(monthVaR, 2)


def main():

	ticker = "AAPL" # Specify stock here
	CI = 0.05 # Specify optional Confidence Interval here

	Fill_Table(ticker) # Pass in a ticker
	value_at_risk = Monthly_VaR(CI) # Pass in an optional confidence interval

	print("VaR: ", value_at_risk, "%")


#Tell python to call main function first
if __name__ == "__main__":
    main()
