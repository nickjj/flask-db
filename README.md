# What is Flask-DB? ![CI](https://github.com/nickjj/flask-db/workflows/CI/badge.svg?branch=master)

It's a Flask CLI extension that helps you initialize and seed your SQL database.

After installing it you'll gain access to a `flask db` command that will give
you a few database management commands to use.

## Table of contents

- [Installation](#installation)
- [Ensuring the `db` command is available](#ensuring-the-db-command-is-available)
- [Going over the `db` command and its sub-commands](#going-over-the-db-command-and-its-sub-commands)
- [FAQ](#faq)
  - [Where should I put my Alembic migrations?](#where-should-i-put-my-alembic-migrations)
  - [What about adding additional DB management commands?](#what-about-adding-additional-db-management-commands)
- [About the Author](#about-the-author)

## Installation

`pip3 install Flask-DB`

That's it!

There's no need to even import or initialize anything in your Flask app because
it's just a CLI command that gets added to your Flask app.

*But if you're curious, a complete example Flask app can be found in the
[tests/
directory](https://github.com/nickjj/flask-db/tree/master/tests/example_app).*

#### Requirements:

- Python 3.6+
- Flask 1.0+
- SQLAlchemy 1.2+

## Ensuring the `db` command is available

You'll want to make sure to at least set the `FLASK_APP` environment variable:

```sh
# Replace `hello.app` with your app's name.
export FLASK_APP=hello.app
export FLASK_ENV=development
```

Then run the `flask` binary to see its help menu:

```sh

Usage: flask [OPTIONS] COMMAND [ARGS]...

  ...

Commands:
  db      Manage your SQL database.
```

If all went as planned you should see the new `db` command added to your
list of commands.

## Going over the `db` command and its sub-commands

Running `flask db --help` will produce this help menu:

```sh
Usage: flask db [OPTIONS] COMMAND [ARGS]...

  Manage your SQL database.

Options:
  --help  Show this message and exit.

Commands:
  init   Initialize the database (this will purge your DB!)
  seed   Seed the database with your custom records.
  reset  Initialize and seed the database.
```

### `init`

Creates your database if it needs to be created along with doing a
`db.drop_all()` and `db.create_all()`.

That is going to purge all of your existing data and create any tables based
on whatever SQLAlchemy models you have.

#### Options

```
Options:
  --with-testdb / --no-with-testdb     Create a test DB too?  [default: False]
```

If you run `flask db init --with-testdb` then a second database will also be
created based on whatever your database name is from your
`SQLALCHEMY_DATABASE_URI` along with appending `_test` to its name.

For example, if you had a db named `hello` and you used `--with-testdb` then
you would end up with both a `hello` and `hello_test` database. It's very
useful to have a dedicated test database so you don't clobber your dev data.

#### When should you use this command?

That depends on the state of your project.

##### Brand new project that you never deployed?

This is something you'll be running all the time in development as you change
your database models.

It's also something you'd typically run once in production the first time you
deploy your app.

##### Deployed your app at least once?

Purging all of your data isn't an option anymore. If you want to make database
changes you should be creating database migrations with
[Alembic](https://alembic.sqlalchemy.org/en/latest/).  That is the official
migration tool created by the same folks who made SQLAlchemy.

This isn't a downside or anything related to using this CLI extension. Running
migrations to change your data without deleting everything is a standard
practice.

### `seed`

Seeds your database with initial records of your choosing.

When you set up your app for the first time in production chances are you'll
want certain things to be created in your database. At the very least probably
an initial admin user.

This command will read in and execute a `seeds.py` file that you create in a
specific location (the path is configurable). This way you have full control
over what gets created in your seeds.

By default it looks for a `db/seeds.py` file in your project. If you want to
customize the path you can set `FLASK_DB_SEEDS_PATH` to whatever you want in
your app's config, as long as the path already exists.

The [tests/
directory](https://github.com/nickjj/flask-db/tree/master/tests/example_app)
has an example app set up to use the default path along with an example
`seeds.py` file that adds a new user to the database if it doesn't already
exist.

It's a good idea to make your seeds file idempotent. Meaning, if you run it 1
time or 100 times the end result should be the same. The example seeds file is
idempotent because it first checks to see if the user exists before adding it.

If the user exists, it skips trying to create the user. Without this check then
you would end up getting a database uniqueness constraint error on the 2nd run.
That's because the example test app added a unique index on the username.

### `reset`

This calls both `init` and `seed` for you under the hood.

#### Options

```
Options:
  --with-testdb / --no-with-testdb     Create a test DB too?  [default: False]
```

This is a convenience command so that you don't have to run both an init &&
seed.

In production you'll likely choose to run a `flask db reset` when you first set
up your app. This way you don't have a test database created in production and
your main db will be created, initialized and seeded.

In development I typically run `flask db reset --with-testdb` all the time on
projects I haven't deployed yet.

## FAQ

### Where should I put my Alembic migrations?

That's a bit out of scope for this package but personally I do an `alembic init
db` and I add in the `seeds.py` file afterwards. This way all of your database
related files are in 1 spot.

That's partly why I made the seeds path configurable. Now you have full control
where to put both your seeds file and your Alembic related files. You could
even choose not to use `flask db seeds`. It's up to you!

### What about adding additional DB management commands?

It's possible new commands will be added in the future. If you have any
suggestions please open an issue.

I've been using the `init`, `seed`, `reset` pattern in my Flask apps since
2015, and up until I open sourced this package most of this code was copy /
pasted between projects and evolved over time.

## About the author

- Nick Janetakis | <https://nickjanetakis.com> | [@nickjanetakis](https://twitter.com/nickjanetakis)

If you're interested in learning Flask I have a 20+ hour video course called
[Build a SAAS App with
Flask](https://buildasaasappwithflask.com/?utm_source=github&utm_medium=flaskdb&utm_campaign=readme).
It's a course where we build a real world SAAS app. Everything about the course
and demo videos of what we build is on the site linked above.
