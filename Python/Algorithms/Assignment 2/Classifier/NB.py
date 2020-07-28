import numpy as np
import math


class NB:


	

	@staticmethod
	def nb(train, test):

		result = []
		Testlabel = test[:,-1]

		


		columns = train[0,:].size-1




		listMeanYes = {}
		listStdYes = {}

		listMeanNo = {}
		listStdNo = {}
		
		numYes = len([True for i in train if i[-1] == "yes"])
		numNo = len(train) - numYes

		
		
		
		for i in range(columns):
			listMeanYes[i], listStdYes[i] = NB.calculate(train[:,[i, -1]], "yes")
			listMeanNo[i], listStdNo[i] = NB.calculate(train[:,[i, -1]], "no")
			
		

		
		
		for i in range(len(test)):

			row = test[i]
			
			
            
			yesProb = NB.bayesian(row, listMeanYes, listStdYes, numYes, numYes+numNo)
			noProb = NB.bayesian(row, listMeanNo, listStdNo, numNo, numYes+numNo)
			
			
			if yesProb >= noProb:
				result.append("yes")

			else:
				result.append("no")

	


		return result



	@staticmethod
	def bayesian(row, listMean, listStd, numLabel, numData):

		
		numerator = numLabel / numData
		
		
	
		for i in range(row.size):

			
						
			p = NB.probabilityDensity(listMean[i], listStd[i], float(row[i]))

			
			
			if p != 0:
				numerator *= p
				

		return numerator





	@staticmethod
	def calculate(data, label):

		df = [float(i[0]) for i in data if i[1] == label]


		mean = 0

		for i in df:

			mean += i

		mean = mean / len(df)

		std = 0

		for i in df:

			
			std += (i - mean)**2

		std = math.sqrt(std /(len(df)-1))
		

		return mean, std



	@staticmethod
	def probabilityDensity(mean, std,x):


		return (1/(std*math.sqrt(2*math.pi))) * math.exp(-math.pow(x-mean,2)/(2*math.pow(std,2)))

