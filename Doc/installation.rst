MouseDB Installation
====================

Configuration
-------------
MouseDB requires both a database and a webserver to be set up.  Ideally, the database should be hosted separately from the webserver and MouseDB installation, but this is not necessary, as both can be used from the same server.  If you are using a remote server for the database, it is best to set up a user for this database that can only be accessed from the webserver.  If you want to set up several installations (ie for different users or different laboratories), you need separate databases and MouseDB installations for each.  You will also need to set up the webserver with different addresses for each installation.

Software Dependencies
---------------------
1. **MouseDB source code**.  Download from one of the following:  

  a. http://github.com/davebridges/mousedb/downloads for the current release
  b. http://github.com/davebridges/mousedb for the source code

Downloading and/or unzipping will create a directory named mousedb.  You can update to the newest revision at any time either using git or downloading and re-installing the newer version.  Changing or updating software versions will not alter any saved data, but you will have to update the localsettings.py file (described below).

2. **Python**.  Requires Version 2.6, is not yet compatible with Python 3.0.  Download from http://www.python.org/download/.
3. **Django**.  Download from http://www.djangoproject.com/download/
4. **Database software**.  Typically MySQL is used, but PostgreSQL, Oracle or SQLite can also be used.  You also need to install the python driver for this database (unless you are using SQLite, which is internal to Python 2.5+).  See http://docs.djangoproject.com/en/dev/topics/install/database-installation - Django Database Installation Documentation for more information.


Database Setup
--------------
1. Create a new database.  You need to record the user, password, host and database name.  If you are using SQLite this step is not required.
2. Go to localsettings_empty.py and edit the settings:

  * DATABASE_ENGINE: 'mysql', 'postgresql_psycopg2' or 'sqlite3 depending on the database software used.
  * DATABASE_NAME: database name
  * DATABASE_USER: database user
  * DATABASE_PASSWORD: database password
  * DATABASE_HOST: database host

3. Save this file as localsettings.py in the main mousedb directory.


MouseDB Setup
-------------
1. Open a command line window and navigate to the mousedb directory
2. Instantiate the database tables by entering python manage.py syncdb and enter a superuser account username, password and email.
3. Enter python manage.py shell to open a python shell and enter the following commands, where "group name" is the name of your group (keep the quotation marks)::

   >>from mousedb.groups.models import Group
   >>g = Group(group="group name")
   >>g.save()

Web Server Setup
----------------
You need to set up a server to serve both the django installation and saved files.  For the saved files.  I recommend using apache for both.  The preferred setup is to use Apache2 with mod\_python.  The following is a httpd.conf example where the code is placed in /usr/src/mousedb::

  Alias /static /usr/src/mousedb/media
  Alias /mousedb-media /usr/src/mousedb/media
  <Directory /usr/mousedb/media>
     Order allow,deny
     Allow from all
  </Directory>
  <Location "/mousedb/">
     SetHandler python-program
     PythonHandler django.core.handlers.modpython
     SetEnv DJANGO_SETTINGS_MODULE mousedb.settings
     SetEnv PYTHON_EGG_CACHE /var/www/eggs
     PythonOption django.root /mousedb
     PythonDebug On
     PythonPath "['/usr/src'] + sys.path"
     PythonInterpreter mousedb
  </Location>

If you want to restrict access to these files, change the Allow from all directive to specific domains or ip addresses (for example Allow from 192.168.0.0/99 would allow from 192.168.0.0 to 192.168.0.99)

Final Configuration and User Setup
----------------------------------
1. Go to your server then /mousedb/admin/groups/group/1/ and log in as superuser.
2. Edit the details of your group, the main contact and create data sharing license (or point out the restrictions for use only by authorized users)
3. Next go to /mousedb/admin/auth/group/ and create user groups.  This will define permissions for users.  Select a name for the group (ie data entry) and select the add, change or delete permissions for that group.  Users can be members of several groups.
4. Go to mousedb/admin/auth/users/ and create users, selecting usernames, full names, password (or have the user set the password) and then choose group permissions.
