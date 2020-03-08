def ignoredSum(innerSumList):

	# Initialized place holders
	foundFour = None
	innerSum = 0

	count = 0
	for num in list(innerSumList):
		count = count + 1
		if num == 4 and foundFour == None: # Found 4 and its the first 4
			try:
				innerSumList[count:].index(5) # Check if there is a 5 following the current 4
				foundFour = True
				continue # Ignore 4
			except:
				innerSum = innerSum + 4 # No 5 following the 4
		elif num == 5 and foundFour:
			foundFour = False
			continue # Ignore 4
		elif foundFour:
			continue # Ignore num between 4 and 5
		else:
			innerSum = innerSum + num

	return innerSum


def isOdd(innerList):
	
	# Initialize place holders
	innerSum = 0
	innerSumList = []
	foundSeven = None

	count = 0
	for element in innerList:
		count = count + 1
		if element == 7 and foundSeven == None: # Found a 7 and its not the first 7
			try:
				innerList[count:].index(4) # Check if there is a 4 following the current 7
				foundSeven = True
				innerSumList.append(21)
			except:
				continue # If there is no following 4, stop looking for 7 values
		elif element == 4 and foundSeven: # Found a 4 after a 7
			foundSeven = False # Found 7 so 7 is not searched for
			innerSumList.append(12)
			continue # Do not try any further cases
		elif foundSeven: # Between 7 and 4 (Found 7 knowing there is a 4 but did not find yet)
			innerSumList.append(element*3)
		else:
			innerSumList.append(element) # Number not between a 7 or a 4
	
	for num in list(innerSumList):
		innerSum = innerSum + num
	
	return innerSum


def isEven(innerList):

	# Initialize place holders
	innerSum = 0
	innerSumList = []
	foundNine = None

	count = 0
	for element in innerList:
		count = count + 1
		if element == 9 and foundNine == None: # Found a 9 and its not the first 9
			try:
				innerList[count:].index(6) # Check if there is a 6 following the current 9
				foundNine = True
				innerSumList.append(18)
			except:
				continue # If there is no following 6, stop looking for 9 values

		elif element == 6 and foundNine: # Found a 6 after a 9
			foundNine = False # Found 9 so 9 is not searched for
			innerSumList.append(12)
			continue # Do not try any further cases
		elif foundNine: # Between 9 and 6 (Found 9 knowing there is a 6 but did not find yet)
			innerSumList.append(element*2)
		else:
			innerSumList.append(element) # Number not between a 9 or a 6

	for num in list(innerSumList):
		innerSum = innerSum + num

	return innerSum


def sum_ssmif(nestedList):
	
	# Initialize a variable to hold sum
	finalSum = 0;
	masterList = [] # Each inner list output is added to this list

	# Iterate through the inner lists
	for innerList in nestedList:
		if (len(innerList)+1) %2 == 0: # length+1 corrects for 0 index, yields correct odd/even index
			evenSum = isEven(innerList)
			masterList.append(evenSum)

		else:
			oddSum = isOdd(innerList)
			masterList.append(oddSum)

	finalSum = ignoredSum(masterList) # Ignore values between 4 and 5
	
	return finalSum


def main():

	ssmif_list = [ [1, 2, 3, 9, 2, 6 , 1], [1, 3], [1, 2, 3], [ 7, 1, 4 , 2], [1, 2, 2] ]

	theSum = sum_ssmif(ssmif_list) # Pass in the nested list as an argument

	print("Sum SSMIF =", theSum) # Print the result



#Tell python to call main function first
if __name__ == "__main__":
    main()
