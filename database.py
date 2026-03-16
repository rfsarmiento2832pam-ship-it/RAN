import mysql.connector
from datetime import datetime

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "helpdesk_db"
}

def get_db_connection(create_db=False):
    if create_db:
        return mysql.connector.connect(host="localhost", user="root", password="")
    return mysql.connector.connect(**db_config)

def init_db():
    conn = get_db_connection(create_db=True)
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS helpdesk_db")
    conn.close()

    conn = get_db_connection()
    cursor = conn.cursor()

    # Table: employees
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INT AUTO_INCREMENT PRIMARY KEY,
        employee_no VARCHAR(255),
        first_name VARCHAR(255),
        last_name VARCHAR(255),
        department_id INT,
        created_at DATETIME,
        created_by VARCHAR(255),
        updated_at DATETIME,
        updated_by VARCHAR(255),
        deleted_at DATETIME NULL,
        deleted_by VARCHAR(255) NULL
    )""")

    # Table: categories
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        created_at DATETIME,
        created_by VARCHAR(255),
        updated_at DATETIME,
        updated_by VARCHAR(255),
        deleted_at DATETIME NULL,
        deleted_by VARCHAR(255) NULL
    )""")

    # Table: tickets
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        id INT AUTO_INCREMENT PRIMARY KEY,
        ticket_no VARCHAR(255),
        employee_id INT,
        category_id INT,
        priority ENUM('Low', 'Medium', 'High', 'Critical'),
        subject VARCHAR(255),
        description TEXT,
        status ENUM('Open', 'In Progress', 'Resolved', 'Closed'),
        created_at DATETIME,
        created_by VARCHAR(255),
        updated_at DATETIME,
        updated_by VARCHAR(255),
        deleted_at DATETIME NULL,
        deleted_by VARCHAR(255) NULL
    )""")

    # Seed Categories
    cursor.execute("SELECT COUNT(*) FROM categories")
    if cursor.fetchone()[0] == 0:
        cats = ["Hardware Issue", "Software Installation", "System Error", "Network Connectivity", 
                "Printer and Peripherals", "Email and Messaging", "Account Access", "Password Reset", 
                "Security Concern", "Performance Issue", "Data Backup and Recovery", "Server Issue"]
        for c in cats:
            cursor.execute("INSERT INTO categories (name, created_at, created_by) VALUES (%s, %s, %s)", 
                           (c, datetime.now(), "Admin"))
    
    conn.commit()
    conn.close()
