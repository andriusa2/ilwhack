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
			id INT,
			tag VARCHAR(25),
			PRIMARY KEY(id)
			)""")
	c.execute("DROP TABLE IF EXISTS items")
	c.execute("""CREATE TABLE items (
			id INT,
			name TINYTEXT,
			location VARCHAR(20),
			PRIMARY KEY(id)
			)""")
	c.execute("DROP TABLE IF EXISTS relations")
	c.execute("""CREATE TABLE relations (
			id INT,
			tagID INT,
			itemID INT,
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

def closeDB( db ):
	db.close()

db = getConnection()
resetDB( db )


