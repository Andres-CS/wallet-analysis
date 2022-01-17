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
			rg = DescriptionColumn_Range(line)
			row = deleteInSubString(line, rg[0], rg[1])
			row = deleteInSubString(row, rg[0], rg[1], ';')
			row = row.replace('"',"").split(',')
			
			#Replace data 00/00 for ,
			row[1] = re.sub("[0-9]{2}\/[0-9]{2}", ",", row[1])
			
			row[1] = row[1].replace("'","")

			#Add , after PURCHASE
			row[1] = addDelimiter(row[1],',','a',"PURCHASE")
			
			row[1] = addDelimiter(row[1],',','a',"WITHDRWL")

			row[1] = addDelimiter(row[1],',','b',"withdrawal")
			row[1] = addDelimiter(row[1],',','a',"withdrawal")
			
			row[1] = addDelimiter(row[1],',','b',"OVERDRAFT")
			row[1] = addDelimiter(row[1],',','a',"OVERDRAFT")

			row[1] = addDelimiter(row[1],',','b',"Check")
			row[1] = addDelimiter(row[1],',','a',"Check")

			row[1] = addDelimiter(row[1],',','b',"CHARGE")
			row[1] = addDelimiter(row[1],',','a',"CHARGE")
			

			row[1] = addDelimiter(row[1],',','b',"CHECK")
			row[1] = addDelimiter(row[1],',','a',"CHECK")

			row[1] = addDelimiter(row[1],',','b',"TAX")
			row[1] = addDelimiter(row[1],',','a',"TAX")
			

			row[1] = addDelimiter(row[1],',','b',"pymt")
			row[1] = addDelimiter(row[1],',','a',"pymt")

			row[1] = addDelimiter(row[1],',','b',"PAY")
			row[1] = addDelimiter(row[1],',','a',"PAY")

			row[1] = addDelimiter(row[1],',','b',"PMT")
			row[1] = addDelimiter(row[1],',','a',"PMT")

			row[1] = addDelimiter(row[1],',','a',"PMNT")

			row[1] = addDelimiter(row[1],',','b',"Payment")
			row[1] = addDelimiter(row[1],',','a',"Payment")

			row[1] = addDelimiter(row[1],',','b',"payment")
			row[1] = addDelimiter(row[1],',','a',"payment")

			row[1] = addDelimiter(row[1],',','b',"PAYMENT")
			row[1] = addDelimiter(row[1],',','a',"PAYMENT")
			

			row[1] = addDelimiter(row[1],',','b',"Fee")
			row[1] = addDelimiter(row[1],',','a',"Fee")

			row[1] = addDelimiter(row[1],',','b',"FEE")
			row[1] = addDelimiter(row[1],',','a',"FEE")

			row[1] = addDelimiter(row[1],',','b',"DEBITS")
			row[1] = addDelimiter(row[1],',','a',"DEBITS")

			row[1] = addDelimiter(row[1],',','b',"CREDITS")
			row[1] = addDelimiter(row[1],',','a',"CREDITS")

			row[1] = addDelimiter(row[1],',','b',"TRANSFER")
			row[1] = addDelimiter(row[1],',','a',"TRANSFER")
		
			row[1] = addDelimiter(row[1],',','b',"Transfer")
			row[1] = addDelimiter(row[1],',','a',"Transfer")

			row[1] = addDelimiter(row[1],',','b',"transfer")
			row[1] = addDelimiter(row[1],',','a',"transfer")

			row[1] = addDelimiter(row[1],',','b',"PAYROLL")
			row[1] = addDelimiter(row[1],',','a',"PAYROLL")

			row[1] = addDelimiter(row[1],',','b',"DEPOSIT")
			row[1] = addDelimiter(row[1],',','a',"DEPOSIT")

			row[1] = addDelimiter(row[1],',','b',"CONSUMER")
			row[1] = addDelimiter(row[1],',','a',"CONSUMER")
			
			
			row[1] = addDelimiter(row[1],',','b',"Funds")
			row[1] = addDelimiter(row[1],',','a',"Funds")
			

			row[1] = addDelimiter(row[1],',','a',"REFUND")
			

			if len(row[1].split(','))<3 or len(row[1].split(','))>3:
				print(row[1].split(','))
			
			row[3]=deleteInSubString(row[3],0,len(row[3]),"\n")
			dataframe.append(row)
	
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
