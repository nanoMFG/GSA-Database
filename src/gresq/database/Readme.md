# GrResq Database Model Developer Documentation
```
__init__.py - Shared Declarative Base "Base" defined.
models - All database table models definitions
dal - Data access layer
```

## Models

Models are defined in `./models` and are imported to the `models` package level.  Import as follows:
```
from gresq.database.models import Sample, Recipe
```

## Data Access Layer (DAL)
### Usage
```
from gresq.database import dal
```
### Code Conventions

An augmented declarative Base class is declared, any mixins defined and an instance of the `dal` is instantiated in:  
 `gresq/database/__init__.py`

 This supports the convention withing the applications of:  
 `from gresq.database import dal`  

 The augmented `Base` declaration:  
 * Automatically sets the `__tablename__` attribute as the ClassName converted to lower "camel_case".
  

## Basic Queries

* Grab a session. 
* run the query.
```
session = dal.Session()
query = session.query(Model)
```

## Insert, Update or Delete
* Create a session context at the beginning of a logical operation (e.g. "submit").
* Pass the session in to various functions
* Allow the context manager to do the right thing (rollback or commit)
```
def submit_or_update_some_stuff():
    with dal.session_scope(autocommit=True) as session:
        do_stuff(session)
        do_more_stuff(session)
```
See the `dal.py` code for details of context manager.  Also refer to sqlalchemy doc:   
 https://docs.sqlalchemy.org/en/13/orm/session_basics.html#when-do-i-construct-a-session-when-do-i-commit-it-and-when-do-i-close-it   

## Testing

Basic testing of the DB models is implemented using a set of `factory boy` factories to generate fake DB data.  When a SampleFactory is generated, all child models also generate.  

### Prerequistes
```
pytest
factory_boy
# set env. vars for DB
source env.sh
```
The testing database connection is defined in `test/database/__init__.py`.  This connection is set to use the environment variables associated with the **testing** database.  Production credentials in the environment are not used.  **Care should be taken to avoid changing this configuration and avoid using production credentials for testing at all cost**

### Model Factories
The database testing frameworks uses the `factory_boy` library to generated mock data and populate the database with test data.  Factories are defined in `test/database/factories`.


### Run the tests

##### Basic test run
```
pytest -v
```
##### See the outputs
```
pytest -v -s
```
##### Pick a test
```
pytest -v -s -k simple
```
##### Keep Database After Tests
```
pytest -v -s --dropdb False
```

### Test Conventions

#### `test/database/models`:

* Sainity checks for model definitions
* Referential integrity enforcement
* Hybrid attribute and associated expression behavior