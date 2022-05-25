from tkinter import *
from tkinter import messagebox as message
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
key_word = []

try:
    lang_data = pandas.read_csv("data/words_to_learn.csv")
except (FileNotFoundError, pandas.errors.EmptyDataError):
    original = pandas.read_csv("data/french_words.csv")
    learn = original.to_dict(orient="records")
else:
    learn = lang_data.to_dict(orient="records")


def new_card():
    global current_card, key_word, timer
    window.after_cancel(timer)
    current_card = random.choice(learn)
    print(current_card)

    for key, value in current_card.items():
        key_word.append(key)
    # print(key_word)
    key_ch = key_word[0]
    value_ch = current_card[key_word[0]]

    canvas.itemconfig(card_title, text=key_ch, fill="black")
    canvas.itemconfig(card_word, text=value_ch, fill="black")
    canvas.itemconfig(card_bg, image=card_front)
    timer = window.after(5000, func=flip)


def flip():
    key_ch = key_word[1]
    value_ch = current_card[key_word[1]]

    canvas.itemconfig(card_title, text=key_ch, fill="white")
    canvas.itemconfig(card_word, text=value_ch, fill="white")
    canvas.itemconfig(card_bg, image=card_back)


def known():
    try:
        learn.remove(current_card)
        print(len(learn))
        data = pandas.DataFrame(learn)
        data.to_csv("data/words_to_learn.csv", index=False)
        new_card()
    except (ValueError, IndexError):
        message.showinfo(title="Congratulations", message="You have completed this challenge. "
                                                          "Close the app to start again")


# creating the window
window = Tk()
window.title("Language Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
timer = window.after(3000, func=flip)

canvas = Canvas(width=800, height=526)

# Loading up the images
right_check = PhotoImage(file="images/right.png")
wrong_check = PhotoImage(file="images/wrong.png")
card_back = PhotoImage(file="images/card_back.png")
card_front = PhotoImage(file="images/card_front.png")

card_bg = canvas.create_image(400, 263, image=card_front)
canvas.config(background=BACKGROUND_COLOR, highlightthickness=0)
card_title = canvas.create_text(400, 150, text=" ", font=("Ariel", 48, "italic"))
card_word = canvas.create_text(400, 263, text=" ", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)


# Buttons
right_button = Button(image=right_check, highlightthickness=0, command=known)
right_button.grid(row=1, column=1,)
#
wrong_button = Button(image=wrong_check, highlightthickness=0, command=new_card)
wrong_button.grid(row=1, column=0)

# Labels
# language_label = Label(text="French:")
# language_label.grid(row=3, column=1)
#
# word_label = Label(text="Bonjour")
# word_label.grid(row=3, column=1)

new_card()

window.mainloop()
