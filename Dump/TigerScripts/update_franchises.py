import pymysql
import csv
import os

def safe_str(value):
    """Helper function to safely convert values to strings."""
    return value.strip() if value and value.strip() else None

def update_franchises(db_config, csv_folder):
    """Process a TeamsFranchises CSV file and update the database."""
    # Get the CSV file path
    csv_file_name = 'TeamsFranchises.csv'
    csv_file_path = os.path.join(csv_folder, csv_file_name)

    # Connect to the MySQL (MariaDB) database using PyMySQL
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    # Process CSV data and insert/update into the table
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        rows = list(csv_reader)

        for idx, row in enumerate(rows, start=1):
            try:
                # Extract and clean data
                franchID = safe_str(row.get('franchID'))
                franchName = safe_str(row.get('franchName'))
                active = safe_str(row.get('active'))
                NAassoc = safe_str(row.get('NAassoc'))

                # Insert or update record
                query = """
                INSERT INTO franchises (franchID, franchName, active, NAassoc)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                    franchName = VALUES(franchName),
                    active = VALUES(active),
                    NAassoc = VALUES(NAassoc);
                """
                cursor.execute(query, (franchID, franchName, active, NAassoc))
            except Exception as e:
                print(f"Error processing row {idx}: {row}")
                print(f"Error details: {e}")
                continue

        # Commit changes
        conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    print(f"Data from {csv_file_path} successfully imported into the 'franchises' table.")

# Main entry point
def main(db_config, csv_folder):
    """Main function to handle the process of importing CSV data into the database."""
    update_franchises(db_config, csv_folder)
