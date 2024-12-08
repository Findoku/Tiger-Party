import pymysql
import csv
import os

def safe_int(value):
    """Safely convert a value to an integer or return None."""
    try:
        return int(value.strip()) if value and value.strip() else None
    except ValueError:
        return None

def safe_str(value):
    """Safely convert a value to a stripped string or return None."""
    return value.strip() if value and value.strip() else None

def insert_managers_with_null_half(cursor, rows):
    """Insert all records from managers.csv with 'half' set to NULL."""
    for idx, row in enumerate(rows, start=2):
        try:
            # Extract data from managers.csv
            playerID = safe_str(row.get('playerID'))
            yearID = safe_int(row.get('yearID'))
            teamID = safe_str(row.get('teamID'))
            inSeason = safe_int(row.get('inseason'))
            manager_G = safe_int(row.get('G'))
            manager_W = safe_int(row.get('W'))
            manager_L = safe_int(row.get('L'))
            teamRank = safe_int(row.get('rank'))
            plyrMgr = safe_str(row.get('plyrMgr'))

            # Set half to NULL for managers.csv
            half = None

            # Check if the record already exists (same playerID, yearID, teamID, inSeason)
            query_check = """
            SELECT managers_ID FROM managers 
            WHERE playerID = %s AND yearID = %s AND teamID = %s AND inSeason = %s;
            """
            cursor.execute(query_check, (playerID, yearID, teamID, inSeason))
            result = cursor.fetchone()

            if result:
                # Update the existing record
                query_update = """
                UPDATE managers 
                SET manager_G = %s, manager_W = %s, manager_L = %s, teamRank = %s, plyrMgr = %s
                WHERE managers_ID = %s;
                """
                cursor.execute(query_update, (manager_G, manager_W, manager_L, teamRank, plyrMgr, result[0]))
            else:
                # Insert the record as a new row if no matching record found
                query_insert = """
                INSERT INTO managers (
                    playerID, yearID, teamID, inSeason, manager_G, manager_W, manager_L, teamRank, plyrMgr, half
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
                cursor.execute(query_insert, (playerID, yearID, teamID, inSeason, manager_G, manager_W, manager_L, teamRank, plyrMgr, half))

        except Exception as e:
            print(f"Error processing row {idx}: {row}")
            print(f"Error details: {e}")
            continue

def update_managers_half(cursor, rows):
    """Insert or update records from ManagersHalf.csv."""
    for idx, row in enumerate(rows, start=2):
        try:
            playerID = safe_str(row.get('playerID'))
            yearID = safe_int(row.get('yearID'))
            teamID = safe_str(row.get('teamID'))
            inSeason = safe_int(row.get('inseason'))
            half = safe_int(row.get('half'))  # The half value from ManagersHalf.csv

            # Check if the record already exists with the same playerID, yearID, teamID, inSeason, and half
            query_check = """
            SELECT managers_ID FROM managers 
            WHERE playerID = %s AND yearID = %s AND teamID = %s AND inSeason = %s AND half = %s;
            """
            cursor.execute(query_check, (playerID, yearID, teamID, inSeason, half))
            result = cursor.fetchone()

            if result:
                # Update the existing record with the correct values
                query_update = """
                UPDATE managers 
                SET manager_G = %s, manager_W = %s, manager_L = %s, teamRank = %s 
                WHERE managers_ID = %s;
                """
                manager_G = safe_int(row.get('G'))
                manager_W = safe_int(row.get('W'))
                manager_L = safe_int(row.get('L'))
                teamRank = safe_int(row.get('rank'))

                cursor.execute(query_update, (manager_G, manager_W, manager_L, teamRank, result[0]))
            else:
                # Insert the record as a new row if no matching record found
                query_insert = """
                INSERT INTO managers (
                    playerID, yearID, teamID, inSeason, manager_G, manager_W, manager_L, teamRank, plyrMgr, half
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
                plyrMgr = safe_str(row.get('plyrMgr'))
                manager_G = safe_int(row.get('G'))
                manager_W = safe_int(row.get('W'))
                manager_L = safe_int(row.get('L'))
                teamRank = safe_int(row.get('rank'))

                cursor.execute(query_insert, (playerID, yearID, teamID, inSeason, manager_G, manager_W, manager_L, teamRank, plyrMgr, half))

        except Exception as e:
            print(f"Error processing row {idx} in ManagersHalf.csv: {row}")
            print(f"Error details: {e}")
            continue

def update_managers_csv(db_config, csv_folder):
    """Process the managers CSV files and update the database."""
    # List of CSV file names
    csv_files = ['managers.csv', 'ManagersHalf.csv']

    # Connect to the MySQL (MariaDB) database using PyMySQL
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    # Iterate over each CSV file
    for csv_file_name in csv_files:
        csv_file_path = os.path.join(csv_folder, csv_file_name)

        # Check if the file exists before processing
        if not os.path.exists(csv_file_path):
            print(f"File not found: {csv_file_path}")
            continue

        print(f"Processing file: {csv_file_name}")

        # Open the CSV file to read data
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file, delimiter=',')
            rows = list(csv_reader)

            # Process based on CSV file type
            if csv_file_name == 'managers.csv':
                insert_managers_with_null_half(cursor, rows)
            elif csv_file_name == 'ManagersHalf.csv':
                update_managers_half(cursor, rows)

        print(f"Finished processing file: {csv_file_name}")

    # Commit the transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    print("Data from all CSV files successfully imported into the 'managers' table.")

# Example usage
def main(db_config, csv_folder):
    """Main function to handle the process of importing CSV data into the database."""
    update_managers_csv(db_config, csv_folder)
