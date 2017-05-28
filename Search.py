# -*- coding: UTF-8 -*-
#Paolo Tamagnini - 1536242
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import pandas as pd
import csv
import numpy as np

def makeIntegerList(l1):
    for i in range(0,len(l1)):
        l1[i] = int(l1[i].replace('document',''))
		
def myIntersection(lista1, lista2):
    result = []
    i = 0
    j = 0
    while(i != len(lista1) and j != len(lista2)):
        if lista1[i] == lista2[j]:
            result.append(lista1[i])
            i = i + 1
            j = j + 1
        elif lista1[i] < lista2[j]:
            i = i + 1
        elif lista1[i] > lista2[j]:
            j = j + 1
    return result

def myIntDocQuery(docx):
    for i in docx:
        makeIntegerList(i)
    while len(docx)!=1:
        docx[0] = myIntersection(docx[0], docx[1])
        del docx[1]
    return docx[0]
	
stemmer = SnowballStemmer("italian")
while True:
	try:
		queryPure = raw_input("please write here your query:")
		query = queryPure.encode("UTF-8")
		break
	except UnicodeDecodeError:
		print "Oops! That was no valid query."
		print "Try again.. maybe without weird symbols this time!"

simb = u',.<>/?;:"’[]{}|=+-_()*^!‘~\\'
query = query.lower()
query = query.replace("'", " ")
query = query.replace("\r", "")
query = query.replace("\n", "")
for u in list(simb):
    query = query.replace(u, " ")
listQuery = query.replace("\t", " ").split(" ")
termQuery = []
for w in listQuery:
    if w not in stopwords.words('italian'):
        w = stemmer.stem(w)
        if w != "": 
            termQuery.append(w)



voc = pd.read_csv(
    "index/vocabulary.txt",
    delimiter = '\t',
    names     = ['termnumber ', 'term'],
    encoding = 'utf-8')

t = voc['term']
numberQuery = []
sortedTermQuery = []
for i in range(0,len(t)):
    if voc['term'][i] in termQuery:
        
        sortedTermQuery.append(voc['term'][i])
        numberQuery.append(str(i+1))

docQuery = []
with open('index/postings.txt', 'r') as csvfile:
    f = csv.reader(csvfile, delimiter='\t')
    for row in f:
        
        if row[0] in numberQuery:
            
            docTerm = []
            for i in range(1,len(row)):
                docTerm.append(row[i])
            
            docQuery.append(docTerm)
			
if len(docQuery) == 0:
	result = []
elif len(docQuery) == 1:
	makeIntegerList(docQuery[0])
	result = docQuery[0]
else:
	result = myIntDocQuery(docQuery)
#print result

if not result:
	print 'Your search -', queryPure, '- did not match any documents.'

for r in result:
	control = r/500.0
	if control.is_integer():
		check1 = int(control*500 - 499)
		check2 = int(control*500)
	else:
		check1 = int(np.floor(control)*500+1)
		check2 = int(np.ceil(control)*500)
	path = 'documents/documents-' + str(check1).zfill(6) + '-' + str(check2).zfill(6) + '/document-' + str(r).zfill(6)
	
	with open(path, 'r') as csvfile:
		f = csv.reader(csvfile, delimiter='\t')
		for row in f:
			print 'TITLE:'
			print row[0]
			print 'LOCATION:'
			print row[1]
			print 'PRICE:'
			print row[2]
			print 'URL:'
			print row[3]
			print '--------------------------------------------------------'
print 'You have found', len(result), 'ads!'
			
