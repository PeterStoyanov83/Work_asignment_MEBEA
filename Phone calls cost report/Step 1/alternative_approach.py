'''this is a project that enters a database located in a server.

STEP 1 :
Makes a sellection of several columns and
outputs a csv file with the result. the conditions in query are make a list by departments and calculate the total
minutes each department spent on the phone. '''

import mysql.connector
import pandas as pd
import os.path

# Connect to the MySQL database
cnx = mysql.connector.connect(user='walld_mebea', password='nyrVN49VniKJvfU',
                              host='mysql1.webland.ch', database='walld_mebea')
cursor = cnx.cursor()

# Query to get the total duration of phone calls for each department and the total duration of phone calls from the phonecalls_with_costs entity
query = """
SELECT t_employees.Name, SUM(telephone_calls.Gespraechsdauer) as total_duration, t_departments.Name as Department, 
t_departments.manager,
       IFNULL(pcc.total_duration, 0) as phone_calls_with_costs_total_duration
FROM telephone_calls
INNER JOIN t_employees ON telephone_calls.Rufnummer = t_employees.phone
INNER JOIN t_departments ON t_employees.department_id = t_departments.id
LEFT JOIN (
    SELECT department, SUM(duration_minutes) as total_duration
    FROM phonecalls_with_cost
    GROUP BY department
) as pcc ON t_departments.Name = pcc.department
GROUP BY t_employees.Name, Department, t_departments.manager, pcc.total_duration
"""

# Execute the query
cursor.execute(query)

# Fetch the results into a pandas dataframe
results = pd.DataFrame(cursor.fetchall(),
                       columns=['Employee Name', 'Total Duration (minutes)', 'Department', 'Manager',
                                'Phone Calls with Costs Total Duration (minutes)'])
# Generate a file name with a suffix number that doesn't already exist
file_name = "phone_calls.csv"
max_attempts = 100
suffix = 1

while os.path.isfile(file_name) and suffix <= max_attempts:
    suffix += 1
    file_name = 'phone_calls' + str(suffix) + '.csv'
if suffix > max_attempts:
    raise Exception("Unable to generate a unique file name.")

# Export the results to a CSV file and puts it in the same directory with the python code file
results.to_csv(file_name, index=False, sep=';')
print('File created! take a look in the folder containing this python script. ')

# Commit the changes to the database
cnx.commit()

# Close the database connection
cursor.close()
cnx.close()
