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
def fixLists( items ) :
	for i in items:
		for key in i.keys():
			if (type(i[key]) is list) :
				i[key] = i[key][0]
	return items
def fixLocation( items ) :
	if items == None :
		return items
	if "Location" not in items[0].keys() : 
		return items
	for i in items:
		i["Location"] = ",".join(
			[ j[0:9] for j in i["Location"].split(", ") ] )
	return items

def fixItems( items ) :
	return fixLocation( fixLists( items ) )
# conversion: dict of originalTag => itemTag
# if some tag not in conversion.keys() -> skip tag
def getItems( tag, conversion ) :
	objs = smartGet( tag )
	items = []
	for obj in objs :
		items.append(
		{ val : obj[key] for key, val in conversion.items() }
		)
	return items



# [u'description', u'title', u'locationnames', u'tags', u'locations', u'uri', u'score', u'accounts', u'id']
