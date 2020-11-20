import os

import click

from flask import current_app
from flask.cli import with_appcontext
from sqlalchemy_utils import database_exists, create_database


DEFAULT_SEEDS_PATH = os.path.join("db", "seeds.py")


@click.group()
def db():
    """
    Manage your SQL database.
    """
    pass


@db.command()
@click.option("--with-testdb/--no-with-testdb",
              default=False, show_default=True, help="Create a test DB too?")
@click.pass_context
@with_appcontext
def reset(ctx, with_testdb):
    """
    Drop, create and seed your database (careful in production).
    """
    db = current_app.extensions["sqlalchemy"].db
    db_uri = current_app.config["SQLALCHEMY_DATABASE_URI"]

    if not database_exists(db_uri):
        create_database(db_uri)

    db.drop_all()
    db.create_all()

    if with_testdb:
        db_uri = f"{db_uri}_test"

        if not database_exists(db_uri):
            create_database(db_uri)

    ctx.invoke(seed)

    return None


@db.command()
@with_appcontext
def seed():
    """
    Seed the database with your custom records.
    """
    seeds_path = current_app.config.get("FLASK_DB_SEEDS_PATH",
                                        DEFAULT_SEEDS_PATH)
    exec(open(seeds_path).read())

    return None


@db.command()
@click.option("--with-testdb/--no-with-testdb",
              default=False, show_default=True, help="Create a test DB too?")
@click.pass_context
@with_appcontext

