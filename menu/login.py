from tkinter import *
import tkinter
from tkinter import messagebox
import pymysql


# this clears the text from the username and password box when the user clicks it.
def clear():
    username.delete(0, END)
    password.delete(0, END)


# this uses exception handling to check whether there is a problem with the database.
def user_login():
    if username.get() == "" or username.get() == "Enter username" or password.get() == "" or password.get() == "Enter password":
        messagebox.showerror("Error", "You have not filled in all fields.")

    else:
        try:
            con = pymysql.connect(host="localhost", user="root", password="password123")
            mycursor = con.cursor()
        except:
            messagebox.showerror("Error", "Something went wrong, please try again.")
            return
        db = "use userdata"
        mycursor.execute(db)
        db = "SELECT * FROM data WHERE username = %s AND password = %s"
        mycursor.execute(db, (username.get(), password.get()))
        row = mycursor.fetchone()

        if row == None:
            messagebox.showerror("Error", "Your username or password is incorrect.")
        else:
            messagebox.showerror("Success", "Login successful.")
            clear()

            screen.destroy()
            import new_game
            # WHEN LOGIN EITHER GO NEW GAME OR LOAD GAME
            # IF LOAD GAME MUST GO TO WHERE PLAYER LEFT OFF


def signup_page():
    screen.destroy()
    import menu.signup


def remove_user(x):  # this function makes it so that when you click the box for the username, the words "Enter username" disappears.
    if username.get() == "Enter username":
        username.delete(0, END)


def add_user(z):
    user = username.get()
    if user == "":
        username.insert(0, "Enter username")


def remove_pass(y):
    if password.get() == "Enter password":
        password.delete(0, END)


def add_pass(q):
    word = password.get()
    if word == "":
        password.insert(0, "Enter password")


def hide():
    password.config(show="*")  # when the user types their password, it is hidden
    password.delete(0, END)


# screen
screen = Tk()
screen.title("Login page")  # this titles the program "Login page".
screen.resizable(False, False)  # this makes it so that the user cannot maximise the screen.
screen.geometry("600x400")  # this is the size of the screen
password_input = tkinter.StringVar()
screen.configure(bg="deepskyblue4")


login_title = Label(screen, text="Login Page", font=("Courier New", 60, "normal"), bg="deepskyblue4", fg="light cyan")
# above is the words seen in the top middle of the screen.
login_title.place(x=120, y=37)  # this centres the word "Login Page"


username = Entry(screen, width=34, font=("Courier New", 21, "normal"), fg="deepskyblue4", highlightbackground="deepskyblue4")  # this is the box where the username is entered.
username.place(x=65, y=130)  # this is where the box for the username is placed.
username.insert(0, "Enter username")  # this doesn't affect the user typing their username.
username.bind("<FocusIn>", remove_user)  # see remove_user function
username.bind("<FocusOut>", add_user)  # see add_user function

password = Entry(screen, width=34, font=("Courier New", 21, "normal"), fg="deepskyblue4",
                 highlightbackground="deepskyblue4", textvariable=password_input)  # this is the box where the password is entered.
password.place(x=65, y=180)  # this is where the box for the password is placed.
password.insert(0, "Enter password")  # this doesn't affect the user typing their password.
password.bind("<FocusIn>", remove_pass)  # see remove_pass function
password.bind("<FocusOut>", add_pass)  # see add_pass function
password.bind("<FocusIn>", lambda event: hide())  # see hide function


login = Button(screen, text="Login", font=("Courier New", 34, "normal"), fg="deepskyblue4",
               bg="white", activeforeground="steel blue", activebackground="white",
               cursor="hand", bd=0, width=5, command=user_login)
login.place(x=230, y=250)

signup = Button(screen, text="Sign up", font=("Courier New", 21, "normal"),
                fg="deepskyblue4", bg="white", activeforeground="steel blue", activebackground="white", cursor="hand", bd=0, width=8, command=signup_page)
signup.place(x=70, y=310)


screen.mainloop()
