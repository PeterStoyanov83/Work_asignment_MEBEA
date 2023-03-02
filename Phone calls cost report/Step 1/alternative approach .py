import mysql.connector
import pandas as pd

# Connect to the MySQL database
cnx = mysql.connector.connect(user='walld_mebea', password='nyrVN49VniKJvfU',
                              host='mysql1.webland.ch', database='walld_mebea')
cursor = cnx.cursor()

# Query to get the total duration of phone calls for each department
query = """
    SELECT t_employees.Name, SUM(telephone_calls.Gespraechsdauer) as total_duration, t_departments.Name as Department, 
    t_departments.manager
FROM telephone_calls
INNER JOIN t_employees ON telephone_calls.Rufnummer = t_employees.phone
INNER JOIN t_departments ON t_employees.department_id = t_departments.id
GROUP BY t_employees.Name, Department, t_departments.manager
"""

# Execute the query
cursor.execute(query)

# Fetch the results into a pandas dataframe
results = pd.DataFrame(cursor.fetchall(),
                       columns=['Employee Name', 'Total Duration (minutes)', 'Department', 'Manager'])

# Export the results to a CSV file and puts it in the same directory with the python code file
results.to_csv('phone_calls.csv', index=False)
print('File created! take a look in the folder containing this python script. ')

# Commit the changes to the database
cnx.commit()

# Close the database connection
cursor.close()
cnx.close()
