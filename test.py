import mysql.connector

# Connect to the database
connection = mysql.connector.connect(
    host="192.168.1.75",
    user="roote",
    password="root",
    database="comic"
)

# Create a cursor object
cursor = connection.cursor()

# Execute a simple query
cursor.execute("SELECT DATABASE();")

# Fetch and print the result
result = cursor.fetchone()
print(result)

# Close the connection
connection.close()
