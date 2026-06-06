import sqlite3

# Connect to the database file (creates it if it doesn't exist)
connection = sqlite3.connect("local_db.db")

# Create a cursor object to execute SQL commands
cursor = connection.cursor()

# Create a table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS squares (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        num INTEGER NOT NULL,
        square INTEGER NOT NULL
    )
""")

# Insert data securely using placeholders (?) to prevent SQL injection
try:
    for i in range(100):
        cursor.execute(
            "INSERT INTO squares (num, square) VALUES (?, ?)", 
            (i, i ** 2)
        )
        # Commit changes to save to the disk
        connection.commit()
except sqlite3.IntegrityError:
    print("Error inserting data")

# 5. Query data
cursor.execute("SELECT * FROM squares limit 5")
data = cursor.fetchall()

print("\n--- Current Data ---")
for row in data:
    print(f"ID: {row[0]} | NUM: {row[1]} | SQUARE: {row[2]}")

# 6. Close the connection when finished
connection.close()
