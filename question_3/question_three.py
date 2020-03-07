def isOdd(innerList):
	
	# Initialize inner sum with sum of the list
	innerSum = sum(innerList)

	# Initialize place holders
	foundSeven = False
	count = 0
	
	for element in innerList:
		count = count + 1
		if element == 7 and not foundSeven: # Found a 7 and its not the first 7
			try:
				innerList[count:].index(4) # Check if there is a 4 following the current 7
				foundSeven = True
				innerSum = innerSum + 14 # Tripled
			except:
				break # If there is no following 4, stop looking for 7 values
		elif element == 4 and foundSeven: # Found a 4 after a 7
			#foundSeven = False
			innerSum = innerSum + 8 # Tripled
			break # Stop looking for 7
		elif foundSeven: # Between 7 and 4 (Found 7 knowing there is a 4 but did not find yet)
			innerSum = innerSum + element + element # Tripled

	return innerSum


def isEven(innerList):
	
	# Initialize inner sum with sum of the list
	innerSum = sum(innerList)

	# Initialize place holders
	foundNine = False
	count = 0
	
	for element in innerList:
		count = count + 1
		if element == 9 and not foundNine: # Found a 9 and its not the first 9
			try:
				innerList[count:].index(6) # Check if there is a 6 following the current 9
				foundNine = True
				innerSum = innerSum + 9
			except:
				break # If there is no following 6, stop looking for 9 values
		elif element == 6 and foundNine: # Found a 6 after a 9
			#foundNine = False
			innerSum = innerSum + 6
			break # Stop looking for 9
		elif foundNine: # Between 9 and 6 (Found 9 knowing there is a 6 but did not find yet)
			innerSum = innerSum + element

	return innerSum


def sum_ssmif(nestedList):
	
	# Initialize a variable to hold sum
	runningSum = 0;

	# Iterate through the inner lists
	for innerList in nestedList:
		if len(innerList) %2 == 0:
			runningSum = runningSum + isEven(innerList)
		else:
			runningSum = runningSum + isOdd(innerList)
	
	return runningSum


def main():

	ssmif_list = [ [1,2,6,3,9,9,6,2,9,1,6,2], [2,4,3,7,7,4,2,7,2], [3,2,1,0,-1] ]

	theSum = sum_ssmif(ssmif_list) # Pass in the nested list as an argument

	print("Sum SSMIF =", theSum) # Print the result



#Tell python to call main function first
if __name__ == "__main__":
    main()
