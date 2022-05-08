from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_gen():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0 or len(email) == 0:
        messagebox.showinfo(title="Warning", message="Please ensure all fields are filled")

    else:

        valid_info = messagebox.askokcancel(title=website, message=f"These are the details entered:\nEmail: {email}\n"
                                                                   f"Password: {password}\nIs it okay to save?")

        if valid_info:
            try:
                with open("password_file.json", "r") as password_file:
                    # Read the current json file state
                    data = json.load(password_file)

            except FileNotFoundError:
                with open("password_file.json", "w") as password_file:
                    # Read the current json file state
                    json.dump(new_data, password_file, indent=4)
            else:
                # Update json file with new content
                data.update(new_data)
                # Write new content to json dictionary
                with open("password_file.json", "w") as password_file:
                    json.dump(data, password_file, indent=4)

            finally:
                # Clear password manager cells for new entry
                website_entry.delete(0, END)
                password_entry.delete(0, END)


def search():
    website = website_entry.get()
    try:
        with open("password_file.json", "r") as data_file:
            result = json.load(data_file)

    except FileNotFoundError:
        messagebox.showerror(title=website, message="No Data File Found")

    else:
        if website in result:
            email = result[website]["email"]
            password = result[website]["password"]
            messagebox.showinfo(title=website, message=f"Email:{email}\nPassword:{password}")
            pyperclip.copy(password)
        else:
            messagebox.showinfo(title=website, message=f"No details for {website} exists.")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=32)
website_entry.grid(row=1, column=1, columnspan=1)
website_entry.focus()

email_entry = Entry(width=42)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "example@email.com")

password_entry = Entry(width=32)
password_entry.grid(row=3, column=1, columnspan=1)

# Buttons
generate_password_button = Button(text="Generate", command=password_gen)
generate_password_button.grid(row=3, column=2, columnspan=1)

add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2)

search_button = Button(text="Search", width=6, command=search)
search_button.grid(row=1, column=2, columnspan=1)

window.mainloop()
