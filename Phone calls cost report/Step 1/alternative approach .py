import mysql.connector

# Connect to the MySQL database
cnx = mysql.connector.connect(user='walld_mebea', password='nyrVN49VniKJvfU',
                              host='mysql1.webland.ch', database='walld_mebea')
cursor = cnx.cursor()

# Query to get the total duration of phone calls for each department
query = """
    SELECT t_employees.name, t_departments.name, SUM(telephone_calls.Gespraechsdauer) as total_duration
    FROM telephone_calls
    INNER JOIN employees ON telephone_calls.Rufnummer = employees.id
    INNER JOIN departments ON employees.DNR = departments.id
    GROUP BY employees.name, departments.name
"""

# Execute the query
cursor.execute(query)

# Print the results
for (employee_name, department_name, total_duration, department_manager) in cursor:
    print(f"{employee_name}: {total_duration} minutes, Department: {department_name} (Manager: {department_manager})")

# Commit the changes to the database
cnx.commit()

# Close the database connection
cursor.close()
cnx.close()
