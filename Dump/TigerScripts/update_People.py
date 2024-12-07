import pymysql
import csv
import os
from datetime import datetime

def update_people(db_config, csv_folder):
    """Function to update people data in the database."""
    current_dir = os.getcwd()
    csv_file_name = 'people.csv'
    csv_file_path = os.path.join(csv_folder, csv_file_name)

    # Function to parse dates and convert to 'YYYY-MM-DD' format for MySQL
    def parse_date(date_str):
        if date_str:
            try:
                parsed_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                return parsed_date
            except ValueError:
                pass
            try:
                parsed_date = datetime.strptime(date_str, '%m/%d/%Y').date()
                return parsed_date
            except ValueError:
                pass
        return None

    # Function to handle empty strings, '0', and additional cases as NULL
    def handle_empty(value):
        if value in ['', '0', 'N/A', 'NA', ' ', None]:
            return None
        return value

    # Connect to the MySQL (MariaDB) database using PyMySQL
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    # Define a mapping from CSV column names to table column names
    column_mapping = {
        'debut': 'debutDate',
        'finalGame': 'finalGameDate',
        'playerID': 'playerID',
        'birthYear': 'birthYear',
        'birthMonth': 'birthMonth',
        'birthDay': 'birthDay',
        'birthCity': 'birthCity',
        'birthCountry': 'birthCountry',
        'birthState': 'birthState',
        'deathYear': 'deathYear',
        'deathMonth': 'deathMonth',
        'deathDay': 'deathDay',
        'deathCountry': 'deathCountry',
        'deathState': 'deathState',
        'deathCity': 'deathCity',
        'nameFirst': 'nameFirst',
        'nameLast': 'nameLast',
        'nameGiven': 'nameGiven',
        'weight': 'weight',
        'height': 'height',
        'bats': 'bats',
        'throws': 'throws',
        'bbrefID': 'bbrefID',
        'retroID': 'retroID'
    }

    # Open the CSV file to read the first line (header)
    with open(csv_file_path, 'r') as file:
        csv_reader = csv.DictReader(file)  # Use DictReader to handle the header mapping automatically
        rows = list(csv_reader)

        # Define the columns that match your table's structure
        table_columns = [
            'playerID', 'birthYear', 'birthMonth', 'birthDay', 'birthCity', 'birthCountry', 
            'birthState', 'deathYear', 'deathMonth', 'deathDay', 'deathCountry', 'deathState', 
            'deathCity', 'nameFirst', 'nameLast', 'nameGiven', 'weight', 'height', 'bats', 'throws', 
            'debutDate', 'finalGameDate'
        ]
        
        # Iterate over each row and insert the data
        for row in rows:
            values = [
                handle_empty(row[column_mapping[col]]) if col in row else None for col in table_columns
            ]

            # Parse dates (e.g., debutDate, finalGameDate)
            values[table_columns.index('debutDate')] = parse_date(row['debut'])  # Assuming 'debut' is the correct column in CSV
            values[table_columns.index('finalGameDate')] = parse_date(row['finalGame'])  # Assuming 'finalGame' is the correct column in CSV

            # Create the INSERT statement with ON DUPLICATE KEY UPDATE
            update_values = ', '.join([f"{col} = VALUES({col})" for col in table_columns if col != 'playerID'])  # Avoid updating primary key
            placeholders = ', '.join(['%s'] * len(values))
            
            query = f"""
            INSERT INTO people ({', '.join(table_columns)}) 
            VALUES ({placeholders})
            ON DUPLICATE KEY UPDATE {update_values};
            """
            
            # Execute the query to insert or update the data
            cursor.execute(query, values)

        conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    print(f"Data from {csv_file_path} successfully imported into the 'people' table.")

# Entry point for the script
def main(db_config, csv_folder):
    update_people(db_config, csv_folder)
