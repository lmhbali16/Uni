import sys
import pandas as pd
import numpy as np


colnames = ["pregnancy", "glucose", "blood", "skin","insulin","bmi","diabetes","age","label"]

df = pd.DataFrame(columns=colnames)

file = open("pima-indians-diabetes.data", "r")

listRow = file.read().strip('\n').strip('\r\n').split('\r\n')

for i in range(len(listRow)):
	
	row = listRow[i].split(',')
	
	rowNew = [np.double(j) for j in row[:-1]]+[row[-1]]

	df.loc[i] = rowNew




for colname, content in df.iteritems():
	if colname == 'label':
		continue

	maxval = max(content)
	minval = min(content)

	for i in range(len(content)):

		content[i] = round((content[i] - minval) / (maxval - minval),2)



df.to_csv('pima.csv', index = False, header=False)