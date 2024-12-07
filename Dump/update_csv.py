import os
import importlib



def get_db_config():
    """Prompt the user for database connection details."""
    print("Enter your database connection details:")
    host = input("Host (default: localhost): ") or "localhost"
    user = input("User: ")
    password = input("Password: ")
    database = input("Database name: ")
    local_infile = input("Enable local infile? (yes/no, default: yes): ").lower() in ['yes', 'y', '']

    return {
        'host': host,
        'user': user,
        'password': password,
        'database': database,
        'local_infile': local_infile
    }

def run_update_scripts(db_config, scripts_folder, csv_folder):
    """Run all update scripts in the specified folder with the provided database config."""
    scripts = [
        "update_People",
        "update_schools",
        "update_collegeplaying",
        "update_leagues",
        "update_divisions",
        "update_franchises",
        "update_parks",
        "update_teams",
        "update_batting",
        "update_battingpost",
        "update_allstarfull",
        "update_appearances",
        "update_awards",
        "update_awardsShare",
        "update_fielding",
        "update_fieldingpost",
        "update_halloffame",
        "update_homegames",
        "update_managers",
        "update_seriespost"
    ]

    for script_name in scripts:
        try:
            print(f"Running {script_name}.py...")
            # Dynamically import the script module from the TigerScripts folder
            script_module = importlib.import_module(f"TigerScripts.{script_name}")
            
            # Ensure the script has a main function or a callable entry point
            if hasattr(script_module, 'main'):
                script_module.main(db_config, csv_folder)
            else:
                print(f"Error: {script_name}.py does not have a 'main(db_config, csv_folder)' function.")
        except Exception as e:
            print(f"Error while running {script_name}.py: {e}")

def main():
    """Main entry point for the parent script."""
    # Get the database configuration from the user
    db_config = get_db_config()

    # Define the folder where the update scripts and CSV files are located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    scripts_folder = os.path.join(current_dir, 'TigerScripts')
    csv_folder = os.path.join(current_dir, 'UpdateCSVs')

    # Check if the folders exist, if not, prompt the user
    if not os.path.exists(scripts_folder):
        print(f"Error: The folder {scripts_folder} does not exist.")
        return
    if not os.path.exists(csv_folder):
        print(f"Error: The folder {csv_folder} does not exist.")
        return

    # Add TigerScripts folder to the module search path
    import sys
    sys.path.append(scripts_folder)

    # Run all update scripts
    run_update_scripts(db_config, scripts_folder, csv_folder)

if __name__ == "__main__":
    main()
