import pandas

BACKGROUND_COLOR = "#B1DDC6"
from tkinter import *
import pandas as pd
import random

# Reading data and displaying it from a CSV file
try:
    df = pd.read_csv("words_to_learn.csv")
except FileNotFoundError:
    df = pd.read_csv("french_words.csv")
list_of_data = df.to_dict(orient="records")

current_card = {}
flip_timer = None  # Initialize flip_timer

# NEXT CARD GIVES ENGLISH EQUIVALENT
def next_Card():
    global current_card, flip_timer
    current_card = random.choice(list_of_data)
    canvas.itemconfig(image_id, image=front)
    canvas.itemconfig(Language_name, text="French", fill="black")
    canvas.itemconfig(text, text=current_card["French"], fill="black")

    # Cancel any existing flip timer
    if flip_timer:
        window.after_cancel(flip_timer)

    # Set a new timer to flip the card
    flip_timer = window.after(3000, flip_card)


#WHEN USER KNOWS THE WORD AND WE DELETE IT FROM THE DICIONARY

def knows_answer():
    global current_card
    if current_card in list_of_data:
        list_of_data.remove(current_card)
        data = pd.DataFrame(list_of_data)
        data.to_csv("words_to_learn.csv", index=False)
    next_Card()

# FLIP CARD GIVES FRENCH WORD
def flip_card():
    global current_card
    canvas.itemconfig(Language_name, text="English", fill="white")
    canvas.itemconfig(image_id, image=back)
    canvas.itemconfig(text, text=current_card["English"], fill="white")

# UI SETUP
window = Tk()
window.title("flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front = PhotoImage(file="./images/card_front.png")
back = PhotoImage(file="./images/card_back.png")
image_id = canvas.create_image(400, 263, image=front)
canvas.grid(row=0, column=0, columnspan=2)

Language_name = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
text = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

right = PhotoImage(file="./images/right.png")
button = Button(image=right, highlightthickness=0, bg=BACKGROUND_COLOR, borderwidth=0, command=knows_answer)
button.grid(row=1, column=0)

left = PhotoImage(file="./images/wrong.png")
button = Button(image=left, highlightthickness=0, bg=BACKGROUND_COLOR, borderwidth=0, )
button.grid(row=1, column=1)

# Start with an initial card
next_Card()

window.mainloop()
