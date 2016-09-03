# [LASA Website](http://lasa.us)
A replacement for the current [LASA High School
website](http://www.lasahighschool.com).

## Dependencies
The project uses the [flask framework](http://flask.pocoo.org) for
python. The comprehensive list of dependencies is available in
requirements.txt.

## Installation
### Virtual environment setup
It is recommended to run everything inside a [python virtual
environment
("venv")](https://docs.python.org/3/library/venv.html). This can be
done by running the command `python -m venv flask`. The new folder
`flask` should appear in the directory in which you ran the command.

### Package installation
`flask/bin/pip3 install -r requirements.txt` should install all
necessary packages.

### Database setup
In order to get database file with the correct columns and records, it
is necessary to run the following scripts:
1. Create a new SQLite database: `./db_create.py`
2. Migrate the existing database models: `./db_migrate.py`

In the future there will likely be a script that will create and
populate the database with some default data. In the meantime, it is
possible to manually setup the database:
1. Start python: `flask/bin/python`
2. Import a SQLite interface and (among other things) the User class:
`from app import db, models`
3. Import modules needed to hash and salt passwords: `import bcrypt, hmac`
4. Create User "u" with specificed information: ```u =
models.User(name="harambe", email="harambe@cincinnatizoo.org",
password=bcrypt.hashpw("IAmHarambe".encode("utf-8"), 
bcrypt.gensalt()))```
5. Add the User to the SQLite session: `db.session.add(u)`
6. Commit the session: `db.session.commit()`

## Licensing
All files are released under the GNU AGPL (whose full text is located
in the LICENSE file), with the following exceptions:
- lowpolybg.jpg is released into the public domain under [the CC0
license](https://creativecommons.org/publicdomain/zero/1.0/).
- All database-related files, secret keys (for cryptographic purposes or
otherwise), and passwords are not intended to be publicly available
and thus may not be used for any purpose.

## Authors
Harrison Tran, Kevin Black, Ojas Ahuja