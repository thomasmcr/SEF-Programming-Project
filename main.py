import sqlite3
from sqlite3 import Error
import os


# The name of the database file, this should be set manually
database_filename = "ticket_database"
# The path of the directory
DIRNAME = ""
# The path to the database file
DATABASE_FILE_PATH = r""
database_connection = sqlite3.Connection
sql_create_tickets_table = """ 
CREATE TABLE IF NOT EXISTS tickets (
    id integer PRIMARY KEY,
    name text NOT NULL,
    priority integer,
    submit_date text NOT NULL
); """


def main():
    print("Hello World!")
    # Store directory and database paths in constant variables
    initialise_directory_variables()

    # Create conncetion to SQL database
    global database_connection
    database_connection = create_database_connection(DATABASE_FILE_PATH)

    # Create a table in the database
    create_database_table(sql_create_tickets_table)

    # Test submission of a ticket to the database
    ticket_1 = ("I have a huge problem that with one of your tools", 10, "2023-20-02")
    create_ticket(ticket_1)
    get_table_contents("TICKETS")
    database_connection.close()


def initialise_directory_variables():
    global DIRNAME
    DIRNAME = os.path.dirname(__file__)

    global DATABASE_FILE_PATH
    DATABASE_FILE_PATH = os.path.join(DIRNAME, database_filename)


def create_database_connection(database_file):
    print("Connecting to database...")
    conn = None
    try:
        conn = sqlite3.connect(database_file)
        print("Successfully connected to database")
        return conn
    except Error as error:
        print(error)


def create_database_table(create_table_sql):
    print("Creating table...")
    try:
        c = database_connection.cursor()
        c.execute(create_table_sql)
        print("Successfully created table")
    except Error as error:
        print(error)


def create_ticket(ticket):
    sql = """INSERT INTO tickets(name,priority,submit_date)
                  VALUES(?,?,?) """
    cur = database_connection.cursor()
    cur.execute(sql, ticket)
    database_connection.commit()
    return cur.lastrowid


def get_table_contents(table_name):
    cur = database_connection.cursor()
    cur.execute("SELECT * FROM " + str(table_name))
    print(cur.fetchall())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
