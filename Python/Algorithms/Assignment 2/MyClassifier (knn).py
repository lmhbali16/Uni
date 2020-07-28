import sys
#from Classifier.KNN import KNN
#from Classifier.NB import NB

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

if classifier.endswith('NN'):
	def euclid_dist(data,inputs):

	    return np.sqrt((np.sum(np.square(inputs - data),1)))

	def knn(k,trainingset, testset):

	    trainingvals = np.array(np.delete(trainingset,-1,1),dtype = float)
	    testvals = np.array(testset,dtype = float)
	    for val in testvals:
	        #print(val)
	        distances = euclid_dist(trainingvals,val)
	        #print()
	        distances = distances.reshape(1,distances.shape[0]).transpose()
	        #print(distances[0:3])
	        neighbours = []
	        for i in range(distances.shape[0]):
	            neighbours.append({'distance':distances[i][0],'class':trainingset[i][-1]})

	        neighbours = sorted(neighbours, key = lambda i: i['distance'])

	        k_points = neighbours[0:k]
	        #print(k_points)
	        count_yes = 0
	        count_no = 0
	        for row in k_points:
	            if row['class'] == 'yes':
	                count_yes += 1
	            if row['class'] == 'no':
	                count_no += 1
	        if count_yes > count_no:
	            print('yes')
	        if count_yes < count_no:
	            print('no')
	        if count_yes == count_no:
	            print('yes')

	knn(int(classifier[0]),dfTrain,dfTest,)


else:
	print("wrong arguments")
