import pymysql
import csv
import os

def safe_str(value):
    """Helper function to safely convert values to strings."""
    return value.strip() if value else None

def main(db_config, csv_folder):
    
    # Define the CSV file name and build the path
    csv_file_name = 'SeriesPost.csv'
    csv_file_path = os.path.join(csv_folder, csv_file_name)
    
    # Connect to the MySQL (MariaDB) database using the provided db_config
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    # Define a mapping from CSV column names to table column names
    column_mapping = {
        'yearID': 'yearID',
        'round': 'round',
        'teamIDwinner': 'teamIDwinner',
        'teamIDloser': 'teamIDloser',
        'wins': 'wins',
        'losses': 'losses',
        'ties': 'ties'
    }

    # Define the table columns based on your database schema
    table_columns = [
        'yearID', 'round', 'teamIDwinner', 'teamIDloser',
        'wins', 'losses', 'ties'
    ]

    try:
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
                        else:
                            cleaned_row[db_col] = value

                    # Ensure required fields are not missing
                    required_fields = ['yearID', 'round', 'teamIDwinner', 'teamIDloser']
                    if not all(cleaned_row.get(field) for field in required_fields):
                        print(f"Skipping row {idx} due to missing required fields: {row}")
                        continue  # Skip row if required fields are missing

                    # Construct the column values
                    values = [cleaned_row[col] for col in table_columns]

                    # Create the INSERT statement with ON DUPLICATE KEY UPDATE
                    update_values = ', '.join([f"{col} = VALUES({col})" for col in table_columns[2:]])  # Skip keys
                    placeholders = ', '.join(['%s'] * len(values))

                    query = f"""
                    INSERT INTO seriespost ({', '.join(table_columns)}) 
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
        print(f"Data from {csv_file_path} successfully imported into the 'seriespost' table.")

    except Exception as e:
        print(f"Error reading the CSV file {csv_file_path}: {e}")

    finally:
        # Close the database connection
        cursor.close()
        conn.close()
