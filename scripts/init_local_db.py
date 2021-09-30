#!/usr/bin/env python
import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Import project settings without installing the wheel.
project_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
src_path = os.path.join(project_root, "src")
sys.path.insert(0, src_path)
from authhero.settings import DevConfig, TestConfig


def init_from_config(cfg, conn):
    sql_commands = [
        f"create database {cfg.SQLALCHEMY_DB};",
        f"create user {cfg.SQLALCHEMY_USER} with encrypted password '{cfg.SQLALCHEMY_PASS}';",
        f"grant all privileges on database {cfg.SQLALCHEMY_DB} to {cfg.SQLALCHEMY_USER};",
    ]
    with conn.cursor() as cur:
        for sql_cmd in sql_commands:
            cur.execute(sql_cmd)


def init_db(user, password):
    """Initialize local databases.
    
    NOTE: delete existing local databases (and user) inside "psql postgres" with:
    
    DROP DATABASE authhero;
    DROP DATABASE authhero_test;
    DROP USER herouser;
    DROP USER herouser_test;
    """
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(user=user, password=password)
    # CREATE TABLESPACE cannot run inside a transaction block
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    
    for cfg in [DevConfig, TestConfig]:
        print(f"Creating {cfg.ENV} DB on: {cfg.SQLALCHEMY_DATABASE_URI}")
        init_from_config(cfg, conn)

    conn.close()


if __name__ == "__main__":
    init_db(user="postgres", password=None)
