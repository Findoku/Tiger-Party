import pymysql
import csv
import os

# Helper function that removes non-ASCII characters
def remove_non_ascii(text):
    return ''.join([char for char in text if ord(char) < 128])

def update_allstarfull(db_config, csv_folder):
    """Update the 'allstarfull' table with data from the CSV file."""
    # Define the CSV file name
    csv_file_name = 'allstarfull.csv'

    # Combine the folder path and CSV file name
    csv_file_path = os.path.join(csv_folder, csv_file_name)

    # Connect to the database
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    # Define a mapping from CSV column names to table column names
    column_mapping = {
        'playerID': 'playerID',
        'yearID': 'yearID',
        'gameNum': 'gameID',  # Assuming gameNum corresponds to gameID
        'gameID': 'gameID',
        'teamID': 'teamID',
        'lgID': 'lgID',
        'GP': 'GP',
        'startingPos': 'startingPos'
    }

    # Define the table columns based on your database schema
    table_columns = [
        'playerID', 'yearID', 'lgID', 'teamID', 'gameID', 'GP', 'startingPos'
    ]

    # Open the CSV file to read data
    with open(csv_file_path, 'r') as file:
        csv_reader = csv.DictReader(file)  # Use DictReader to handle the header mapping automatically
        rows = list(csv_reader)

        # Iterate over each row and insert or update the data
        for row in rows:
            # Clean the row values to remove any non-ASCII characters
            for key in row:
                row[key] = remove_non_ascii(row[key])  # Clean each field in the row

            # Construct the column values based on the mapping
            values = [
                row[column_mapping[col]] if col in column_mapping and row.get(column_mapping[col]) else None
                for col in table_columns
            ]

            # Check if the record already exists based on the composite key (playerID, teamID, yearID, gameID)
            check_query = """
            SELECT COUNT(*) FROM allstarfull 
            WHERE playerID = %s AND teamID = %s AND yearID = %s AND gameID = %s;
            """
            cursor.execute(check_query, (values[0], values[3], values[1], values[4]))
            result = cursor.fetchone()

            if result[0] == 0:  # If no existing record, insert new data
                placeholders = ', '.join(['%s'] * len(values))
                insert_query = f"""
                INSERT INTO allstarfull ({', '.join(table_columns)}) 
                VALUES ({placeholders});
                """
                cursor.execute(insert_query, values)
            else:  # If record exists, update the data
                update_values = ', '.join([f"{col} = %s" for col in table_columns[2:]])  # Skip primary key
                update_query = f"""
                UPDATE allstarfull 
                SET {update_values}
                WHERE playerID = %s AND teamID = %s AND yearID = %s AND gameID = %s;
                """
                cursor.execute(update_query, values[2:] + [values[0], values[3], values[1], values[4]])

    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    print(f"Data from {csv_file_path} successfully imported into the 'allstarfull' table.")

def main(db_config, csv_folder):
    """Main entry point for the script."""
    # Call the update_allstarfull function
    update_allstarfull(db_config, csv_folder)

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
