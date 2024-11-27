import sqlite3

#  To establish SQLite database connection
conn = sqlite3.connect('users_data.db')  
cursor = conn.cursor()

# Create Table For Login
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    email TEXT
)
''')
conn.commit() 

print("Database aand table successfully Created!")

# To close Database Connection
conn.close()
