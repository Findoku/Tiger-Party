import pymysql
import csv
import os

def update_allstar_csv(db_config, csv_file_path):
    # Connect to the MySQL (MariaDB) database using PyMySQL
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    ...


# Get the current working directory
current_dir = os.getcwd()

# Define the CSV file name
csv_file_name = 'Salaries.csv'

# Combine the current directory with the CSV file name
csv_file_path = os.path.join(csv_folder, csv_file_name)

# Connect to the MySQL (MariaDB) database
conn = pymysql.connect(**db_config)
cursor = conn.cursor()

# Define a mapping from CSV column names to table column names
column_mapping = {
    'playerID': 'playerID',
    'yearID': 'yearId',
    'teamID': 'teamID',
    'salary': 'salary'
}

# Define the table columns based on your database schema
table_columns = ['playerID', 'yearId', 'teamID', 'salary']

# Open the CSV file to read data
with open(csv_file_path, 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    rows = list(csv_reader)

    # Iterate over each row and insert or update the data
    for idx, row in enumerate(rows, start=1):
        try:
            # Validate and clean data
            cleaned_row = {}
            for csv_col, db_col in column_mapping.items():
                value = row.get(csv_col, '').strip()

                if value == '':  # Handle empty strings as default
                    cleaned_row[db_col] = None if db_col == 'salary' else ''
                elif db_col == 'salary':  # Handle numeric fields
                    cleaned_row[db_col] = float(value) if value else None
                else:  # Handle string fields
                    cleaned_row[db_col] = value

            # Ensure required fields are not missing
            required_fields = ['playerID', 'yearId', 'teamID']
            if not all(cleaned_row.get(field) for field in required_fields):
                print(f"Skipping row {idx}: Missing required fields: {cleaned_row}")
                continue  # Skip row if required fields are missing

            # Construct the column values
            values = [cleaned_row[col] for col in table_columns]

            # Create the INSERT statement with ON DUPLICATE KEY UPDATE
            update_values = ', '.join([f"{col} = VALUES({col})" for col in table_columns[1:]])  # Skip primary key
            placeholders = ', '.join(['%s'] * len(values))

            query = f"""
            INSERT INTO salaries ({', '.join(table_columns)}) 
            VALUES ({placeholders})
            ON DUPLICATE KEY UPDATE {update_values};
            """

            # Execute the query
            cursor.execute(query, values)

        except Exception as e:
            print(f"Error processing row {idx}: {row}")
            print(f"Error details: {e}")
            continue

    # Commit the changes
    conn.commit()

# Close the database connection
cursor.close()
conn.close()

print(f"Data from {csv_file_path} successfully imported into the 'salaries' table.")
