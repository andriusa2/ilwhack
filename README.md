DoED project
=======

The __DoEd__ project by team _"); DROP TABLE ``users``;--_
Created during ILW Smart Data Hack 2013 in University of Edinburgh

Description:
-----

This project enables Edinburgh's residents to find various local (or not so much) activites based on simple tag/search system.
The actual data for all activties is gathered from [Edinburgh Council's public data API](http://www.edinburgh.gov.uk/directories) and [ALISS public database API](http://www.aliss.org/), but it is preprocessed and cached in our local database because of the inconsistencies between both APIs formats.

We are using public data from ALISS and Edinburgh Council (namely sports/recreation, outdoor eduation providers and monuments/parks). For map visualisation the google maps API wrapper [gmap3](http://gmap3.net/) is used in tandem with [jQuery](http://jquery.com/) (w/ Tagcloud plugin) and [Bootstrap](http://twitter.github.com/bootstrap/)

Prerequisites / requirements:
------

For python data parsing/dumping scripts one needs `python-mysqld` module, script does not support python 3.0, but can be easily ported to it (as long as `python-mysqld` is as well)

PHP backend can be run on almost any PHP 5.x version, it might even work on older builds, but that's not recommended.

Setup instructions:
------

1. Install `python-mysqldb` (it's in apt-get or w/e your distro uses for package management)
2. Update mysql login info for PHP (`./src/includes/define.php`) and Python (`./mysql.py`) scripts
3. Update API keys on Python scripts (`./parse_edbra.py`)
4. run `python dataDump.py`

Now you should have precached data and the project just works

Notes:
------

There might be some inappropriate and/or unclear tags because of the natural tag-extraction process, please ignore these (or try them out if you are curious)
We have tried to incorporate [Insight Arcade's data](http://educationhackers.org/) in our data stack, but sadly their database did not have enough data for geolocation determination.

Licence
------

This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/.

Team/credits
------
Andrius Žiūkas - Team leader/data mining/database structure
Martynas Melninkas - Backend/frontend-backend linking

