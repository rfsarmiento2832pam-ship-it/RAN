import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database import init_db, get_db_connection

class HelpdeskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Helpdesk Ticket Management System")
        self.root.geometry("800x600")
        init_db()
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)
        self.dashboard()

    def clear_screen(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # Module 1 - Dashboard
    def dashboard(self):
        self.clear_screen()
        tk.Label(self.main_frame, text="Dashboard", font=("Arial", 20)).pack(pady=20)
        tk.Button(self.main_frame, text="Create Ticket", width=25, command=self.create_ticket_form).pack(pady=5)
        tk.Button(self.main_frame, text="View Tickets", width=25, command=self.view_tickets_module).pack(pady=5)
        tk.Button(self.main_frame, text="Manage Employees", width=25, command=self.manage_employees).pack(pady=5)
        tk.Button(self.main_frame, text="Manage Categories", width=25, command=self.manage_categories).pack(pady=5)

    # Module 2 - Create Ticket Form
    def create_ticket_form(self):
        self.clear_screen()
        tk.Label(self.main_frame, text="Create New Ticket", font=("Arial", 15)).pack(pady=10)
        
        fields = ["Ticket Number", "Employee ID", "Category ID", "Subject", "Description"]
        entries = {}
        for f in fields:
            tk.Label(self.main_frame, text=f).pack()
            e = tk.Entry(self.main_frame, width=40)
            e.pack()
            entries[f] = e

        tk.Label(self.main_frame, text="Priority").pack()
        pri = ttk.Combobox(self.main_frame, values=["Low", "Medium", "High", "Critical"])
        pri.pack()

        def save():
            conn = get_db_connection(); cursor = conn.cursor()
            cursor.execute("""INSERT INTO tickets (ticket_no, employee_id, category_id, priority, subject, description, status, created_at, created_by) 
                           VALUES (%s, %s, %s, %s, %s, %s, 'Open', %s, 'Admin')""",
                           (entries["Ticket Number"].get(), entries["Employee ID"].get(), entries["Category ID"].get(), pri.get(), entries["Subject"].get(), entries["Description"].get(), datetime.now()))
            conn.commit(); conn.close()
            messagebox.showinfo("Success", "Ticket Created"); self.dashboard()

        tk.Button(self.main_frame, text="Save Ticket", command=save).pack(pady=10)
        tk.Button(self.main_frame, text="Back", command=self.dashboard).pack()

    # Module 3 - View Tickets
    def view_tickets_module(self):
        self.clear_screen()
        cols = ("Ticket Number", "Employee ID", "Category ID", "Priority", "Status", "Date Created")
        tree = ttk.Treeview(self.main_frame, columns=cols, show="headings")
        for c in cols: tree.heading(c, text=c)
        tree.pack(fill="both", expand=True)

        conn = get_db_connection(); cursor = conn.cursor()
        cursor.execute("SELECT ticket_no, employee_id, category_id, priority, status, created_at FROM tickets WHERE deleted_at IS NULL")
        for r in cursor.fetchall(): tree.insert("", "end", values=r)
        conn.close()

        tk.Button(self.main_frame, text="Back", command=self.dashboard).pack(pady=10)

    # Module 4 - Manage Employees
    def manage_employees(self):
        self.clear_screen()
        tk.Label(self.main_frame, text="Manage Employees").pack()
        
        f_emp = tk.Frame(self.main_frame); f_emp.pack(pady=10)
        tk.Label(f_emp, text="Emp No").grid(row=0, column=0)
        en = tk.Entry(f_emp); en.grid(row=0, column=1)
        tk.Label(f_emp, text="First").grid(row=0, column=2)
        ef = tk.Entry(f_emp); ef.grid(row=0, column=3)
        tk.Label(f_emp, text="Last").grid(row=0, column=4)
        el = tk.Entry(f_emp); el.grid(row=0, column=5)
        tk.Label(f_emp, text="Dept ID").grid(row=0, column=6)
        ed = tk.Entry(f_emp); ed.grid(row=0, column=7)

        def add():
            conn = get_db_connection(); cursor = conn.cursor()
            cursor.execute("INSERT INTO employees (employee_no, first_name, last_name, department_id, created_at) VALUES (%s, %s, %s, %s, %s)",
                           (en.get(), ef.get(), el.get(), ed.get(), datetime.now()))
            conn.commit(); conn.close(); self.manage_employees()

        tk.Button(self.main_frame, text="Add Employee", command=add).pack()
        tk.Button(self.main_frame, text="Back", command=self.dashboard).pack(pady=10)

    # Module 5 - Manage Categories
    def manage_categories(self):
        self.clear_screen()
        tk.Label(self.main_frame, text="Manage Categories").pack()
        
        e_cat = tk.Entry(self.main_frame)
        e_cat.pack()

        def add():
            conn = get_db_connection(); cursor = conn.cursor()
            cursor.execute("INSERT INTO categories (name, created_at) VALUES (%s, %s)", (e_cat.get(), datetime.now()))
            conn.commit(); conn.close(); self.manage_categories()

        tk.Button(self.main_frame, text="Add Category", command=add).pack()
        
        tree = ttk.Treeview(self.main_frame, columns=("Name"), show="headings")
        tree.heading("Name", text="Category Name")
        tree.pack()
        
        conn = get_db_connection(); cursor = conn.cursor()
        cursor.execute("SELECT name FROM categories WHERE deleted_at IS NULL")
        for r in cursor.fetchall(): tree.insert("", "end", values=r)
        conn.close()

        tk.Button(self.main_frame, text="Back", command=self.dashboard).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = HelpdeskApp(root)
    root.mainloop()
