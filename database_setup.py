import sqlite3

# SQLite database ka connection establish karna
conn = sqlite3.connect('users_data.db')  # Agar file nahi hai to yeh nayi file create karega
cursor = conn.cursor()

# Ek table banayen login ke liye
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    email TEXT
)
''')
conn.commit()  # Changes ko save karne ke liye

print("Database aur table successfully ban gaya!")

# Database connection close karna
conn.close()
