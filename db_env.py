import os
import sys

var_host = "DBHOST"
file_host = "config/dbhost"

var_port = "PORT"
file_port = "config/dbport"

var_user = "DBUSER"
file_user = "config/dbuser"

var_pass = "DBPASS"
file_pass = "config/dbpassword"

var_schema = "DBSCHEMA"
file_schema = "config/dbschema"


def _get_value(var_name, file_name, default=None):
    if var_name in os.environ.keys() and len(os.environ[var_name]) > 0:
        return os.environ[var_name].strip()
    elif os.path.isfile(file_name):
        with open(file_name) as f:
            return f.readline().strip()
    elif default:
        return default
    else:
        print("Neither ENV['" + var_name + "'] or file " + file_name + " provided")
        sys.exit(1)


def get_host():
    return _get_value(var_host, file_host, '127.0.0.1')


def get_port():
    return _get_value(var_port, file_port, '3306')


def get_user():
    return _get_value(var_user, file_user)


def get_pass():
    return _get_value(var_pass, file_pass)


def get_schema():
    return _get_value(var_schema, file_schema)


def substitute(url):
    return (
        url
        .replace('<host>', get_host())
        .replace('<port>', get_port())
        .replace('<user>', get_user())
        .replace('<password>', get_pass())
        .replace('<schema>', get_schema())
    )
