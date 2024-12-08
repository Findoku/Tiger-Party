import pymysql
import csv
import os

# Mapping CSV columns to database columns
CSV_TO_DB_MAPPING = {
    'playerID': 'playerID',
    'yearID': 'yearID',
    'teamID': 'teamID',
    'round': 'round',
    'position': 'position',
    'G': 'f_G',
    'GS': 'f_GS',
    'InnOuts': 'f_InnOuts',
    'PO': 'f_PO',
    'A': 'f_A',
    'E': 'f_E',
    'DP': 'f_DP',
    'TP': 'f_TP',
    'PB': 'f_PB'
}

# Define the list of fields that will be inserted into the database
fieldingpost_columns = [
    'playerID', 'yearID', 'teamID', 'round', 'position', 'f_G', 'f_GS',
    'f_InnOuts', 'f_PO', 'f_A', 'f_E', 'f_DP', 'f_TP', 'f_PB'
]

# Helper function to safely convert to integer
def safe_int(value, default=0):
    try:
        return int(value.strip()) if value.strip() != '' else default
    except ValueError:
        return default

# Function to determine if a field should be NULL based on position
def position_specific_value(position, stat_value, field_name):
    """Returns the stat value as NULL if it is irrelevant to the position."""
    if field_name == 'f_PB':
        irrelevant_positions = ['1B', '2B', '3B', 'OF']
        if position in irrelevant_positions:
            return None
    return stat_value

# Function to process a CSV file and insert data into the database
def process_csv(file_path, cursor, conn):  # Pass conn here
    with open(file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        rows = list(csv_reader)

        for idx, row in enumerate(rows, start=1):
            try:
                # Prepare the cleaned row based on the CSV-to-DB mapping
                cleaned_row = {col: None for col in fieldingpost_columns}

                # Extract and clean data for each row based on the CSV mapping
                position = row.get('POS', '').strip()
                for csv_col, db_col in CSV_TO_DB_MAPPING.items():
                    cleaned_row[db_col] = row.get(csv_col, '').strip() if row.get(csv_col) else None

                # Convert relevant columns to integers using safe_int
                cleaned_row['f_G'] = safe_int(row.get('G'))
                cleaned_row['f_GS'] = safe_int(row.get('GS'))
                cleaned_row['f_InnOuts'] = safe_int(row.get('InnOuts'))
                cleaned_row['f_PO'] = safe_int(row.get('PO'))
                cleaned_row['f_A'] = safe_int(row.get('A'))
                cleaned_row['f_E'] = safe_int(row.get('E'))
                cleaned_row['f_DP'] = safe_int(row.get('DP'))
                cleaned_row['f_TP'] = safe_int(row.get('TP'))
                cleaned_row['f_PB'] = position_specific_value(position, safe_int(row.get('PB')), 'f_PB')

                # Remove None keys to prevent issues with placeholders
                filtered_row = {k: v for k, v in cleaned_row.items() if v is not None}
                values = [filtered_row.get(col) for col in fieldingpost_columns]

                # Construct the INSERT statement with ON DUPLICATE KEY UPDATE
                update_values = ', '.join([ 
                    f"{col} = CASE WHEN {col} != 0 AND {col} IS NOT NULL THEN VALUES({col}) ELSE {col} END"
                    for col in fieldingpost_columns[5:]
                ])
                placeholders = ', '.join(['%s'] * len(values))

                query = f"""
                INSERT INTO fieldingpost ({', '.join(fieldingpost_columns)})
                VALUES ({placeholders})
                ON DUPLICATE KEY UPDATE {update_values};
                """
                
                cursor.execute(query, values)

            except Exception as e:
                print(f"Error processing row {idx}: {row}")
                print(f"Error details: {e}")
                continue

        # Commit changes for the file after all rows are processed
        conn.commit()  # Commit here

# Main entry point for the fieldingpost update script
def main(db_config, csv_folder):
    """Main function to process the fieldingpost data and update the database."""
    # Connect to the MySQL (MariaDB) database
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    # Define the CSV file name
    csv_file_name = 'FieldingPost.csv'
    file_path = os.path.join(csv_folder, csv_file_name)

    try:
        process_csv(file_path, cursor, conn)  # Pass conn here
    except Exception as e:
        print(f"Critical error while processing {csv_file_name}: {e}")

    # Close the database connection
    cursor.close()
    conn.close()
