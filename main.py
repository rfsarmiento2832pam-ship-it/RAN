import tkinter as tk
from db_connection import connect_db
from tkinter import ttk
from tkinter import messagebox


db = connect_db()
cursor = db.cursor()

selected_user_id = None


root = tk.Tk()

root.title("Multi Page Form Demo")
root.geometry("600x700")



# Make grid expandable
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# ----------------------------
# Function to switch pages
# ----------------------------
def show_frame(frame):
    frame.tkraise()

# ============================
# PAGE 1 (FORM)
# ============================
page1 = tk.Frame(root)
page1.grid(row=0, column=0, sticky="nsew")

tk.Label(page1, text="Registration Form").grid(row=0, column=0, columnspan=2, pady=10)

# First Name
tk.Label(page1, text="First Name:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
first_name_entry = tk.Entry(page1)
first_name_entry.grid(row=1, column=1, padx=10, pady=5)

# Last Name
tk.Label(page1, text="Last Name:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
last_name_entry = tk.Entry(page1)
last_name_entry.grid(row=2, column=1, padx=10, pady=5)

#Combobox membership
ttk.Label(page1, text = "Membership Type:").grid(row=3, column=0, padx=10, pady=5)

n = tk.StringVar()
type = ttk.Combobox(page1, textvariable = n)

type['values'] = ('Regular', 'Premium', 'Student', 'Senior')
type.grid(row=3, column=1, padx=10, pady=5)

#Combobox genre
ttk.Label(page1, text = "Preffered Genre:").grid(row=4, column=0, padx=10, pady=5)

n = tk.StringVar()
genre = ttk.Combobox(page1, textvariable = n)

genre['values'] = ('Fiction', 'Non-Fiction', 'Science', 'History', 'Technology', 'Fantasy')
genre.grid(row=4, column=1, padx=10, pady=5)

def only_numbers(char):
    return char.isdigit() or char == ""

validation = root.register(only_numbers)

#barrow limit
tk.Label(page1, text="Borrow Limit:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
borrow_limit_entry = tk.Entry(page1, validate="key", validatecommand=(validation, '%P'))
borrow_limit_entry.grid(row=5, column=1, padx=10, pady=5)

#Membership Status
ttk.Label(page1, text="Membership Status:").grid(row=6, column=0, padx=10, pady=5)

status_var = tk.StringVar()
status = ttk.Combobox(page1, textvariable=status_var)

status['values'] = ('Active', 'Suspended', 'Expired')
status.grid(row=6, column=1, padx=10, pady=5)

#Email
tk.Label(page1, text="Email Address:").grid(row=7, column=0, padx=10, pady=5, sticky="e")
email_entry = tk.Entry(page1)
email_entry.grid(row=7, column=1, padx=10, pady=5)


def clear_form():
    first_name_entry.delete(0, tk.END)
    last_name_entry.delete(0, tk.END)
    borrow_limit_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    type.set("")
    genre.set("")
    status.set("")



# Button to go to page 2
def go_to_page2():

    global selected_user_id

    fname = first_name_entry.get()
    lname = last_name_entry.get()
    membership_type = type.get()
    preferred_genre = genre.get()
    borrow_limit = borrow_limit_entry.get()
    membership_status = status.get()
    email = email_entry.get()

    full_name = fname + " " + lname

    if not borrow_limit.isdigit():
        messagebox.showerror("Error", "Borrow limit must be a number")
        return

    if "@" not in email:
        messagebox.showerror("Error", "Email must contain '@'")
        return

    val_limit = int(borrow_limit)

    if selected_user_id is None:

        sql = """
        INSERT INTO users
        (full_name, membership_type, preferred_genre, borrow_limit, membership_status, email)
        VALUES (%s,%s,%s,%s,%s,%s)
        """

        values = (full_name, membership_type, preferred_genre, val_limit, membership_status, email)
        cursor.execute(sql, values)

    else:

        sql = """
        UPDATE users
        SET full_name=%s, membership_type=%s, preferred_genre=%s,
        borrow_limit=%s, membership_status=%s, email=%s
        WHERE id=%s
        """

        values = (full_name, membership_type, preferred_genre, val_limit, membership_status, email, selected_user_id)
        cursor.execute(sql, values)

        selected_user_id = None

    db.commit()

    display_label.config(
        text=f"""
Full Name: {full_name}
Membership Type: {membership_type}
Preferred Genre: {preferred_genre}
Borrow Limit: {val_limit}
Membership Status: {membership_status}
Email: {email}
"""
    )

    clear_form()

    show_frame(page2)



def delete_user(user_id):

    cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
    db.commit()
    show_all_users()



def edit_user(row):

    global selected_user_id

    selected_user_id = row[0]

    name = row[1].split(" ")

    first_name_entry.insert(0, name[0])
    last_name_entry.insert(0, name[1])

    type.set(row[2])
    genre.set(row[3])
    borrow_limit_entry.insert(0, row[4])
    status.set(row[5])
    email_entry.insert(0, row[6])

    show_frame(page1)



def show_all_users():

    for widget in users_frame.winfo_children():
        widget.destroy()

    cursor.execute("SELECT * FROM users")
    records = cursor.fetchall()

    for row in records:

        row_frame = tk.Frame(users_frame)
        row_frame.pack(pady=5)

        tk.Label(row_frame, text=row[0], width=5).pack(side="left")
        tk.Label(row_frame, text=row[1], width=20).pack(side="left")
        tk.Label(row_frame, text=row[2], width=10).pack(side="left")
        tk.Label(row_frame, text=row[4], width=5).pack(side="left")

        tk.Button(row_frame, text="Edit",
                  command=lambda r=row: edit_user(r)).pack(side="left", padx=5)

        tk.Button(row_frame, text="Delete",
                  command=lambda uid=row[0]: delete_user(uid)).pack(side="left")

    show_frame(page3)


tk.Button(page1, text="Submit", command=go_to_page2).grid(row=9, column=0, columnspan=2, pady=15)
tk.Button(page1, text="Show Users", command=show_all_users).grid(row=10, column=0, columnspan=2, pady=15)

# ============================
# PAGE 2 (DISPLAY DATA)
# ============================
page2 = tk.Frame(root)
page2.grid(row=0, column=0, sticky="nsew")

tk.Label(page2, text="Entered Information", font=("Arial", 14)).pack(pady=10)

display_label = tk.Label(page2, text="", font=("Arial", 12))
display_label.pack(pady=10)

tk.Button(page2, text="Back", command=lambda: show_frame(page1)).pack(pady=10)

# ============================
# PAGE 3 (USERS LIST)
# ============================
page3 = tk.Frame(root)
page3.grid(row=0,column=0,sticky="nsew")

tk.Label(page3, text="Users List", font=("Arial", 14)).pack(pady=10)

users_frame = tk.Frame(page3)
users_frame.pack()

tk.Button(page3, text="Back", command=lambda: show_frame(page1)).pack(pady=10)

# End Page 3

# Start with page 1
show_frame(page1)

root.mainloop()