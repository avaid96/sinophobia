from bs4 import BeautifulSoup
import csv
import webbrowser
import urllib
import re
from alchemyapi import AlchemyAPI
import csv
from datetime import date
import requests
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
		if page=="http://www.chinadaily.com.cn/china/index.html":
			if link.startswith("2016"):
				link="http://www.chinadaily.com.cn/china/"+link
			if link.startswith("../"):
				link="http://www.chinadaily.com.cn/"
		getsent(link)

#scrape the two forbes pages using xml response from http://www.forbes.com/sites/wadeshepard/feed/ and then scrape individual articles using
#print requests.get(url, headers={"referer": url.replace("print/", "")}).content
#then toss this into alchemy
def forbesxml(author):
	url="http://www.forbes.com/sites/"+author+"/feed/"
	artpage=scrapeapage(url)
	soup=BeautifulSoup(artpage,"xml")
	links=soup.find_all("link")
	linkreg=re.compile(r'http:\/\/www.forbes.com\/[^<]*')
	linklist=[]
	links=links[2:]
	for i,l in enumerate(links): 
		links[i]=linkreg.search(str(links[i]))
		if(links[i]!=None):
			linklist.append(links[i].group())
	print linklist
	print "got linklist now get text and run sentiment on it"
	for link in linklist:
		link=link+"print/"
		print requests.get(link, headers={"referer": link.replace("print/", "")}).content
		# got html of each article now go ahead and get the article text
		break

def main():
	c=csv.writer(open("SentimentOp.csv","a"),lineterminator='\n')
	c.writerow(["Date","URL","Author","Sentiment Type","Sentiment score"])
	today=date.today()
	nytch=("http://www.nytimes.com/topic/destination/china","a","story-link",r'"http:\/\/www.nytimes.com\/(?!slideshow)(?!video)[^"]*"')
	nytsin=("http://www.nytimes.com/column/sinosphere","a","story-link",r'"http:\/\/www.nytimes.com\/(?!slideshow)(?!video)[^"]*"')
	#issue reading a wsj.com article because of subscription- http://www.wsj.com/news/world/china
	wsrr=("http://blogs.wsj.com/chinarealtime/","h4","headline",r'"http:\/\/blogs.wsj.com\/.*"')
	wpapac=("https://www.washingtonpost.com/world/asia-pacific/","div","story-headline",r'"https:\/\/www.washingtonpost.com\/.*(china|chinese|beijing|shanghai|sinosphere)[^"]*"')
	cnnch=("http://edition.cnn.com/china","h3","cd__headline",r'"\/2016\/[^"]*"|"http:\/\/[a-z]*.cnn.com\/[^"]*"')
	guardch=("http://www.theguardian.com/world/china","div", "fc-item__container", r'"http:\/\/www.theguardian.com\/[^"#]*"|"https:\/\/www.theguardian.com\/[^"#]*"')
	#issue reading a foreignpolicy article because of subscription- http://foreignpolicy.com/
	#understand epoch's dirty html
	chdailyheadlines=("http://www.chinadaily.com.cn/china/index.html","div","tw_box6 busNews",r'"\d\d\d\d-\d\d\/\d\d\/[^"]*"')
	chdailysubs=("http://www.chinadaily.com.cn/china/index.html","ul","busLis3",r'"\d\d\d\d-\d\d\/\d\d\/[^"]*"')
	sites=[nytch,nytsin,wsrr,wpapac,cnnch,guardch,chdailyheadlines,chdailysubs]
	for site in sites:
		c.writerow([site[0]])
		scrapenp(site[0],site[1],site[2],site[3])




