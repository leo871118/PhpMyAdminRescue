# Ispiration
# https://stackoverflow.com/questions/18022809/how-can-i-solve-error-mysql-shutdown-unexpectedly

import os
from datetime import datetime
import shutil
import subprocess

def is_mysql_running():
    """Checks if XAMPP's MySQL is running."""
    try:
        # Checks the mysqld.exe process
        result = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq mysqld.exe"],
            capture_output=True,
            text=True
        )
        return "mysqld.exe" in result.stdout

    except subprocess.CalledProcessError as e:
        print(f"Error checking MySQL status: {e}")
        return False

def stop_mysql():
    """Stops XAMPP's MySQL process."""
    if is_mysql_running():
        try:
            subprocess.run(["taskkill", "/F", "/IM", "mysqld.exe"], check=True)
            print("MySQL has been stopped successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error stopping MySQL: {e}")
    else:
        print("MySQL is not running.")

def start_mysql():
    """Starts XAMPP's MySQL."""
    try:
        # Assumes mysqld.exe is in this location
        mysql_path = "C:\\xampp\\mysql\\bin\\mysqld.exe"
        subprocess.Popen([mysql_path, "--defaults-file=C:\\xampp\\mysql\\bin\\my.ini"])
        print("MySQL has been started successfully.")
    except Exception as e:
        print(f"Error starting MySQL: {e}")

def generate_backup_timestamp():
    """Generates a formatted timestamp for backup folder names."""
    now = datetime.now()
    return now.strftime("%Y_%m_%d_%H_%M")

# Renames folder mysql/data to mysql/bp_data_timestamp
def backUpOldFolder():
    formatted_time = generate_backup_timestamp()
    old_folder_name = "C:\\xampp\\mysql\\data"
    new_folder_name = f"C:\\xampp\\mysql\\bp_data_{formatted_time}"

    try:
        os.rename(old_folder_name, new_folder_name)
        print(f"Backup of '{old_folder_name}' to '{new_folder_name}' successful.")
    except FileNotFoundError:
        print(f"Error: folder '{old_folder_name}' not found.")
    except FileExistsError:
        print(f"Error: folder '{new_folder_name}' already exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Makes a copy of mysql/backup folder and names it as mysql/data
def moveBackUpFolderToData():
    # Paths of the folders involved
    source_folder = "C:\\xampp\\mysql\\backup"  # Path of the source folder
    destination_folder = "C:\\xampp\\mysql\\data"  # Path of the destination folder

    if os.path.exists(destination_folder):
        print(f"Error: the folder '{destination_folder}' already exists.")
    else:
        try:
            shutil.copytree(source_folder, destination_folder)
            print(f"The folder '{source_folder}' succesofulid copied in '{destination_folder}'.")
        except Exception as e:
            print(f"An error occured: {e}")

# Copies all user database folders from mysql/bp_data_timestamp into mysql/data (excluding system folders)
def moveOldsubFolder():
    formatted_time = generate_backup_timestamp()
    source_folder = f"C:\\xampp\\mysql\\bp_data_{formatted_time}"  # Path of the source folder
    destination_folder = 'C:\\xampp\\mysql\\data'  # Path of the destination folder

    # Folders to exclude from copying
    excluded_folders = {'mysql', 'performance_schema', 'phpmyadmin', 'test'}

    # Check if the destination folder exists, create if not
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Iterate through items in the source folder
    for folder_name in os.listdir(source_folder):
        # If it's a directory and not in the excluded list
        if folder_name not in excluded_folders:
            source_path = os.path.join(source_folder, folder_name)
            destination_path = os.path.join(destination_folder, folder_name)

            # If it's a directory, copy it
            if os.path.isdir(source_path):
                shutil.copytree(source_path, destination_path)
                print(f"Copied the folder '{folder_name}' from '{source_folder}' to '{destination_folder}'")
            else:
                print(f"'{folder_name}' is not a directory, ignoring.")

# Copies mysql/bp_data_timestamp/ibdata1 file into mysql/data folder
def moveOldFile():
    formatted_time = generate_backup_timestamp()
    source_file = f"C:\\xampp\\mysql\\bp_data_{formatted_time}\\ibdata1"  # Path of the source file
    destination_folder = 'C:\\xampp\\mysql\\data'          # Path of the destination folder
    destination_file = os.path.join(destination_folder, 'ibdata1')  # Path of the destination file

    # Check if the source file exists
    if os.path.exists(source_file):
        # Copy the file to the destination
        shutil.copy2(source_file, destination_file)
        print(f"File '{source_file}' copied in '{destination_file}' successfully.")
    else:
        print(f"Error: the file '{source_file}' doesn't exist.")


if __name__ == "__main__":
    try:
        # Stop MySQL service if running
        stop_mysql()

        # Perform backup and data restoration steps
        backUpOldFolder()
        moveBackUpFolderToData()
        moveOldsubFolder()
        moveOldFile()

        # Restart MySQL service
        start_mysql()
        
        print("MySQL data recovery completed successfully")
        
    except Exception as e:
        print(f"An error occurred during recovery: {e}")
        print("Please check logs and try again")
