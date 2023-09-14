import subprocess
import os

import click

from flask import current_app
from flask.cli import with_appcontext
from sqlalchemy_utils import database_exists, create_database

from flask_db.init import generate_configs


DEFAULT_SEEDS_PATH = os.path.join("db", "seeds.py")


@click.group()
def db():
    """
    Migrate and manage your SQL database.
    """
    pass


@db.command()
@click.argument("path", default="db/")
@with_appcontext
def init(path):
    """
    Generate Alembic config files and seeds.py.
    """
    copied_files, existing_files = generate_configs(path,
                                                    current_app.import_name)

    if copied_files is not None:
        msg = f"""alembic.ini was created in the root of your project
{path} was created with your Alembic configs, versions/ directory and seeds.py
"""
        click.echo(msg)

    if existing_files:
        click.echo("Also, you already had these files in your project:\n")

        for file in existing_files:
            click.echo(f"  {file[0]}")

        msg = """
Instead of aborting or erroring out, a new version of any existing files have
been created with a .new file extension in their respective directories.

Now you can diff them and decide on what to do next.

Chances are you'll want to use the .new version of any file but if you have
any custom Alembic configuration you may want to copy those changes over.

If you want to use the .new file as is you can delete your original file and
then rename the .new file by removing its .new file extension."""
        click.echo(msg)

    return None


@db.command()
@click.option("--with-testdb", is_flag=True,
              help="Create a test DB in addition to your main DB?")
@click.pass_context
@with_appcontext
def reset(ctx, with_testdb):
    """
    Drop, create and seed your database (careful in production).
    """
    db = current_app.extensions["sqlalchemy"]
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

    if os.path.isfile and os.path.exists(seeds_path):
        exec(open(seeds_path).read())
    else:
        msg = f"""{seeds_path} does not exist

If you haven't done so already, run: flask db init

If you're using a custom init path (ie. not db/ (the default)) then you can
define a custom seeds path by setting FLASK_DB_SEEDS_PATH in your app's config.

For example if you did flask db init myapp/migrations then you would want
to set FLASK_DB_SEEDS_PATH = "myapp/migrations/seeds.py"."""
        click.echo(msg)

    return None


@db.command(context_settings=dict(ignore_unknown_options=True))
@click.argument("alembic_args", nargs=-1, type=click.UNPROCESSED)
@with_appcontext
def migrate(alembic_args):
    """Wrap the alembic CLI tool (defaults to running upgrade head)."""
    if not alembic_args:
        alembic_args = ("upgrade", "head")

    cmdline = ["alembic"] + list(alembic_args)

    subprocess.call(cmdline)

    return None
