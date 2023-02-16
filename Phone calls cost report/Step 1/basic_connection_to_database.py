"""create a python script that extracts phone call durations/costs
from a database on a server and outputs a costs by department and time period"""

import psycopg2

# Connect to the database
conn = psycopg2.connect(
    host="52.166.243.62",
    database="bitnami",
    user="postgres",
    password="Pratteln.4133",
    port="5432"
)

# Create a cursor object
cur = conn.cursor()

# Query the database for phone call durations and costs by department and time period
cur.execute("""
    SELECT
        phone_calls_department.name AS department,
        SUM(phone_calls_call.duration) AS total_duration,
        SUM(phone_calls_call.cost) AS total_cost,
        DATE_TRUNC('month', phone_calls_call.call_time) AS month_year
    FROM
        phone_calls_call
        JOIN phone_calls_department ON phone_calls_call.department_id = phone_calls_department.id
    WHERE
        phone_calls_call.call_time >= '2022-01-01' AND phone_calls_call.call_time < '2023-01-01'
    GROUP BY
        phone_calls_department.name,
        DATE_TRUNC('month', phone_calls_call.call_time)
""")

# Fetch the results and print them
results = cur.fetchall()
for result in results:
    department = result[0]
    total_duration = result[1]
    total_cost = result[2]  # multiply with price per second
    month_year = result[3].strftime("%Y-%m")
    print(f"{department}, {month_year}: Total duration = {total_duration} seconds, Total cost = {total_cost} ")

# Close the database connection
cur.close()
conn.close()
print(results)