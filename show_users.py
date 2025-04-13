import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("eduassist.db")
cursor = conn.cursor()

# Fetch all entries from the users table
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

# Print the table header
print("{:<5} {:<20} {:<30} {:<60} {:<20}".format(
    "ID", "Name", "Email", "Password (Hashed)", "Interests"
))
print("=" * 130)

# Print each row
for row in rows:
    id, name, email, password, interests = row
    # Decode the hashed password from bytes to string
    password_str = password.decode("utf-8") if isinstance(password, bytes) else str(password)
    print("{:<5} {:<20} {:<30} {:<60} {:<20}".format(
        id, name, email, password_str, interests if interests else "None"
    ))

# Close the database connection
conn.close()