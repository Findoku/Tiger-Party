import pymysql
import csv
import os

# Function to safely clean string values
def safe_str(value):
    return value.strip() if value and value.strip() else None

# Mapping CSV columns to database columns
CSV_TO_DB_MAPPING = {
    'playerID': 'playerID',
    'yearid': 'yearID',
    'votedBy': 'votedBy',
    'ballots': 'ballots',
    'needed': 'needed',
    'votes': 'votes',
    'inducted': 'inducted',
    'category': 'category',
    'needed_note': 'note'
}

# Process CSV data and insert/update into the Hall of Fame table
def process_csv(file_path, cursor):
    with open(file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        rows = list(csv_reader)

        for idx, row in enumerate(rows, start=1):
            try:
                # Extract and clean data based on the CSV-to-DB mapping
                cleaned_data = {
                    db_col: safe_str(row.get(csv_col)) if csv_col in row else None
                    for csv_col, db_col in CSV_TO_DB_MAPPING.items()
                }

                # Convert numerical fields to integers where appropriate
                cleaned_data['yearID'] = int(cleaned_data['yearID']) if cleaned_data['yearID'] else None
                cleaned_data['ballots'] = int(cleaned_data['ballots']) if cleaned_data['ballots'] else None
                cleaned_data['needed'] = int(cleaned_data['needed']) if cleaned_data['needed'] else None
                cleaned_data['votes'] = int(cleaned_data['votes']) if cleaned_data['votes'] else None

                # Prepare values for insertion
                values = tuple(cleaned_data[db_col] for db_col in CSV_TO_DB_MAPPING.values())

                # Insert or update record
                query = """
                INSERT INTO halloffame (
                    playerID, yearID, votedBy, ballots, needed, votes, inducted, category, note
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    ballots = VALUES(ballots),
                    needed = VALUES(needed),
                    votes = VALUES(votes),
                    inducted = VALUES(inducted),
                    category = VALUES(category),
                    note = VALUES(note);
                """
                cursor.execute(query, values)
            except Exception as e:
                print(f"Error processing row {idx}: {row}")
                print(f"Error details: {e}")
                continue

# Main entry point for the script
def main(db_config, csv_folder):
    """Main function to process the Hall of Fame data and update the database."""
    # Connect to the MySQL (MariaDB) database
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    # Define the CSV file path
    csv_file_name = 'HallofFame.csv'
    file_path = os.path.join(csv_folder, csv_file_name)

    try:
        process_csv(file_path, cursor)
        # Commit changes after processing the file
        conn.commit()
    except Exception as e:
        print(f"Critical error while processing {csv_file_name}: {e}")

    # Close the database connection
    cursor.close()
    conn.close()

