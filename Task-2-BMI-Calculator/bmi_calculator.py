import tkinter as tk
from tkinter import ttk
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

database= sqlite3.connect("bmi_history.db")
cursor=database.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS bmi_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        weight REAL NOT NULL,
        height REAL NOT NULL,
        bmi REAL NOT NULL,
        category TEXT NOT NULL
    )
""")
database.commit()

try:
    cursor.execute("""
        ALTER TABLE bmi_history
        ADD COLUMN date_time TEXT
    """)
    database.commit()
except sqlite3.OperationalError:
    pass

window = tk.Tk()

window.title("BMI Calculator")
window.geometry("400x300")

name_label = tk.Label(window, text="Name:")
name_label.pack()
name_entry=tk.Entry(window)
name_entry.pack()

weight_label=tk.Label(window, text="weight(kg):")
weight_label.pack()
weight_entry=tk.Entry(window)
weight_entry.pack()

height_label=tk.Label(window, text="height(m):")
height_label.pack()
height_entry=tk.Entry(window)
height_entry.pack()

#function to calculate BMI
def calculate_bmi():
    try:
        name = name_entry.get().strip()
        if name == "":
            result_label.config(
                text="Please enter your name.",
                fg="red"
            )
            return
        weight=float(weight_entry.get())
        height=float(height_entry.get())

        if weight <= 0 or height <= 0:
            result_label.config(text="weight and height must be greater than zero.")
            return
        
        bmi=weight/ (height ** 2)
        if bmi < 18.5:
            category="You are underweight"
            result_color="blue"
        elif bmi < 25:
            category="You have a normal weight"
            result_color="green"
        elif bmi < 30:
            category="You are overweight"
            result_color="orange"
        else:
            category="You are obese"
            result_color="red"

        result_label.config(
            text=f"BMI: {bmi:.2f}\nCategory: {category}",
            fg=result_color
        )
        date_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO bmi_history
            (name, weight, height, bmi, category, date_time)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, 
              weight, 
              height, 
              bmi, 
              category,
              date_time)
        )
        database.commit()

    except ValueError:
        result_label.config(text="Invalid input, please enter numbers only.")
        result_label.config(fg="red")

result_label=tk.Label(window, text="",
font=("Arial", 12)
)
result_label.pack(pady=10)

calculate_button=tk.Button(window, text="Calculate BMI",
                           command=calculate_bmi)
calculate_button.pack(pady=5)

#view history of BMI records
def view_history():
    history_window = tk.Toplevel(window)
    history_window.title("BMI History")
    history_window.geometry("750x350")

    columns=("Name", "Weight", "Height", "BMI", "Category", "Date & Time")

    history_table=ttk.Treeview(
            history_window,
            columns=columns,
            show="headings"
        )

    history_table.heading("Name", text="Name")
    history_table.heading("Weight", text="Weight (kg)")            
    history_table.heading("Height", text="Height (m)")
    history_table.heading("BMI", text="BMI")
    history_table.heading("Category", text="Category")
    history_table.heading("Date & Time", text="Date & Time")
        

    history_table.column("Name", width=120, anchor="center")
    history_table.column("Weight", width=120, anchor="center")
    history_table.column("Height", width=120, anchor="center")
    history_table.column("BMI", width=100, anchor="center")
    history_table.column("Category", width=220, anchor="center")
    history_table.column("Date & Time", width=180, anchor="center")

    cursor.execute("""
        SELECT name, weight, height, bmi, category, date_time
        FROM bmi_history
    """)

    records= cursor.fetchall()
    print(records)

    for record in records:
        name, weight, height, bmi, category, date_time = record
        history_table.insert(
            "",
            tk.END, 
            values=(
                name,
                f"{weight: .1f}",
                f"{height: .2f}",
                f"{bmi: .2f}",
                category,
                date_time if date_time else "Not available"
            )
        )

    history_table.pack(fill="both", 
                       expand=True,
                       padx=10,
                       pady=10
    )

def view_bmi_trend():
    cursor.execute("""
    SELECT date_time, bmi
    FROM bmi_history
    WHERE date_time IS NOT NULL
    ORDER BY date_time
    """)

    records = cursor.fetchall()

    if not records:
        print("No BMI available for graph.")
        return
    dates=[]
    bmi_values=[]

    for record in records:
        date_time, bmi= record
        dates.append(
            datetime.strptime(
                date_time,
               "%Y-%m-%d %H:%M:%S"
            )
        )

        bmi_values.append(bmi)

    plt.figure(figsize=(8,5))

    plt.plot(
        dates,
        bmi_values,
        marker="o"
    )

    plt.title("BMI Trend")
    plt.xlabel("Date & Time")
    plt.ylabel("BMI")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.show()

history_button=tk.Button(
    window,
    text="View BMI History",
    command=view_history
)
history_button.pack(pady=10)

trend_button=tk.Button(
    window,
    text="View BMI Trend",
    command=view_bmi_trend
)
trend_button.pack(pady=5)

window.mainloop()