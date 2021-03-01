from setuptools import setup

desc = 'A Flask CLI extension to help migrate and manage your SQL database.'

setup(
    name='Flask-DB',
    version='0.3.1',
    author='Nick Janetakis',
    author_email='nick.janetakis@gmail.com',
    url='https://github.com/nickjj/flask-db',
    description=desc,
    license='MIT',
    packages=['flask_db'],
    setup_requires=['setuptools_scm'],
    include_package_data=True,
    platforms='any',
    python_requires='>=3.6',
    zip_safe=False,
    install_requires=[
        'Flask>=1.0',
        'SQLAlchemy>=1.2',
        'SQLAlchemy-Utils',
        'Flask-SQLAlchemy>=2.4',
        'alembic>=1.3'
    ],
    entry_points={
        'flask.commands': [
            'db=flask_db.cli:db'
        ],
    },
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Database'
    ]
)
