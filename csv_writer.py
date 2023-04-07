import csv
import os
def create_csv_file(file_path):
    """
    Creates a CSV file with the specified columns.

    Args:
        file_path (str): File path of the CSV file.

    Returns:
        None
    """
    # Define the column names
    fieldnames = ["similarity_score", "url_link", "parent_url", "outgoing_links_list", "webpage_vector"]

    # Create the CSV file with column names
    with open(file_path, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
    print(f"CSV file '{file_path}' created successfully!")

def update_csv_file(file_path, data):
    """
    Updates the CSV file with new data. If CSV file does not exists, it will be created by invoking create_csv_file

    Args:
        file_path (str): File path of the CSV file.
        data (dict): Data to be written to the CSV file. Should be a dictionary with keys as column names and values
                     as data to be written. In form :["similarity_score", "url_link", "source_link", "outgoing_links_list", "webpage_vector"]

    Returns:
        None
    """
    # Check if the file path exists
    if not os.path.exists(file_path):
        create_csv_file(file_path)

    # Append new data to the CSV file
    with open(file_path, mode='a', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=data.keys())
        writer.writerow(data)
    print(f"Data updated in CSV file '{file_path}' successfully!")
