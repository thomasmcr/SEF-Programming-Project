import sqlite3
from sqlite3 import Error
import os
import cmd
from datetime import date
import database_manager
from database_manager import *


def main():
    # Connect to database
    database_manager.initialise()

    # Start the CMD library mainloop
    MainLoop().cmdloop()

    # Close the database
    database_manager.close()


class MainLoop(cmd.Cmd):
    intro = "Welcome to the ticket manager, type help or ? to list commands. To create a new ticket simply type: create"
    prompt = ">>"

    def do_list(self, arg):
        """Prints ticket with matching ID to the console. If no ID is provided, all tickets are printed
            >>list   | prints all tickets
            >>list 1 | prints ticket with an ID of 1
        """
        print("Primary Key | Software Name | Description | Email | Priority | Submit Date | Resolved | Comment "
              "| Resolved Date")
        if get_number_of_active_tickets() <= 0:
            print("There are no active tickets")
            return
        elif arg == "":
            for ticket in get_table():
                print(ticket)
        elif not arg.isnumeric():
            print("Argument must be an integer ID")
            return
        else:
            print(get_ticket(arg[0]))

    def do_exit(self, arg):
        """Exits the application"""
        print("Powering down :O")
        return True

    def do_count(self, arg):
        """Gets the number of active tickets"""
        count = get_number_of_active_tickets()
        print("There are " + str(count) + " active tickets")

    def do_create(self, arg):
        """Creates a new ticket
            >>Create  | Opens the ticket creation form
        """
        current_date = date.today().strftime("%d/%m/%Y")
        software_name = validate_string_input("Please enter the name of the software package the ticket relates to: ")
        description = validate_string_input("Please describe your problem: ")
        email = validate_string_input("Enter a contact email so we can get back to you: ")
        priority = 5
        submit_date = current_date
        resolved = False

        ticket = (software_name, description, email, priority, submit_date, resolved, None, None)
        create_ticket(ticket)

    def do_delete(self, arg):
        """Removes a ticket from the table using its ID"""
        if not arg.isnumeric():
            print("Argument cannot be string")
            return
        elif arg == "":
            print("No argument provided")
            return
        elif not check_ticket_exists(arg[0]):
            print("No ticket with given ID")
            return
        else:
            delete_ticket(arg[0])

    def do_amend(self, arg):
        """Amends ticket with the given ID
            >>amend 1  | amends the details of ticket with ID 1
        """
        if arg == "":
            print("Please provide a valid ticket ID")
            return
        elif not arg.isnumeric():
            print("Argument must be an integer ID")
            return

        if not database_manager.check_ticket_exists(arg[0]):
            print("Ticket can't be amended as no ticket with that ID exists")
            return

        old_ticket = database_manager.get_ticket(arg[0])

        print(old_ticket)

        current_date = date.today().strftime("%d/%m/%Y")
        software_name = validate_string_input("Enter the amended software name: ")
        description = validate_string_input("Enter the amended description: ")
        email = validate_string_input("Enter the amended contact email: ")

        priority = 5
        submit_date = current_date
        resolved = False
        amended_ticket = (software_name, description, email, priority, submit_date, resolved, None, None)
        database_manager.amend_ticket(arg[0], amended_ticket)

    def do_resolve(self, arg):
        """Sets ticket with the given ID to resolved
            >>resolve 1 | resolves ticket and lets you provide a resolution comment
        """
        if arg == "":
            print("Please provide a valid ticket ID")
            return
        elif not arg.isnumeric():
            print("Argument must be an integer ID")
            return

        if not check_ticket_exists(arg[0]):
            print("Ticket can't be resolved as no ticket with that ID exists")
            return

        resolution_comment = validate_string_input("Enter a resolution comment: ")
        resolve_ticket(arg[0], resolution_comment)

    def do_resolved(self, arg):
        """Lists all resolved tickets
            >>resolved | prints resolved tickets to console
        """

        if get_number_of_active_tickets() <= 0:
            print("There are no active tickets")
            return

        print("Ticket ID, Software Name, Description, Contact Email, Priority, Submission Date, "
              "Resolved, Resolution Comment, Resolved Date \n")
        for ticket in get_resolved_tickets():
            print(ticket)


# Ensures that string input isn't blank
def validate_string_input(message):
    string_input = input(message)
    if len(string_input) and string_input != "":
        return string_input.lower()
    else:
        print("Invalid input, ensure field isn't blank")
        return validate_string_input(message)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
