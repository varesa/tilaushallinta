import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'alembic ~= 1.4',
    'bcrypt ~= 3.2',
    'mysqlclient ~= 2.0',
    'pyramid ~= 1.10',
    'pyramid_chameleon ~= 0.3',
    'pyramid_debugtoolbar ~= 4.6',
    'pyramid_tm ~= 2.4',
    'pyramid_exclog ~= 1.0',
    'python-dateutil ~= 2.8',
    'SQLAlchemy ~= 1.3.19',
    'SQLAlchemy-Continuum ~= 1.3.11',
    'transaction ~= 3.0',
    'waitress ~= 2.1.2',
    'zope.sqlalchemy ~= 1.3',
    ]

setup(name='tilaushallinta',
      version='0.0',
      description='tilaushallinta',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='tilaushallinta',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = tilaushallinta:main
      [console_scripts]
      initialize_tilaushallinta_db = tilaushallinta.scripts.initializedb:main
      """,
      )
