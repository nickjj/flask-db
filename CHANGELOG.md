# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a
Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

- Nothing yet!

## [0.3.0] - 2020-11-27

### Removed

- `--no-with-testdb` option for `flask db reset` since that is the behavior
  when `--with-testdb` is omit

## [0.2.0] - 2020-11-20

### Added

- `flask db init` to generate Alembic config files and a `seeds.py` file
- `flask db migrate` which forwards all commands straight to the `alembic` CLI

### Changed

- `flask db init` in its original form has been replaced with `flask db reset`
- `flask db seed` will fail with a helpful error if `seeds.py` cannot be found

## [0.1.1] - 2020-11-19

### Fixed

- A flake8 malfunction that caused a syntax error in the example `seeds.py` file

## [0.1.0] - 2020-11-19

### Added

- Everything!

[Unreleased]: https://github.com/nickjj/flask-db/compare/0.3.0...HEAD
[0.3.0]: https://github.com/nickjj/flask-db/compare/0.2.0...0.3.0
[0.2.0]: https://github.com/nickjj/flask-db/compare/0.1.1...0.2.0
[0.1.1]: https://github.com/nickjj/flask-db/compare/0.1.0...0.1.1
[0.1.0]: https://github.com/nickjj/flask-db/releases/tag/0.1.0
