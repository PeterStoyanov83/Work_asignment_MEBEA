import pandas as pd

# Read the input CSV file
input_file = "Telefonkosten_2023_with_Costs.csv"
df = pd.read_csv(input_file, encoding='ISO-8859-1')

# Convert the first column to a date/time format with the specified format
df[df.columns[0]] = pd.to_datetime(df[df.columns[0]], format="%Y-%m-%d %H:%M:%S")

# Convert the date/time column to the desired format
df[df.columns[0]] = df[df.columns[0]].dt.strftime('%H:%M:%S')

# Combine the modified first column with the rest of the columns
df_out = pd.concat([df[df.columns[0]], df.iloc[:, 1:]], axis=1)

# Write the modified data to a new CSV file
output_file = input_file.split("-")[0] + "1.csv"
df.to_csv(output_file, index=False)

print("Done!")