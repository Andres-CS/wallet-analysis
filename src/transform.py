import csv
import re

'''
Delete char in substring of original string.

Used this function when, you want to delete 
a character in a substring but not in the
rest of the original string.

text: original string
start: start of subString
end: end of subString
char: char to delete, default is ','.

'''
def deleteInSubString(text, start, end, char=','):
	subText = text[start:(end+1)]
	commaPos = subText.find(char)
	if commaPos >= 0:
		subText = subText[:commaPos]+""+subText[commaPos+1:]
		text = text[:start]+subText+text[end+1:]
		return text
	return text


#Get range of first pair of quotes. 
def DescriptionColumn_Range(txt):
	count = 0
	pos=list()
	for i in range(len(txt)):
		if txt[i] == '"':
			pos.append(i)
			count += 1
		if count == 2:
			return pos

def addDelimiter(text,delimiter,flag,target):
	pos = text.find(target)
	if not pos == -1:
		if flag == "b":
			text = text[:pos]+delimiter+text[pos:]

		else:
			offset =  len(text[:pos])+len(target)
			text = text[:offset+1]+delimiter+text[offset+1:]

	return text 	



def cleanData(srcF):
	dataframe = list()

	with open(srcF,'r') as src:
		for line in src:
			line = line.lower()
			rg = DescriptionColumn_Range(line)
			row = deleteInSubString(line, rg[0], rg[1])
			row = deleteInSubString(row, rg[0], rg[1], ';')
			row = row.replace('"',"").split(',')
			
			#Replace data 00/00 for ,
			row[1] = re.sub("[0-9]{2}\/[0-9]{2}", ",", row[1])
			
			for i in ["'",",/20",",/21"]:
				row[1] = row[1].replace(i,"")

				#Add , after PURCHASE

			wordBank={
				'c':["CREDITS","check","Check","CHARGE","CONSUMER"],
				'd':["DEPOSIT","DEBITS"],
				'f':["Fee","FEE","Funds"],
				'o':["OVERDRAFT"],
				'p':["PURCHASE","PAY","pymt","PMT","PMNT","Payment","PAYMENT","payment","PAYROLL"],
				'r':["REFUND"],
				't':["TAX","Transfer","transfer","TRANSFER"],
				'w':["WITHDRWL","withdrawal"]
			}

			for k in wordBank:
				for i in wordBank[k]:
					if i in row[1]:
						print()
						print(row[1])
						row[1] = addDelimiter(row[1],",", "b" , i)
						row[1] = addDelimiter(row[1],",", "a" , i)
						print(row[1])
						print()

			
			
			row[3]=deleteInSubString(row[3],0,len(row[3]),"\n")
			
			#
			newR = list()
			for R in range(len(row)):
				if R == 1:
					for subr in row[R].split(","):
						newR.append(subr)
				else:
					newR.append(row[R])
			
			#print(str(len(newR))+" : ",end="")
			#print(newR)
			
			dataframe.append(newR)
	
	


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
	#saveToFile(dataFrame, targetFile)
