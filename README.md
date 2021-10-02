# AuthHero

![](image.png)

A simple authentication service.

## Setup

### Prerequisites

* Dependency management using [poetry](https://python-poetry.org/docs/#installation)
    * If you'd rather not install poetry on your system, you can download the wheel from the Github Releases page and install the `authhero` package in a local virtual environment.

* PostgreSQL

    * The app will connect to a Postgres database running on localhost
    * If you'd rather not install Postgres, but still want to run the tests, you can skip the tests that need a database with: `pytest -m "not functional"`
    * Set up the local development and test databases with:

```bash
# Assumes username: postgres, without password (configurable)
./scripts/init_local_db.py
```

### Installation

You can either setup a local virtual environment with poetry or install the `authhero` package with a wheel from the project's Releases page on Github.

## Running

Run a local Flask dev server from the `src` directory with:

```
flask run
```

You should be able to see the Swagger API documentation with fully functioning UI to call the API on http://127.0.0.1:5000/.

### User journey 🚀

* Register a new user with `/auth/register`
* Login with entered credentials at `/auth/login`
    * Save the `api_key` token provided in the response
    * In the Swagger Docs, enter the token in the `Authorize` menu on the top-right
* Interact with the User CRUD API at `/users/*`
    * Can view all active users
* Logging out will invalidate all of users active tokens, and the user will need to login again, and request a new token
* Deleting a user can only be done on the logged in user, and it is a soft-delete, where the user's API keys will no longer be able to be used for authentication.

## Testing

There are two kinds of tests: "simple" *unit* tests and *functional* tests that, while not being true end-to-end tests, they test the full functionality, including the database.

* Inside a virtual env, run `pytest` from the repo root.
* Run only the unit tests with `pytest -m "not functional"

Due to time, only partial code coverage.

## Design decisions

* Picked MVC to structure the code, since it should be a simple project
    * Would try the Repository pattern for more complex use cases
    * Added a layer for business logic, so as to not pollute models or views, in `services.py` files
* Flask as a simple web server, with the following libraries:
    * [flask-restx](https://flask-restx.readthedocs.io/en/latest/) - a handy library for building REST APIs in Flask, comes with integrated Swagger Docs.
    * [SQLAlchemy](https://www.sqlalchemy.org/) - a database toolkit
    * [bcrypt](https://github.com/pyca/bcrypt/) - for secure password hashing
* Configuration through `Config` objects 
* Storing of hashed passwords using `bcrypt` (hashing and salt using default configuration)
* Minimal validation in User CRUD, done using `flask_restx.reqparse`
* No AUTOCOMMIT, prefer "Unit of Work" pattern
* PostgreSQL instead of SQLite
    * Slightly more complicated to set up, but since I had enough time to do so, I did :)
    * Much more likely to be used in a real product

### Data Model:

* [Two entities]((src/authhero/models.py)): `User` and `ApiKey` (one-to-many relationship)
* All models have the `created_on` and `updated_on` attributes for easy auditing and data analysis
* Implemented "soft" deletion of Users, with the `is_active` flag

### Authentication

* Decided to implement only Token-authentication, due to time restrictions
* Currently can only authenticate from custom header: "X-API-KEY"
    * Authentication via querystring was not implemented due to time

## Future improvements and ideas

* Use [pydantic](https://pydantic-docs.helpmanual.io/) for configuration and secrets handling
    * Also add a `ProductionConfig` using this
* Document all possible responses and status codes
    * Did not cover all in docs due to time
* Handle all database errors since it's quite an important dependency
* Better test coverage - would've done more with more time
    * Also different tests:
        * end-to-end
        * smoke tests
        * load testing, for example with [locust](https://locust.io/)
* CI/CD system
* Docker container
* Kubernetes configuration
* `User.id` currently is currently an `int` that autoincrements from `1`
    * In a distributed authentication system, would prefer `uuid` over `int` to avoid collision
    * If still `int`, would configure primary key generation differently
* Introduce role-based access and have a more sophisticated authorization system, with at least an "admin" role
* Have the authentication system be more abstract so that it's extendable to more ways of authenticating and/or providers, for example to be able to add JWT and OAuth
