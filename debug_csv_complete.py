
import os
import csv
import glob

SOURCE_DIR = r"C:\Users\Shiro\Downloads\New folder (3)\data\processed"

def debug_full_file():
    csv_pattern = os.path.join(SOURCE_DIR, "*_finance.csv")
    files = glob.glob(csv_pattern)
    
    if not files:
        print("No files found.")
        return

    # Pick PLP file
    target_file = None
    for f in files:
        if "PLP" in f:
            target_file = f
            break
            
    if not target_file:
        target_file = files[0]

    print(f"Reading FULL content of: {target_file}")
    
    with open(target_file, mode='r', encoding='utf-8-sig') as f:
        reader = csv.reader(f) # Use simple reader to see raw rows
        for i, row in enumerate(reader):
            print(f"Line {i}: {row}")
            if i > 50: # Limit to 50 lines
                break

if __name__ == "__main__":
    debug_full_file()
