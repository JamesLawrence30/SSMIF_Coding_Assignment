import sqlite3
"""
import pandas as pd
from pandas import DataFrame, Series
from datetime import datetime
import datetime as dt
"""


def main():
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


#Tell python to call main function first
if __name__ == "__main__":
    main()
