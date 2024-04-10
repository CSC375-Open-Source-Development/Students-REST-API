# Students REST API

This is just a simple REST API that allows a client to interact with Student data.

The `docs.html` file contains the REST API documentation for the Students routes. 
The `/docs` route returns it so it can be viewed conveniently in a web browser.
There are a few other non-student related routes defined in the `app.py` file that are used for testing.

The Student data is kept in a SQLite database `students.db` that can be created by the script located in the `bin` directory.
I recommend using [DB Browser for SQLite](https://sqlitebrowser.org/) to look at its contents after creating it.

# How to run this REST API Server

## Setup

This project was written in Python and uses the Flask package.

If you do not have it already, install [Python 3](https://www.python.org/downloads/).

Then:

1. Navigate to the project's root folder in your command line.
1. Run `pip install -r requirements.txt`

If all succeeded, the Flask package (and all other dependencies) should now be installed properly.

## Start Server

1. Navigate to the project's root folder in your command line.
1. Run `python -m src.app`

