#!/usr/bin/python
"""
tags:
ID(int), Tag(varchar)

relations:
ID(int), TagID(int), ItemID(int)

items:
ID(int), name(varchar), location(varchar)

"""

import MySQLdb

def resetDB( db ):
	c = db.cursor()
	c.execute("DROP TABLE IF EXISTS tags")
	c.execute("""CREATE TABLE tags (
			id INT NOT NULL,
			tag VARCHAR(25) NOT NULL,
			PRIMARY KEY(id)
			)""")
	c.execute("DROP TABLE IF EXISTS items")
	c.execute("""CREATE TABLE items (
			id INT NOT NULL,
			name TINYTEXT NOT NULL,
			location VARCHAR(20) NOT NULL,
			PRIMARY KEY(id)
			)""")
	c.execute("DROP TABLE IF EXISTS relations")
	c.execute("""CREATE TABLE relations (
			id INT NOT NULL AUTO_INCREMENT,
			tagID INT NOT NULL,
			itemID INT NOT NULL,
			PRIMARY KEY(id),
			INDEX(tagID)
			)""")
	c.close()
	db.commit()

def getConnection():
	return MySQLdb.connect(host='localhost', user='user', passwd='password', db='doed')

def insertItems( items, db ):
	i = 0;
	c = db.cursor()
	for item in items :
		if 'Name' not in item.keys():
			print "WARNING: NO NAME FOR ITEM W/ ID ", i
			item['Name'] = "N/A"
		if 'Location' not in item.keys():
			print "WARNING: NO LOCATION FOR ITEM W/ ID ", i
			item['Location'] = ""

		c.execute( "INSERT INTO items(id, name, location) VALUES(%s, %s, %s)",
			(int(i), item['Name'], item['Location'],) )
		i += 1
	db.commit()
	c.close()

def insertTags( aTags, db ):
	c = db.cursor()
	for tag in aTags.keys():
		c.execute( "INSERT INTO tags(id, tag) VALUES(%s, %s)",
			(aTags[tag], tag,) )
	db.commit()
	c.close()

def insertRels( relations, db ):
	c = db.cursor()
	for rel in relations:
		c.execute( "INSERT INTO relations(tagID, itemID) VALUES(%s, %s)", rel)
	c.close()
	db.commit()

def insertRel( rel, db_cursor):
	c = db_cursor
	c.execute( "INSERT INTO relations(tagID, itemID) VALUES(%s, %s)", rel )

def closeDB( db ):
	db.commit()
	db.close()

