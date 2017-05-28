# -*- coding: UTF-8 -*-
#Paolo Tamagnini - 1536242
import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt
import string
import codecs
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import collections
import os
stemmer = SnowballStemmer("italian")

simb = ',.<>/?;:"[]{}|=+-_()*^#!~\\'
simb = simb.encode("UTF-8")

term = []
docID = []
print "the script will create the index for the files in the folder 'documents'"
print "it will use as input all the files from document1 to documentN"
n = int(raw_input("please insert the N value:"))
n_old = 63968
count = 1
check = 1
for i in range(1,n+1):
	if count == 501:
		count = 1
		check = check + 500
	path = 'documents/documents-' + str(check).zfill(6) + '-' + str(check + 499).zfill(6) + '/document-' + str(i).zfill(6)
	print path
	count = count + 1
	documentID = 'document' + str(i) 
	fileAd =  codecs.open(path, 'r', encoding='utf8')
	contentAd =  fileAd.read()
	contentAd = contentAd.split('\t')
	
	del contentAd[2]
	del contentAd[2]
	
	contentAd = ' '.join(contentAd)
	contentAd = contentAd.lower()
	contentAd = contentAd.replace(u"’", " ")
	contentAd = contentAd.replace(u"‘", " ")
	contentAd = contentAd.replace("'", " ")
	contentAd = contentAd.replace("\r", "")
	contentAd = contentAd.replace("\n", "")
	for u in list(simb):
		contentAd = contentAd.replace(u, " ")
	
	listInAd = contentAd.replace("\t", " ").split(" ")
	
	for w in listInAd:     
		if w not in stopwords.words('italian'):
			w = stemmer.stem(w)
			if w != "":
				term.append(w)
				docID.append(documentID)
                
	
	

termdoclist = zip(term, docID)

d = {}
for i,j in termdoclist:
    d.setdefault(i,[]).append(j)
for x in sorted(d):
    d[x] = sorted(list(set(d[x])))
	
d = collections.OrderedDict(sorted(d.items()))
if not os.path.isdir('index'):
	os.makedirs('index')
termID = range(1,len(d)+1)
file = open('index/vocabulary.txt', 'w')
writer = csv.writer(file, delimiter='\t')

o = 0
for x in d:
    rigaVoc = []
    rigaVoc.append(termID[o])
    o = o + 1
    rigaVoc.append(x.encode("UTF-8"))
    writer.writerow(rigaVoc)
file.close()

file = open('index/postings.txt', 'w')
writer = csv.writer(file, delimiter='\t')
o = 0
for x in d:
    rigaPost = []
    rigaPost.append(termID[o])
    o = o + 1
    for u in d[x]:
        rigaPost.append(u)
    writer.writerow(rigaPost)
file.close()