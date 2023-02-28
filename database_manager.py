import os
import sqlite3
from sqlite3 import Error


database_filename = "ticket_database"
database_connection = sqlite3.Connection
# I've built the validation rules into the table itself, data cannot be entered into the table if it is not of the
# correct type and meets the conditions defined inside the CHECK() statement
sql_create_tickets_table = """ 
CREATE TABLE IF NOT EXISTS tickets (
    id integer PRIMARY KEY NOT NULL UNIQUE,
    software_name text NOT NULL CHECK(length(software_name) > 0),
    description text NOT NULL CHECK(length(description) > 0),
    email text NOT NULL CHECK(length(email) > 0), 
    priority integer CHECK(priority <= 10 and priority >= 1) NOT NULL,
    submit_date text NOT NULL,
    resolved boolean NOT NULL,
    resolution_comment text,
    resolution_date text 
); """



def initialise():
    # Directory of the project
    directory = os.path.dirname(__file__)

    # Directory of the database file
    database_directory = os.path.join(directory, database_filename)

    # Create the database connection
    global database_connection
    database_connection = create_database_connection(database_directory)

    # Create the tickets table
    create_database_table(sql_create_tickets_table)


def close():
    database_connection.close()


def create_database_connection(database_file):
    conn = None
    try:
        conn = sqlite3.connect(database_file)
        return conn
        print("Successfully connected to database")
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
    sql = """INSERT INTO tickets(software_name,description,email,priority,submit_date,
             resolved,resolution_comment,resolution_date)
             VALUES(?,?,?,?,?,?,?,?) """
    cur = database_connection.cursor()
    cur.execute(sql, ticket)
    database_connection.commit()


def delete_ticket(ticket_id):
    ticket_id = ticket_id.strip()
    sql = """DELETE FROM tickets WHERE id ="""+ticket_id
    cur = database_connection.cursor()
    cur.execute(sql)
    database_connection.commit()


def amend_ticket(ticket_id, amended_ticket):
    sql = """UPDATE tickets SET software_name = ?,
    description = ?, email = ?, priority = ?, submit_date = ?, 
    resolved = ?, resolution_comment = ?, resolution_date = ? WHERE id="""+ticket_id
    cur = database_connection.cursor()
    cur.execute(sql, amended_ticket)
    database_connection.commit()


def get_table():
    cur = database_connection.cursor()
    cur.execute("SELECT * FROM tickets")
    # Can be replaced with the property name I'm trying to get
    tickets = cur.fetchall()
    return tickets


def get_number_of_active_tickets():
    cur = database_connection.cursor()
    cur.execute("SELECT COUNT(*) FROM tickets")
    return cur.fetchone()[0]


def get_ticket(ticket_id):
    ticket_id = ticket_id.strip()
    cur = database_connection.cursor()
    cur.execute("SELECT * FROM tickets WHERE id ="+ticket_id)
    ticket = cur.fetchall()
    return ticket


# Returns true if a ticket exists with the given ID
def check_ticket_exists(ticket_id):
    sql = """SELECT * FROM tickets WHERE id="""+ticket_id
    cur = database_connection.cursor()
    cur.execute(sql)
    tickets = cur.fetchall()
    if(len(tickets)) == 0:
        return False
    return True


# Checks the date in the tickets table is valid and isn't corrupt. should be called before reading or after writing to
# the database
def validate_table_contents():
    for ticket in get_table():
        ticket_id = ticket[0]
        description = ticket[1]
        priority = ticket[3]
        submit_date = ticket[4]






