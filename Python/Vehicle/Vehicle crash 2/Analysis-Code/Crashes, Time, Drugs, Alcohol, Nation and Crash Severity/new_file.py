import matplotlib.pyplot as plt
import numpy as np


file = open("analysis.csv","w+")


for i in open("final.csv"):
	if i.startswith("Nation"):
		i = i.strip()

	else:
		i = i.strip()


	a = i.strip().split(",")
	t = a[8].split(":")
	if a[8] !="Time" and len(t[1]) ==5:
		
		if float(t[1][1]) < 5 and t[1][0]=="0":
			a[8]= a[8][:-5]+"00"+a[8][-3:]
		elif float(t[1][1]) >= 5 and t[1][0]=="0":
			a[8]= a[8][:-5]+"10"+a[8][-3:]
		elif float(t[1][0:2]) < 15 and float(t[1][0:2]) >= 10:
			a[8]= a[8][:-5]+"10"+a[8][-3:]
		elif int(t[1][0:2]) >= 15 and int(t[1][0:2]) < 25:
			a[8]= a[8][:-5]+"20"+a[8][-3:]
		elif int(t[1][0:2]) >= 25 and int(t[1][0:2]) < 35:
			a[8]= a[8][:-5]+"30"+a[8][-3:]
		elif int(t[1][0:2]) >= 35 and int(t[1][0:2]) < 45:
			a[8]= a[8][:-5]+"40"+a[8][-3:]
		elif int(t[1][0:2]) >= 45 and int(t[1][0:2]) < 55:
			a[8]= a[8][:-5]+"50"+a[8][-3:]
		elif int(t[1][0:2]) >= 55 and int(t[1][0:2]) < 65:
			if not t[0].startswith(" 12"):
				a[8]= " "+str(int(t[0][1:])+1)+":00"+a[8][-3:]
			elif t[0].startswith(" 12"):
				a[8]= " 00:00"+t[1][-3:]

	

	elif a[8] !="Time" and len(t[1]) ==4:
		if float(t[1][0]) < 5:
			a[8]= t[0]+":00"+t[1][1:]
		elif float(t[1][0]) >= 5:
			a[8]= t[0]+":10"+t[1][1:]

	if a[8] !="Time":
		if t[1].endswith("pm") and len(t[0]) == 3 and not t[0].startswith(" 12"):
			l = a[8].split(":")
			a[8] = str(int(l[0][1:])+12)+":"+l[1][:len(l[1])-2]
		elif t[1].endswith("pm") and len(t[0]) == 2 and not t[0].startswith(" 12"):
			a[8] = str(int(a[8][1])+12)+a[8][2:len(a[8])-2]
		elif t[1].endswith("am") and t[0].startswith(" 12"):
			a[8] = "00"+a[8][3:len(a[8])-2]
		elif t[1].endswith("am") and not t[0].startswith(" 12"):
			a[8] = a[8][1:len(a[8])-2]
		elif t[1].endswith("pm") and t[0].startswith(" 12"):
			a[8] = a[8][1:3]+a[8][3:len(a[8])-2]

	b= ""

	for c in range(len(a)):
		if c != len(a)-1:
			b += a[c]+","
		elif c== len(a)-1:
			b+= a[c]+"\n"

	file.write(b)
file.close()








