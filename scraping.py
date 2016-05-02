from bs4 import BeautifulSoup
import csv
import webbrowser
import urllib
import re

def scrapeapage(url):
	opener=urllib.FancyURLopener({})
	openerFile = opener.open(url)
	htmlFile = openerFile.read()
	return htmlFile

def wsjrtrep():
	mainpage=scrapeapage("http://blogs.wsj.com/chinarealtime/")
	soup = BeautifulSoup(mainpage,"html.parser")
	links=soup.find_all("h4","headline")
	linkreg=re.compile(r'"http:\/\/blogs.wsj.com\/.*"')
	linklist=[]
	for i,l in enumerate(links): 
		links[i]=linkreg.search(str(links[i]))
		if(links[i]!=None):
			linklist.append(links[i].group()[1:-1])
	return linklist #list of the links of the headliners

wsjrtrep()