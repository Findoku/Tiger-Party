import pymysql
import csv
import os

def update_divisions(db_config, csv_folder):
    """Update the 'divisions' table from the CSV data."""
    # Get the path to the CSV file
    csv_file_path = os.path.join(csv_folder, 'divisions.csv')

    # Connect to the MySQL (MariaDB) database using PyMySQL
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    # Define a mapping from CSV column names to table column names
    column_mapping = {
        'divID': 'divID',
        'lgID': 'lgID',
        'division_name': 'division_name',
        'division_active': 'division_active'
    }

    # Define the table columns based on your database schema
    table_columns = ['divID', 'lgID', 'division_name', 'division_active']

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

                    if value == '':  # Handle empty strings as None to make NULL
                        cleaned_row[db_col] = None
                    else:
                        cleaned_row[db_col] = value

                # Ensure required fields are not missing
                required_fields = ['divID', 'lgID', 'division_name', 'division_active']
                if not all(cleaned_row.get(field) for field in required_fields):
                    continue  # Skip row if required fields are missing

                # Construct the column values
                values = [cleaned_row[col] for col in table_columns]

                # Create the INSERT statement with ON DUPLICATE KEY UPDATE
                update_values = ', '.join([f"{col} = VALUES({col})" for col in table_columns[1:]])  # Skip divID (unique key)
                placeholders = ', '.join(['%s'] * len(values))

                query = f"""
                INSERT INTO divisions ({', '.join(table_columns)}) 
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

    print(f"Data from {csv_file_path} successfully imported into the 'divisions' table.")

# Define the main function for this script
def main(db_config, csv_folder):
    """Main entry point for the update script."""
    update_divisions(db_config, csv_folder)
