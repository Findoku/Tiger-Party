import os
import csv
import pymysql

def safe_str(value):
    """Helper function to safely strip and convert values to strings."""
    return value.strip() if value else None

def process_csv(file_path, cursor):
    """Process the CSV file and update the parks table."""
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        # Read the CSV file
        csv_reader = csv.DictReader(file, delimiter=',')  # Ensure the delimiter matches the CSV format

        # Skip the header if needed (csv.DictReader already handles the header, so we don't need to skip explicitly)
        for idx, row in enumerate(csv_reader, start=2):  # Start from the second row (skipping header)
            try:
                # Extract and clean data
                parkID = safe_str(row.get('parkkey'))  # Ensure parkkey is correctly extracted
                
                # Skip rows where parkID is missing
                if not parkID:
                    print(f"Skipping row {idx} due to missing parkID: {row}")
                    continue
                
                park_alias = safe_str(row.get('parkalias'))
                park_name = safe_str(row.get('parkname'))
                city = safe_str(row.get('city'))
                state = safe_str(row.get('state'))
                country = safe_str(row.get('country'))

                # Insert or update the record in the parks table
                query = """
                INSERT INTO parks (
                    parkID, park_alias, park_name, city, state, country
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    park_alias = VALUES(park_alias),
                    park_name = VALUES(park_name),
                    city = VALUES(city),
                    state = VALUES(state),
                    country = VALUES(country);
                """
                cursor.execute(query, (parkID, park_alias, park_name, city, state, country))
            except Exception as e:
                print(f"Error processing row {idx}: {row}")
                print(f"Error details: {e}")
                continue

def main(db_config, csv_folder):
    """Main function to process the parks data and update the database."""
    # Connect to the database
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    try:
        # Process the parks CSV file
        parks_csv = os.path.join(csv_folder, "parks.csv")
        if os.path.exists(parks_csv):
            process_csv(parks_csv, cursor)
        else:
            print(f"Error: File {parks_csv} not found.")
            return

        # Commit changes to the database
        conn.commit()
    except Exception as e:
        print(f"Error while updating parks data: {e}")
    finally:
        # Close the database connection
        cursor.close()
        conn.close()
