import mysql.connector
import time



# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="yourusername",
    password="yourpassword",
    database="yourdatabase"
)

# Create a cursor object to execute SQL queries
cursor = db.cursor()

# Insert data into the database
query = "INSERT INTO clockinout (datetime, status) VALUES (%s, %s)"
values = (datetime.datetime.now(), "Clock In")
cursor.execute(query, values)
db.commit()

# Retrieve data from the database
query = "SELECT * FROM clockinout WHERE status = 'Clock In'"
cursor.execute(query)
result = cursor.fetchall()

# Close the database connection
db.close()
