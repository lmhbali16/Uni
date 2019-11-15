import pandas as pd
import numpy as np


#Read our final csv file
df = pd.read_csv("final.csv")

#I grouped the values based on two conditions:
#Whether it is US or AUS and whether that day was rainy or not
#The I separated the table to minor and major injuries
#in order to calculate the number of minor and major injures separately

major = df.sort_values(["Nation"]).groupby(["Nation", " Adverse Weather Conditions"], sort=False)["Total Serious Injuries"]
minor = df.sort_values(["Nation"]).groupby(["Nation", " Adverse Weather Conditions"], sort=False)["Total Minor Injuries"]

#I use the sum function to sum up the injuries
num_major = major.sum()
num_minor = minor.sum()

#Here I created a new column using the np.where function
#where if there was no minor and major injury
#it returned 1 and 0 if there was
df['No Injury'] = np.where((df['Total Serious Injuries']==0)&(df['Total Minor Injuries']==0), 1,0)

#Here I used the sum function to calculate how many crashes there were
#where injury did not result
no_inj = df.sort_values(["Nation"]).groupby(["Nation", " Adverse Weather Conditions"], sort=False)["No Injury"].sum()

#create dictionaries
num_minor_dict = num_minor.to_dict()
num_major_dict = num_major.to_dict()
num_noinj_dict =no_inj.to_dict()

print("Number of major injuries based on Nation and weather condition:\n")
for i in num_major_dict:
	print(str(i)+" : "+str(num_major_dict[i]))
print("\n")
print("Number of minor injuries based on Nation and weather condition:\n")
for i in num_minor_dict:
	print(str(i)+" : "+str(num_minor_dict[i]))
print("\n")
print("Number of major injuries based on Nation and weather condition:\n")
for i in num_noinj_dict:
	print(str(i)+" : "+str(num_noinj_dict[i]))
print("\n")
print("Percentage of major injuries based on Nation and weather condition:\n")
for i in num_major_dict:
	print(str(i)+" : "+str(round(num_major_dict[i]/(num_noinj_dict[i]+num_major_dict[i]),2)))
print("\n")
print("Percentage of minor injuries based on Nation and weather condition:\n")
for i in num_minor_dict:
	print(str(i)+" : "+str(round(num_minor_dict[i]/(num_noinj_dict[i]+num_minor_dict[i]),2)))
print("\n")
print("Percentage of injuries based on Nation and weather condition:\n")
for i in num_minor_dict:
	a = (num_major_dict[i]+num_minor_dict[i])/(num_minor_dict[i]+num_major_dict[i]+num_noinj_dict[i])
	print(str(i)+" : "+str(round(a,2)))


