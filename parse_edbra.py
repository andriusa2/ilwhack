#!/usr/bin/python



# simple XML parser for data feeds
import xml.etree.ElementTree as ET
import urllib2 as URL

import mysql_test as SQL

tagsSet = set()
# tag set, used for initial tag cloud creation
tagsList = []

# tags associated with unique ids
assoc_tags = dict()

# items (dicts attrib=>val)
items = []

# relations, tuples: (tagID, itemID)
rels = []

MAX_TAG_LEN = 25
MIN_AVG_LEN = 5

#DEBUG:
keysID = []
#
# TODO consider "deleting" a word from tag
#      instead of marking whole tag as invalid
#

badWords = [")", " etc", "including", "e.g."]
noiseChars = [" & ", " x ", " / ", "on "]

defaultKeys =  {'Activities' : ('Activities','TEXT'),
				'Name' : ('Name','TINYTEXT'),
				'Timetables' : ('TimeTables','TINYTEXT'),
				'Telephone' : ('Telephone','TINYTEXT'),
				'More information' : ('Details','TINYTEXT'),
				'Address' : ('Address','TINYTEXT'),
				'Prices' : ('Prices','TINYTEXT'),
				'Email' : ('Email','TINYTEXT'),
				'Location' : ('Location','TINYTEXT')}

# replace works on only one char
# translate does not delete on unicode strings
# yay...
def remChars(s, chs) :
	for c in chs:
		s = s.replace(c, '')
	return s

def remBad(s, bads) :
	for bad in bads:
		s = s.replace(bad, '')
	return s.strip()

def avgWordLen(s) :
	return len(s)/(s.count(" ") + 1)

def clean_tags() :
	global tagsList
	print "Tag cleanup started"
	print "Amount of tags before the purge: ", len(tagsList)
	del_list = []

	# removing "bad" words
	tagsList = [remBad(tag, badWords) for tag in tagsList]

	# sanity check for some random cases (e.g. and much more)
	for tag in tagsList :
		ttag = remBad(tag, noiseChars)
		if (ttag.count(" ") > 1 and avgWordLen(ttag) < MIN_AVG_LEN) :
			print "DBG: Removing tag `", tag, "`, assuming worthless for avglen"
			del_list.append(tagsList.index(tag))
	
	# creating tag-comparison-friendly tags (no punctuation, whitespace,etc)
	tags = [remChars(tag, "-().[];'\"?\t\r ") for tag in tagsList]

	for sTag in tags :
		if len(sTag) < 3 : # too short tag, something's wrong
			continue
		for lTag in tags :
			if sTag is lTag :
				continue
			if len(sTag) <= len(lTag) :
				if (sTag in lTag) :
					# TODO: check word ratios before deleting tag
					#       favour the tag with more hits
					del_list.append(tags.index(lTag))
					tags[tags.index(lTag)] = " "
					continue
	# delete all deemed tags from the end of the list
	# so we don't screw up the indexes
	for i in sorted(del_list, reverse=True) :
		del tagsList[i]

	tagsList.sort( key=len )
	# delete too long tags TODO: split them up on read
	br = 0
	while (br < len(tagsList) ) :
		if (len(tagsList[br]) > MAX_TAG_LEN):
			break;
		br += 1
	if (br < len(tagsList)) :
		del tagsList[br:]
	
	print "Amount of tags after the purge: ", len(tagsList)


def parse_file( filename, dbg = False, defaultTags = "" ):
	global tagsList
	tree = ET.parse( filename )
	# for all entries
	for entry in tree.getroot().iter("entry") :
		items.append( dict() )

		# add all fields to a dict
		# blah, unicode causes moar problems than it's worth
		for field in entry.iter("field") :
			items[-1][field.get("name")] = unicode(field.text)
		if "Name" not in items[-1].keys() :
			items[-1]["Name"] = unicode(entry.find("title").text)
		for field in defaultKeys :
			if field not in items[-1] or items[-1][field] == None:
				items[-1][field] = ""
		if "Postcode" not in items[-1] :
			items[-1]["Postcode"] = ""
		if "Location map" in items[-1] :
			items[-1]["Location"] = items[-1]["Location map"]
		if items[-1]['Timetables'] == "" and 'Opening hours' in items[-1].keys() :
			items[-1]['Timetables'] = items[-1]['Opening hours']

		items[-1]['Address'] = " ".join([items[-1]['Address'], items[-1]['Postcode']])

		items[-1]["Tags"] = items[-1]["Activities"].lower()
		items[-1]["Tags"].join(defaultTags)

		t = items[-1]["Location"].split(',')
		# good enough
		if (len(t) == 2 and " " not in items[-1]["Location"]) :
			items[-1]["Location"] = str(float(t[0]))[0:9] + "," + str(float(t[1]))[0:9]
		else:
			items[-1]["Location"] = None

		if items[-1]["Location"] == None :
			print "WARNING: No location data, deleting record for ", items[-1]["Name"]
			del items[-1]
			continue
		# try to add all tags (separated by newlines in activities)
		for tag in items[-1]["Tags"].splitlines() :
			# sometimes they try to name few activities
			for t in tag.split(',') :
				t = t.strip()
				if (":" in t):
					t = t[t.index(":")+1 : ]
					t = t.strip()
				if ("(" in t):
					tmp = [i.strip().strip(")") for i in t.split("(")]
					[tagsSet.add(d) for d in tmp if (len(d)>=3) and (d not in tagsSet)]
					continue
				if (len(t) < 3):
					continue
				if (t not in tagsSet):
					tagsSet.add(t)
	if dbg:
		keysID.append(items[-1].keys())
	tagsList = list(tagsSet)
# creates associated list of (tag, item) pairs
# 
# TODO this should be called every time `tags` set is changed
#      maybe ditch the neat `in`?
def make_assoc():
	i = 0
	global rels
	# remove too long/complex tags
	clean_tags()

	assoc_tags.clear()
	del rels
	rels = []
	# create dict of tag=>id
	for tag in sorted(tagsList) :
		assoc_tags[tag] = i + 1
		i += 1
	# create all relations for tagID=>itemID
	# lets keep it sorted
	for tag in sorted(assoc_tags.keys(), key=lambda t : assoc_tags[t]) :
		for i in range(len(items)) :
			if (tag in items[i]["Tags"]) :
				rels.append( (assoc_tags[tag], i + 1) )


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
			retval.append(items[iID-1])
	return retval

# testing method
def out_tags():
	print "TagID\tTag"
	for tag in sorted(tagsList):
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
def parseXML_URL( url, dbg = False, defaultTags = "" ):
	u = URL.urlopen(url)
	parse_file( u, dbg, defaultTags )

def parse_edi_gov( dirID, defaultTags = "" ):
	s = "http://www.edinburgh.gov.uk/api/directories/%d/entries.xml?api_key=de14fcd88efece2cf0bf335df1004f54&per_page=100&page=1" % (dirID,)
	print "Parsing XML from url at (",s,")"
	parseXML_URL( s, True, defaultTags )



# parse_file("tmp.xml")
#useful ids (http://www.edinburgh.gov.uk/directories)
#25 - sports/recreation
#105 - day services and lunch clubs
#11 - museums and galleries
#35 - outdoor education providers
#24 - community centres?
#110 - monuments in parks...

parse_edi_gov( 25, "\nSport\nRecreation" )
parse_edi_gov( 35 )
parse_edi_gov( 110, "\nMonuments\nSightseeing" )
inp = raw_input("Do you want to dump the data to database (recreates all the tables)?(Yn)")
inp = inp.lower()
if (inp == "y"):
	dumpToDB()
elif (inp == "n"):
	print "Okay..."
else:
	print "'Maybe' means 'No'!"
# parse_edi_gov( 105 )
# make_assoc()
