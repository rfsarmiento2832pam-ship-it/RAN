import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime



conn = sqlite3.connect("helpdesk.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS categories(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets(
ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
employee_id INTEGER,
category_id INTEGER,
priority TEXT,
status TEXT,
date_created TEXT
)
""")

conn.commit()



root = tk.Tk()
root.title("Helpdesk Ticket System")
root.geometry("900x500")

# Frame container
container = tk.Frame(root)
container.pack(fill="both", expand=True)



def dashboard():

    for widget in container.winfo_children():
        widget.destroy()

    frame = tk.Frame(container)
    frame.pack(pady=40)

    tk.Label(frame, text="Dashboard", font=("Arial", 20)).pack(pady=20)

    tk.Button(frame, text="Create Ticket", width=20, command=create_ticket).pack(pady=10)
    tk.Button(frame, text="View Tickets", width=20, command=view_tickets).pack(pady=10)
    tk.Button(frame, text="Manage Employees", width=20, command=manage_employees).pack(pady=10)
    tk.Button(frame, text="Manage Categories", width=20, command=manage_categories).pack(pady=10)



def create_ticket():

    for widget in container.winfo_children():
        widget.destroy()

    frame = tk.Frame(container)
    frame.pack(pady=20)

    tk.Label(frame, text="Create Ticket", font=("Arial", 18)).grid(row=0, columnspan=2, pady=10)

    tk.Label(frame, text="Employee ID").grid(row=1, column=0)
    emp = tk.Entry(frame)
    emp.grid(row=1, column=1)

    tk.Label(frame, text="Category ID").grid(row=2, column=0)
    cat = tk.Entry(frame)
    cat.grid(row=2, column=1)

    tk.Label(frame, text="Priority").grid(row=3, column=0)
    priority = ttk.Combobox(frame, values=["Low", "Medium", "High"])
    priority.grid(row=3, column=1)

    tk.Label(frame, text="Status").grid(row=4, column=0)
    status = ttk.Combobox(frame, values=["Open", "In Progress", "Closed"])
    status.grid(row=4, column=1)

    def save_ticket():
        cursor.execute("""
        INSERT INTO tickets(employee_id,category_id,priority,status,date_created)
        VALUES(?,?,?,?,?)
        """, (
            emp.get(),
            cat.get(),
            priority.get(),
            status.get(),
            datetime.now().strftime("%Y-%m-%d")
        ))

        conn.commit()
        messagebox.showinfo("Success", "Ticket Created")

    tk.Button(frame, text="Save Ticket", command=save_ticket).grid(row=5, columnspan=2, pady=10)
    tk.Button(frame, text="Back", command=dashboard).grid(row=6, columnspan=2)



def view_tickets():

    for widget in container.winfo_children():
        widget.destroy()

    frame = tk.Frame(container)
    frame.pack()

    tk.Label(frame, text="All Tickets", font=("Arial", 18)).pack(pady=10)

    columns = ("Ticket", "Employee", "Category", "Priority", "Status", "Date")

    tree = ttk.Treeview(frame, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)

    tree.pack()

    cursor.execute("SELECT * FROM tickets")
    rows = cursor.fetchall()

    for r in rows:
        tree.insert("", tk.END, values=r)

    def delete_ticket():
        selected = tree.selection()
        if not selected:
            return

        item = tree.item(selected[0])
        ticket_id = item["values"][0]

        cursor.execute("DELETE FROM tickets WHERE ticket_id=?", (ticket_id,))
        conn.commit()

        tree.delete(selected)

    btn_frame = tk.Frame(frame)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Delete Ticket", command=delete_ticket).pack(side="left", padx=10)
    tk.Button(btn_frame, text="Back", command=dashboard).pack(side="left", padx=10)



def manage_employees():

    for widget in container.winfo_children():
        widget.destroy()

    frame = tk.Frame(container)
    frame.pack(pady=20)

    tk.Label(frame, text="Manage Employees", font=("Arial", 18)).pack()

    name_entry = tk.Entry(frame)
    name_entry.pack(pady=10)

    def add_emp():
        cursor.execute("INSERT INTO employees(name) VALUES(?)", (name_entry.get(),))
        conn.commit()
        messagebox.showinfo("Success", "Employee Added")

    tk.Button(frame, text="Add Employee", command=add_emp).pack(pady=5)
    tk.Button(frame, text="Back", command=dashboard).pack()



def manage_categories():

    for widget in container.winfo_children():
        widget.destroy()

    frame = tk.Frame(container)
    frame.pack(pady=20)

    tk.Label(frame, text="Manage Categories", font=("Arial", 18)).pack()

    name_entry = tk.Entry(frame)
    name_entry.pack(pady=10)

    def add_cat():
        cursor.execute("INSERT INTO categories(name) VALUES(?)", (name_entry.get(),))
        conn.commit()
        messagebox.showinfo("Success", "Category Added")

    tk.Button(frame, text="Add Category", command=add_cat).pack(pady=5)
    tk.Button(frame, text="Back", command=dashboard).pack()


# Start Dashboard
dashboard()

root.mainloop()