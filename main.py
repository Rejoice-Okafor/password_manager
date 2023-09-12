from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_new_password():
    uppercase_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    lowercase_letters = [letter.lower() for letter in uppercase_letters]
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_uppercase = [choice(uppercase_letters) for _ in range(randint(2, 4))]
    password_lowercase = [choice(lowercase_letters) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

    password_list = password_uppercase + password_lowercase + password_numbers + password_symbols
    shuffle(password_list)

    generated_password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, generated_password)
    pyperclip.copy(generated_password)

def find_saved_password():
    website = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            # Read old data from the file
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="Data file not found!")
    else:
        if website in data:
            email = data[website]["email"]
            saved_password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nSaved Password: {saved_password}")
        else:
            messagebox.showinfo(title="Error", message="No details exist for this website")

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {website: {"email": email, "password": password}}

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please ensure all fields are filled.")
    else:
        try:
            with open("data.json", "r") as data_file:
                # Read old data from the file
                data = json.load(data_file)
        except FileNotFoundError:
            # Create a new data file if it doesn't exist
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Update existing data with the new data
            data.update(new_data)
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)

# ---------------------------- UI SETUP ------------------------------- #
FONT = ("Arial", 11, "bold")

window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

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
website_entry = Entry(width=35)
website_entry.grid(row=1, column=1, columnspan=2)
website_entry.focus()
email_entry = Entry(width=35)
email_entry.insert(0, "your_email@gmail.com")
email_entry.grid(row=2, column=1, columnspan=2)

password_entry = Entry(width=35)
password_entry.grid(row=3, column=1,)

# Buttons
generate_password_button = Button(text="Generate Password", bg="blue", width=15, command=generate_new_password)
generate_password_button.grid(row=3, column=3, columnspan=2)
search_button = Button(text="Search", bg="blue", width=15, command=find_saved_password)
search_button.grid(row=1, column=3, columnspan=2)

add_button = Button(text="Add", width=21, bg="white", command=save_password)
add_button.grid(row=5, column=1, columnspan=2)

window.mainloop()
