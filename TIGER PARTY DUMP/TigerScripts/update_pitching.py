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
csv_file_name = 'pitching.csv'

# Combine the current directory with the CSV file name
sv_file_path = os.path.join(csv_folder, csv_file_name)

# Connect to the MySQL (MariaDB) database
conn = pymysql.connect(**db_config)
cursor = conn.cursor()

# Define a mapping from CSV column names to table column names
column_mapping = {
    'playerID': 'playerID',
    'yearID': 'yearID',
    'stint': 'stint',
    'teamID': 'teamID',
    'W': 'p_W',
    'L': 'p_L',
    'G': 'p_G',
    'GS': 'p_GS',
    'CG': 'p_CG',
    'SHO': 'p_SHO',
    'SV': 'p_SV',
    'IPouts': 'p_IPOuts',
    'H': 'p_H',
    'ER': 'p_ER',
    'HR': 'p_HR',
    'BB': 'p_BB',
    'SO': 'p_SO',
    'BAOpp': 'p_BAOpp',  # Decimal field
    'ERA': 'p_ERA',      # Decimal field
    'IBB': 'p_IBB',
    'WP': 'p_WP',
    'HBP': 'p_HBP',
    'BK': 'p_BK',
    'BFP': 'p_BFP',
    'GF': 'p_GF',
    'R': 'p_R',
    'SH': 'p_SH',
    'SF': 'p_SF',
    'GIDP': 'p_GIDP'
}

# Define the table columns based on your database schema
table_columns = [
    'playerID', 'yearID', 'stint', 'teamID', 'p_W', 'p_L', 'p_G', 'p_GS', 
    'p_CG', 'p_SHO', 'p_SV', 'p_IPOuts', 'p_H', 'p_ER', 'p_HR', 'p_BB', 
    'p_SO', 'p_BAOpp', 'p_ERA', 'p_IBB', 'p_WP', 'p_HBP', 'p_BK', 'p_BFP', 
    'p_GF', 'p_R', 'p_SH', 'p_SF', 'p_GIDP'
]

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

                if value == '':  # Handle empty strings as None
                    cleaned_row[db_col] = None
                elif db_col.startswith('p_') or db_col in ['yearID', 'stint']:  # Numeric fields
                    try:
                        if db_col == 'p_G' or db_col == 'p_W' or db_col == 'p_L':  # Handle integer fields
                            cleaned_row[db_col] = int(value) if value else None
                        elif db_col in ['p_BAOpp', 'p_ERA']:  # Handle decimal (float) fields
                            cleaned_row[db_col] = float(value) if value else None
                        elif value.isdigit():  # Handle other integer values
                            cleaned_row[db_col] = int(value)
                        else:
                            cleaned_row[db_col] = None  # Set to None if not valid number
                    except ValueError:
                        cleaned_row[db_col] = None  # Set as None if parsing fails
                else:  # String fields
                    cleaned_row[db_col] = value

            # Ensure required fields are not missing
            required_fields = ['playerID', 'yearID', 'stint', 'teamID']
            if not all(cleaned_row.get(field) for field in required_fields):
                continue  # Skip row if required fields are missing

            # Construct the column values
            values = [cleaned_row[col] for col in table_columns]

            # Create the INSERT statement with ON DUPLICATE KEY UPDATE
            update_values = ', '.join([f"{col} = VALUES({col})" for col in table_columns[4:]])  # Skip keys
            placeholders = ', '.join(['%s'] * len(values))

            query = f"""
            INSERT INTO pitching ({', '.join(table_columns)}) 
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

print(f"Data from {csv_file_path} successfully imported into the 'pitching' table.")
