# -*- coding: UTF-8 -*-
#Paolo Tamagnini - 1536242
import requests, time
import bs4
from bs4 import BeautifulSoup
import csv
import os

BASE_URL = 'http://www.kijiji.it/case/vendita/roma-annunci-roma/'

def addAdsProPlus(url):

	r = requests.get(url)
	content = r.content
	soup = BeautifulSoup(content)
	listarigatab = []

	results = soup.find_all(class_='cta')
	for res in results:

		rigatab = []

		rigatab.append(res.attrs['href'].encode("UTF-8"))
		for ch in res.descendants:
			if(isinstance(ch,bs4.element.Tag) and ch.attrs.has_key("class")):
				if(['title'] in ch.attrs.values()):
					rigatab.append(next(ch.children).encode("UTF-8"))
				if(['description'] in ch.attrs.values()):
					rigatab.append(next(ch.children).encode("UTF-8"))
				if(['locale'] in ch.attrs.values()):
					rigatab.append(next(ch.children).encode("UTF-8"))
				if(['price'] in ch.attrs.values()):
					rigatab.append(next(ch.children).encode("UTF-8"))

		Url = rigatab[0]
		Tit = rigatab[1]
		Desc = rigatab[2]
		Loc = rigatab[3]
		if len(rigatab) == 5:
			Pri = rigatab[4]
		else:
			rigatab.append(u'the price is missing')
		rigatab[0] = Tit
		rigatab[1] = Loc
		rigatab[2] = Pri
		rigatab[3] = Url
		rigatab[4] = Desc
		listarigatab.append(rigatab)
		
	return listarigatab
	
def processAllPages(baseURL, minPage=1, maxPage=1, delay=2,):

    
    z = 1
    count = 1
    check = 1
    if not os.path.isdir('documents'):
        os.makedirs('documents')
    if not os.path.isdir('documents/documents-' + str(check).zfill(6) + '-' + str(check + 499).zfill(6)):
        os.makedirs('documents/documents-' + str(check).zfill(6) + '-' + str(check + 499).zfill(6))
    for i in range(minPage, maxPage+1):
        print "Processing page: " + str(i)
        listofonepage = addAdsProPlus(BASE_URL + "?p=" + str(i))
        
        for j in range(0,len(listofonepage)):
            if count == 501:
                count = 1
                check = check + 500
                if not os.path.isdir('documents/documents-' + str(check).zfill(6) + '-' + str(check + 499).zfill(6)):
                    os.makedirs('documents/documents-' + str(check).zfill(6) + '-' + str(check + 499).zfill(6))
            file = open('documents/documents-' + str(check).zfill(6) + '-' + str(check + 499).zfill(6) + '/document-' + str(z).zfill(6), 'w')
            writer = csv.writer(file, delimiter='\t')
            z = z + 1
            count = count + 1

            writer.writerow(listofonepage[j])
            file.close()
            
        time.sleep(delay)
print "the script will create ads from the website:"
print BASE_URL
print "from the page 1 to page N (the max N is 1999)"
n = int(raw_input("please insert the N value:"))		
processAllPages(BASE_URL, 1, n)