import sqlite3
from sqlite3 import Error
import os
import cmd
from datetime import date

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

# The table needs to be expanded so that each entry has 8 columns


def main():
    # Store directory and database paths in constant variables
    initialise_directory_variables()

    # Create conncetion to SQL database
    global database_connection
    database_connection = create_database_connection(DATABASE_FILE_PATH)

    # Create a table in the database
    create_database_table(sql_create_tickets_table)

    # Test submission of a ticket to the database
    # ticket_1 = ("Every time I open your tool it crashes my laptop!", 10, "2023-20-02")
    # create_ticket(ticket_1)
    MainLoop().cmdloop()
    # Print tables contents to the console
    database_connection.close()


class MainLoop(cmd.Cmd):
    intro = "Welcome to the ticket manager, type help or ? to list commands."
    prompt = ">>"

    def do_list(self, arg):
        """get all the tickets"""
        print_table()

    def do_list_specific(self, arg):
        """gets a specific ticket, enter the id of the ticket you want e.g. print_ticket 1"""
        if not arg.isnumeric():
            print("Argument cannot be string")
            return
        if arg == "":
            print("No argument provided")
            return
        print_ticket(arg[0])

    def do_count(self, arg):
        """Gets the number of active tickets"""
        print_number_of_active_tickets()

    def do_create(self, arg):
        """Creates a ticket and adds it to the tickets table"""
        description = input("Please describe your problem: ")
        priority = int(input("Please enter a priority for your ticket between 1 and 10: "))
        current_date = date.today().strftime("%d/%m/%Y")

        ticket = (description, priority, current_date)
        create_ticket(ticket)

    def do_delete(self, arg):
        """Removes a ticket from the table using its ID"""
        if not arg.isnumeric():
            print("Argument cannot be string")
            return
        if arg == "":
            print("No argument provided")
            return
        delete_ticket(arg[0])


def initialise_directory_variables():
    global DIRNAME
    DIRNAME = os.path.dirname(__file__)

    global DATABASE_FILE_PATH
    DATABASE_FILE_PATH = os.path.join(DIRNAME, database_filename)


def create_database_connection(database_file):
    conn = None
    try:
        conn = sqlite3.connect(database_file)
        print("Successfully connected to database")
        return conn
    except Error as error:
        print(error)


def create_database_table(create_table_sql):
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


def delete_ticket(ticket_id):
    ticket_id = ticket_id.strip()
    sql = """DELETE FROM tickets WHERE id ="""+ticket_id
    cur = database_connection.cursor()
    cur.execute(sql)
    database_connection.commit()


def print_table():
    cur = database_connection.cursor()
    cur.execute("SELECT * FROM tickets")
    # Can be replaced with the property name I'm trying to get
    tickets = cur.fetchall()
    for ticket in tickets:
        print(ticket)


def print_number_of_active_tickets():
    cur = database_connection.cursor()
    cur.execute("SELECT COUNT(*) FROM tickets")
    print(cur.fetchone()[0])


def print_ticket(ticket_id):
    ticket_id = ticket_id.strip()
    cur = database_connection.cursor()
    cur.execute("SELECT * FROM tickets WHERE id ="+ticket_id)
    print(cur.fetchall())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
