# Database sever for Magic Butler

database sever for Sleep reminder chatbot, Magic Butler

## Quickstart

### Local development

This project is built using the Flask web framework. It runs on Python 3.4+.

To run the sever locally follow these steps:

1. Clone this repository and `cd` into `database_sever` repo.

1. Create a new virtual environment and activte it :

    ``bash
    python3 -m venv venv
    source venv/bin/activate
    ``

1. Install the requirements.

    ``bash
    pip install -r requirements.txt
    ``

1. Initial the database.

    ``bash
    python3 manage.py db init
    ``

1. Run the migration.

    ``bash
    python3 manage.py db migrate -m "initial migration"
    python3 manage.py db upgrade
    ``

1. Start the database server.

    ``bash
    python3 manage.py runserver -p [portnum]
    ``

## Database Overview

### Datebase Structure

![](./image/ERD.png)

### Sever API

1. For User column:
	- Search (request method: GET)
		a. http://localhost:port/users: return all users
		b. http://localhost:port/user/id/[idnum]: return user by id
		c. http://localhost:port/user/phone/[phonenum]: return user by phone
	- Create (request method: POST)
		a. http://localhost:port/user:  request body's example is in example folder 
	- Delete
		a. http://localhost:port/user/[idnum]: Delete user by ID
	- Update
		a.http://localhost:port/user/[idnum]: Update user by ID
2. For Record column:
	- Search (request method: GET)
		a. http://localhost:port/records: return all records
		b. http://localhost:port/record/id/[idnum]: return record by id
	- Create (request method: POST)
		a. http://localhost:port/record:  request body's example is in example folder 
	- Delete (request method: DELETE)
		a. http://localhost:port/record/[idnum]: Delete record by ID
	- Update (request method: PUT)
		a.http://localhost:port/record/[idnum]: Update record by ID
3. For Datum column:
	- Search (request method: GET)
		a. http://localhost:port/data: return all raw data
		b. http://localhost:port/datum/id/[idnum]: return datum by id
	- Create (request method: POST)
		a. http://localhost:port/datum:  request body's example is in example folder 
	- Delete (request method: DELETE)
		a. http://localhost:port/datum/[idnum]: Delete datum by ID
	- Update (request method: PUT)
		a.http://localhost:port/datum/[idnum]: Update datum by ID