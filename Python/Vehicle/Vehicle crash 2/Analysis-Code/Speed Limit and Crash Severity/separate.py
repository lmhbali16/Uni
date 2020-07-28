#Write speed limit values to separated files based on crash severity levels 
import csv
fatal = 'fatal.csv'
major = 'major.csv'
minor = 'minor.csv'
non = 'non.csv'	
	
with open("final.csv") as f:	
	reader = csv.reader(f)
	l = [row[9] for row in reader] #Speed limit is the 8th variable
	
with open("final.csv") as f:	
	reader = csv.reader(f)	
	s = [row[14] for row in reader] #Crash severity is the 15th variable
	
	with open(fatal, "w") as fa:
		writer = csv.writer(fa)
		writer.writerow(['Speed Limit'])
		for i in range(len(s)):
			if s[i] == ' Fatal':
				writer.writerow([l[i]])
	
	with open(major, "w") as fa:
		writer = csv.writer(fa)
		writer.writerow(['Speed Limit'])
		for i in range(len(s)):
			if s[i] == ' Major Injury':
				writer.writerow([l[i]])
	
	with open(minor, "w") as fa:
		writer = csv.writer(fa)
		writer.writerow(['Speed Limit'])
		for i in range(len(s)):
			if s[i] == ' Minor Injury':
				writer.writerow([l[i]])
	
	with open(non, "w") as fa:
		writer = csv.writer(fa)
		writer.writerow(['Speed Limit'])
		for i in range(len(s)):
			if s[i] == ' Not Injured':
				writer.writerow([l[i]])