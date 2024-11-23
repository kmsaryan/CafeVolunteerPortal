import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("db.sqlite")
cursor = conn.cursor()

# Create Signups table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Signups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    attendance TEXT DEFAULT 'Pending'
);
""")

# Create Credits table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Credits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    date DATE NOT NULL,
    amount_made REAL NOT NULL,
    balance REAL NOT NULL
);
""")

# Create Debits table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Debits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    date DATE NOT NULL,
    amount_spent REAL NOT NULL,
    balance REAL NOT NULL
);
""")

# Commit changes and close connection
conn.commit()
conn.close()
print("Database setup complete.")
