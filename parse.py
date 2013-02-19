#!/usr/bin/python



# simple XML parser for data feeds
import xml.etree.ElementTree as ET

# http://www.edinburgh.gov.uk/api/directories/25/entries.xml?api_key=de14fcd88efece2cf0bf335df1004f54&per_page=100&page=1
tags = dict()
items = []

MAX_TAG_LEN = 25

def clean_tags() :
	tmp_keys = sorted(tags.keys(), key=lambda s : len(s))
	print "sz before: ", len(tags.keys())
# should make this moar optimal
	for sTag in tmp_keys :
		for lTag in tmp_keys :
			if len(sTag) < len(lTag) :
				if (lTag in tags.keys()) and (sTag in lTag) :
					tags[sTag] += tags[lTag]
					del tags[lTag]
					del lTag
					
	for tag in tags.keys():
		if (len(tag) > MAX_TAG_LEN):
			print "Tag rejected for its length: " + tag
			del tags[tag]
		elif ":" in tag :
			print "Tag rejected for having : in itself: " + tag
			del tags[tag]
			
	print "sz after: ", len(tags.keys())


def parse_file( filename ):
	tree = ET.parse( filename )
# for all entries
	for entry in tree.getroot().iter("entry") :
		items.append( dict() )
# add all fields to a dict
		for field in entry.iter("field") :
			items[-1][field.get("name")] = unicode(field.text)
# try to add all tags (separated by newlines in activities)
		for tag in items[-1]["Activities"].split('\n') :
			for t in tag.split(',') :
				t = t.lower().strip()
# tag counting, blah blah blah
				if (t in tags.keys()):
					tags[t] += 1	
				else:
					tags[t] = 1
# remove too long tags/complex tags
	clean_tags()

parse_file("tmp.xml")
