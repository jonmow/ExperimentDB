ExperimentDB Installation
=========================

Configuration
-------------
ExperimentDB requires both a database and a webserver to be set up.  Ideally, the database should be hosted separately from the webserver and ExperimentDB installation, but this is not necessary, as both can be used from the same server.  If you are using a remote server for the database, it is best to set up a user for this database that can only be accessed from the webserver.  If you want to set up several installations (ie for different users or different laboratories), you need separate databases and ExperimentDB installations for each.  You will also need to set up the webserver with different addresses for each installation.

Software Dependencies
---------------------
1. **ExperimentDB source code**.  Download from one of the following:  

  a. http://github.com/davebridges/ExperimentDB/downloads for the current release
  b. http://github.com/davebridges/ExperimentDB for the source code
  c. from pypi by entering::

      pip install experimentdb

Downloading and/or unzipping will create a directory named ExperimentDB.  You can update to the newest revision at any time either using git or downloading and re-installing the newer version.  Changing or updating software versions will not alter any saved data, but you will have to update the localsettings.py file (described below).

2. **Python**.  Requires Version 2.6, is not yet compatible with Python 3.0.  Download from Python_.
3. **Django**.  Download from Django_.  This will be automatically installed if you installed experimentdb with pip.  This will be automatically installed if you installed experimentdb with pip.
4. **Database software**.  Typically MySQL is used, but PostgreSQL, Oracle or SQLite can also be used.  You also need to install the python driver for this database (unless you are using SQLite, which is internal to Python 2.5+).  For more information see Instructions_.
5. **Biopython Packages**.  Download and install from Biopython_. This will be automatically installed if you installed experimentdb with pip.
6. **South**.  Install using pip (**pip install south**).  This will be automatically installed if you installed experimentdb with pip.
7. **Django Ajax Select**.  Install using pip (**pip install django-ajax-selects**).  This will be automatically installed if you installed experimentdb with pip.
8. **Python Imaging Library**.  Install using pip (**pip install pil**).  Available at PIL_.  This will be automatically installed if you installed experimentdb with pip.

.. _Python: http://www.python.org/download
.. _Django: http://www.djangoproject.com/download/
.. _Instructions: http://docs.djangoproject.com/en/dev/topics/install/database-installation
.. _Biopython: http://biopython.org
.. _PIL: http://www.pythonware.com/products/pil/

Database Setup
--------------
1. Create a new database.  You need to record the user, password, host and database name.  Refer to the database documentation for how to do this with a specific database engine.  If you are using SQLite3, you only need to set the engine and the database name.  It is recommended to use MySQL.
2. Go to localsettings_empty.py and edit the settings::

    ENGINE: 'mysql', 'postgresql_psycopg2' or 'sqlite3 depending on the database software used.
    NAME: database name
    USER: database user.  Unless using sqlite3
    PASSWORD: database password.  Unless using sqlite3
    HOST: database host.

3. Save this file as localsettings.py in the main ExperimentDB directory.
4. Run the test client by going into the experimentdb directory and running the following.  There should be no errors at this point::

    python manage.py test
	 
5. Generate the initial database tables by entering::

    python manage.py syncdb

6. When asked generate an administrative superuser and set the email and password.

Web Server Setup
----------------
You need to set up a server to serve both the django installation and saved files.  For the saved files.  I recommend using apache for both.  The preferred setup is to use Apache2 with mod\_wsgi.  The following is a httpd.conf example where the code is placed in /usr/src/django/experimentdb::

    Alias /static /usr/src/django/experimentdb/media
    Alias /media /usr/src/django/experimentdb/media
    
	<Directory /usr/src/django/experimentdb/media>
        Order allow,deny
        Allow from all
    </Directory>

    WSGIScriptAlias /experimentdb /usr/src/django/experimentdb/apache/django.wsgi

    <Directory /usr/src/django/experimentdb/apache>
        Order deny,allow
        Allow from all
    </Directory>

If you want to restrict access to these files, change the Allow from all directive to specific domains or ip addresses (for example Allow from 192.168.0.0/99 would allow from 192.168.0.0 to 192.168.0.99)

Final Configuration and User Setup
----------------------------------
1. Go to experimentdb/admin/auth/users/ and create users, selecting usernames, full names, password (or have the user set the password) and then choose group permissions.
