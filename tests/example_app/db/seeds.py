# This file should contain records you want created when you run flask db seed.
#
# Example:
from tests.example_app.example.app import User


initial_user = {
    'username': 'superadmin'
}
if User.find_by_username(initial_user['username']) is None:
    User(**initial_user).save()

print('This print statement is only here for the test suite'.)
