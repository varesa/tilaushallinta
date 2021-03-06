from __future__ import with_statement
from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.dialects import mysql
from sqlalchemy import Boolean
from logging.config import fileConfig

import os.path
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parent_dir)

import db_env
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

from tilaushallinta import models
target_metadata = models.Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def fix_config_url():
    """
    Insert database host, user and password to alembic config.
    """
    url = config.get_main_option('sqlalchemy.url')
    url = db_env.substitute(url)
    config.set_main_option('sqlalchemy.url', url)


def boolean_compare_type(context, inspected_column,
        metadata_column, inspected_type, metadata_type):
    """
    Custom type comparision to prevent migrations from attempting to convert TINYINTs to BOOLEANs as
    mysql does the opposite.

    When comparing other types falls back to default compare_type
    """
    if isinstance(inspected_type, mysql.TINYINT) and isinstance(metadata_type, Boolean):
        return False
    else:
        return None


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, compare_type=boolean_compare_type)

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    engine = engine_from_config(
                config.get_section(config.config_ini_section),
                prefix='sqlalchemy.',
                poolclass=pool.NullPool)

    connection = engine.connect()
    context.configure(
                connection=connection,
                target_metadata=target_metadata,
                compare_type=boolean_compare_type
                )

    try:
        with context.begin_transaction():
            context.run_migrations()
    finally:
        connection.close()

fix_config_url()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

