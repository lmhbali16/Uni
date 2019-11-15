import csv

#These lists are used to help the cleaning process.
monthList = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
dayList = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
collisionList = ["Non collision", "Rear End", "Head On", "Rear End", "Right Angle", "Side Swipe", "Side Swipe", "Hit Fixed Object", "Hit Pedestrian", "Other or Unknown"]
severityList = ["Not Injured", "Minor Injury", "Major Injury", "Fatal"]


#The purpose of this function is for overall cleaning. Given a particular write
#from the dataset, it checks for missing values and accounts for inconsistent
#and incorrect values.
def cleaningFunction(list):
    flag = True

    #We determine if there are any missing values firstly.
    if "" in list:
        flag = False

    #For alcohol there is an inconsistency as the American dataset uses
    #binary notation while the Australian one uses Y/N. We will convert the
    #binary to Y/N
    alcohol = list[15]
    #The dataset keeps no alcohol as blank spaces, but it is more useful to us as "N".
    #So we convert blank spaces to "N"
    if not alcohol:
        alcohol = "N"

    #This makes values from the American dataset consistent with the Australian one
    if alcohol == "0":
        alcohol = "N"
    elif alcohol == "1":
        alcohol = "Y"
    list[15] = alcohol

    #Inconsistency for month as the American dataset uses the numerical value
    #for the month instead of the name of the month like the Australian one.
    month = list[6]
    for i in range(12):
        if month == str(i + 1):
            month = monthList[i]
    list[6] = month

    #Days of the week also has a similar problem to month.
    day = list[7]
    for i in range(7):
        if day == str(i + 1):
            day = dayList[i]
    list[7] = day

    #Time in the American dataset is in 24 hour time instead of 12 hour like
    #the Australian one. We shall convert the Amercian time into 12 hour time
    time = list[8]
    #This if statement determines if it is from the Australian or American dataset.
    if ':' in time:
        pass
    else:
        if len(time) == 4:
            hour = time[:2]
            minutes = time[2:4]

            if int(hour) > 12:

                realHour = int(hour) - 12
                timeString = str(realHour) + ":" + minutes + " pm"
            else:
                timeString = hour + ":" + minutes + " am"
        elif len(time) == 3:
            hour = time[:1]
            minutes = time[1:3]

            if int(hour) > 12:

                realHour = int(hour) - 12
                timeString = str(realHour) + ":" + minutes +" pm"
            else:
                timeString = hour + ":" + minutes + " am"
        elif len(time) == 2:
            hour  = 12
            minutes = time[:2]

            timeString = str(hour) + ":" + minutes + " am"
        elif len(time) == 1:
            hour = 12
            minutes = time[:1]

            timeString = str(hour) + ":" + minutes + " am"
        else:
            timeString = "12:00 am"

        list[8] = timeString


    #The American dataset also uses binary to display whether the road is
    #wet or dry.
    moisture = list[10]
    if moisture == "0":
        moisture = "Dry"
    elif moisture == "1":
        moisture = "Wet"
    list[10] = moisture

    #For weather the American one also uses a numbering system, so we shall make
    #it consistent with the Australian dataset by determing if it is raining or
    #not raining
    weather = list[11]
    #We transform  values into Y or N to denote if there are adverse weather
    #conditions or not.
    if weather == "Not Raining":
        weather = "N"
    elif weather == "Raining":
        weather = "Y"
    elif weather == "1":
        weather = "N"

    #We then transform the numeric weather values into Y or N for the American data
    for i in range(2, 8):
        if weather == str(i):
            weather = "Y"

    #We account for any unknown values in the American dataset.
    if weather == "8":
        weather = "Unknown"
    elif weather == "9":
        weather = "Unknown"
    list[11] = weather

    #For day or night the American one also uses a numbering system again. The
    #process here is similar to the American one.
    daynight = list[12]
    if daynight == "1":

        daynight = "Daylight"

    for i in range(2, 5):
        if daynight == str(i):
            daynight = "Night"

    if daynight == "5":
        daynight = "Daylight"
    elif daynight == "6":
        daynight = "Night"
    elif daynight == "8":
        daynight = "Unknown"
    elif daynight == "9":
        daynight = "Unknown"
    list[12] = daynight

    #For collision type the American dataset uses enumeration again. We transform
    #the American values to be consistent with the Australian ones. However,
    #the two datasets had different types of observations between them for this
    #column, so any observation that was not common between the two datasets ended
    #up not being included in the final dataset.
    collision = list[13]

    if collision == "1":
        collision = "Rear End"
    elif collision == "2":
        collision = "Head On"
    elif collision  == "4":
        collision = "Right Angle"
    elif collision == "5" or collision == "6":
        collision = "Side Swipe"
    elif collision == "7":
        collision = "Hit Object on Road"
    elif collision == "8":
        collision = "Hit Pedestrian"
    elif collision == "9":
        collision = "Other"
    list[13] = collision

    #For severity the American one again used a numbering system, and we also
    #convert some Australian values to be nicer to the eyes. Again, since the two
    #datasets did not share the same type of observations we disregarded any values
    #that weren't common beween the two datasets.
    severity = list[14]

    if severity == "1: PDO":
        severity = "Not Injured"
    elif severity == "2: MI":
        severity = "Minor Injury"
    elif severity == "3: SI":
        severity = "Major Injury"
    elif severity == "4: Fatal":
        severity = "Fatal"
    elif severity == "0":
        severity = "Not Injured"
    elif severity == "1":
        severity = "Fatal"
    elif severity == "2":
        severity = "Major Injury"
    elif severity == "3":
        severity = "Minor Injury"
    elif severity == "4":
        severity = "Minor Injury"
    list[14] = severity

    #The American data uses bianry for drug presence
    drugs = list[16].strip() #We strip here as it has a newline character, being
    #the last value of the row.
    if not drugs:
        drugs = "N"
    if drugs == "0":
        drugs = "N"
    elif drugs == "1":
        drugs = "Y"
    list[16] = drugs

    '''This begins the part of code for checking for incorrect values'''

    #Check alcohol column is all the values we want and delete values which are
    #not what we expect
    alcohol = list[15]
    if not(alcohol == "Y" or alcohol == "N"):
        
        flag = False

    #This ensures that all count values are int values and are not decimals.
    if int(list[1]) != float(list[1]) or int(list[2]) != float(list[2]) or int(list[3]) != float(list[3]) or int(list[4]) != float(list[4]):
        flag = False
        


    #TotalUnits should be >= 0 and should be of type int
    try:
        totalUnits = int(list[1])
        if not(totalUnits >= 0):
            flag = False
    except:
        flag = False

    #TotalFatalities should be >= 0 and an int
    try:
        totalFatalities = int(list[2])
        if not(totalFatalities >= 0):
            flag = False
            
    except:
        flag = False
        



    #Major Injury count is the same deal
    try:
        totalMAjury = int(list[3])
        if not(totalMAjury >= 0):
            flag = False
            
    except:
        flag = False
        

    #Minor injury count is the same deal
    try:
        totalMinInjury = int(list[4])
        if not(totalMinInjury >= 0):
            flag = False
            
    except:
        flag = False
        

    #CrashYear should be of 2017 as that is what we chose our dataset to be in
    crashyear = list[5]
    if not(crashyear == "2017"):
        flag = False
        

    #CrashMonth should be one of the possible months.
    month = list[6]
    if not(month in monthList):
        flag = False
        

    #Day should be one of the possible days.
    day = list[7]
    if not(day in dayList):
        flag = False
       

    #The hours for the time should be <= 12, minutes should be <= 59 and
    #it should be am or pm and hour and minute should be of type int and all greater than 0
    time = list[8]
    timeList = time.split()
    hourminuteList = timeList[0].split(":")
    try:
        hour = int(hourminuteList[0])
        minute = int(hourminuteList[1])
        endThing = timeList[1].lower()

        if hour > 12 or hour < 0 or minute > 59 or minute < 0:
            
            flag = False
        if not(endThing == "am" or endThing == "pm"):
            
            flag = False
    except:
        
        flag = False

    #Speedlimit should be > 0 and an int. It should also be in increments of 10.
    try:
        speed = int(list[9])
        if not(speed > 0) or speed % 10 != 0:
            
            flag = False
    except:
        
        flag = False



    #Road Moisture we check if it is dry or wet
    moisture = list[10]
    if not(moisture == "Dry") and not(moisture == "Wet"):
        flag = False
        

    #Check if weather is "Y" or "N" (it also removes NA values)
    weather = list[11]
    if not(weather == "Y" or weather == "N"):
        flag = False
       

    #Check that light is either Daylight or Night (removes unknown values)
    light = list[12]
    if not(light == "Night" or light == "Daylight"):
        flag = False
        

    #Check the crash type is one of the expexcted ones. This doesn't remove
    #other and unknown though which we may want to do.
    collision = list[13]
    if not(collision in collisionList):
        flag = False
        


    #Check that drugs is either "Y" or "N"
    drugs = list[16]
    if not(drugs == "Y" or drugs == "N"):
        flag = False
        
    list[16] = drugs + "\n"#Add the newline character back to drugs now.

    #We make sure that severity is one of the expected ones.
    severity = list[14]
    if not(severity in severityList):
        flag = False
        


    return (flag, list)

file = open("final.csv", "w+")
csv_readerSA = csv.reader(open("2017_DATA_SA_Crash.csv"))
first_line = True

#I will first sort and filter through the SA dataset.
for line in csv_readerSA:
    if first_line:
        header = "Nation,Total Units,Total Fatalities,Total Serious Injuries,Total Minor Injuries,Year,Month,Day,Time,Speed Limit,Moisture,Adverse Weather Conditions,DayNight,Crash Type,Crash Severity,Alcohol Related ,Drug Related\n"
        file.write(header)
        first_line = False
    else:
        nation = "AUS"
        alcohol = line[28]
        totalUnits = line[5]
        totalFatalities = line[7]
        totalCasualties = line[6]
        totalSeriousInjury = line[8]
        totalMinorInjury = line[9]
        year = line[10]
        month = line[11]
        day = line[12]
        time = line[13]
        speedLimit = line[14]
        positionType = line[15]

        roadMoisture = line[20]
        weather = line[21]
        #lightCondition = line Actually I can't seem to find this one in the dataset, maybe we can replace it with the daytime or nighttime one?
        crashType = line[23]
        crashSeverity = line[26]
        trafficControl = line[27]
        drugs = line[29]
        lightCondition = line[22]


        if not drugs:
            drugs = "N"

        #The dataset keeps no alcohol information as blank spaces, but it is more useful to us as "N".
        if not alcohol:
            alcohol = "N"

        row = "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(nation, totalUnits, totalFatalities, totalSeriousInjury, totalMinorInjury, year, month, day, time, speedLimit, roadMoisture, weather, lightCondition, crashType, crashSeverity, alcohol, drugs)
        list = row.split(",")#first I turn the row string into a list for use with
        #the cleaning function.

        tuple = cleaningFunction(list)#We assign a value to the tuple that the
        #cleaning function returns.
        flag = tuple[0]#In the cleaning function, there was a boolean value which
        #determines if there were any incorrect values. It is set to true, by
        #default, and if the function encounters any incorrect values it is set to false.

        list = tuple[1]#We retrieve the newly transformed list that now accounts
        #for inconsistent values due to the cleaningFunction

        #If there were no incorrect values, then we right this particular row to
        #the file by converting the list back to a string.
        if flag:
            file.write(", ".join(list))

#We apply similar logic to the American dataset.
csv_readerA = csv.reader(open("bf8b3c7e-8d60-40df-9134-21606a451c1a.csv"))
first_line = True

for line in csv_readerA:
    if first_line:
        pass
        
        first_line = False
    else:
        Nation = "US"
        alcohol = line[127]
        totalUnits = line[21]
        totalFatalities = line[32]
        totalSeriousInjury = line[34]
        totalMinorInjury = line[36]
        year = line[5]
 
        month = line[6]
        day = line[7]
        time = line[8]

        #I account for the fact that the American dataset is in mph and round it up
        #to the nearest 10.
        speedLimit = line[184]
        if speedLimit != "":
            speedLimit = round(int(speedLimit) * 1.60934)
        speedLimit = str(speedLimit)
        if len(speedLimit) >= 2:
            if int(speedLimit[-1]) < 5:
                speedLimit = speedLimit[0:len(speedLimit) - 1] + "0"
            elif int(speedLimit[-1]) >= 5:
                speedLimit = str(int(speedLimit[0:len(speedLimit) - 1]) + 1) + "0"



        roadMoisture = line[91]
        weather = line[11]
       
        crashType = line[13]
        crashSeverity = line[52]
        
        drugs = line[165]
        lightCondition = line[10]


        row = "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(Nation, totalUnits, totalFatalities, totalSeriousInjury, totalMinorInjury, year, month, day, time, speedLimit, roadMoisture, weather, lightCondition, crashType, crashSeverity, alcohol, drugs)
        list = row.split(",")

        tuple = cleaningFunction(list)
        flag = tuple[0]
        list = tuple[1]


        if flag:
            file.write(", ".join(list))

file.close()
