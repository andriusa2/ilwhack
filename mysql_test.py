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

def resetDB( db, defaultKeys = ["Name", "Email", "Address"] ):
	c = db.cursor()
	c.execute("DROP TABLE IF EXISTS tags")
	c.execute("""CREATE TABLE tags (
			id INT NOT NULL,
			tag VARCHAR(25) NOT NULL,
			PRIMARY KEY(id)
			)""")
	c.execute("DROP TABLE IF EXISTS items")
	c.execute("""CREATE TABLE items (
			id INT NOT NULL AUTO_INCREMENT,
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
	c.execute("DROP TABLE IF EXISTS info")
	query = """CREATE TABLE info (
			id INT NOT NULL AUTO_INCREMENT,
			"""
	query = "".join([query,
			",\n".join([name + " " + t +" NOT NULL" for name, t in defaultKeys.values()]),
			",\nPRIMARY KEY(id))"])
	c.execute(query)
	c.close()
	db.commit()

def getConnection():
	db = MySQLdb.connect(host='localhost', user='user', passwd='password', db='doed')
	return db

def insertItems( items, db ):
	c = db.cursor()
	for item in items :
		c.execute( "INSERT INTO items(name, location) VALUES(%s, %s)",
			(item['Name'], item['Location']) )
	db.commit()
	c.close()

def insertTags( aTags, db ):
	c = db.cursor()
	for tag in aTags.keys():
		c.execute( "INSERT INTO tags(id, tag) VALUES(%s, %s)",
			(aTags[tag], tag) )
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

def insertInfo( items, defaultKeys, db ):
	c = db.cursor()
	query = "".join(["INSERT INTO info(",
			", ".join([key for _,(key,_) in sorted(defaultKeys.items())]),
			") VALUES(",
			", ".join( ["%s" for _ in range( len(defaultKeys.keys()) )] ),
			")"])

	for item in items :
		c.execute(query, tuple( [item[key] for key in sorted(defaultKeys.keys())] ) )

	c.close()
def closeDB( db ):
	db.commit()
	db.close()

