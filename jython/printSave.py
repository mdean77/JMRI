# printSave.py
# Mike Dean January 24 2019
#
# routine should print and write to a file in append mode.
#
def printSave(aString):
	print(aString)
	filename = "SpeedOutput.txt"
	f = open(filename,'a')
	f.write(aString,"\n")
	f.close()

printSave("Hello")
	