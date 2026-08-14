import tkinter as tk
from tkinter import messagebox
import random
import string

# PASSWORD GENERATOR
# OIBSIP - Python Programming Internship
# Task 3 - Random Password Generator
# Beginner Tier

# MAIN WINDOW
window = tk.Tk()

window.title("Random Password Generator")
window.geometry("700x650")
window.minsize(600, 600)
window.resizable(True, True)
window.configure(bg="#F4F7FB")

# COLORS
NAVY = "#243B53"
BLUE = "#2F80ED"
BLUE_DARK = "#1F6FD1"
LIGHT_BG = "#F4F7FB"
WHITE = "#FFFFFF"
TEXT = "#243B53"
SECONDARY = "#627D98"
BORDER = "#D9E2EC"
LIGHT_BLUE = "#EAF2FF"
LIGHT_GRAY = "#E8EEF4"
ERROR = "#E74C3C"
SUCCESS = "#27AE60"

# HEADER
header = tk.Frame(
    window,
    bg=NAVY,
    height=130
)

header.pack(
    fill="x"
)

title_label = tk.Label(
    header,
    text="RANDOM PASSWORD",
    font=("Segoe UI", 26, "bold"),
    bg=NAVY,
    fg=WHITE
)

title_label.pack(
    pady=(24, 2)
)

subtitle_label = tk.Label(
    header,
    text="Generate secure passwords based on your preferences",
    font=("Segoe UI", 11),
    bg=NAVY,
    fg="#D9E2EC"
)

subtitle_label.pack()

# MAIN CONTENT
content = tk.Frame(
    window,
    bg=LIGHT_BG
)

content.pack(
    fill="both",
    expand=True,
    padx=45,
    pady=25
)

# SETTINGS CARD
settings_card = tk.Frame(
    content,
    bg=WHITE,
    highlightbackground=BORDER,
    highlightthickness=1
)

settings_card.pack(
    fill="x",
    pady=(0, 18)
)


settings_title = tk.Label(
    settings_card,
    text="Password Settings",
    font=("Segoe UI", 16, "bold"),
    bg=WHITE,
    fg=TEXT
)

settings_title.pack(
    anchor="w",
    padx=25,
    pady=(20, 15)
)

# PASSWORD LENGTH
length_label = tk.Label(
    settings_card,
    text="Password Length",
    font=("Segoe UI", 10, "bold"),
    bg=WHITE,
    fg=SECONDARY
)

length_label.pack(
    anchor="w",
    padx=25
)


length_entry = tk.Entry(
    settings_card,
    font=("Segoe UI", 11),
    relief="solid",
    bd=1,
    width=12
)

length_entry.pack(
    anchor="w",
    padx=25,
    pady=(6, 18),
    ipady=7
)

length_entry.insert(
    0,
    "12"
)

# CHARACTER TYPE SELECTION
type_label = tk.Label(
    settings_card,
    text="Character Types",
    font=("Segoe UI", 10, "bold"),
    bg=WHITE,
    fg=SECONDARY
)

type_label.pack(
    anchor="w",
    padx=25,
    pady=(0, 8)
)


# Checkbox variables

uppercase_var = tk.BooleanVar(value=True)
lowercase_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=False)


# Checkbox frame

checkbox_frame = tk.Frame(
    settings_card,
    bg=WHITE
)

checkbox_frame.pack(
    fill="x",
    padx=25,
    pady=(0, 20)
)


# Uppercase

uppercase_check = tk.Checkbutton(
    checkbox_frame,
    text="Uppercase (A-Z)",
    variable=uppercase_var,
    font=("Segoe UI", 10),
    bg=WHITE,
    fg=TEXT,
    activebackground=WHITE,
    activeforeground=TEXT,
    selectcolor=WHITE
)

uppercase_check.grid(
    row=0,
    column=0,
    sticky="w",
    padx=(0, 30),
    pady=4
)


# Lowercase

lowercase_check = tk.Checkbutton(
    checkbox_frame,
    text="Lowercase (a-z)",
    variable=lowercase_var,
    font=("Segoe UI", 10),
    bg=WHITE,
    fg=TEXT,
    activebackground=WHITE,
    activeforeground=TEXT,
    selectcolor=WHITE
)

lowercase_check.grid(
    row=0,
    column=1,
    sticky="w",
    pady=4
)


# Numbers

numbers_check = tk.Checkbutton(
    checkbox_frame,
    text="Numbers (0-9)",
    variable=numbers_var,
    font=("Segoe UI", 10),
    bg=WHITE,
    fg=TEXT,
    activebackground=WHITE,
    activeforeground=TEXT,
    selectcolor=WHITE
)

numbers_check.grid(
    row=1,
    column=0,
    sticky="w",
    padx=(0, 30),
    pady=4
)


# Symbols

symbols_check = tk.Checkbutton(
    checkbox_frame,
    text="Symbols (!@#$)",
    variable=symbols_var,
    font=("Segoe UI", 10),
    bg=WHITE,
    fg=TEXT,
    activebackground=WHITE,
    activeforeground=TEXT,
    selectcolor=WHITE
)

symbols_check.grid(
    row=1,
    column=1,
    sticky="w",
    pady=4
)

# RESULT CARD
result_card = tk.Frame(
    content,
    bg=WHITE,
    highlightbackground=BORDER,
    highlightthickness=1
)

result_card.pack(
    fill="x",
    pady=(0, 18)
)


result_heading = tk.Label(
    result_card,
    text="GENERATED PASSWORD",
    font=("Segoe UI", 10, "bold"),
    bg=WHITE,
    fg=SECONDARY
)

result_heading.pack(
    pady=(18, 8)
)


password_display = tk.Label(
    result_card,
    text="Your password will appear here",
    font=("Consolas", 18, "bold"),
    bg=LIGHT_BLUE,
    fg=TEXT,
    wraplength=580,
    padx=20,
    pady=18
)

password_display.pack(
    fill="x",
    padx=25,
    pady=(0, 10)
)


message_label = tk.Label(
    result_card,
    text="Choose at least two character types.",
    font=("Segoe UI", 9),
    bg=WHITE,
    fg=SECONDARY
)

message_label.pack(
    pady=(0, 18)
)

# GENERATE PASSWORD FUNCTION
def generate_password():

    # Get password length

    length_text = length_entry.get().strip()

    # Validate length input

    if length_text == "":
        messagebox.showwarning(
            "Missing Information",
            "Please enter a password length."
        )
        return

    try:
        length = int(length_text)

    except ValueError:
        messagebox.showerror(
            "Invalid Length",
            "Password length must be a whole number."
        )
        return

    # Minimum length validation

    if length < 8:
        messagebox.showwarning(
            "Length Too Short",
            "Password length must be at least 8 characters."
        )
        return

    # Maximum length for practical use

    if length > 100:
        messagebox.showwarning(
            "Length Too Large",
            "Please enter a password length between 8 and 100."
        )
        return

    # Create selected character groups

    character_groups = []

    if uppercase_var.get():
        character_groups.append(string.ascii_uppercase)

    if lowercase_var.get():
        character_groups.append(string.ascii_lowercase)

    if numbers_var.get():
        character_groups.append(string.digits)

    if symbols_var.get():
        character_groups.append(string.punctuation)

    # At least two types must be selected

    if len(character_groups) < 2:

        messagebox.showwarning(
            "Character Types Required",
            "Please select at least two character types."
        )

        return

    # Combine selected groups

    all_characters = "".join(character_groups)

    # Make sure the generated password contains
    # at least one character from every selected type

    password_characters = []

    for group in character_groups:
        password_characters.append(
            random.choice(group)
        )

    # Fill remaining positions

    remaining_length = length - len(password_characters)

    for _ in range(remaining_length):

        password_characters.append(
            random.choice(all_characters)
        )

    # Shuffle password so required characters
    # are not always at the beginning

    random.shuffle(password_characters)

    password = "".join(password_characters)

    # Display password

    password_display.config(
        text=password,
        fg=TEXT
    )

    message_label.config(
        text="Password generated successfully.",
        fg=SUCCESS
    )

# CLEAR / RESET FUNCTION
def clear_fields():

    length_entry.delete(
        0,
        tk.END
    )

    length_entry.insert(
        0,
        "12"
    )

    uppercase_var.set(True)
    lowercase_var.set(True)
    numbers_var.set(True)
    symbols_var.set(False)

    password_display.config(
        text="Your password will appear here",
        fg=TEXT
    )

    message_label.config(
        text="Choose at least two character types.",
        fg=SECONDARY
    )

# BUTTON FRAME
button_frame = tk.Frame(
    content,
    bg=LIGHT_BG
)

button_frame.pack(
    pady=(0, 15)
)

# GENERATE BUTTON
generate_button = tk.Button(
    button_frame,
    text="Generate Password",
    command=generate_password,
    font=("Segoe UI", 11, "bold"),
    bg=BLUE,
    fg=WHITE,
    activebackground=BLUE_DARK,
    activeforeground=WHITE,
    relief="flat",
    padx=28,
    pady=11,
    cursor="hand2"
)

generate_button.grid(
    row=0,
    column=0,
    padx=8
)

# CLEAR BUTTON
clear_button = tk.Button(
    button_frame,
    text="Clear",
    command=clear_fields,
    font=("Segoe UI", 11, "bold"),
    bg=LIGHT_GRAY,
    fg=TEXT,
    activebackground=BORDER,
    activeforeground=TEXT,
    relief="flat",
    padx=28,
    pady=11,
    cursor="hand2"
)

clear_button.grid(
    row=0,
    column=1,
    padx=8
)

# FOOTER
footer_label = tk.Label(
    content,
    text="Oasis Infobyte • Python Programming Internship • Task 3",
    font=("Segoe UI", 9),
    bg=LIGHT_BG,
    fg="#829AB1"
)

footer_label.pack(
    pady=(5, 0)
)

# START APPLICATION
window.mainloop()