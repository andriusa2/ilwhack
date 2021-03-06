#! /usr/bin/python
#
#ALISS keys:
# ['description', 'title', 'locationnames', 'tags', 'locations', 'uri', 'score', 'accounts', 'id']
# ['description', 'name',  'Address' (?),    None,  'Location',  'web',  None,    None,       None]
#

# not much TBH :/
alissTranslation = {
				'description' : 'Description',
				'title' : 'Name',
				'locationnames' : 'Address',
				'uri' : 'web',
				'tags' : 'tags',
				'locations' : 'Location',
				'origin' : 'origin'
				}
# there is more translation done inside edbra parser...
edbraTranslation = {
				'Activities' : 'Description',
				'Name' : 'Name',
				'Timetables' : 'Timetables',
				'More information' : 'web',
				'Address' : 'Address',
				'Location' : 'Location',
				'Email' : 'Email',
				'Telephone' : 'Phone',
				'tags' : 'tags',
				'origin' : 'origin'
				}


# keys for DB construction/insertation/stuff
dbKeys =  {'Description' : ('description','TEXT'),
			'shortName' : ('shortName','TINYTEXT'),
			'Name' : ('name','TINYTEXT'),
			#'Timetables' : ('Timetables','TINYTEXT'),
			'Phone' : ('phone','TINYTEXT'),
			'web' : ('web','TINYTEXT'), # not true somewhere, /care
			'Address' : ('address','TINYTEXT'),
			#'Prices' : ('Prices','TINYTEXT'),
			'Email' : ('email','TINYTEXT'),
			'Location' : ('location','TINYTEXT'),
			'origin' : ('origin','TINYTEXT')}
defaultKeys = {key : "" for key,_ in dbKeys.items()}
nontagChars = "\n\r\t _-&%().,/?\\[]"
def remChars(s, chs) :
	for c in chs:
		s = s.replace(c, '')
	return s

def translateItem( item, table ) :
	return { val : unicode(item[key]) for key, val in table.items() }

def translateItems( items, table ) :
	return [ translateItem( item, table) for item in items ]

def fillMissing( items, keys ) : #cba to use dictview
	return [item.update(
				{key:val for key, val in keys.items() \
						if key not in item.keys()}
			) for item in items]
def fixNames( items ) :
	return [item.update({"shortName":item["Name"].split("(")[0].strip()}) for item in items]

def rmDups( items ) :
	# removing items based on their location
	# that isn't great way to do it
	# but with current datasets it's precise enough
	if len(items) < 2 :
		return items
	sItems = sorted(items, key=lambda i : i["Location"])
	delList = []
	for i, val in enumerate(sItems[:-1]) :
		if (sItems[i+1]["Location"] == val["Location"]) :
			print "DBG: Found dup by loc:", val["Name"], "->", sItems[i+1]["Name"]
			delList.append(i+1)
	for i in reversed(delList) :
		del sItems[i]
	return sItems

def make_assoc( tags, items ) :
		# items should have prepared ["tags"] fields
		# i.e. only alphanums in them
		
		rels = []
		for tagID, tag in enumerate(tags, 1) :
			tagt = remChars(tag, nontagChars)
			rels.extend(
				[ (tagID, itemID) for itemID, item in enumerate(items, 1)
								if tagt in item["tags"] ]
			)
		return rels

def dumpToDB( tags, items, rels ) :
	import mysql as SQL
	db = SQL.getConnection()
	SQL.resetDB( db, dbKeys )
	SQL.insertItems( items, dbKeys, db )
	SQL.insertTags( tags, db )
	SQL.insertRels( rels, db )
	SQL.closeDB( db )

inp = raw_input("Do you want to add data from ALISS (takes longer time)?(Y/N): ")
doALISS = (inp.lower()[0] == 'y')

import parse_edbra as ED
import parse_aliss as AL
print "Parsing data from Edinburgh council's Public API"
print "Fetching may take a while"
ED.parse()
print "Data parsed, importing it..."
tags = ED.getCleanTags()
ed_items = ED.getItems()
print "Done"
print '-' * 16
items = translateItems( ed_items, edbraTranslation )
#doALISS = False
if (doALISS) :
	print "Fetching data from ALISS database"
	print "It will take a while"
	ln = len(tags)
	al_items = []
	for i, tag in enumerate(tags,1) :
		if ( ((i * 10) / ln) > ( ((i - 1) * 10) / ln ) ):
			print str((i*10)/ln * 10)+"%..."
		if (" " in tag):
			continue
		#if ( i > 10): break
		al_items.extend(AL.getItems(tag))
	print "Data fetched, importing it..."
	al_items = AL.removeDuplicates( al_items )
	items.extend(translateItems( al_items, alissTranslation ) )

	items = rmDups( items ) # that shouldn't be useful, but just in case...
	print "Done"
	print '-' * 16
fillMissing( items, defaultKeys )
fixNames( items )
rels = make_assoc( tags, items )
inp = raw_input("Do you want to dump all this data to DB?\nNOTE: current data will be purged! (Y/N): ")
if (inp.lower()[0] == 'y'):
	dumpToDB( tags, items, rels )


