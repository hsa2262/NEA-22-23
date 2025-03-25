from tkinter import *
from tkinter import messagebox
import pymysql


# this clears the text in the box when the user clicks the box.
def clear():
    email.delete(0, END)
    username.delete(0, END)
    password.delete(0, END)


# this connects to the database. It checks the validity of the user's input.
# I use a single table in the sql database.
# I create the database, enter the data and retrieve the data where necessary.
def connect_database():
    if email.get() == "" or email.get() == "Enter email" or username.get() == "" or username.get() == "Enter username" or password.get() == "" or password.get() == "Enter password":
        messagebox.showerror("Error", "You have not filled in all fields.")  # if user has not entered any sign up details, an error message is displayed.
    else:
        try:
            con = pymysql.connect(host='localhost', user='root', password='password123')  # this connects to the database.
            mycursor = con.cursor()
        except:
            messagebox.showerror("Error", "Cannot connect to database.")
            return

        # create table
        try:
            db = "create database userdata"
            mycursor.execute(db)
            db = "use userdata"
            mycursor.execute(db)
            db = """CREATE TABLE DATA(
                ID INT NOT NULL AUTO_INCREMENT,
                EMAIL VARCHAR(30),
                USERNAME VARCHAR(30),
                PASSWORD VARCHAR(30),
                PRIMARY KEY(ID)
            )"""
            mycursor.execute(db)

        except:
            mycursor.execute("use userdata")

        # search table
        db = "SELECT * FROM data WHERE username = %s"
        mycursor.execute(db, (username.get()))

        row = mycursor.fetchone()
        if row != None:
            messagebox.showerror("Error", "Username is taken.")

        else:
            db = "insert into data(email, username, password) values(%s, %s, %s)"
            mycursor.execute(db, (email.get(), username.get(), password.get()))
            con.commit()
            con.close()
            messagebox.showinfo("Success", "Registration complete")
            clear()
            screen.destroy()
            import menu.login


def remove_email(x):  # this function makes it so that when you click the box for the email, the words "Enter email" disappears.
    if email.get() == "Enter email":
        email.delete(0, END)


def add_email(z):  # this displays the text that is in the email box.
    mail = email.get()
    if mail == "":
        email.insert(0, "Enter email")


def remove_user(y):  # this  function makes it so that when you click the box for the username, the words "Enter username" disappears.
    if username.get() == "Enter username":
        username.delete(0, END)


def add_user(z):  # this displays the text that is in the username box.
    user = username.get()
    if user == "":
        username.insert(0, "Enter username")


def remove_pass(z):  # this  function makes it so that when you click the box for the password, the words "Enter password" disappears.
    if password.get() == "Enter password":
        password.delete(0, END)


def add_pass(q):  # this displays the text that is in the password box.
    word = password.get()
    if word == "":
        password.insert(0, "Enter password")


def hide():
    password.config(show="*")  # when the user types their password, it is hidden
    password.delete(0, END)


# screen
screen = Tk()
screen.title("Sign up page")  # this titles the program "Sign up page".
screen.resizable(False, False)  # this makes it so that the user cannot maximise the screen.
screen.geometry("600x400")  # this is the size of the screen
screen.configure(bg="deepskyblue4")

signup_title = Label(screen, text="Sign up page", font=("Courier New", 46, "normal"), bg="deepskyblue4", fg="light cyan")
# above is the words seen in the top middle of the screen.
signup_title.place(x=130, y=34)  # this centres the word "Sign up Page"

email = Entry(screen, width=34, font=("Courier New", 21, "normal"), fg="deepskyblue4", highlightbackground="deepskyblue4")  # this is the box where the email is entered.
email.place(x=65, y=130)  # this is where the box for the email is placed.
email.insert(0, "Enter email")  # this doesn't affect the user typing their email.
email.bind("<FocusIn>", remove_email)  # see remove_email function
email.bind("<FocusOut>", add_email)

username = Entry(screen, width=34, font=("Courier New", 21, "normal"), fg="deepskyblue4", highlightbackground="deepskyblue4")  # this is the box where the username is entered.
username.place(x=65, y=180)  # this is where the box for the username is placed.
username.insert(0, "Enter username")  # this doesn't affect the user typing their username.
username.bind("<FocusIn>", remove_user)  # see remove_user function
username.bind("<FocusOut>", add_user)  # see add_user function

password = Entry(screen, width=34, font=("Courier New", 21, "normal"), fg="deepskyblue4", highlightbackground="deepskyblue4")  # this is the box where the password is entered.
password.place(x=65, y=230)  # this is where the box for the password is placed.
password.insert(0, "Enter password")  # this doesn't affect the user typing their password.
password.bind("<FocusIn>", remove_pass)  # see remove_pass function
password.bind("<FocusOut>", add_pass)  # see add_pass function
password.bind("<FocusIn>", lambda event: hide())  # see hide function

signup = Button(screen, text="Sign up", font=("Courier New", 34, "normal"),
                fg="deepskyblue4", bg="white", activeforeground="steel blue", cursor="hand", bd=0, width=8, command=connect_database)
signup.place(x=200, y=300)

screen.mainloop()
