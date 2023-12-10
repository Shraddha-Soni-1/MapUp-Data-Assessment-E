import os
import json
import csv
import argparse

def process_json_files(input_dir, output_dir):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Create CSV file for output
    output_csv_path = os.path.join(output_dir, 'transformed_data.csv')
    with open(output_csv_path, 'w', newline='') as csvfile:
        # Define CSV header
        fieldnames = ['unit', 'trip_id', 'toll_loc_id_start', 'toll_loc_id_end',
                      'toll_loc_name_start', 'toll_loc_name_end', 'toll_system_type',
                      'entry_time', 'exit_time', 'tag_cost', 'cash_cost', 'license_plate_cost']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header to CSV file
        writer.writeheader()

        # Process each JSON file in the input directory
        for json_file in os.listdir(input_dir):
            if json_file.endswith('.json'):
                process_single_json(os.path.join(input_dir, json_file), writer)

    print(f"Processing completed. Results saved to {output_csv_path}")

def process_single_json(json_file_path, csv_writer):
    # Read JSON data from file
    with open(json_file_path) as json_file:
        data = json.load(json_file)

    # Check if there are tolls in the route
    if 'tolls' not in data or not data['tolls']:
        return

    # Extract relevant data and write to CSV
    for toll in data['tolls']:
        csv_writer.writerow({
            'unit': data.get('unit', ''),
            'trip_id': os.path.basename(json_file_path),
            'toll_loc_id_start': toll.get('start', {}).get('id', ''),
            'toll_loc_id_end': toll.get('end', {}).get('id', ''),
            'toll_loc_name_start': toll.get('start', {}).get('name', ''),
            'toll_loc_name_end': toll.get('end', {}).get('name', ''),
            'toll_system_type': toll.get('systemType', ''),
            'entry_time': toll.get('entryTime', ''),
            'exit_time': toll.get('exitTime', ''),
            'tag_cost': toll.get('cost', {}).get('tag', ''),
            'cash_cost': toll.get('cost', {}).get('cash', ''),
            'license_plate_cost': toll.get('cost', {}).get('licensePlate', '')
        })

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Extract toll information from JSON files.")
    parser.add_argument("--to_process", required=True, help="Path to the JSON responses folder.")
    parser.add_argument("--output_dir", required=True, help="Folder where the final CSV will be stored.")
    args = parser.parse_args()

    # Call the function to process JSON files and create CSV
    process_json_files(args.to_process, args.output_dir)
