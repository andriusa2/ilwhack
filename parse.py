#!/usr/bin/python



# simple XML parser for data feeds
import xml.etree.ElementTree as ET

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


def parse_file( filename ):
	tree = ET.parse( filename )

	# for all entries
	for entry in tree.getroot().iter("entry") :
		items.append( dict() )

		# add all fields to a dict
		for field in entry.iter("field") :
			items[-1][field.get("name")] = unicode(field.text)
		
		# I don't use this text anywhere, so lets keep it simple
		items[-1]["Activities"] = items[-1]["Activities"].lower()

		# try to add all tags (separated by newlines in activities)
		for tag in items[-1]["Activities"].split('\n') :
			# sometimes they try to name few activities
			for t in tag.split(',') :
				t = t.strip()
				if (t not in tags):
					tags.add(t)

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

parse_file("tmp.xml")
make_assoc()

