## Chkprase ##

Welcome to __chkphrase__. This application was mainly created to allow
distributed QA of large collections of found words. This readme is intended
to enable a user to setup and install the application for local development.

### Dependencies ###

Chkphrase is a [Flask](http://flask.pocoo.org/) application that uses
[SQLAlchemy](http://www.sqlalchemy.org/) for communication with the
database. Most users are comfortable working with MySQL as the DB backend,
but anything that SQLAlchemy supports should work just fine. 

Also, and this isn't a strict dependency, I strongly recommend developing
using a [virtual environment](http://pypi.python.org/pypi/virtualenv). The
documentation will assume that that's what you are doing

### Installation ###

These instructions will assume that you have installed virtualenv and
[pip](http://pypi.python.org/pypi/pip).

__Fetch the source code from github.__
    
    $ git clone git://github.com/siramix/chkphrase.git

__Setup the MySQL database (This assumes you have MySQL installed on your
   platform)__

    ```
    $ mysql -u root -p # Enter your password   
    mysql> create database chkphrase;
    mysql> create user chkphrase;   
    mysql> grant all on chkphrase.* to 'chkphrase'@'localhost' identified by 'chkphrase'   
    mysql> \q
    ```

__Setup the installation for development__

    ```
    $ virtualenv chkphrase_env
    $ source chkphrase_env/bin/activate
    (chkphrase_env)$ cd chkphrase
    (chkphrase_env)$ python setup.py develop # This should fetch dependencies
    ```

__Initialize the database and create a user__

    ```
    (chkphrase_env)$ python
    >>> import chkphrase.database as db
    >>> from chkphrase.models import User
    >>> db.init_db()
    >>> new_user = User('userid', 'User Full Name', 'password') # do better :)
    >>> db.db_session.add(new_user)
    >>> db.db_session.commit() # There may be a warning (it's okay)
    >>> quit()
    ```

__Startup the dev server__

    ```
    (chkphrase_env)$ python runserver.py
    ```

That's it! You should be able to access the system at http://localhost:5000/.

### Notes ###

* To change the credentials edit chphrase/conf.py
* To edit the html/css/js look in chkphrase/templates
