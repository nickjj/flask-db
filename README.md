# What is Flask-DB? ![CI](https://github.com/nickjj/flask-db/workflows/CI/badge.svg?branch=master)

It's a Flask CLI extension that helps you migrate, drop, create and seed your
SQL database.

After installing it you'll gain access to a `flask db` command that will give
you a few database management commands to use.

For the migrations it uses Alembic. Anything you can do with Alembic can be
done with this CLI extension. If you're wondering why you might want to use
this tool instead of Alembic directly or Flask-Migrate, [check out this FAQ
item](#differences-between-alembic-flask-migrate-flask-alembic-and-flask-db).

## Table of contents

- [Installation](#installation)
- [Ensuring the `db` command is available](#ensuring-the-db-command-is-available)
- [Going over the `db` command and its sub-commands](#going-over-the-db-command-and-its-sub-commands)
- [FAQ](#faq)
  - [Differences between Alembic, Flask-Migrate, Flask-Alembic and Flask-DB](#differences-between-alembic-flask-migrate-flask-alembic-and-flask-db)
  - [Migrating from using Alembic directly or Flask-Migrate](#migrating-from-using-alembic-directly-or-flask-migrate)
  - [Is it safe to edit the files that `flask db init` created?](#is-it-safe-to-edit-the-files-that-flask-db-init-created)
  - [Should I add migration the files to version control?](#should-i-add-the-migration-files-to-version-control)
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
- Alembic 1.3+

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
  db      Migrate and manage your SQL database.
```

If all went as planned you should see the new `db` command added to your
list of commands.

## Going over the `db` command and its sub-commands

Running `flask db --help` will produce this help menu:

```sh
Usage: flask db [OPTIONS] COMMAND [ARGS]...

  Migrate and manage your SQL database.

Options:
  --help  Show this message and exit.

Commands:
  init     Generate Alembic config files and seeds.py.
  seed     Seed the database with your custom records.
  reset    Drop, create and seed your database (careful in production).
  migrate  Wrap the alembic CLI tool (defaults to running upgrade head).
```

### `init`

If you've ever used Alembic before, you'll be familiar with `alembic init`.  If
you've never used it before it creates an `alembic.ini` file in the root of
your project along with a few other Alembic files in a `yourappname/migrations`
directory by default.

You can treat `flask db init` as a drop in replacement for `alembic init`.

`flask db init` does something similar. The 4 main differences are:

1. It defaults to `db/` instead of `yourappname/migrations`, but you can modify
   this path by running `flask db init any/path/you/want`.

2. It will create the same Alembic config files but it modifies them to be a
   bit more generic and portable when it comes to finding your
   `SQLALCHEMY_DATABASE_URI`.

3. It also configures Alembic to support auto generating migrations in case you
   want to use `revision --autogenerate` as a starting point for your
   migrations (always review them afterwards!).

4. It creates a `seeds.py` file in the same directory you initialized things to
   (more on this next).

### `seed`

Seeds your database with initial records of your choosing.

When you set up your app for the first time in production chances are you'll
want certain things to be created in your database. At the very least probably
an initial admin user.

This command will read in and execute a `seeds.py` file that exists in the
directory that you initialized with `flask db init`. By default that will be
`db/seeds.py`.

If you supplied a custom init path you must change your seeds path. You can do
that by setting `FLASK_DB_SEEDS_PATH` in your app's config. For example if you
ran `flask db init yourappname/migrations` then you'd set `FLASK_DB_SEEDS_PATH
= "yourappname/migrations/seeds.py"`.

As for the seeds file, you have full control over what you want to do. You can
add whatever records that make sense for your app or keep the file empty to not
seed anything.

#### Best practices for seeding data

It's a good idea to make your seeds file idempotent. Meaning, if you run it 1
time or 100 times the end result should be the same. The [example in the seeds
file](https://github.com/nickjj/flask-db/tree/master/tests/example_app/db/seeds.py)
is idempotent because it first checks to see if the user exists before adding
it.

If the user exists, it skips trying to create the user. Without this check then
you would end up getting a database uniqueness constraint error on the 2nd run.
That's because the example test app added a [unique index on the
username](https://github.com/nickjj/flask-db/blob/master/tests/example_app/example/app.py#L20).

### `reset`

Creates your database if it needs to be created along with doing a
`db.drop_all()` and `db.create_all()`.  That is going to purge all of your
existing data and create any tables based on whatever SQLAlchemy models you
have.

It also automatically calls `flask db seed` for you.

#### Options

```
Options:
  --with-testdb  Create a test DB in addition to your main DB?
```

If you run `flask db reset --with-testdb` then a second database will also be
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
changes you should be creating database migrations with `flask db migrate`,
which is really running [Alembic](https://alembic.sqlalchemy.org/en/latest/)
commands behind the scenes. That is the official migration tool created by the
same folks who made SQLAlchemy.

That leads us into the next command.

### `migrate`

The `flask db migrate` command is an alias to the `alembic` command.

Here's a few examples:

```sh
flask db migrate revision -m "hi" -> alembic revision -m "hi"
flask db migrate upgrade head     -> alembic upgrade head
flask db migrate                  -> alembic upgrade head (convenience shortcut)
flask db migrate -h               -> alembic -h
```

Every possible thing you can run with `alembic` can now be run with `flask db
migrate`. That means you can follow Alembic's tutorials and documentation
exactly.

You can still use alembic commands directly if you prefer. I just liked the
idea of having all db related commands under the same namespace and the `flask
db migrate` shortcut is handy.

You'll also be happy to hear that this tool doesn't hard code all of Alembic's
commands, options and arguments with hundreds of lines of code. What that means
is, as Alembic's CLI API changes in the future this `flask db migrate` command
will continue to work with all future versions.

All it does is forward everything you pass in, similar to `$@` in Bash.

That's also why you need to run `-h` to get Alembic's help menu instead of
`--help` because that will ultimately call the internal help menu for `flask db
migrate`.

## FAQ

### Differences between Alembic, Flask-Migrate, Flask-Alembic and Flask-DB

Here's the breakdown of these tools:

*Disclaimer: I'm not here to crap on the work of others, I'm simply giving my
opinion on why I chose to create Flask-DB and don't use the Alembic CLI
directly, Flask-Migrate or Flask-Alembic.*

#### Alembic

The official database migration tool for SQLAlchemy written by the same team
who made SQLAlchemy.

Alembic generates a bunch of config files and often times you'll want to go in
and edit them to be more dynamic for finding your `SQLALCHEMY_DATABASE_URI` as
well as adding a few useful opinions that you'll want in 99.999% of apps.

It got a little tedious making these adjustments in every app.

Besides having config files, Alembic also includes an `alembic` CLI tool to
interact with your database such as generating migration files, executing
migrations and more. This tool is fantastic.

Flask-Migrate, Flask-Alembic and Flask-DB all use Alembic behind the scenes,
but they are implemented in much different ways.

#### Flask-Migrate

At the time of writing this FAQ item (November 2020) the approach this library
takes is to manually map `alembic` commands, options and arguments internally.
That leads to hundreds upon hundreds of lines of code to carefully mimic
Alembic's API.

In my opinion this is very error prone and also not future proof.

For example, here's a tiny snippet of code from [Flask-Migrate's `migrate`
command](https://github.com/miguelgrinberg/Flask-Migrate/blob/4887bd53bc08f10087fe27a4a7d9fe853031cdcf/flask_migrate/cli.py#L64=L90):

```py
@db.command()
@click.option('-d', '--directory', default=None,
              help=('Migration script directory (default is "migrations")'))
@click.option('-m', '--message', default=None, help='Revision message')
@click.option('--sql', is_flag=True,
              help=('Don\'t emit SQL to database - dump to standard output '
                    'instead'))
@click.option('--head', default='head',
              help=('Specify head revision or <branchname>@head to base new '
                    'revision on'))
@click.option('--splice', is_flag=True,
              help=('Allow a non-head revision as the "head" to splice onto'))
@click.option('--branch-label', default=None,
              help=('Specify a branch label to apply to the new revision'))
@click.option('--version-path', default=None,
              help=('Specify specific path from config for version file'))
@click.option('--rev-id', default=None,
              help=('Specify a hardcoded revision id instead of generating '
                    'one'))
@click.option('-x', '--x-arg', multiple=True,
              help='Additional arguments consumed by custom env.py scripts')
@with_appcontext
def migrate(directory, message, sql, head, splice, branch_label, version_path,
            rev_id, x_arg):
    """Autogenerate a new revision file (Alias for 'revision --autogenerate')"""
    _migrate(directory, message, sql, head, splice, branch_label, version_path,
             rev_id, x_arg)
```

Needless to say when you do this for a dozen commands with many dozens of flags
it's easy for errors to slip by. It also requires waiting for Flask-Migrate to
release a new build if Alembic changes how their CLI tool works.

Another thing is Flask-Migrate's `flask db migrate` command defaults to using
auto-generated migrations. This feature is useful for speeding up the process
of creating migration files but Alembic doesn't detect everything which can be
very confusing if you're not aware of [Alembic's limitations with
auto-generate](https://alembic.sqlalchemy.org/en/latest/autogenerate.html#what-does-autogenerate-detect-and-what-does-it-not-detect).

There's also no help for doing things like managing and seeding your database.
It's a tool exclusively designed for running database migrations with Alembic.

#### Flask-Alembic

This tool internally imports the Alembic Python library and creates its own CLI
around that. Not of all of the commands are API compatible with the `alembic`
CLI.

For example, here's a snippet from [Flask-Alembic's `revision`
command](https://github.com/davidism/flask-alembic/blob/c8f202d4522123760a52865b6d3806470fa396e9/src/flask_alembic/cli/script.py#L94-L117):

```py
@manager.option("message")
@manager.option("--empty", action="store_true", help="Create empty script.")
@manager.option(
    "-b", "--branch", default="default", help="Use this independent branch name."
)
@manager.option(
    "-p",
    "--parent",
    default="head",
    type=str.split,
    help="Parent revision(s) of this revision.",
)
@manager.option("--splice", action="store_true", help="Allow non-head parent revision.")
@manager.option(
    "-d", "--depend", type=str.split, help="Revision(s) this revision depends on."
)
@manager.option(
    "-l", "--label", type=str.split, help="Label(s) to apply to the revision."
)
@manager.option("--path", help="Where to store the revision.")
def revision(message, empty, branch, parent, splice, depend, label, path):
    """Create new migration."""

    base.revision(message, empty, branch, parent, splice, depend, label, path)
```

It's missing a few flags that `alembic revision --help` would provide you.
Personally I'd rather use the official `alembic` CLI since it already exists
and it's very well tested and developed by the Alembic team.

Also, it doesn't handle `alembic init` or have its own form of `init` so you're
left having to generate and modify the default Alembic config files in every
project.

Like Flask-Migrate it also doesn't help with resetting and seeding your
database.

#### Flask-DB

Flask-DB is more than a database migration tool that wraps Alembic. It also
includes being able to reset and seed your database.

Unlike using Alembic directly it modernizes and applies a few opinions to the
default Alembic configuration so that you can usually use these files as is in
your projects.

As for migrations, it wraps the `alembic` CLI but it does it with about 5 lines
of code for everything rather than hundreds of lines of code. The lines of code
aren't that important, it's mainly being future proof and less error prone.

Since about 2015 I used to create my own `db` CLI command in each project which
handled resetting and seeding the database. Then I used Alembic directly.
Anyone who has taken my [Build a SAAS App with Flask
course](https://buildasaasappwithflask.com/?utm_source=github&utm_medium=flaskdb&utm_campaign=readme)
is probably used to that. 

Flask-DB was created as an improvement to that work flow. Now it's as easy as
pip installing this tool and you're good to go with ready to go configs, a
consistent Alembic CLI API and the added reset + seed functionality.

### Migrating from using Alembic directly or Flask-Migrate

You have 2 options depending on what you want to do:

#### 1. Keep all of your existing Alembic files and directory structure

By default Alembic (and therefore Flask-Migrate) will put a `migrations/`
directory inside of your application.

You can still keep your files there with Flask-DB too. You'll just need to
configure `FLASK_DB_SEEDS_PATH` to be `yourappname/migrations/seeds.py`. You'll
also want to create that file manually (keeping it empty for now is ok).

That's pretty much all you need to do.

If you're using Flask-Migrate, Flask-DB has more up to date Alembic config
files so you may still want to initialize a new directory with `flask db init`.
Then you can pick and choose what you want to keep from your existing Alembic
configs and what's been generated by the Flask-DB's init command.

#### 2. Initialize a new directory and move your `versions/` into it (recommended)

The other option would be to run `flask db init` and let it create a `db/`
directory in the root of your project.

Chances are you already have an `alembic.ini` file. The init command will
recognize that and create an `alembic.ini.new` file to avoid clobbering your
existing file. Then you can delete your old `alembic.init` file and `mv
alembic.ini.new alembic.ini` to use the new one.

From here you can take your existing migration files in your old `versions/`
directory and move them into `db/versions/`. At this point you can delete your
old `yourappname/migrations/` directory as long as you haven't done any drastic
customizations to your alembic related config files.

If you've done a bunch of custom configurations that's ok, you can manually
merge in your changes. You're free to edit these files however you see fit.

### Is it safe to edit the files that `flask db init` created?

Absolutely. The init command is there to set up the initial files that Alembic
expects to be created, along with adding things like the `seeds.py` file too.

The Alembic files will likely be good to go for you without having to modify
anything but you can change them however you see fit. One thing worth
mentioning is if your app factory function isn't called `create_app` you will
want to change the `db/env.py` file's import near the top to use your custom
factory function's name instead.

You also have free reign to add whatever you want to the `seeds.py` file. By
default it generates a couple of comments to help show how you can use it
generate an initial user in your database.

### Should I add the migration files to version control?

Yes! Your `alembic.ini` along with your entire `db/` directory (default `init`
directory) including the `versions/*` files should all be commit to version
control.

This way you can develop and test your migrations locally on your dev box, make
sure everything works then commit and push your code. At that point you can run
your migrations in CI and ultimately in production with confidence that it all
works.

## About the author

- Nick Janetakis | <https://nickjanetakis.com> | [@nickjanetakis](https://twitter.com/nickjanetakis)

If you're interested in learning Flask I have a 20+ hour video course called
[Build a SAAS App with
Flask](https://buildasaasappwithflask.com/?utm_source=github&utm_medium=flaskdb&utm_campaign=readme).
It's a course where we build a real world SAAS app. Everything about the course
and demo videos of what we build is on the site linked above.
