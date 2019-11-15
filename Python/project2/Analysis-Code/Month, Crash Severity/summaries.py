import statistics

#This function finds the mean and SD for each crashType and for each month.
#It also finds the top 3 motnhs with the highest average for that particular month.
#It also finds the number of the given crashType that occurred for that particular month
#And finds the month with the highest amount of crashes.
def crashSummary(crashType):
    first_line = True

    fatal_dict = {}

    for line in open("analysis.csv"):
        if first_line:
            first_line = False
        else:
            values = line.split(",")

            fatal = int(values[2])
            serious = int(values[3])
            minor = int(values[4])

            month = values[6]

            if month in fatal_dict:
                if crashType == "Fatal":
                    fatal_dict[month].append(fatal)
                elif crashType == "Serious":
                    fatal_dict[month].append(serious)
                elif crashType == "Minor":
                    fatal_dict[month].append(minor)
            else:
                if crashType == "Fatal":
                    fatal_dict[month] = [fatal]
                elif crashType == "Serious":
                    fatal_dict[month] = [serious]
                elif crashType == "Minor":
                    fatal_dict[month] = [minor]

    highestMean = 0
    highestMonth = ""
    highestCrashCount = 0
    highestCrashMonth = ""

    print("Statistics for {} crashes:".format(crashType))

    for i,k in fatal_dict.items():
        total = sum(k)
        mean = statistics.mean(k)
        sd = statistics.stdev(k)

        print("Mean {} crashes for {}: {}".format(crashType, i, mean))
        print("Standard deviation of {} for {}: {}".format(crashType, i, sd))
        print("Total amount of {} crashes: {}".format(crashType, total))
        print()

        if mean > highestMean:
            highestMean = mean
            highestMonth = i

        if total > highestCrashCount:
            highestCrashCount = total
            highestCrashMonth = i

        fatal_dict[i] = mean

    highestList = sorted(fatal_dict, key=fatal_dict.get, reverse=True)[:3]

    print("The months with the highest average {} crashes were:".format(crashType))
    for key in highestList:
        print(key)
    print()

    print("The month with the most amount of {} crashes was: {}, corresponding to {} crashes".format(crashType, highestCrashMonth, highestCrashCount))
    print()


#This function will find the mean amount of fatalities, minior, and major injuries
#per the different types of crashes (alcohol, drugs etc..)  as well as the standard deviation.
def alcoholdrugCrash(crashType):
    first_line = True

    crash_dict = {"DA": [], "A": [], "D": [], "NDA": []}

    for line in open("analysis.csv"):




        if first_line:
            first_line = False
        else:
            values = line.split(",")

            fatal = int(values[2])
            serious = int(values[3])
            minor = int(values[4])

            alcohol = values[15].strip()
            drugs = values[16].strip()


            if drugs == "Y" and alcohol == "Y":


                if crashType == "Fatal":
                    crash_dict["DA"].append(fatal)
                elif crashType == "Serious":
                    crash_dict["DA"].append(serious)
                elif crashType == "Minor":
                    crash_dict["DA"].append(minor)

            elif drugs == "N" and alcohol == "Y":
                if crashType == "Fatal":
                    crash_dict["A"].append(fatal)
                elif crashType == "Serious":
                    crash_dict["A"].append(serious)
                elif crashType == "Minor":
                    crash_dict["A"].append(minor)

            elif drugs == "Y" and alcohol == "N":
                if crashType == "Fatal":
                    crash_dict["D"].append(fatal)
                elif crashType == "Serious":
                    crash_dict["D"].append(serious)
                elif crashType == "Minor":
                    crash_dict["D"].append(minor)

            elif drugs == "N" and alcohol == "N":

                if crashType == "Fatal":
                    crash_dict["NDA"].append(fatal)
                elif crashType == "Serious":
                    crash_dict["NDA"].append(serious)
                elif crashType == "Minor":
                    crash_dict["NDA"].append(minor)

    firsttime = True

    for i, k in crash_dict.items():

        if len(k) == 0:

            continue

        mean = statistics.mean(k)
        sd = statistics.stdev(k)

        if firsttime:
            print("Statistics for {} injuries: ".format(crashType))
            firsttime = False



        if i == "DA":
            print("The mean number of {} injuries for crashes involving alcohol and drugs is: {}".format(crashType, mean))
            print("The standard deviation of {}ities for crashes involving alcohol and drugs is: {}".format(crashType, sd))
            print()
        if i == "A":
            print("The mean number of {} injuries for crashes involving alcohol is: {}".format(crashType, mean))
            print("The standard deviation of {} injuries for crashes involving alcohol and drugs is: {}".format(crashType, sd))
            print()
        if i == "D":
            print("The mean number of {} injuries for crashes involving drugs is: {}".format(crashType, mean))
            print("The standard deviation of {} accidents for crashes involving alcohol and drugs is: {}".format(crashType, sd))
            print()
        if i == "NDA":
            print("The mean number of {} injuries for crashes not involving alcohol and drugs is: {}".format(crashType, mean))
            print("The standard deviation of {} injuries for crashes involving alcohol and drugs is: {}".format(crashType, sd))
            print()







crashSummary("Fatal")
crashSummary("Serious")
crashSummary("Minor")
alcoholdrugCrash("Fatal")
alcoholdrugCrash("Serious")
alcoholdrugCrash("Minor")
