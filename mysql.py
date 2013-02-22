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

def resetDB( db, defaultKeys ):
	if "location" not in [key.lower() for key in defaultKeys.keys()] :
		print "Can't create tables because there's no Location information..."
		raise NameError("No Location key in defaultKeys")

	c = db.cursor()
	c.execute("DROP TABLE IF EXISTS tags")
	c.execute("""CREATE TABLE tags (
			id INT NOT NULL AUTO_INCREMENT,
			tag VARCHAR(25) NOT NULL,
			PRIMARY KEY(id)
			)""")
	c.execute("DROP TABLE IF EXISTS items")
	query = "".join([
		"""CREATE TABLE items (
			id INT NOT NULL AUTO_INCREMENT,""",
			",\n".join([ " ".join([name, t]) for name, t in defaultKeys.values()]),
			",\nPRIMARY KEY(id))"])
	c.execute(query)
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
	db = MySQLdb.connect(host='127.0.0.1', user='user', passwd='password', db='doed', use_unicode=True, charset="utf8")
	return db

def insertItems( items, defaultKeys, db ):
	c = db.cursor()
	# just getting keys in the correct order
	# constructing a query in fairly complex manner
	# This lad doesn't understand that either:
	# (\_/)
	# (O.o)
	# (> <)

	query = "".join(["INSERT INTO items(",
			", ".join([key for _,(key,_) in sorted(defaultKeys.items())]),
			") VALUES(",
			", ".join( ["%s" for _ in range( len(defaultKeys.keys()) )] ),
			")"])
	vals = [tuple( [item[key] for key in sorted( defaultKeys.keys() )] ) \
			for item in items ]
	c.executemany(query, vals )	
	db.commit()
	c.close()

def insertTags( aTags, db ):
	c = db.cursor()
	c.executemany( "INSERT INTO tags(tag) VALUES(%s)",
			aTags )
	db.commit()
	c.close()

def insertRels( relations, db ):
	c = db.cursor()
	c.executemany( "INSERT INTO relations(tagID, itemID) VALUES(%s, %s)", relations)
	c.close()
	db.commit()

def insertRel( rel, db_cursor):
	c = db_cursor
	c.execute( "INSERT INTO relations(tagID, itemID) VALUES(%s, %s)", rel )

def insertInfo( items, defaultKeys, db ):
	c = db.cursor()
	

	c.close()
def closeDB( db ):
	db.commit()
	db.close()

