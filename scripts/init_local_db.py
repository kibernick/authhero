#!/usr/bin/env python
import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import errors

import flask_migrate
from flask import current_app

# Import project settings without installing the wheel.
project_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
src_path = os.path.join(project_root, "src")
sys.path.insert(0, src_path)

from authhero.settings import Config, DevConfig, TestConfig
from authhero.factories import create_app


def create_user_and_db(config: Config, conn):
    try:
        sql_commands = [
            f"create database {cfg.SQLALCHEMY_DB};",
            f"create user {cfg.SQLALCHEMY_USER} with encrypted password '{cfg.SQLALCHEMY_PASS}';",
            f"grant all privileges on database {cfg.SQLALCHEMY_DB} to {cfg.SQLALCHEMY_USER};",
        ]
        with conn.cursor() as cur:
            for sql_cmd in sql_commands:
                cur.execute(sql_cmd)
    except errors.DuplicateDatabase:  # type: ignore
        print("Database already exists, skipping...")


if __name__ == "__main__":
    """Initialize local development and test databases.

    NOTE: you can delete existing local databases (and user) inside "psql postgres" with:

    DROP DATABASE authhero;
    DROP DATABASE authhero_test;
    DROP USER herouser;
    DROP USER herouser_test;
    """
    user, password = "postgres", None

    print("Connecting to the PostgreSQL database server...")
    conn = psycopg2.connect(user=user, password=password)
    # CREATE TABLESPACE cannot run inside a transaction block
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    migrations_dir = os.path.join(src_path, "migrations")
    for cfg in [DevConfig, TestConfig]:
        app = create_app(cfg)
        with app.app_context():
            print(f"Creating {cfg.ENV} DB on: {cfg.SQLALCHEMY_DATABASE_URI}")
            create_user_and_db(cfg, conn)
            print("Database and user created!")

            # Testing db is managed via conftest fixtures
            if not cfg.TESTING: 
                print("Running migrations...")
                flask_migrate.upgrade(migrations_dir)
                print("Migrations successfully run!")

    conn.close()
