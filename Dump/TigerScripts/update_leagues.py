import pymysql
import csv
import os

def safe_str(value):
    """Helper function to safely convert values to strings."""
    return value.strip() if value and value.strip() else None

def update_leagues(db_config, csv_folder):
    """Process a Leagues CSV file and update the database."""
    # Define the CSV file name
    csv_file_name = 'Leagues.csv'
    csv_file_path = os.path.join(csv_folder, csv_file_name)

    # Connect to the MySQL (MariaDB) database using PyMySQL
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    # Define a mapping from CSV column names to table column names
    column_mapping = {
        'lgID': 'lgID',
        'league_name': 'league_name',
        'league_active': 'league_active'
    }

    # Define the table columns based on your database schema
    table_columns = ['lgID', 'league_name', 'league_active']

    # Open the CSV file to read data
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        rows = list(csv_reader)

        for idx, row in enumerate(rows, start=1):
            try:
                # Validate and clean data
                cleaned_row = {}
                for csv_col, db_col in column_mapping.items():
                    value = row.get(csv_col, '').strip()

                    if value == '':  # Handle empty strings as None
                        cleaned_row[db_col] = None
                    else:
                        cleaned_row[db_col] = value

                # Ensure required fields are not missing
                required_fields = ['lgID']
                if not all(cleaned_row.get(field) for field in required_fields):
                    print(f"Skipping row {idx} due to missing required fields.")
                    continue

                # Construct the column values
                values = [cleaned_row[col] for col in table_columns]

                # Create the INSERT statement with ON DUPLICATE KEY UPDATE
                update_values = ', '.join([f"{col} = VALUES({col})" for col in table_columns[1:]])  # Skip unique key columns
                placeholders = ', '.join(['%s'] * len(values))

                query = f"""
                INSERT INTO leagues ({', '.join(table_columns)}) 
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

    print(f"Data from {csv_file_path} successfully imported into the 'leagues' table.")

# Main entry point
def main(db_config, csv_folder):
    """Main function to handle the process of importing CSV data into the database."""
    update_leagues(db_config, csv_folder)
