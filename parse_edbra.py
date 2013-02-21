#!/usr/bin/python
#
# NOT IMPLEMENTED:
# * Pagination (edbra is nice enough to have < 100 records)
# * Great Tag system

# PYTHON Y U NO DO import maketags (http://xkcd.com/353/)

# simple XML parser for data feeds
import xml.etree.ElementTree as ET
# SLOW AS HELL url fetcher
import urllib2 as URL

tagsSet = set()
# tag set, used for initial tag cloud creation
tagsList = []

# tags associated with unique ids
assoc_tags = dict()

# items (dicts attrib=>val)
items = []

# relations, tuples: (tagID, itemID)
rels = []

# magic numbahs
MAX_TAG_LEN = 25
MIN_AVG_LEN = 5

#DEBUG:
keysID = []
#
# TODO consider "deleting" a word from tag
#      instead of marking whole tag as invalid
#
apiKey = "de14fcd88efece2cf0bf335df1004f54"
badWords = [")", " etc", "including", "e.g.", "none"]
noiseChars = [" & ", " x ", " / ", "on "]
nontagChars = "\n\r\t _-&%().,/?\\[]"

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
	print "EDBRA: Tag cleanup started"
	print "EDBRA: Amount of tags before the purge: ", len(tagsList)
	del_list = []

	# removing "bad" words
	tagsList = [remBad(tag, badWords) for tag in tagsList if len(remBad(tag, badWords)) > 2]
	
	# sanity check for some random cases (e.g. and much more)
	for tag in tagsList :
		ttag = remBad(tag, noiseChars)
		if (ttag.count(" ") > 1 and avgWordLen(ttag) < MIN_AVG_LEN) :
			print "EDBRA: DBG: Removing tag `", tag, "`, assuming worthless for avglen"
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
	print "EDBRA: Amount of tags after the purge: ", len(tagsList)

def fixItem( item, title, defTags ) :
	# loads of fixes, can still be broken
	# by sensitive data
	# Y U SO INCONSISTENT???
	compKeys = ["Address", "Postcode", "Activities", "Timetables",
		"Email", "Telephone", "More information"]
	for k in compKeys :
		if k not in item:
			item[k] = ""
	if "Name" not in item :
		item["Name"] = title
	if "Location map" in item :
		item["Location"] = item["Location map"]
	if item['Timetables'] == "" and 'Opening hours' in item :
		item['Timetables'] = item['Opening hours']
	item['Address'] = " ".join([item['Address'], item['Postcode']])
	item["tags"] = item["Activities"].lower()
	item["tags"] += defTags
	for field in item.keys() :
		if item[field] == None or item[field] == u'None':
			item[field] = ""
		else:
			item[field] = item[field].strip()
	return item

def parse_file( filename, dbg = False, defaultTags = "" ):
	global tagsList
	global tagsSet
	global items
	tree = ET.parse( filename )
	# for all entries
	for entry in tree.getroot().iter("entry") :
		items.append( dict() )

		# add all fields to a dict
		for field in entry.iter("field") :
			items[-1][field.get("name")] = unicode(field.text)

		items[-1] = fixItem(items[-1], unicode(entry.find("title").text.strip()), defaultTags)
		items[-1]["origin"] = "EDBRA"
		t = items[-1]["Location"].split(',')
		# good enough
		if (len(t) == 2 and " " not in items[-1]["Location"]) :
			items[-1]["Location"] = str(float(t[0]))[0:9] + "," + str(float(t[1]))[0:9]
		else:
			items[-1]["Location"] = None

		if items[-1]["Location"] == None :
			print "EDBRA: WARNING: No location data, deleting record for ", items[-1]["Name"]
			del items[-1]
			continue

		# try to add all tags (separated by newlines in activities)
		for tag in items[-1]["tags"].splitlines() :
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
		items[-1]["tags"] = remChars(items[-1]["tags"], nontagChars)

	if dbg:
		keysID.append(items[-1].keys())
	tagsList = list(tagsSet)

def parseXML_URL( url, dbg = False, defaultTags = "" ):
	u = URL.urlopen(url)
	parse_file( u, dbg, defaultTags )

def parse_edi_gov( dirID, defaultTags = "" ):
	s = "http://www.edinburgh.gov.uk/api/directories/%s/entries.xml?api_key=%s&per_page=100&page=1"
	s = s % (dirID, apiKey)
#	print "EDBRA: DBG: Parsing XML from url (",s,")"
	parseXML_URL( s, False, defaultTags )


#useful ids (http://www.edinburgh.gov.uk/directories)
dataSources = {
		#11 : ("museums and galleries", "\nsightseeing"),
		25 : ("Sports/recreation facilities", "\nsport\nrecreation" ),
		35 : ("Outdoor education providers", "" ),
		#105 : ("day services and lunch clubs", "" ),
		110 : ("Monuments in parks/etc", "\nsightseeing" )
		}

def parse() :
	for num, (name, dTag) in dataSources.items() :
		print "EDBRA: fetching data of", name,"..."
		parse_edi_gov(num, dTag)

def getCleanTags() :
	clean_tags()
	return tagsList

def getItems() :
	return items
