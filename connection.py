from psycopg2 import connect

settings = {
    'host': 'localhost',
    'database': 'flask_shop',
    'user': 'postgres',
    'password': 'postgres',
    'port': '5432'
}


def connect_to_db():
    connection = connect(**settings)
    return connection
