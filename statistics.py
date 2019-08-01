import math

def mean(list_of_numbers):
	sum_of_numbers = 0
	for number in list_of_numbers:
		sum_of_numbers += number
	return sum_of_numbers/len(list_of_numbers)

def variance(list_of_numbers):
	m = mean(list_of_numbers)
	var = 0
	for number in list_of_numbers:
		var += pow(abs(m - number), 2)
	return var/len(list_of_numbers)

def stdev(list_of_numbers):
	return math.sqrt(variance(list_of_numbers))