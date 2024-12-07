import pymysql
import csv
import os

# Helper function to remove non-ASCII characters
def remove_non_ascii(text):
    return ''.join([char for char in text if ord(char) < 128])

def update_appearances(db_config, csv_folder):
    """Update the 'appearances' table with data from the CSV file."""
    csv_file_name = 'appearances.csv'
    csv_file_path = os.path.join(csv_folder, csv_file_name)

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    column_mapping = {
        'playerID': 'playerID',
        'yearID': 'yearID',
        'teamID': 'teamID',
        'G_all': 'G_all',
        'GS': 'GS',
        'G_batting': 'G_batting',
        'G_defense': 'G_defense',
        'G_p': 'G_p',
        'G_c': 'G_c',
        'G_1b': 'G_1b',
        'G_2b': 'G_2b',
        'G_3b': 'G_3b',
        'G_ss': 'G_ss',
        'G_lf': 'G_lf',
        'G_cf': 'G_cf',
        'G_rf': 'G_rf',
        'G_of': 'G_of',
        'G_dh': 'G_dh',
        'G_ph': 'G_ph',
        'G_pr': 'G_pr'
    }

    table_columns = [
        'playerID', 'yearID', 'teamID', 'G_all', 'GS', 'G_batting', 'G_defense',
        'G_p', 'G_c', 'G_1b', 'G_2b', 'G_3b', 'G_ss', 'G_lf', 'G_cf', 'G_rf',
        'G_of', 'G_dh', 'G_ph', 'G_pr'
    ]

    with open(csv_file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        rows = list(csv_reader)

        for idx, row in enumerate(rows, start=2):
            # Clean the row values to remove any non-ASCII characters
            for key in row:
                row[key] = remove_non_ascii(row[key])

            team_id = row.get('teamID', '').strip()
            if not team_id or team_id == 'N/A':
                print(f"Skipping row {idx} due to invalid teamID: {row}")
                continue

            player_id = row.get('playerID', '').strip()
            year_id = row.get('yearID', '').strip()
            if not player_id or not year_id:
                print(f"Skipping row {idx} due to missing playerID or yearID: {row}")
                continue

            values = [
                row[column_mapping[col]] if col in column_mapping and row.get(column_mapping[col]) else None
                for col in table_columns
            ]

            update_values = ', '.join([f"{col} = VALUES({col})" for col in table_columns])
            placeholders = ', '.join(['%s'] * len(values))

            query = f"""
            INSERT INTO appearances ({', '.join(table_columns)}) 
            VALUES ({placeholders})
            ON DUPLICATE KEY UPDATE {update_values};
            """
            
            try:
                cursor.execute(query, values)
            except pymysql.MySQLError as e:
                print(f"Error processing row {idx} with playerID {player_id}: {row}")
                print(f"Error details: {e}")
                continue

    conn.commit()
    cursor.close()
    conn.close()

    print(f"Data from {csv_file_path} successfully imported into the 'appearances' table.")

def main(db_config, csv_folder):
    """Main entry point for the script."""
    update_appearances(db_config, csv_folder)
