pip install requests python-dotenv

import os
import requests
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
import argparse

# Load environment variables from .env file
load_dotenv()

# Set TollGuru API key and URL
TOLLGURU_API_KEY = os.getenv("TOLLGURU_API_KEY")
TOLLGURU_API_URL = os.getenv("TOLLGURU_API_URL")

# Check if API key and URL are provided
if not TOLLGURU_API_KEY or not TOLLGURU_API_URL:
    raise ValueError("TollGuru API key and URL must be provided in the .env file")

# Function to upload CSV file to TollGuru API
def upload_to_tollguru(file_path, output_dir):
    url = f'{TOLLGURU_API_URL}/toll/v2/gps-tracks-csv-upload?mapProvider=osrm&vehicleType=5AxlesTruck'
    headers = {'x-api-key': TOLLGURU_API_KEY, 'Content-Type': 'text/csv'}

    with open(file_path, 'rb') as file:
        response = requests.post(url, data=file, headers=headers)

    # Save the JSON response to a file with the same name as the CSV file
    json_file_path = os.path.join(output_dir, os.path.basename(file_path).replace('.csv', '.json'))
    with open(json_file_path, 'w') as json_file:
        json_file.write(response.text)

def process_files(input_folder, output_dir):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Get a list of CSV files in the input folder
    csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

    # Use ThreadPoolExecutor for concurrent processing
    with ThreadPoolExecutor() as executor:
        # Submit tasks to upload each CSV file to TollGuru API
        futures = [executor.submit(upload_to_tollguru, os.path.join(input_folder, csv_file), output_dir)
                   for csv_file in csv_files]

        # Wait for all tasks to complete
        for future in futures:
            future.result()

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Upload GPS tracks to TollGuru API.")
    parser.add_argument("--to_process", required=True, help="Path to the CSV folder.")
    parser.add_argument("--output_dir", required=True, help="Folder where resulting JSON files will be stored.")
    args = parser.parse_args()

    # Call the function to process CSV files and upload to TollGuru API
    process_files(args.to_process, args.output_dir)
