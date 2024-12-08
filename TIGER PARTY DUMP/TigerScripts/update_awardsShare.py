import pymysql
import csv
import os

# Helper function to remove non-ASCII characters
def remove_non_ascii(text):
    return ''.join([char for char in text if ord(char) < 128])

def update_awardsshare(db_config, csv_folder):
    """Update the 'awardsshare' table with data from the CSV files."""
    # Connect to the database
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    # List of CSV file names to process
    csv_files = ['AwardsShareManagers.csv', 'awardsSharePlayers.csv']

    # Define the table columns based on your database schema
    table_columns = ['awardID', 'yearID', 'lgID', 'playerID', 'pointsWon', 'pointsMax', 'votesFirst']

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
                
                # Default empty fields to NULL, ensuring correct numeric types for points and votes
                row['pointsWon'] = float(row['pointsWon'].strip()) if row.get('pointsWon', '').strip() else None
                row['pointsMax'] = int(row['pointsMax'].strip()) if row.get('pointsMax', '').strip() else None
                row['votesFirst'] = float(row['votesFirst'].strip()) if row.get('votesFirst', '').strip() else None

                # Construct the column values based on the mapping
                values = [row.get(column, None) for column in table_columns]

                # Create the INSERT statement with ON DUPLICATE KEY UPDATE
                update_values = ', '.join([f"{col} = VALUES({col})" for col in table_columns])  # All columns can be updated
                placeholders = ', '.join(['%s'] * len(values))

                query = f"""
                INSERT INTO awardsshare ({', '.join(table_columns)}) 
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

    print("Data from all CSV files successfully imported into the 'awardsshare' table.")

def main(db_config, csv_folder):
    """Main entry point for the script."""
    # Call the update_awardsshare function
    update_awardsshare(db_config, csv_folder)

# Ensure that the script runs when executed directly
if __name__ == "__main__":
    # Get the current working directory (where the script is being run from)
    current_dir = os.getcwd()

    # Define the CSV folder (same folder as script for simplicity)
    csv_folder = current_dir

    # Database configuration (replace with your actual credentials)
    db_config = {
        'host': 'your_host',
        'user': 'your_user',
        'password': 'your_password',
        'database': 'your_database'
    }

    # Call the main function
    main(db_config, csv_folder)
