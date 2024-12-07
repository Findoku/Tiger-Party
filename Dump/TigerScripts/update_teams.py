import pymysql
import csv
import os

def safe_str(value):
    """Helper function to safely convert values to strings."""
    return value.strip() if value else None

def update_teams_table(db_config, csv_file_path):
    """Process the Teams CSV file and update the database."""
    # Connect to the MySQL (MariaDB) database using PyMySQL
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    # Define a mapping from CSV column names to table column names
    column_mapping = {
        'yearID': 'yearID',
        'lgID': 'lgID',
        'teamID': 'teamID',
        'franchID': 'franchID',
        'divID': 'divID',
        'Rank': 'team_rank',
        'G': 'team_G',
        'Ghome': 'team_G_home',
        'W': 'team_W',
        'L': 'team_L',
        'DivWin': 'DivWin',
        'WCWin': 'WCWin',
        'LgWin': 'LgWin',
        'WSWin': 'WSWin',
        'R': 'team_R',
        'AB': 'team_AB',
        'H': 'team_H',
        '2B': 'team_2B',
        '3B': 'team_3B',
        'HR': 'team_HR',
        'BB': 'team_BB',
        'SO': 'team_SO',
        'SB': 'team_SB',
        'CS': 'team_CS',
        'HBP': 'team_HBP',
        'SF': 'team_SF',
        'RA': 'team_RA',
        'ER': 'team_ER',
        'ERA': 'team_ERA',
        'CG': 'team_CG',
        'SHO': 'team_SHO',
        'SV': 'team_SV',
        'IPouts': 'team_IPouts',
        'HA': 'team_HA',
        'HRA': 'team_HRA',
        'BBA': 'team_BBA',
        'SOA': 'team_SOA',
        'E': 'team_E',
        'DP': 'team_DP',
        'FP': 'team_FP',
        'name': 'team_name',
        'park': 'park_name',
        'attendance': 'team_attendance',
        'BPF': 'team_BPF',
        'PPF': 'team_PPF',
    }

    table_columns = [
        'yearID', 'lgID', 'teamID', 'franchID', 'divID', 'team_rank',
        'team_G', 'team_G_home', 'team_W', 'team_L', 'DivWin', 'WCWin', 
        'LgWin', 'WSWin', 'team_R', 'team_AB', 'team_H', 'team_2B', 
        'team_3B', 'team_HR', 'team_BB', 'team_SO', 'team_SB', 'team_CS',
        'team_HBP', 'team_SF', 'team_RA', 'team_ER', 'team_ERA', 'team_CG',
        'team_SHO', 'team_SV', 'team_IPouts', 'team_HA', 'team_HRA', 
        'team_BBA', 'team_SOA', 'team_E', 'team_DP', 'team_FP', 
        'team_name', 'park_name', 'team_attendance', 'team_BPF', 'team_PPF'
    ]

    # Open the CSV file to read data
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        rows = list(csv_reader)

        for idx, row in enumerate(rows, start=1):
            try:
                # Clean and validate data
                cleaned_row = {}
                for csv_col, db_col in column_mapping.items():
                    value = row.get(csv_col, '').strip()
                    if value == '':  # Handle empty strings as None
                        cleaned_row[db_col] = None
                    else:
                        cleaned_row[db_col] = value

                # Ensure required fields are not missing
                required_fields = ['teamID', 'yearID', 'lgID', 'divID', 'franchID']
                if not all(cleaned_row.get(field) for field in required_fields):
                    continue  # Skip row if required fields are missing

                # Construct the column values
                values = [cleaned_row[col] for col in table_columns]

                # Create the INSERT statement with ON DUPLICATE KEY UPDATE
                update_values = ', '.join([f"{col} = VALUES({col})" for col in table_columns[5:]])  # Skip primary key
                placeholders = ', '.join(['%s'] * len(values))

                query = f"""
                INSERT INTO teams ({', '.join(table_columns)}) 
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

    # Close the database connection
    cursor.close()
    conn.close()
    print(f"Data from {csv_file_path} successfully imported into the 'teams' table.")

def main(db_config, csv_folder):
    """Main function to handle the process of importing CSV data into the database."""
    # Define the CSV file name
    csv_file_name = 'Teams.csv'

    # Combine the current directory with the CSV file name
    csv_file_path = os.path.join(csv_folder, csv_file_name)

    # Call the function to update the teams table
    update_teams_table(db_config, csv_file_path)

