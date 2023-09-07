# bored-junior-test-task
This program executes api call to the bored API which returns activity and saves it to the DB, also
it provides a possibility to look up last added activities.

## Technology stack:
- Programming language: Python
- ORM: Sqlalchemy
- Database: Sqlite3
- Testing framework: Pytest
- Library for api calls: Requests
- Console arguments parser: Argparse

## Database structure
Database has one single scheme called Activities:
```
create table activities
(
    id            INTEGER not null
        primary key,
    name          VARCHAR not null,
    type          VARCHAR not null,
    participants  INTEGER not null,
    price         FLOAT   not null,
    link          VARCHAR,
    key           INTEGER not null,
    accessibility FLOAT   not null
);
```
## Installation
1. First, create and activate your virtual environment
```
pip install virtualenv
python<version> -m venv <virtual-environment-name>
source env/bin/activate
```
2. Install all packages from requirements.txt
```
pip install -r requirements.txt
```
3. Run scripts for creating DB and tables
```
python connect.py
python models.py
```
4. Run the main file
```
python main.py new <arguments>
python main.py list
```
5. For running test run the tests file
```
pytest tests.py
```