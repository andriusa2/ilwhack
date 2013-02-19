#!/usr/bin/python



# simple XML parser for data feeds
import xml.etree.ElementTree as ET

import urllib2 as URL
# http://www.edinburgh.gov.uk/api/directories/25/entries.xml?api_key=de14fcd88efece2cf0bf335df1004f54&per_page=100&page=1

#useful ids (http://www.edinburgh.gov.uk/directories)
#25 - sports/recreation
#105 - day services and lunch clubs
#11 - museums and galleries
#35 - outdoor education providers
#24 - community centres?
#110 - monuments in parks...
#noxml:http://www.edinburgh.gov.uk/directory_record/221327/youth_work_opportunities_in_edinburgh

# tag set, used for initial tag cloud creation
tags = set()

# tags associated with unique ids
assoc_tags = dict()

# items (dicts attrib=>val)
items = []

# relations, tuples: (tagID, itemID)
rels = []

MAX_TAG_LEN = 25


#DEBUG:
keysID = []
#
# TODO consider "deleting" a word from tag
#      instead of marking whole tag as invalid
#

def clean_tags() :
	print "sz before: ", len(tags)
	del_list = []
	# should make this moar optimal
	for sTag in tags :
		for lTag in tags :
			if len(sTag) < len(lTag) :
				if (sTag in lTag) :
					del_list.append(lTag)

	# delete too long or improper tags
	for tag in tags:
		if (len(tag) > MAX_TAG_LEN):
			print "Tag rejected for its length: " + tag
		elif ":" in tag :
			print "Tag rejected for having : in itself: " + tag
		else:
			continue;
		del_list.append(tag)
	
	# delete all rejects
	for i in del_list :
		if (i in tags) :
			tags.remove(i)

	print "sz after: ", len(tags)


def parse_file( filename, dbg = False ):
	tree = ET.parse( filename )

	# for all entries
	for entry in tree.getroot().iter("entry") :
		items.append( dict() )

		# add all fields to a dict
		for field in entry.iter("field") :
			items[-1][field.get("name")] = unicode(field.text)
		# I don't use this text anywhere, so lets keep it simple
		if "Activities" not in items[-1].keys():
			break
		items[-1]["Activities"] = items[-1]["Activities"].lower()
		t = items[-1]["Location"].split(',')
		if (" " not in items[-1]["Location"] and len(t) == 2) :
			items[-1]["Location"] = str(float(t[0]))[0:9] + "," + str(float(t[1]))[0:9]
		else:
			items[-1]["Location"] = ""
		if items[-1]["Location"] == "" :
			print "WARNING: ", items[-1]["Name"], " doesn't have location coords"
			print "Falling back to Address/postcode lookup/gMaps API"
			#TODO lat/long extraction
			print "WARNING: No location data, deleting record for ", items[-1]["Name"]
			del items[-1]
			continue
		# try to add all tags (separated by newlines in activities)
		for tag in items[-1]["Activities"].split('\n') :
			# sometimes they try to name few activities
			for t in tag.split(',') :
				t = t.strip()
				if (len(t) < 3):
					continue
				if (t not in tags):
					tags.add(t)
	if dbg:
		keysID.append(items[-1].keys())
	# remove too long/complex tags
	clean_tags()

# creates associated list of (tag, item) pairs
# 
# TODO this should be called every time `tags` set is changed
#      maybe ditch the neat `in`?
def make_assoc():
	i = 0
	assoc_tags.clear()
	# create dict of tag=>id
	for tag in sorted(list(tags)) :
		assoc_tags[tag] = i
		i += 1
	# create all relations for tagID=>itemID
	# lets keep it sorted
	for tag in sorted(assoc_tags.keys(), key=lambda t : assoc_tags[t]) :
		for i in range(len(items)) :
			if (tag in items[i]["Activities"]) :
				rels.append( (assoc_tags[tag], i) )


# testing method
def get_items( tag ):
	if (tag not in assoc_tags.keys()) :
		return ["N/A"]

	retval = []
	tagID = assoc_tags[tag]
	# we have build relation table
	# such that it is sorted by tagID (asc)
	# binary search would be useful here, but meh
	for (tID, iID) in rels :
		if (tagID < tID): break
		if (tagID == tID):
			retval.append(items[iID])
	return retval

# testing method
def out_tags():
	print "TagID\tTag"
	for tag in sorted(list(tags)):
		print assoc_tags[tag], "\t", tag

# testing method
def print_items( items ) :
	# if it isn't a list nor a list of dicts
	# return empty output
	if (type(items) != list) or \
		not ( (len(items) > 0) and \
					(type(items[0]) == dict) ) :
		print "N/A"
		return
	# otw, print those suckers out
	for item in items:
		print "* ", item["Name"]

# TODO pagination
def parseXML_URL( url, dbg = False ):
	u = URL.urlopen(url)
	parse_file( u, dbg )

def parse_edi_gov( dirID ):
	s = "http://www.edinburgh.gov.uk/api/directories/%d/entries.xml?api_key=de14fcd88efece2cf0bf335df1004f54&per_page=100&page=1" % (dirID,)
	print "Parsing XML from url at (",s,")"
	parseXML_URL( s, True)
# parse_file("tmp.xml")
#useful ids (http://www.edinburgh.gov.uk/directories)
#25 - sports/recreation
#105 - day services and lunch clubs
#11 - museums and galleries
#35 - outdoor education providers
#24 - community centres?
#110 - monuments in parks...

# parse_edi_gov( 25 )
# parse_edi_gov( 35 )
# parse_edi_gov( 105 )
# make_assoc()

import mysql_test

