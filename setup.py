from setuptools import setup


setup(
    name='Flask-DB',
    version='0.1.1',
    author='Nick Janetakis',
    author_email='nick.janetakis@gmail.com',
    url='https://github.com/nickjj/flask-db',
    description='A Flask CLI extension to help manage your SQL database.',
    license='MIT',
    packages=['flask_db'],
    platforms='any',
    python_requires='>=3.6',
    zip_safe=False,
    install_requires=[
        'Flask>=1.0',
        'SQLAlchemy>=1.2',
        'SQLAlchemy-Utils',
        'Flask-SQLAlchemy>=2.4'
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
