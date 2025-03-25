from tkinter import *
from settings.settings import *
from PIL import ImageTk, Image

# screen
window = Tk()
window.minsize(WIDTH, HEIGHT)
window.configure(bg="black")
login_title = Label(window, text="Game Title", font=("courier new", 68, "bold"),
                    bg="black", fg="white")  # these are the words seen on the top middle of the screen.
login_title.place(x=150, y=30)  # this centres the word "Login Page"


# this closes the screen and imports the new screen depending on the button pressed.
def new_game():
    window.destroy()
    import menu.signup


def load_game():
    window.destroy()
    import menu.login


def options():
    window.destroy()
    import menu.options


def leaderboard():
    window.destroy()
    import menu.leaderboard


def quit():
    exit()


# these are all the button_images that the user can press, once a button is pressed,
# it goes to their corresponding functions. For example, the newgame button
# goes to the newgame function.

# new game
newgame_photo = (Image.open("/Users/ashleylim/PycharmProjects/NEA project/images/button_images/new_game image.png"))
photo1 = newgame_photo.resize((232, 45))
newgame_image = ImageTk.PhotoImage(photo1)

newgame = Button(window, state=ACTIVE, image=newgame_image, highlightthickness=0, command=new_game)
newgame.place(x=240, y=140)

# load game
loadgame_photo = (Image.open("/Users/ashleylim/PycharmProjects/NEA project/images/button_images/load_game image.png"))
photo1 = loadgame_photo.resize((232, 45))
loadgame_image = ImageTk.PhotoImage(photo1)

loadgame = Button(window, state=ACTIVE, image=loadgame_image, highlightthickness=0, command=load_game)
loadgame.place(x=240, y=200)

# options
options_game = (Image.open("/Users/ashleylim/PycharmProjects/NEA project/images/button_images/options_image.png"))
photo1 = options_game.resize((232, 45))
options_image = ImageTk.PhotoImage(photo1)

options_game = Button(window, state=ACTIVE, image=options_image, highlightthickness=0, command=options)
options_game.place(x=240, y=260)

# leaderboard
leaderboard_game = (Image.open("/Users/ashleylim/PycharmProjects/NEA project/images/button_images/leaderboard_image.png"))
photo1 = leaderboard_game.resize((232, 45))
leaderboard_image = ImageTk.PhotoImage(photo1)

leaderboard_game = Button(window, state=ACTIVE, image=leaderboard_image, highlightthickness=0, command=leaderboard)
leaderboard_game.place(x=240, y=320)

# quit
quit_game = (Image.open("/Users/ashleylim/PycharmProjects/NEA project/images/button_images/quit_image.png"))
photo1 = quit_game.resize((232, 45))
quit_image = ImageTk.PhotoImage(photo1)

quit_game = Button(window, state=ACTIVE, image=quit_image, highlightthickness=0, command=quit)
quit_game.place(x=240, y=380)


window.mainloop()
