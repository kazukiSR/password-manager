from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


def findPassword():
    websiteStr = websiteEntry.get()
    try:
        with open("passwords.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showwarning(title="Error", message="No file found.")
    else:
        if websiteStr in data:
            userCreds = data[websiteStr]
            messagebox.showinfo(title=websiteStr, message=f"Username: {userCreds['username']}"
                                                          f"\nPassword: {userCreds['password']}"
                                                          f"\n(Password copied to clipboard)")
            pyperclip.copy(userCreds['password'])
        else:
            messagebox.showwarning(title="Error", message="Website not found")


def generatePassword():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    passwordL = [random.choice(letters) for _ in range(nr_letters)]
    passwordN = [random.choice(numbers) for _ in range(nr_numbers)]
    passwordS = [random.choice(symbols) for _ in range(nr_symbols)]
    password_list = passwordL + passwordS + passwordN
    random.shuffle(password_list)

    password = "".join(password_list)
    passwordEntry.delete(0, END)
    passwordEntry.insert(0, password)
    pyperclip.copy(password)


def saveEntry():
    websiteStr = websiteEntry.get()
    userStr = userEntry.get()
    passwordStr = passwordEntry.get()

    newData = {
        websiteStr: {
            "username": userStr,
            "password": passwordStr,
        }
    }

    if not websiteStr or not userStr or not passwordStr:
        messagebox.showwarning(title="Error", message="Please don't leave any fields empty!")
    else:
        try:
            with open("passwords.json", "r") as file:
                data = json.load(file)
                data.update(newData)
        except FileNotFoundError:
            with open("passwords.json", "w") as file:
                json.dump(newData, file, indent=4)
        else:
            with open("passwords.json", "w") as file:
                json.dump(data, file, indent=4)
        finally:
            websiteEntry.delete(0, END)
            userEntry.delete(0, END)
            passwordEntry.delete(0, END)
            websiteEntry.focus()


window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas = Canvas(width=200, height=200, highlightthickness=0)
logoImg = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logoImg)
canvas.grid(column=1, row=0)

Label(text="Website:").grid(column=0, row=1, sticky=E)
Label(text="Email/Username:").grid(column=0, row=2, sticky=E)
Label(text="Password:").grid(column=0, row=3, sticky=E)

websiteEntry = Entry(width=33)
websiteEntry.grid(column=1, row=1, columnspan=2, sticky=W)
websiteEntry.focus()

userEntry = Entry(width=52)
userEntry.grid(column=1, row=2, columnspan=2, sticky=W)

passwordEntry = Entry(width=33)
passwordEntry.grid(column=1, row=3, sticky=W)

generatePasswordButton = Button(text="Generate Password", command=generatePassword, width=16)
generatePasswordButton.grid(column=2, row=3)

searchButton = Button(text="Search", command=findPassword, width=16)
searchButton.grid(column=2, row=1)

addButton = Button(text="Add", command=saveEntry, width=50)
addButton.grid(column=1, row=4, columnspan=2)

window.mainloop()
