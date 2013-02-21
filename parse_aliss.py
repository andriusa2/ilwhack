#!/usr/bin/python

import json
import urllib2 as URL

#import requests
#import timeit
url = "http://www.aliss.org/api/resources/search/?location=edinburgh&query=%s&max=%d"

nontagChars = "\n\r\t _-&%().,/?\\[]"
def remChars(s, chs) :
	for c in chs:
		s = s.replace(c, '')
	return s
def getObjectsByTag( tag, maxR = 15 ) :
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
			i[key] = unicode(i[key])
	return items
def fixKeys( items ) :
	if items == None or len(items) == 0:
		return items
	if "locations" not in items[0].keys() : 
		return items
	for i in items:
		i["locations"] = ",".join(
			[ j[0:9] for j in i["locations"].split(", ") ] )
		i["tags"] = remChars("".join(i["tags"]),nontagChars)
		i["description"] = i["description"]#.encode("utf-8")
	return items

def fixItems( items ) :
	return fixKeys( fixLists( items ) )
# conversion: dict of originalTag => itemTag
# if some tag not in conversion.keys() -> skip tag
def getItems( tag ) :
	objs = smartGet( tag )
	return fixItems(objs)

def removeDuplicates( items ) :
	# we have aliss id for these things
	# yaysoeasy
	items.sort(key = lambda i : i["id"] )
	delList = []
	for i, val in enumerate(items[:-1]) :
		if (items[i+1]["id"] == val["id"]) :
			delList.append(i+1)
	for i in reversed(delList) :
		del items[i]
	return items
# [u'description', u'title', u'locationnames', u'tags', u'locations', u'uri', u'score', u'accounts', u'id']
