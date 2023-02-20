import tkinter
from tkinter import *
window = Tk()


def main():
    window.title("Hello World!")
    window.geometry("1280x720")
    create_table(3, 6)
    window.mainloop()


# Creates a table, loading the data from the datastore
def create_table(width, height):
    for x in range(width):
        for y in range(height):
            grid_frame = Frame(window, relief="solid")

            entry = Entry(grid_frame, width=10, fg="blue", font=("Arial", 16, "bold"), justify=CENTER)
            button = Button(grid_frame, width=5, fg="blue", font=("Arial", 16, "bold"), text="info")

            entry.pack(side="left", fill="both", expand=True)
            button.pack(side="right", fill="x")

            grid_id_string = str(x) + ":" + str(y)
            entry.insert(END, grid_id_string)
            entry.config(state="readonly")

            grid_frame.grid(row=y, column=x)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

