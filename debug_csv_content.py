
import os
import csv
import glob

SOURCE_DIR = r"C:\Users\Shiro\Downloads\New folder (3)\data\processed"

def debug_file():
    csv_pattern = os.path.join(SOURCE_DIR, "*_finance.csv")
    files = glob.glob(csv_pattern)
    
    if not files:
        print("No files found.")
        return

    # Pick the first file (e.g. VSI or PLP)
    file_path = files[1] # Usually PLP or similar
    print(f"Inspecting file: {file_path}")
    
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        if reader.fieldnames:
            print(f"Headers found: {reader.fieldnames}")
            
        count = 0
        for row in reader:
            print(f"Row {count} Keys: {list(row.keys())}")
            print(f"Row {count} Values: {list(row.values())}")
            count += 1
            if count > 5:
                break

if __name__ == "__main__":
    debug_file()
