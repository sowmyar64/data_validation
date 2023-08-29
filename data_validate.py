import pandas as pd
from datetime import datetime, timedelta
import os
from google.cloud import storage

# Initialize a client
client = storage.Client()

# Replace 'your-project-id' with your actual GCP project ID
bucket_name = 'source_data_raw_ml'

# Access the bucket
bucket = client.get_bucket(bucket_name)

# List objects in the bucket
print("Objects in the bucket:")
blobs = bucket.list_blobs()
for blob in blobs:
    print(blob.name)

# Upload a file to the bucket
local_file_path = 'path/to/local/file.txt'  # Replace with your local file path
destination_blob_name = 'uploaded-file.txt'  # Destination file name in the bucket

blob = bucket.blob(destination_blob_name)
blob.upload_from_filename(local_file_path)

print(f"File {local_file_path} uploaded to {destination_blob_name} in the bucket.")

# Define the folder path containing the Excel files
folder_path = "C:\\Users\\vinay\\Desktop\\sowmya\\Data"

# List all Excel files in the folder
data_files = [file for file in os.listdir(folder_path) if file.endswith('.xlsx')]


def generate_monthly_filenames(start_date, end_date, file_extension):
    filenames = []
    current_date = start_date

    while current_date <= end_date:
        formatted_date = current_date.strftime("%b %Y")
        filenames.append(f"{formatted_date}.{file_extension}")
        # Move to the next month
        current_date = current_date + timedelta(days=32)
        current_date = current_date.replace(day=1)

    return filenames


if __name__ == "__main__":
    # Define the date ranges
    date_ranges = [
        (datetime.strptime("01012022", "%d%m%Y"), datetime.strptime("31052022", "%d%m%Y")),
        (datetime.strptime("01082022", "%d%m%Y"), datetime.strptime("01082022", "%d%m%Y")),
        (datetime.strptime("August 2023", "%B %Y"), datetime.strptime("August 2023", "%B %Y")),
        (datetime.strptime("july 2023", "%B %Y"), datetime.strptime("july 2023", "%B %Y")),
        (datetime.strptime("May 2023", "%B %Y"), datetime.strptime("June 2023", "%B %Y")),
        (datetime.strptime("Sep 2022", "%b %Y"), datetime.strptime("Jan 2023", "%b %Y"))
    ]

    # Initialize an empty list to store filenames
    all_filenames = []

    # Loop through each date range and generate filenames
    for start_date, end_date in date_ranges:
        filenames = generate_monthly_filenames(start_date, end_date, "xlsx")
        all_filenames.extend(filenames)

    # Print the combined list of filenames
    print(all_filenames)


# Define the function to validate data received
def validate_data_received(folder_path, start_date, end_date):
    # Generate the list of expected filenames for the given date range
    expected_filenames = generate_monthly_filenames(start_date, end_date, "xlsx")
    # Print all_filenames and expected_filenames for debugging
    print("all_filenames in list:", all_filenames)
    print("Expected Filenames:", expected_filenames)

    # Create a list of dictionaries to store the validation results
    validation_data = []

    for expected_filename in expected_filenames:
        if expected_filename.lower() in [file.lower() for file in all_filenames]:
            status = "Yes"
        else:
            status = "No"

        # Extract the month and year from the filename
        month, year = expected_filename.split('.')[0].split()

        validation_data.append({"Month": f"{month} {year}", "Status": status})

    # Create a DataFrame from the validation data
    validation_df = pd.DataFrame(validation_data)

    # Save the validation results to an Excel file
    validation_df.to_excel("data_validation3.xlsx", index=False)


if __name__ == "__main__":
    start_date1 = datetime.strptime("01012022", "%d%m%Y")
    end_date1 = datetime.strptime("31122023", "%d%m%Y")  # Assuming data for all of 2022 and 2023
    validate_data_received(folder_path, start_date1, end_date1)
