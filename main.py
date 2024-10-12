from tkinter import *
from random import choice
import pandas

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=30, bg="#AADFC0")
canvas = Canvas(width=800, height=650, bg="#AADFC0", highlightthickness=0)


#### CARDS ####
front_card_img = PhotoImage(file="card_front.png")
back_card_img = PhotoImage(file="card_back.png")
bg_img = canvas.create_image(400, 270, image="")


### DATA_MECHANISM ###
current_card = {}

try:
    data = pandas.read_csv("words_to_learn.csv")
except FileNotFoundError:
    main_data = pandas.read_csv("Japanese words.csv")
    data_dict = main_data.to_dict(orient="records")
else:
    data_dict = data.to_dict(orient="records")


title = canvas.create_text(390, 150, text="", font=("Ariel", 35, "italic"))
text = canvas.create_text(390, 300, text="", font=("Ariel", 50, "bold"))


def next_jp_card():
    global current_card, front_card_img, flip_timer
    window.after_cancel(flip_timer)
    canvas.itemconfig(bg_img, image=front_card_img)

    current_card = choice(data_dict)

    canvas.itemconfig(title, text="Japanese", fill="Black")
    canvas.itemconfig(text, text=current_card["Japanese"], fill="Black")

    flip_timer = window.after(ms=3000, func=eng_card)


def eng_card():
    global current_card, back_card_img

    canvas.itemconfig(bg_img, image=back_card_img)

    canvas.itemconfig(title, text="English", fill="White")
    canvas.itemconfig(text, text=current_card["English"], fill="White")


def known_jp_card():

    data_dict.remove(current_card)
    data = pandas.DataFrame(data_dict)
    data.to_csv("words_to_learn.csv", index=False)

    next_jp_card()


##### BUTTONS ####
right_pic = PhotoImage(file="right.png")
wrong_pic = PhotoImage(file="wrong.png")

right_button = Button(text="right", image=right_pic, command=known_jp_card, bg="#AADFC0")
wrong_button = Button(text="wrong", image=wrong_pic, command=next_jp_card, bg="#AADFC0")

right_button.place(x=600, y=550)
wrong_button.place(x=100, y=550)


flip_timer = window.after(ms=3000, func=eng_card)
next_jp_card()


canvas.pack()

window.mainloop()
