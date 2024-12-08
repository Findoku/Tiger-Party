import pymysql
import csv
import os

# Helper function to remove non-ASCII characters
def remove_non_ascii(text):
    return ''.join([char for char in text if ord(char) < 128])

def update_awards(db_config, csv_folder):
    """Update the 'awards' table with data from the CSV files."""
    # Connect to the database
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    # List of CSV file names to process
    csv_files = ['AwardsManagers.csv', 'AwardsPlayers.csv']

    # Define the table columns based on your database schema
    table_columns = ['awardID', 'yearID', 'playerID', 'lgID', 'tie', 'notes']

    # Iterate over each CSV file
    for csv_file_name in csv_files:
        csv_file_path = os.path.join(csv_folder, csv_file_name)

        # Check if the file exists before processing
        if not os.path.exists(csv_file_path):
            print(f"File not found: {csv_file_path}")
            continue

        print(f"Processing file: {csv_file_name}")

        # Open the CSV file to read data
        with open(csv_file_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            rows = list(csv_reader)

            # Iterate over each row and insert or update the data
            for row in rows:
                # Clean the row values to remove non-ASCII characters
                for key in row:
                    row[key] = remove_non_ascii(row[key])  # Clean each field in the row

                # Handle 'tie' and 'notes' fields (strip and replace empty strings with None)
                row['tie'] = row.get('tie', '').strip() or None
                row['notes'] = row.get('notes', '').strip() or None

                # Construct the column values based on the mapping
                values = [row.get(column, None) for column in table_columns]

                # Create the INSERT statement with ON DUPLICATE KEY UPDATE
                update_values = ', '.join([f"{col} = VALUES({col})" for col in table_columns])  # All columns can be updated
                placeholders = ', '.join(['%s'] * len(values))

                query = f"""
                INSERT INTO awards ({', '.join(table_columns)}) 
                VALUES ({placeholders})
                ON DUPLICATE KEY UPDATE {update_values};
                """
                
                # Execute the query to insert or update the data
                cursor.execute(query, values)

        print(f"Finished processing file: {csv_file_name}")

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    print("Data from all CSV files successfully imported into the 'awards' table.")

def main(db_config, csv_folder):
    """Main entry point for the script."""
    # Call the update_awards function
    update_awards(db_config, csv_folder)


