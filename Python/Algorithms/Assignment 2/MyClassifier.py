import sys
from Classifier.KNN import KNN
from Classifier.NB import NB

import numpy as np



trainFile = sys.argv[1]
testFile = sys.argv[2]
classifier = sys.argv[3]



train = open(trainFile, "r")
test = open(testFile, "r")
#.strip('\r\n').split('\r\n')
rowTrain = train.read().strip('\n').split('\n')
rowTest = test.read().strip('\n').split('\n')




dfTest = []
dfTrain = []


for i in range(len(rowTrain)):

	row = rowTrain[i].split(',')

	dfTrain.append(row)


for i in range(len(rowTest)):

	row = rowTest[i].split(',')

	dfTest.append(row)



dfTrain = np.array(dfTrain)
dfTest = np.array(dfTest)



if classifier == "NB":

	result = NB.nb(dfTrain, dfTest)
	print("\n".join(result))
	"""
	a = 0
	for i in range(dfTest[:,1].size):
		if dfTest[i,-1] == result[i]:
			a+= 1

	print(str(a/dfTest[:,1].size))
	"""


elif classifier.endswith('NN'):
	result = KNN.knn(int(classifier[0]),dfTrain, dfTest)
	print("\n".join(result))
else:
	print("wrong arguments")
