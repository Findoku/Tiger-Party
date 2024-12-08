import pymysql
import csv
import os

def update_collegeplaying(db_config, csv_folder):
    """Function to update college playing data in the database."""
    # Get the current working directory
    current_dir = os.getcwd()

    # Define the CSV file name
    csv_file_name = 'CollegePlaying.csv'

    # Combine the current directory with the CSV file name
    csv_file_path = os.path.join(csv_folder, csv_file_name)

    # Connect to the MySQL (MariaDB) database using PyMySQL
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    # Open the CSV file to read data
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        rows = list(csv_reader)

        # Iterate over each row and insert or update the data
        for idx, row in enumerate(rows, start=1):
            try:
                # Clean and validate data
                playerID = row.get('playerID', '').strip()
                schoolID = row.get('schoolID', '').strip()
                yearID = row.get('yearID', '').strip()

                # Skip rows with missing required fields
                if not playerID or not schoolID or not yearID:
                    print(f"Skipping row {idx} due to missing required fields.")
                    continue

                # Ensure yearID is an integer
                try:
                    yearID = int(yearID)
                except ValueError:
                    print(f"Skipping row {idx}: Invalid yearID '{yearID}'")
                    continue

                # Create the INSERT statement with ON DUPLICATE KEY UPDATE
                query = """
                INSERT INTO collegeplaying (playerID, schoolID, yearID)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                    schoolID = VALUES(schoolID),
                    yearID = VALUES(yearID);
                """

                # Execute the query
                cursor.execute(query, (playerID, schoolID, yearID))

            except Exception as e:
                print(f"Error processing row {idx}: {row}")
                print(f"Error details: {e}")
                continue

        # Commit the changes
        conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    print(f"Data from {csv_file_path} successfully imported into the 'collegeplaying' table.")

def main(db_config, csv_folder):
    """Main function to execute the update_collegeplaying function."""
    update_collegeplaying(db_config, csv_folder)
