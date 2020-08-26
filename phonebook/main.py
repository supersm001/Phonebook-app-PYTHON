from tkinter import *
from tkinter import messagebox
import sqlite3
import datetime

date = datetime.datetime.now().date()
date = str(date)

con = sqlite3.connect('database.db')
cur = con.cursor()
table = "CREATE TABLE IF NOT EXISTS addressbook (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, number TEXT)"
cur.execute(table)
con.commit()


class Application(object):
    def __init__(self, master):
        self.master = master
        # TITLE
        self.title = Label(self.master, font=('TIMES NEW ROMAN', 20, 'bold'), text="PHONEBOOK", bg='gray')
        self.title.pack(side=TOP, pady=5, fill=X)
        # LEFT FRAME
        self.left = Frame(self.master, height=300, width=300, bd=1, padx=10, pady=50)
        self.left.place(x=10, y=50)
        # LEFT LABELS
        self.dateLabel = Label(self.left, text="Today : " + date, font=('TIMES NEW ROMAN', 20, 'bold'))
        self.dateLabel.pack()

        self.blankLabel = Label(self.left, font=('TIMES NEW ROMAN', 20, 'bold'), text="         ")
        self.blankLabel.pack()

        self.nameLabel = Label(self.left, font=('TIMES NEW ROMAN', 20, 'bold'), text="CONTACT NAME")
        self.nameLabel.pack()

        self.nameTxt = Entry(self.left, font=('TIMES NEW ROMAN', 20, 'bold'), textvariable='name')
        self.nameTxt.pack()

        self.numberLabel = Label(self.left, font=('TIMES NEW ROMAN', 20, 'bold'), text="CONTACT NUMBER")
        self.numberLabel.pack()

        self.numberTxt = Entry(self.left, font=('TIMES NEW ROMAN', 20, 'bold'), textvariable='number')
        self.numberTxt.pack()
        # RIGHT FRAME
        self.right = Frame(self.master, height=480, width=320, bd=1)
        self.right.place(x=320, y=50)

        self.scroll = Scrollbar(self.right, orient=VERTICAL)
        self.list = Listbox(self.right, height=20, width=30, font=('TIMES NEW ROMAN', 15, 'bold'))
        self.list.grid(row=0, column=0)

        persons = cur.execute("select * from 'addressbook'").fetchall()
        count = 0
        for person in persons:
            self.list.insert(count, str(count+1)+". "+person[1]+" - "+person[2])
            count += 1
        self.scroll.config(command=self.list.yview)
        self.list.config(yscrollcommand=self.scroll.set)
        self.scroll.grid(row=0, column=1, sticky=N + S)
        # BUTTON FRAME
        self.button = Frame(self.master, height=170, width=300, bd=1)
        self.button.place(x=10, y=360)

        self.Add = Button(self.button, bd=4, height=1, width=10, font=('TIMES NEW ROMAN', 20, 'bold'), text="ADD",
                          bg='gray', command=self.addNew)
        self.Add.grid(padx=60, pady=10)
        self.Delete = Button(self.button, bd=4, height=1, width=10, font=('TIMES NEW ROMAN', 20, 'bold'),
                             text="DELETE", bg='gray', command=self.delete)
        self.Delete.grid(padx=60, pady=10)

    def delete(self):
        selected = self.list.curselection()
        person = self.list.get(selected)
        person_name = person.split("-")[1]

        query = "delete from addressbook where number ={}".format(person_name)
        answer = messagebox.askquestion("Warning", "Are you sur to Delete?")
        if answer == 'yes':
            try:
                cur.execute(query)
                con.commit()
                messagebox.showinfo("Success", "Selected Contact Deleted")
                self.list.delete(0, END)
                persons = cur.execute("select * from 'addressbook'").fetchall()
                count = 0
                for person in persons:
                    self.list.insert(count, str(count+1) + ". " + person[1] + " - " + person[2])
                    count += 1

            except Exception as e:
                messagebox.showinfo("Info", str(e))

    def addNew(self):
        name = self.nameTxt.get()
        number = self.numberTxt.get()

        if name and number != 0:
            try:
                query = "insert into 'addressbook' (name, number) values(?, ?)"
                cur.execute(query, (name, number))
                con.commit()
                messagebox.showinfo("Success", "Contact Added")
                self.nameTxt.delete(0, END)
                self.numberTxt.delete(0, END)
                self.list.delete(0, END)
                persons = cur.execute("select * from 'addressbook'").fetchall()
                count = 0
                for person in persons:
                    self.list.insert(count, str(count+1) + ". " + person[1] + " - " + person[2])
                    count += 1
            except Exception as e:

                messagebox.showinfo("Info", str(e))

        else:
            messagebox.showerror("error", "fill all the Fields", icon='warning')


def main():
    root = Tk()
    app = Application(root)
    root.title("Phonebook App Coded By SANJAY MANDAL")
    root.geometry("650x550+350+200")
    root.resizable(False, False)
    root.mainloop()


if __name__ == '__main__':
    main()
