# [LASA Website](http://lasa.us)
A replacement for the current [LASA High School
website](http://www.lasahighschool.com).

## Dependencies
The project uses the flask framework for python. The comprehensive
list of dependencies is available in requirements.txt.

## Installation
### Virtual environment setup

Run everything inside a python virtual environment (venv):  `python -m
venv flask`. 

### Package installation
Install all necessary packages: `flask/bin/pip3 install -r
requirements.txt`

### Database setup
In order to get database file with the correct columns and records, it
is necessary to run the following scripts:

1. Create a new SQLite database: `./db_create.py`

2. Migrate the existing database models: `./db_migrate.py`

To create a user that can log in and edit the website, run the following script:

`./create_user.py harambe gorilla@cincinnatizoo.org neverforget`

where the three arguments are the username, email, and password, respectively.

## Licensing
All files are released under the GNU AGPL (whose full text is located
in the LICENSE file), with the following exceptions:
- lowpolybg.jpg is released into the public domain under [the CC0
license](https://creativecommons.org/publicdomain/zero/1.0/).
- All database-related files, secret keys (for cryptographic purposes or
otherwise), and passwords are not intended to be publicly available
and thus may not be used for any purpose.
- Files relating to mascots/logos of LASA High School or Austin ISD
may be covered under a seperate license. Please obtain advanced
written permission from the appropriate entity before using them for
any purpose.

## Authors
Harrison Tran, Kevin Black, Ojas Ahuja
