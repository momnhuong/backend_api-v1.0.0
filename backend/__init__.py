import os
# import pymysql

# pymysql.install_as_MySQLdb()


def get_os_env(name, default=None, assert_exist=True):
    if name in os.environ:
        return os.environ[name]
    return default
