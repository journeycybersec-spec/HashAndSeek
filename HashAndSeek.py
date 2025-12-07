import os
import hashlib
import time
import sys
import logging
from itertools import cycle

# Setup logging for output file
logging.basicConfig(filename='hash_search_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

# Setup logging for skipped files
skipped_files_log = logging.getLogger('skipped_files')
file_handler = logging.FileHandler('skipped_files_log.txt')
file_handler.setLevel(logging.WARNING)
formatter = logging.Formatter('%(asctime)s - %(message)s')
file_handler.setFormatter(formatter)
skipped_files_log.addHandler(file_handler)

# ANSI escape codes for colors
RESET = '\033[0m'
BOLD = '\033[1m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
CYAN = '\033[36m'
RED = '\033[31m'

# Function to print custom ASCII art
def print_ascii_art():
    ascii_art = """
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
▗▖ ▗▖ ▗▄▖  ▗▄▄▖▗▖ ▗▖ ▗▄▖ ▗▖  ▗▖▗▄▄▄  ▗▄▄▖▗▄▄▄▖▗▄▄▄▖▗▖ ▗▖
▐▌ ▐▌▐▌ ▐▌▐▌   ▐▌ ▐▌▐▌ ▐▌▐▛▚▖▐▌▐▌  █▐▌   ▐▌   ▐▌   ▐▌▗▞▘
▐▛▀▜▌▐▛▀▜▌ ▝▀▚▖▐▛▀▜▌▐▛▀▜▌▐▌ ▝▜▌▐▌  █ ▝▀▚▖▐▛▀▀▘▐▛▀▀▘▐▛▚▖ 
▐▌ ▐▌▐▌ ▐▌▗▄▄▞▘▐▌ ▐▌▐▌ ▐▌▐▌  ▐▌▐▙▄▄▀▗▄▄▞▘▐▙▄▄▖▐▙▄▄▖▐▌ ▐▌
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
"""
    print(CYAN + BOLD + ascii_art + RESET)

# Function to calculate the hash of a file
def hash_file(file_path, hash_algo='sha256'):
    """Generate a hash for a given file using the specified hash algorithm."""
    hash_obj = hashlib.new(hash_algo)  # Initialize the specified hashing algorithm
    try:
        with open(file_path, 'rb') as file:
            # Read and update the hash object in chunks to handle large files
            for chunk in iter(lambda: file.read(4096), b""):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()  # Return the hash as a hexadecimal string
    except PermissionError:
        return None
    except Exception as e:
        logging.error(f"Error hashing file {file_path}: {e}")
        return None

# Function to format elapsed time in hours:minutes:seconds
def format_elapsed_time(seconds):
    """Format seconds into hours:minutes:seconds."""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

# Function to check if a directory/file is a system directory
def is_system_directory(path):
    """Return True if the path is a system directory to be skipped."""
    system_dirs = ['/sys/', '/proc/', '/dev/', '/run/', '/mnt/', '/boot/', '/tmp/']
    return any(path.startswith(system_dir) for system_dir in system_dirs)

# Function to check if a file is a device file (e.g., /dev/vsock, /dev/zfs)
def is_device_file(file_path):
    """Check if the file is a device file or special system file."""
    return not os.path.isfile(file_path) and not os.path.isdir(file_path)

# Function to search for files with the same hash
def find_files_with_hash(start_directory, target_hash, hash_algo='sha256', skip_restricted=False):
    """Search the entire system (or specified directory) for files that match the target hash."""
    matching_files = []
    start_time = time.time()  # Track when the function starts
    skipped_files = 0  # Track skipped files due to permission errors

    # Create spinner cycle for progress indicator
    spinner = cycle(['|', '/', '-', '\\'])
    sys.stdout.write(f"{CYAN}Searching for matching files... {RESET}")

    total_files = sum([len(files) for _, _, files in os.walk(start_directory)])  # Total number of files to process
    files_processed = 0

    # Force timer updates every second
    last_update_time = time.time()

    for dirpath, dirnames, filenames in os.walk(start_directory):
        # Skip system directories (like /sys/, /proc/, etc.) if user chooses to skip
        if skip_restricted and is_system_directory(dirpath):
            continue

        for filename in filenames:
            file_path = os.path.join(dirpath, filename)

            # Skip device files (e.g., /dev/ files)
            if is_device_file(file_path):
                skipped_files += 1
                skipped_files_log.warning(f"Skipping device file: {file_path}")  # Log skipped device files
                continue

            file_hash = hash_file(file_path, hash_algo)
            if file_hash == target_hash:
                matching_files.append(file_path)

            files_processed += 1

            # Periodically update the elapsed time and spinner every 100 files
            if files_processed % 100 == 0:  # Update every 100 files processed
                current_time = time.time()
                elapsed_time = int(current_time - start_time)
                sys.stdout.write(f"\r{next(spinner)} Elapsed Time: {format_elapsed_time(elapsed_time)} | Processed: {files_processed}/{total_files}    ")
                sys.stdout.flush()
                last_update_time = current_time  # Update the last update time

    sys.stdout.write("\n")  # New line after spinner

    # Display summary of skipped files
    if skipped_files > 0:
        print(f"\n{YELLOW}==== WARNING ====")
        print(f"   {skipped_files} files were skipped due to permission errors or being device files.")
        logging.info(f"Skipped {skipped_files} files due to permission issues or being device files.")

    # Print a separator for visual clarity
    print(f"{CYAN}==== MATCHING FILES FOUND ===={RESET}")

    return matching_files

# Main UX program
def main():
    while True:  # Keep the program running until the user chooses to exit
        print_ascii_art()  # Display ASCII art header
        print(RESET + "Choose an option:")
        print(CYAN + "1. " + BOLD + "Calculate file hash(SHA256 or MD5)")
        print(CYAN + "2. " + BOLD + "Search for matching hash in the system")
        print(CYAN + "3. " + BOLD + "Exit")

        option = input(CYAN + "Enter 1, 2, or 3: ").strip()

        if option == '1':
            # Option 1: Hash a file
            file_path = input(GREEN + "Enter the file path to hash: ").strip()
            if not os.path.isfile(file_path):
                print(f"{RED}The file '{file_path}' does not exist.")
                continue

            # Choose hash algorithm (default to SHA256)
            hash_algo = input(CYAN + "Choose hash algorithm (SHA256/MD5) [default: SHA256]: ").strip().lower() or 'sha256'
            if hash_algo not in ['sha256', 'md5']:
                print(f"{RED}Invalid algorithm. Please choose 'SHA256' or 'MD5'.")
                continue

            print(f"{GREEN}Hashing the file: {file_path}")
            file_hash = hash_file(file_path, hash_algo)
            if file_hash:
                print(f"{GREEN}File hash ({hash_algo}): {file_hash}")
                logging.info(f"File hashed: {file_path} | Hash ({hash_algo}): {file_hash}")
            else:
                print(f"{RED}Error calculating the hash.")

        elif option == '2':
            # Option 2: Search for a hash
            input_hash = input(CYAN + "Enter the hash (SHA256 or MD5): ").strip()
            if len(input_hash) not in [32, 64]:
                print(f"{RED}Invalid hash length. Please provide a valid MD5 (32 characters) or SHA256 (64 characters) hash.")
                continue

            hash_algo = 'sha256' if len(input_hash) == 64 else 'md5'
            print(f"{GREEN}Searching for files with hash {input_hash} ({hash_algo})...")

            search_directory = input(CYAN + "Enter the directory to search (default is current directory): ").strip()
            if not search_directory:
                search_directory = os.getcwd()  # Default to current directory

            skip_restricted = input(CYAN + "Skip restricted access directories (like /sys, /proc)? (y/n): ").strip().lower()
            skip_restricted = True if skip_restricted in ['y', 'yes'] else False

            # Find matching files
            matches = find_files_with_hash(search_directory, input_hash, hash_algo, skip_restricted)

            if matches:
                print(f"{GREEN}Found the following matching files:")
                for match in matches:
                    print(f" - {match}")
                    logging.info(f"Match found: {match} | Hash ({hash_algo}): {input_hash}")
            else:
                print(f"{RED}No matching files found.")
                logging.info(f"No matches found for hash ({hash_algo}): {input_hash}")

        elif option == '3':
            # Option 3: Exit the program
            print(f"{YELLOW}Exiting the program. Goodbye!")
            break

        else:
            print(f"{RED}Invalid option. Please choose '1', '2', or '3'.")

if __name__ == "__main__":
    main()
