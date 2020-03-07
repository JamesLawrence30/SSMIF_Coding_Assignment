import sqlite3
from pandas_datareader import data
from datetime import datetime
import datetime as dt


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

		for row in df.iterrows():
			date = datetime.date(row[0])
			dateInt = int(str(date).replace("-",""))
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


def main():

	ticker = "AAPL" # Specify stock here

	Fill_Table(ticker) # Pass in a ticker

#Tell python to call main function first
if __name__ == "__main__":
    main()
