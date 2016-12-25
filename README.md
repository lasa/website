# [LASA Website](http://lasa.us)
A replacement for the current [LASA High School
website](http://www.lasahighschool.com).

## Dependencies
The project uses the flask framework for python. The comprehensive
list of dependencies is available in requirements.txt.

## Installation
### Virtual environment setup

Run everything inside a python virtual environment (venv):  `python -m
venv flask` or `python3 -m venv flask` if Python 3 is not the system default. 

### Package installation
Install all necessary packages: `flask/bin/pip3 install -r
requirements.txt`

### Database setup
First, install and set up the latest version of MySQL. The following are instructions for Debian linux:

1. Install the latest version of MySQL server and client: `sudo apt-get install mysql-server libmysqlclient-dev`

2. When prompted, enter "password" as the MySQL root password, or otherwise change the SQLALCHEMY\_DATABASE\_URI in config.py to match your password.

3. Start the MySQL service: `sudo systemctl start mysql`

4. Create a new database: `./db_create.py`

5. Set up database migrations: `./db_migrate.py db init`

To create a user that can log in and edit the website, run the following script:

`./create_user.py harambe gorilla@cincinnatizoo.org #neverforget123`

where the three arguments are the username, email, and password, respectively.

### Testing the application

To run an instance of the website in debug mode on localhost:5000: `./run.py`

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
