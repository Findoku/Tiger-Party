import pymysql
import csv
import os
from datetime import datetime

def update_homegames(db_config, csv_folder):
    """Process the HomeGames CSV file and update the database."""
    # Get the path to the CSV file
    csv_file_path = os.path.join(csv_folder, 'Homegames.csv')

    # Connect to the MySQL database using PyMySQL
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    # Mapping CSV columns to database columns for homegames
    CSV_TO_DB_MAPPING = {
        'yearkey': 'yearID',
        'teamkey': 'teamID',
        'parkkey': 'parkID',
        'spanfirst': 'firstGame',
        'spanlast': 'lastGame',
        'games': 'games',
        'openings': 'openings',
        'attendance': 'attendance'
    }

    def safe_str(value):
        """Safely convert a value to a stripped string or return None."""
        return value.strip() if value and value.strip() else None

    def parse_date(date_str):
        """Parse a date string into a datetime.date object."""
        if not date_str:
            return None
        date_formats = ['%Y-%m-%d', '%m/%d/%Y', '%d-%b-%Y']
        for fmt in date_formats:
            try:
                return datetime.strptime(date_str.strip(), fmt).strftime('%Y-%m-%d')  # Return as YYYY-MM-DD for date type
            except ValueError:
                continue
        return None  # Return None if no format matches

    def check_park_exists(cursor, parkID):
        """Check if parkID exists in the 'parks' table."""
        query = "SELECT COUNT(*) FROM parks WHERE parkID = %s"
        cursor.execute(query, (parkID,))
        result = cursor.fetchone()
        return result[0] > 0

    # Open the CSV file and process data
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        headers = lines[0].strip().split(',')  # Get the CSV headers
        file.seek(0)
        csv_reader = csv.DictReader(file, fieldnames=headers, delimiter=',')
        next(csv_reader)  # Skip the header row

        for idx, row in enumerate(csv_reader, start=2):
            try:
                # Prepare the cleaned row based on the CSV-to-DB mapping
                cleaned_row = {col: None for col in CSV_TO_DB_MAPPING.values()}

                # Extract and clean data based on the CSV-to-DB mapping
                for csv_col, db_col in CSV_TO_DB_MAPPING.items():
                    cleaned_row[db_col] = safe_str(row.get(csv_col))

                # Additional type conversion for fields where necessary
                yearID = int(cleaned_row['yearID']) if cleaned_row['yearID'] else None
                teamID = cleaned_row['teamID']
                parkID = cleaned_row['parkID']
                firstGame = parse_date(row.get('spanfirst'))
                lastGame = parse_date(row.get('spanlast'))
                games = int(row.get('games')) if row.get('games') else None
                openings = int(row.get('openings')) if row.get('openings') else None
                attendance = int(row.get('attendance')) if row.get('attendance') else None

                # Check if the parkID exists in the parks table before inserting
                if not check_park_exists(cursor, parkID):
                    print(f"Skipping row {idx}: parkID {parkID} does not exist in parks table.")
                    continue

                # Insert or update the record
                query = """
                INSERT INTO homegames (
                    yearID, teamID, parkID, firstGame, lastGame, games, openings, attendance
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    firstGame = VALUES(firstGame),
                    lastGame = VALUES(lastGame),
                    games = VALUES(games),
                    openings = VALUES(openings),
                    attendance = VALUES(attendance);
                """
                cursor.execute(query, (yearID, teamID, parkID, firstGame, lastGame, games, openings, attendance))

            except Exception as e:
                print(f"Error processing row {idx}: {row}")
                print(f"Error details: {e}")
                continue

        # Commit changes
        conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    print(f"Data from {csv_file_path} successfully imported into the 'homegames' table.")

# Define the main function for this script
def main(db_config, csv_folder):
    """Main entry point for the update script."""
    update_homegames(db_config, csv_folder)
