import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

# DATABASE
database = sqlite3.connect("bmi_history.db")
cursor = database.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS bmi_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    weight REAL NOT NULL,
    height REAL NOT NULL,
    bmi REAL NOT NULL,
    category TEXT NOT NULL,
    date_time TEXT
)
""")

database.commit()

# MAIN WINDOW
window = tk.Tk()
window.title("BMI Calculator")
window.geometry("800x750")
window.minsize(600, 650)
window.resizable(True, True)
window.configure(bg="#F4F7FB")

# STYLE
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "TEntry",
    font=("Segoe UI", 11),
    padding=10
)

style.configure(
    "Treeview",
    font=("Segoe UI", 10),
    rowheight=32
)

style.configure(
    "Treeview.Heading",
    font=("Segoe UI", 10, "bold"),
    padding=8
)

# HEADER
header = tk.Frame(
    window,
    bg="#243B53",
    height=120
)

header.pack(fill="x")

title_label = tk.Label(
    header,
    text="BMI CALCULATOR",
    font=("Segoe UI", 26, "bold"),
    bg="#243B53",
    fg="white"
)

title_label.pack(pady=(22, 3))

subtitle_label = tk.Label(
    header,
    text="Calculate and track your Body Mass Index",
    font=("Segoe UI", 11),
    bg="#243B53",
    fg="#D9E2EC"
)

subtitle_label.pack()

# MAIN CONTENT
content = tk.Frame(
    window,
    bg="#F4F7FB"
)

content.pack(
    fill="both",
    expand=True,
    padx=45,
    pady=25
)

# INPUT CARD
input_card = tk.Frame(
    content,
    bg="white",
    highlightbackground="#D9E2EC",
    highlightthickness=1
)

input_card.pack(
    fill="x",
    pady=(0, 18)
)


input_title = tk.Label(
    input_card,
    text="Enter Your Details",
    font=("Segoe UI", 16, "bold"),
    bg="white",
    fg="#243B53"
)

input_title.pack(
    pady=(20, 15)
)

# NAME
name_label = tk.Label(
    input_card,
    text="Name",
    font=("Segoe UI", 10, "bold"),
    bg="white",
    fg="#486581"
)

name_label.pack()

name_entry = ttk.Entry(
    input_card,
    width=32
)

name_entry.pack(
    pady=(5, 15)
)

# WEIGHT
weight_label = tk.Label(
    input_card,
    text="Weight (kg)",
    font=("Segoe UI", 10, "bold"),
    bg="white",
    fg="#486581"
)

weight_label.pack()

weight_entry = ttk.Entry(
    input_card,
    width=32
)

weight_entry.pack(
    pady=(5, 15)
)

# HEIGHT
height_label = tk.Label(
    input_card,
    text="Height (m)",
    font=("Segoe UI", 10, "bold"),
    bg="white",
    fg="#486581"
)

height_label.pack()

height_entry = ttk.Entry(
    input_card,
    width=32
)

height_entry.pack(
    pady=(5, 20)
)

# RESULT CARD
result_card = tk.Frame(
    content,
    bg="white",
    highlightbackground="#D9E2EC",
    highlightthickness=1
)

result_card.pack(
    fill="x",
    pady=(0, 18)
)


result_heading = tk.Label(
    result_card,
    text="YOUR BMI RESULT",
    font=("Segoe UI", 10, "bold"),
    bg="white",
    fg="#829AB1"
)

result_heading.pack(
    pady=(18, 5)
)


result_label = tk.Label(
    result_card,
    text="Enter your details and calculate your BMI",
    font=("Segoe UI", 15, "bold"),
    bg="white",
    fg="#243B53",
    justify="center"
)

result_label.pack(
    pady=(0, 20)
)

# BMI CALCULATION
def calculate_bmi():

    try:

        name = name_entry.get().strip()

        if name == "":
            messagebox.showwarning(
                "Missing Information",
                "Please enter your name."
            )
            return

        weight = float(weight_entry.get())
        height = float(height_entry.get())

        if weight <= 0 or height <= 0:
            messagebox.showwarning(
                "Invalid Input",
                "Weight and height must be greater than zero."
            )
            return

        bmi = weight / (height ** 2)

        if bmi < 18.5:
            category = "Underweight"
            result_color = "#2980B9"

        elif bmi < 25:
            category = "Normal"
            result_color = "#27AE60"

        elif bmi < 30:
            category = "Overweight"
            result_color = "#F39C12"

        else:
            category = "Obese"
            result_color = "#E74C3C"

        result_label.config(
            text=f"{name}\nBMI: {bmi:.2f}\nCategory: {category}",
            fg=result_color
        )

        date_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        cursor.execute("""
            INSERT INTO bmi_history
            (name, weight, height, bmi, category, date_time)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            name,
            weight,
            height,
            bmi,
            category,
            date_time
        ))

        database.commit()

    except ValueError:

        messagebox.showerror(
            "Invalid Input",
            "Please enter valid numbers for weight and height."
        )

# CLEAR FUNCTION
def clear_fields():

    name_entry.delete(0, tk.END)
    weight_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)

    result_label.config(
        text="Enter your details and calculate your BMI",
        fg="#243B53"
    )

# MAIN BUTTONS
button_frame = tk.Frame(
    content,
    bg="#F4F7FB"
)

button_frame.pack(
    pady=(0, 18)
)


calculate_button = tk.Button(
    button_frame,
    text="Calculate BMI",
    command=calculate_bmi,
    font=("Segoe UI", 11, "bold"),
    bg="#2F80ED",
    fg="white",
    activebackground="#1F6FD1",
    activeforeground="white",
    relief="flat",
    padx=25,
    pady=10,
    cursor="hand2"
)

calculate_button.grid(
    row=0,
    column=0,
    padx=8
)


clear_button = tk.Button(
    button_frame,
    text="Clear",
    command=clear_fields,
    font=("Segoe UI", 11, "bold"),
    bg="#E8EEF4",
    fg="#243B53",
    activebackground="#D9E2EC",
    relief="flat",
    padx=25,
    pady=10,
    cursor="hand2"
)

clear_button.grid(
    row=0,
    column=1,
    padx=8
)

# BMI HISTORY
def view_history():

    history_window = tk.Toplevel(window)

    history_window.title("BMI History")
    history_window.geometry("900x500")
    history_window.minsize(750, 400)

    history_window.configure(
        bg="#F4F7FB"
    )

    heading = tk.Label(
        history_window,
        text="BMI History",
        font=("Segoe UI", 20, "bold"),
        bg="#F4F7FB",
        fg="#243B53"
    )

    heading.pack(
        pady=(20, 10)
    )

    table_frame = tk.Frame(
        history_window,
        bg="white"
    )

    table_frame.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=15
    )

    columns = (
        "ID",
        "Name",
        "Weight",
        "Height",
        "BMI",
        "Category",
        "Date & Time"
    )

    history_table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    for column in columns:
        history_table.heading(
            column,
            text=column
        )

    history_table.column(
        "ID",
        width=50,
        anchor="center"
    )

    history_table.column(
        "Name",
        width=120,
        anchor="center"
    )

    history_table.column(
        "Weight",
        width=90,
        anchor="center"
    )

    history_table.column(
        "Height",
        width=90,
        anchor="center"
    )

    history_table.column(
        "BMI",
        width=80,
        anchor="center"
    )

    history_table.column(
        "Category",
        width=130,
        anchor="center"
    )

    history_table.column(
        "Date & Time",
        width=180,
        anchor="center"
    )

    cursor.execute("""
        SELECT id, name, weight, height, bmi, category, date_time
        FROM bmi_history
        ORDER BY id ASC
    """)

    records = cursor.fetchall()

    for record in records:

        history_table.insert(
            "",
            tk.END,
            values=(
                record[0],
                record[1],
                f"{record[2]:.1f}",
                f"{record[3]:.2f}",
                f"{record[4]:.2f}",
                record[5],
                record[6] if record[6] else "Not available"
            )
        )

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=history_table.yview
    )

    history_table.configure(
        yscrollcommand=scrollbar.set
    )

    history_table.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

# BMI TREND GRAPH
def view_bmi_trend():

    cursor.execute("""
        SELECT date_time, bmi
        FROM bmi_history
        WHERE date_time IS NOT NULL
        ORDER BY date_time
    """)

    records = cursor.fetchall()

    if not records:

        messagebox.showinfo(
            "BMI Trend",
            "No BMI records available for the graph."
        )

        return

    dates = []
    bmi_values = []

    for record in records:

        date_time, bmi = record

        dates.append(
            datetime.strptime(
                date_time,
                "%Y-%m-%d %H:%M:%S"
            )
        )

        bmi_values.append(bmi)

    plt.figure(
        figsize=(9, 5)
    )

    plt.plot(
        dates,
        bmi_values,
        marker="o",
        linewidth=2
    )

    plt.title(
        "BMI Trend",
        fontsize=16,
        fontweight="bold"
    )

    plt.xlabel(
        "Date & Time"
    )

    plt.ylabel(
        "BMI"
    )

    plt.xticks(
        rotation=45
    )

    plt.grid(
        alpha=0.3
    )

    plt.tight_layout()

    plt.show()

# HISTORY & TREND BUTTONS
extra_button_frame = tk.Frame(
    content,
    bg="#F4F7FB"
)

extra_button_frame.pack()


history_button = tk.Button(
    extra_button_frame,
    text="View BMI History",
    command=view_history,
    font=("Segoe UI", 10, "bold"),
    bg="#FFFFFF",
    fg="#243B53",
    activebackground="#E8EEF4",
    relief="solid",
    bd=1,
    padx=20,
    pady=8,
    cursor="hand2"
)

history_button.grid(
    row=0,
    column=0,
    padx=8
)


trend_button = tk.Button(
    extra_button_frame,
    text="View BMI Trend",
    command=view_bmi_trend,
    font=("Segoe UI", 10, "bold"),
    bg="#FFFFFF",
    fg="#243B53",
    activebackground="#E8EEF4",
    relief="solid",
    bd=1,
    padx=20,
    pady=8,
    cursor="hand2"
)

trend_button.grid(
    row=0,
    column=1,
    padx=8
)

# START APPLICATION
window.mainloop()

# CLOSE DATABASE
database.close()