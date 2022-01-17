import csv

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


def cleanData(srcF):
	dataframe = list()

	with open(srcF,'r') as src:
		for line in src:
			rg = DescriptionColumn_Range(line)
			row = deleteInSubString(line, rg[0], rg[1])
			row = deleteInSubString(row, rg[0], rg[1], ';')
			row = row.replace('"',"").split(',')
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
