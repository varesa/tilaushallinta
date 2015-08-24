import os
import sys

var_host = "DBHOST"
file_host= "dbhost"
var_user = "DBUSER"
file_user = "dbuser"
var_pass = "DBPASS"
file_pass = "dbpassword"


def get_host():
    if var_host in os.environ.keys() and len(os.environ[var_host]) > 0:
        return os.environ[var_host].strip()
    elif os.path.isfile(file_host):
        with open(file_host) as host:
            return host.readline().strip()
    else:
        print("Neither ENV['" + var_host + "'] or file " + file_host + " provided")
        sys.exit(1)


def get_user():
    if var_user in os.environ.keys() and len(os.environ[var_user]) > 0:
        return os.environ[var_user].strip()
    elif os.path.isfile(file_user):
        with open(file_user) as user:
            return user.readline().strip()
    else:
        print("Neither ENV['" + var_user + "'] or file " + file_user + " provided")
        sys.exit(1)


def get_pass():
    if var_pass in os.environ.keys() and len(os.environ[var_pass]) > 0:
        return os.environ[var_pass].strip()
    elif os.path.isfile(file_pass):
        with open(file_pass) as passwd:
            return passwd.readline().strip()
    else:
        print("Neither ENV['" + var_pass + "'] or file " + file_pass + " provided")
        sys.exit(1)

def substitute(url):
    return url\
        .replace('<host>', get_host())\
        .replace('<user>', get_user())\
        .replace('<password>', get_pass())
