from bs4 import BeautifulSoup
import csv
import webbrowser
import urllib
import re
from alchemyapi import AlchemyAPI
import csv
from datetime import date
alchemyapi=AlchemyAPI()

def scrapeapage(url):
	opener=urllib.FancyURLopener({})
	openerFile = opener.open(url)
	htmlFile = openerFile.read()
	return htmlFile

def getsent(link):
	myText = alchemyapi.text("url",link)
	author = alchemyapi.author("url",link)
	author= author['author'].encode('utf-8')
	myText=myText['text'].encode('utf-8')
	sentiment = alchemyapi.sentiment("text", myText)
	print "Author: ", author
	print "\n"
	print "Url: ", link
	print "\n"
	print "Sentiment: ", sentiment
	c.writerow([today,link,author,sentiment['docSentiment']['type'],sentiment['docSentiment']['score']])

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
	print linklist #list of the links of the headliners
	for link in linklist:
		getsent(link)

c=csv.writer(open("SentimentOp.csv","a"),lineterminator='\n')
c.writerow(["Date","URL","Author","Sentiment Type","Sentiment score"])
today=date.today()
wsjrtrep()
