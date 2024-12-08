import pymysql
import csv
import os

def update_batting_csv(db_config, csv_folder):
    """Process a batting CSV file with column mapping and update the database."""
    # Define the CSV file name
    csv_file_name = 'batting.csv'

    # Combine the folder path and CSV file name
    csv_file_path = os.path.join(csv_folder, csv_file_name)

    # Connect to the database
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    # Define a mapping from CSV column names to table column names
    column_mapping = {
        'playerID': 'playerID',
        'yearID': 'yearId',
        'stint': 'stint',
        'teamID': 'teamID',
        'G': 'b_G',
        'AB': 'b_AB',
        'R': 'b_R',
        'H': 'b_H',
        '2B': 'b_2B',
        '3B': 'b_3B',
        'HR': 'b_HR',
        'RBI': 'b_RBI',
        'SB': 'b_SB',
        'CS': 'b_CS',
        'BB': 'b_BB',
        'SO': 'b_SO',
        'IBB': 'b_IBB',
        'HBP': 'b_HBP',
        'SH': 'b_SH',
        'SF': 'b_SF',
        'GIDP': 'b_GIDP'
    }

    table_columns = [
        'playerID', 'yearId', 'stint', 'b_G', 'teamID', 'b_AB', 'b_R', 'b_H', 
        'b_2B', 'b_3B', 'b_HR', 'b_RBI', 'b_SB', 'b_CS', 'b_BB', 'b_SO', 
        'b_IBB', 'b_HBP', 'b_SH', 'b_SF', 'b_GIDP'
    ]

    # Open the CSV file and read data
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        rows = list(csv_reader)

        for idx, row in enumerate(rows, start=1):
            try:
                cleaned_row = {}
                for csv_col, db_col in column_mapping.items():
                    value = row.get(csv_col, '').strip()
                    if value == '':
                        cleaned_row[db_col] = None
                    elif db_col.startswith('b_') or db_col in ['yearId', 'stint']:
                        try:
                            cleaned_row[db_col] = int(value) if value else None
                        except ValueError:
                            cleaned_row[db_col] = None
                    else:
                        cleaned_row[db_col] = value

                # Ensure required fields are not missing
                required_fields = ['playerID', 'yearId', 'stint', 'teamID']
                if not all(cleaned_row.get(field) for field in required_fields):
                    print(f"Skipping row {idx} due to missing required fields.")
                    continue

                # Prepare the column values
                values = [cleaned_row[col] for col in table_columns]
                update_values = ', '.join([f"{col} = VALUES({col})" for col in table_columns[4:]])  # Skip primary key columns
                placeholders = ', '.join(['%s'] * len(values))

                # Create the SQL query for inserting or updating data
                query = f"""
                INSERT INTO batting ({', '.join(table_columns)}) 
                VALUES ({placeholders})
                ON DUPLICATE KEY UPDATE {update_values};
                """
                cursor.execute(query, values)

            except Exception as e:
                print(f"Error processing row {idx}: {row}")
                print(f"Error details: {e}")
                continue

        # Commit changes to the database
        conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    print(f"Data from {csv_file_path} successfully imported into the 'batting' table.")

# Define the main function for this script
def main(db_config, csv_folder):
    """Main entry point for the update script."""
    # Call the function to update the batting data
    update_batting_csv(db_config, csv_folder)
