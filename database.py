import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
from os import getenv

load_dotenv()


def get_connection_string():
    host = getenv("PSQL_HOST")
    user = getenv("PSQL_USER_NAME")
    pwd = getenv("PSQL_PASSWORD")
    dbname = getenv("PSQL_DATABASE")

    return f"postgres://{user}:{pwd}@{host}:5432/{dbname}"


def open_connection():
    try:
        connection = psycopg2.connect(get_connection_string())
        connection.autocommit = True
        return connection
    except psycopg2.DatabaseError as e:
        print("\n\nConnection error:\n")
        raise e


def handler(function):
    def wrapper(*args, **kwargs):
        connection = open_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        return_value = function(cursor, *args, **kwargs)
        cursor.close()
        connection.close()
        return return_value

    return wrapper


def run_query(query_string, vars={}, single=False, debug=False):
    connection = open_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cursor.execute(query_string, vars=vars)

    if single:
        result = cursor.fetchone()
    else:
        result = cursor.fetchall()

    if debug:
        print(cursor.query.decode("utf-8"))

    cursor.close()
    connection.close()

    return result
