import os
import glob
import csv

input_folder = ""
output_file = "train-replaced-for-each-gesture.csv"

# Get all CSV files in the input folder
csv_files = glob.glob(os.path.join(input_folder, "*.csv"))

# Initialize an empty list to store the data from all CSV files
combined_data = []

# Read each CSV file and append its data to the combined_data list
for file in csv_files:
    with open(file, "r") as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip the header row

        # If it's the first file, save the header
        if not combined_data:
            combined_data.append(header)

        # Append rows from the current file to the combined_data list
        for row in reader:
            combined_data.append(row)

# Write the combined data to the output file
with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(combined_data)

print(f"Successfully combined {len(csv_files)} CSV files into {output_file}.")
