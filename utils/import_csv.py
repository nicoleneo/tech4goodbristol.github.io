import csv
import unicodedata
import re
import os

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    value = unicode(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    return re.sub('[-\s]+', '-', value)

def replaceKeyVal(inputStr, keyName, val):
	return inputStr.replace('{'+keyName+'}', val)


def writeMdFile(lineDict, dateStr):
	templatefile = 'shout-outs-template.md'
	file = open(templatefile, 'r') 
	contents = file.read()
	for key, value in lineDict.items():
		contents = replaceKeyVal(contents, key, value)
	print contents
	mdFileName = '../_shout_outs/'+dateStr+'/'+slugify(lineDict['organisation'])+'.md'
	print mdFileName

	newMdFile = open(mdFileName, 'w')
	newMdFile.write(contents)
	newMdFile.close()
	file.close()

csvFileName = '2017-03-23-T4GB-CSO.csv'
with open(csvFileName, 'rb') as csvfile:
	csvreader = csv.reader(csvfile, delimiter=',', quotechar='\\')
	for row in  csvreader:
		data = {}
		data['organisation'] = row[0]
		data['main_contact'] = row[1]
		data['contact_details'] = row[2]
		data['description'] = row[3]
		data['action_requested'] = row[4]
		match = re.search(r'\d{4}-\d{2}-\d{2}', csvFileName)
		dateStr = match.group()
		shout_outs_folder = '../_shout_outs/'+dateStr
		if not os.access(shout_outs_folder, os.F_OK):
			os.mkdir(shout_outs_folder)
		writeMdFile(data, dateStr)