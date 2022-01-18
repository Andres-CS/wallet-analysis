import csv
import re

'''
Delete char in substring of original string.

Used this function when, you want to delete 
a character in a substring but not in the
rest of the original string.

Returns a string

 -- PARAMETERS --
text: 	original string
start: 	start of subString
end: 	end of subString
char: 	char to delete, default is ','.

'''
def deleteInSubString(text, start, end, char=','):
	subText = text[start:(end+1)]
	commaPos = subText.find(char)
	if commaPos >= 0:
		subText = subText[:commaPos]+""+subText[commaPos+1:]
		text = text[:start]+subText+text[end+1:]
		return text
	return text


'''
Get the position of the Description Column.

Loops through String and finds the first set
of enclosing quotes.

Returns array with initial and closing position.
 
 -- PARAMETERS --
txt: string to loop
''' 
def DescriptionColumn_Range(txt):
	count = 0
	pos=list()
	for i in range(len(txt)):
		if txt[i] == '"':
			pos.append(i)
			count += 1
		if count == 2:
			return pos


'''
Adds a delimiter

Returns a new string with the delimiter 
added.

-- PARAMETERS --
text: 		string to be modified
delimiter: 	char or string to be inserted
flad:  		b - before target
			a - after target
target: 	substring where delimiter will be 
		 	inserted
'''
def addDelimiter(text,delimiter,flag,target):
	pos = text.find(target)
	if not pos == -1:
		if flag == "b":
			text = text[:pos]+delimiter+text[pos:]

		else:
			offset =  len(text[:pos])+len(target)
			text = text[:offset+1]+delimiter+text[offset+1:]

	return text

'''
Clean up of Description Column

Inital draft of data clean up on the 
description column.

Removal of extra commas and 'garbage' data

Returns a string

 -- PARAMETERS --
data:	string 
'''
def clean_Description_Column(data):
	#Replace data 00/00 for ,
	data = re.sub("[0-9]{2}\/[0-9]{2}", ",", data)
	
	for i in ["'",",/20",",/21"]:
		data = data.replace(i,"")

	wordBank={
		'c':["CREDITS","check","Check","CHARGE","CONSUMER"],
		'd':["DEPOSIT","DEBITS"],
		'f':["Fee","FEE","Funds"],
		'o':["OVERDRAFT"],
		'p':["PURCHASE","PAY","pymt","PMT","PMNT","Payment","PAYMENT","payment","PAYROLL"],
		'r':["REFUND"],
		't':["TAX","Transfer","transfer","TRANSFER"],
		'w':["WITHDRWL","withdrawal","withdrwl"]
	}

	for k in wordBank:
		for i in wordBank[k]:
			i = i.lower()
			if i in data:
				data = addDelimiter(data,",", "b" , i)
				data = addDelimiter(data,",", "a" , i)
				#print(data)
	
	#Get Rid of repeating commas.
	data = re.sub("#[0-9]+","",data)
	data = re.sub(	'(,\s*,)',
					',',
					re.sub(	'(,{1,10}|,\s*,\b)', ",", data)
				 )
	
	for match in re.finditer("\s[a-zA-Z]{2}$",data):
		data = addDelimiter(data,',','b',data[match.start():match.end()+1])	
	
	return data

'''
Re-arranges nested list to become a 1-level list

Descript column, item 1 in array, is a nested list
items are moved one level up to become a single list
and not a list of list.

Returns a list

 -- PARAMETERS --
 
 data: list
'''
def addNewColumns(data):
	newR = list()
	for R in range(len(data)):
		if R == 1:
			for subr in data[R].split(","):
				newR.append(subr)
		else:
			newR.append(data[R])
	return newR

'''
Takes charge of initializing clean up data
process.

Returns the 'idea' of a clean dataFrame

 -- PARAMETERS --

 srcF:	path of raw file to clean up
'''
def cleanData(srcF):
	dataframe = list()

	with open(srcF,'r') as src:
		for line in src:
			line = line.lower()
			rg = DescriptionColumn_Range(line)
			row = deleteInSubString(line, rg[0], rg[1])
			row = deleteInSubString(row, rg[0], rg[1], ';')
			row = row.replace('"',"").split(',')
			
			
			row[1] = clean_Description_Column(row[1])
			
			row[3]=deleteInSubString(row[3],0,len(row[3]),"\n")
			
			
			dataframe.append(addNewColumns(row))


	return dataframe
	

#Save to CSV file
def saveToFile(data, trgFile):
	with open(trgFile, 'w') as trg:
		write = csv.writer(trg)
		write.writerows(data)


if __name__ == "__main__":

	sourceFile = "/home/delphinus/Devlp/WalletAnalysis/app/data/raw/stmt.csv"
	targetFile = "/home/delphinus/Devlp/WalletAnalysis/app/data/modify/modf.csv"

	dataFrame = cleanData(sourceFile)
	saveToFile(dataFrame, targetFile)
