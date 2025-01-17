import psycopg2
import configparser

config = configparser.ConfigParser()
config.read("settings_db.ini")

HOST = config["DB"]["host"]
PORT = config["DB"]["port"]
DATABASE = config["DB"]["database"]
USER = config["DB"]["user"]
PASSWORD = config["DB"]["password"]


def delete_db(cursor):
    cursor.execute('''
    DROP TABLE IF EXISTS users CASCADE;
    DROP TABLE IF EXISTS found CASCADE;
    DROP TABLE IF EXISTS favourites CASCADE;
    ''')
    conn.commit()


def create_db(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        user_id integer PRIMARY KEY);

    CREATE TABLE IF NOT EXISTS found(
        found_id integer PRIMARY KEY,
        user_id integer not null REFERENCES users(user_id),
        first_name varchar(50),
        last_name varchar(50),
        age integer,
        gender varchar(10),
        city varchar(50));
        
    CREATE TABLE IF NOT EXISTS favourites(
        user_id integer REFERENCES users(user_id),
        found_id integer REFERENCES found(found_id),
        CONSTRAINT pk PRIMARY KEY (user_id, found_id));        
    ''')
    conn.commit()


if __name__ == '__main__':
    conn = psycopg2.connect(host=HOST, port=PORT, database=DATABASE, user=USER, password=PASSWORD)

    with conn.cursor() as cur:

        create_db(cur)

    conn.close()
