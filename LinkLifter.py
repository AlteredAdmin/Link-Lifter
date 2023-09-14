import re
import os
import csv
from datetime import datetime


def find_urls_in_file(file_path):
    """Extract URLs from a given file."""
    urls = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Regular expression to match URLs
            url_pattern = re.compile(r'https?://\S+|www\.\S+|\w+\.\w+')
            urls = url_pattern.findall(content)
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return urls


def search_directory(directory):
    """Recursively search for URLs in all files in a directory."""
    all_urls = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            urls_in_file = find_urls_in_file(file_path)
            for url in urls_in_file:
                all_urls.append((url, file_path))
    return all_urls


def save_to_csv(data):
    """Save the URLs and their file paths to a CSV."""
    current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    csv_filename = f"LinkLifter_{current_time}.csv"
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["URL", "File Path"])
        for row in data:
            writer.writerow(row)
    print(f"Data saved to {csv_filename}")


if __name__ == "__main__":
    path = input("Enter the path to a file or directory: ").strip()
    if os.path.isfile(path):
        urls = find_urls_in_file(path)
        data = [(url, path) for url in urls]
    elif os.path.isdir(path):
        data = search_directory(path)
    else:
        print("Invalid path. Please provide a valid file or directory path.")
        exit(1)
    save_to_csv(data)
