#This program finds the mean amount of units for crashes in each nation corresponding to positive and negative weather conditions.
import statistics;
import pandas as pd
import numpy as np

data_by_nation = {}
is_first_line = True
file = open("analysis.txt","w+")
print("Analysis 1\n")
file.write("Analysis 1\n\n")
for row in open("final.csv"):
  if is_first_line:
    is_first_line = False

  else:
    #We extract the values for all the necessary information from the file.
    values = row.split(",")
    nation = values[0]
    weather = values[11]
    totalUnits = int(values[1])
    #We create a key which contains information on the nation and the weather conditions.
    dict_key = (nation, weather)

    if dict_key in data_by_nation:
        data_by_nation[dict_key].append(totalUnits)
    else:
        data_by_nation[dict_key] = [totalUnits]

#We go through all the nation and weather combinations and find the mean.
print("Mean for each nation and corresponding weather condition:\n")
file.write("Mean for each nation and corresponding weather condition:\n\n")
for key in data_by_nation:
    print("{}: {}\n".format(key, statistics.mean(data_by_nation[key])))
    file.write("{}: {}\n".format(key, statistics.mean(data_by_nation[key])))

#These combined lists concatenate the two lists for each nation and then later finds the mean of them.
combinedUS = data_by_nation[('US', ' N')] + data_by_nation[('US', ' Y')]
combinedAUS = data_by_nation[('AUS', ' N')] + data_by_nation[('AUS', ' Y')]
print()
file.write("\n\n")
print("Overall mean for US: {}\n".format(statistics.mean(combinedUS)))
file.write("Overall mean for US: {}\n".format(statistics.mean(combinedUS)))
print("Overall mean for AUS: {}\n".format(statistics.mean(combinedAUS)))
file.write("Overall mean for AUS: {}\n".format(statistics.mean(combinedAUS)))
file.write("\n\n")

#------------------------------||--||------------------------------------------
#------------------------------||--||------------------------------------------

print("Analysis 2\n")
file.write("Analysis 2\n\n")

#Read our final csv file
df = pd.read_csv("final.csv")

#I grouped the values based on two conditions:
#Whether it is US or AUS and whether that day was rainy or not
#The I separated the table to minor and major injuries
#in order to calculate the number of minor and major injures separately

major = df.sort_values(["Nation"]).groupby(["Nation", "Adverse Weather Conditions"], sort=False)["Total Serious Injuries"]
minor = df.sort_values(["Nation"]).groupby(["Nation", "Adverse Weather Conditions"], sort=False)["Total Minor Injuries"]

#I use the sum function to sum up the injuries
num_major = major.sum()
num_minor = minor.sum()

#Here I created a new column using the np.where function
#where if there was no minor and major injury
#it returned 1 and 0 if there was
df['No Injury'] = np.where((df['Total Serious Injuries']==0)&(df['Total Minor Injuries']==0), 1,0)

#Here I used the sum function to calculate how many crashes there were
#where injury did not result
no_inj = df.sort_values(["Nation"]).groupby(["Nation", "Adverse Weather Conditions"], sort=False)["No Injury"].sum()

#create dictionaries
num_minor_dict = num_minor.to_dict()
num_major_dict = num_major.to_dict()
num_noinj_dict =no_inj.to_dict()
file.write("Number of major injuries based on Nation and weather condition:\n\n")
print("Number of major injuries based on Nation and weather condition:\n")
for i in num_major_dict:
	print(str(i)+" : "+str(num_major_dict[i]))
	file.write(str(i)+" : "+str(num_major_dict[i])+"\n")
file.write("\n\n")
print("\n")
print("Number of minor injuries based on Nation and weather condition:\n")
file.write("Number of minor injuries based on Nation and weather condition:\n\n")
for i in num_minor_dict:
	print(str(i)+" : "+str(num_minor_dict[i]))
	file.write(str(i)+" : "+str(num_minor_dict[i])+"\n")
print("\n")
file.write("\n\n")
print("Number of no injuries based on Nation and weather condition:\n")
file.write("Number of no injuries based on Nation and weather condition:\n\n")
for i in num_noinj_dict:
	print(str(i)+" : "+str(num_noinj_dict[i]))
	file.write(str(i)+" : "+str(num_noinj_dict[i])+"\n")
print("\n")
file.write("\n\n")
print("Percentage of major injuries based on Nation and weather condition:\n")
file.write("Percentage of major injuries based on Nation and weather condition:\n\n")
for i in num_major_dict:
	file.write(str(i)+" : "+str(round(num_major_dict[i]*100/(num_minor_dict[i]+num_noinj_dict[i]+num_major_dict[i]),2))+"\n")
	print(str(i)+" : "+str(round(num_major_dict[i]*100/(num_minor_dict[i]+num_noinj_dict[i]+num_major_dict[i]),2)))
print("\n")
file.write("\n\n")
print("Percentage of minor injuries based on Nation and weather condition:\n")
file.write("Percentage of minor injuries based on Nation and weather condition:\n\n")
for i in num_minor_dict:
    #print(num_minor_dict[i])
	file.write(str(i)+" : "+str(round(num_minor_dict[i]*100/(num_noinj_dict[i]+num_minor_dict[i]+num_major_dict[i]),2))+"\n")
	print(str(i)+" : "+str(round(num_minor_dict[i]*100/(num_noinj_dict[i]+num_minor_dict[i]+num_major_dict[i]),2)))
print("\n")
file.write("\n\n")
print("Percentage of injuries based on Nation and weather condition:\n")
file.write("Percentage of injuries based on Nation and weather condition:\n\n")
for i in num_minor_dict:
	a = (num_major_dict[i]+num_minor_dict[i])*100/(num_minor_dict[i]+num_major_dict[i]+num_noinj_dict[i])
	print(str(i)+" : "+str(round(a,2)))
	file.write(str(i)+" : "+str(round(a,2))+"\n")



#_________________________________________________________________________________
#Analysis 3 - Daily script
#_________________________________________________________________________________

import csv
is_first_line = True
countMonday = 0
countTuesday = 0
countWednesday = 0
countThursday = 0
countFriday = 0
countSaturday = 0
countSunday = 0
countWeekday = 0
countWeekend = 0
countWeekdayAUS = 0
countWeekdayUS = 0
countWeekendAUS = 0
countWeekendUS = 0


for row in open("final.csv"):
       if is_first_line:
            is_first_line = False
       else:
            values = row.split(",")
            if values[7] == " Monday":
               countMonday += 1
               countWeekday += 1
               if values[0] == "AUS":
                   countWeekdayAUS += 1
               else:
                    countWeekdayUS +=1
            if values[7] == " Tuesday":
               countTuesday += 1
               countWeekday += 1
               if values[0] == "AUS":
                   countWeekdayAUS += 1
               else:
                    countWeekdayUS +=1
            if values[7] == " Wednesday":
               countWednesday += 1
               countWeekday += 1
               if values[0] == "AUS":
                   countWeekdayAUS += 1
               else:
                   countWeekdayUS +=1
            if values[7] == " Thursday":
               countThursday += 1
               countWeekday += 1
               if values[0] == "AUS":
                   countWeekdayAUS += 1
               else:
                   countWeekdayUS +=1
            if values[7] == " Friday":
               countFriday += 1
               countWeekday += 1
               if values[0] == "AUS":
                   countWeekdayAUS += 1
               else:
                   countWeekdayUS +=1
            if values[7] == " Saturday":
               countSaturday += 1
               countWeekend += 1
               if values[0] == "AUS":
                   countWeekendAUS += 1
               else:
                    countWeekendUS +=1
            if values[7] == " Sunday":
               countSunday += 1
               countWeekend += 1
               if values[0] == "AUS":
                   countWeekendAUS += 1
               else:
                   countWeekendUS +=1

print("\nAnalysis 3\n")
file.write("\nAnalysis 3\n\n")

print("number of crashes on weekdays are:\n")
file.write("number of crashes on weekdays are:\n\n")
print(countWeekday)
file.write(str(countWeekday)+"\n")
print("number of crashes on weekends are:\n")
file.write("number of crashes on weekends are:\n\n")
print(countWeekend)
file.write(str(countWeekend)+"\n")
print("number of crashes on Mondays are:\n")
file.write("number of crashes on Mondays are:\n\n")
print(countMonday)
file.write(str(countMonday)+"\n")
print("number of crashes on Tuesdays are:\n")
file.write("number of crashes on Tuesdays are:\n\n")
print(countTuesday)
file.write(str(countTuesday)+"\n")
print("number of crashes on Wednesdays are:\n")
file.write("number of crashes on Wednesdays are:\n\n")
print(countWednesday)
file.write(str(countWednesday)+"\n")
print("number of crashes on Thursdays are:\n")
file.write("number of crashes on Thursdays are:\n\n")
print(countThursday)
file.write(str(countThursday)+"\n")
print("number of crashes on Fridays are:\n")
file.write("number of crashes on Fridays are:\n\n")
print(countFriday)
file.write(str(countFriday)+"\n")
print("number of crashes on Saturdays are:\n")
file.write("number of crashes on Saturdays are:\n\n")
print(countSaturday)
file.write(str(countSaturday)+"\n")
print("number of crashes on Sundays are:\n")
file.write("number of crashes on Sundays are:\n\n")
print(countSunday)
file.write(str(countSunday)+"\n")
print("number of crashes in Australia on weekdays are:\n")
file.write("number of crashes in Australia on weekdays are:\n\n")
print(countWeekdayAUS)
file.write(str(countWeekdayAUS)+"\n")
print("number of crashes in US on weekdays are:\n")
file.write("number of crashes in US on weekdays are:\n\n")
print(countWeekdayUS)
file.write(str(countWeekdayUS)+"\n")
print("number of crashes in Australia on weekends are:\n")
file.write("number of crashes in Australia on weekends are:\n\n")
print(countWeekendAUS)
file.write(str(countWeekendAUS)+"\n")
print("number of crashes in US on weekends are:\n")
file.write("number of crashes in US on weekends are:\n\n")
print(countWeekendUS)
file.write(str(countWeekendUS)+"\n")

file.close()
