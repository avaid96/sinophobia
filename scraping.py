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
	print "Url: ", link
	print "\n"
	print "Sentiment: ", sentiment
	print "\n"
	c.writerow([today,link,author,sentiment['docSentiment']['type'],sentiment['docSentiment']['score']])

def scrapenp(page,tag,iden,reg):
	mainpage=scrapeapage(page)
	soup = BeautifulSoup(mainpage,"html.parser")
	links=soup.find_all(tag,iden)
	# links=links[0:9]
	linkreg=re.compile(reg)
	linklist=[]
	for i,l in enumerate(links): 
		links[i]=linkreg.search(str(links[i]))
		if(links[i]!=None):
			linklist.append(links[i].group()[1:-1])
	if page=="http://www.nytimes.com/topic/destination/china":
		linklist=linklist[:len(linklist)/2]
	print linklist #list of the links of the headlines
	for link in linklist:
		if page=="http://edition.cnn.com/china":
			if link.startswith("/2016"):
				link="http://edition.cnn.com"+link
		getsent(link)

c=csv.writer(open("SentimentOp.csv","a"),lineterminator='\n')
c.writerow(["Date","URL","Author","Sentiment Type","Sentiment score"])
today=date.today()
nytch=("http://www.nytimes.com/topic/destination/china","a","story-link",r'"http:\/\/www.nytimes.com\/(?!slideshow)(?!video)[^"]*"')
nytsin=("http://www.nytimes.com/column/sinosphere","a","story-link",r'"http:\/\/www.nytimes.com\/(?!slideshow)(?!video)[^"]*"')
#issue reading a wsj.com article because of subscription- http://www.wsj.com/news/world/china
wsrr=("http://blogs.wsj.com/chinarealtime/","h4","headline",r'"http:\/\/blogs.wsj.com\/.*"')
wpapac=("https://www.washingtonpost.com/world/asia-pacific/","div","story-headline",r'"https:\/\/www.washingtonpost.com\/.*(china|chinese|beijing|shanghai|sinosphere)[^"]*"')
cnnchheadline=("http://edition.cnn.com/china","h3","cd__headline",r'"\/2016\/[^"]*"|"http:\/\/[a-z]*.cnn.com\/[^"]*"')
#now do the guardian
sites=[nytch,nytsin,wsrr,wpapac,cnnchheadline]
sites=[sites[-1]]
for site in sites:
	c.writerow([site[0]])
	scrapenp(site[0],site[1],site[2],site[3])

