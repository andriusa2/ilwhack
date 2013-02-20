#!/usr/bin/python

import json
import urllib2 as URL

url = "http://www.aliss.org/api/resources/search/?location=edinburgh&query=%s&max=%d"

def getObjectsByTag( tag, maxR = 100 ) :
	tag = URL.quote( tag )
	link = URL.urlopen( url % (tag, maxR) )
	return json.load(link)["data"][0]["results"]

def filterObjectsByScore( objs, score = 5.0 ) :
	return [item for item in objs if item["score"] >= score]

def smartGet( tag, th = 5.0 ) :
	return filterObjectsByScore( getObjectsByTag( tag ), th )
	
def getItems( tag, defaultKeys ) :
	objs = smartGet( tag )
	
