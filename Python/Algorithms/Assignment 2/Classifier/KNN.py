import numpy as np




class KNN:


	@staticmethod
	def knn(k,trainingset, testset):
		trainingvals = np.array(np.delete(trainingset,-1,1),dtype = float)
		
		testvals = np.array(testset,dtype = float)
		result = []
		for val in testvals:	
			distances = KNN.euclid_dist(trainingvals,val)

			distances = distances.reshape(1,distances.shape[0]).transpose()

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
				result.append('yes')
			if count_yes < count_no:
				result.append('no')
			if count_yes == count_no:
				result.append('yes')

		return result

	@staticmethod
	def euclid_dist(data,inputs):

		return np.sqrt((np.sum(np.square(inputs - data),1)))