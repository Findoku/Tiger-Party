import pymysql
import csv
import os

def update_battingpost(db_config, csv_folder):
    """Process the battingpost CSV file and update the database."""
    # Define the CSV file name
    csv_file_name = 'battingpost.csv'

    # Combine the folder path and CSV file name
    csv_file_path = os.path.join(csv_folder, csv_file_name)

    # Connect to the database
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    # Define a mapping from CSV column names to table column names for battingpost
    column_mapping = {
        'yearID': 'yearId',
        'round': 'round',
        'playerID': 'playerID',
        'teamID': 'teamID',
        'lgID': 'lgID',
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

    # Define the table columns based on your database schema
    table_columns = [
        'playerID', 'yearId', 'round', 'teamID', 'b_G', 'b_AB', 'b_R', 'b_H',
        'b_2B', 'b_3B', 'b_HR', 'b_RBI', 'b_SB', 'b_CS', 'b_BB', 'b_SO',
        'b_IBB', 'b_HBP', 'b_SH', 'b_SF', 'b_GIDP'
    ]

    # Open the CSV file and read data
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        rows = list(csv_reader)

        for idx, row in enumerate(rows, start=1):
            try:
                # Validate and clean data
                cleaned_row = {}
                for csv_col, db_col in column_mapping.items():
                    value = row.get(csv_col, '').strip()

                    if value == '':  # Handle empty strings as None to make it NULL
                        cleaned_row[db_col] = None
                    elif db_col.startswith('b_') or db_col in ['yearId']:  # Numeric fields
                        try:
                            if db_col == 'b_G':
                                cleaned_row[db_col] = int(value) if value else None
                            elif value.isdigit():
                                cleaned_row[db_col] = int(value)
                            else:
                                cleaned_row[db_col] = None  # Set to None if not valid number
                        except ValueError:
                            cleaned_row[db_col] = None  
                    else:  
                        cleaned_row[db_col] = value

                # Ensure required fields are not missing
                required_fields = ['playerID', 'yearId', 'round', 'teamID']
                if not all(cleaned_row.get(field) for field in required_fields):
                    continue  # Skip row if required fields are missing

                # Construct the column values
                values = [cleaned_row[col] for col in table_columns]

                # Create the INSERT statement with ON DUPLICATE KEY UPDATE
                update_values = ', '.join([f"{col} = VALUES({col})" for col in table_columns[4:]])  # Skip keys
                placeholders = ', '.join(['%s'] * len(values))

                query = f"""
                INSERT INTO battingpost ({', '.join(table_columns)}) 
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

    print(f"Data from {csv_file_path} successfully imported into the 'battingpost' table.")

# Define the main function for this script
def main(db_config, csv_folder):
    """Main entry point for the update script."""
    # Call the function to update the battingpost data
    update_battingpost(db_config, csv_folder)
