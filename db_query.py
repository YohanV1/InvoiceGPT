import sqlite3

# Connect to (or create) the database
conn = sqlite3.connect('invoices_data.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Execute the query
cursor.execute('SELECT * FROM line_items')

# Fetch all rows from the result
rows = cursor.fetchall()

# Print each row
for row in rows:
    print(row)

# Close the connection
conn.close()