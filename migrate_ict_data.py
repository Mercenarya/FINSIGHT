
import os
import csv
import sys
from pymongo import MongoClient

# MongoDB Config
MONGO_URI = 'mongodb://localhost:27017/'
MONGO_DB = 'dataset'
MONGO_COLLECTION = 'companies'

def read_csv_to_list(file_path):
    data_list = []
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Filter out the "time: " column or empty keys if any
                clean_row = {k.strip(): v.strip() for k, v in row.items() if k and 'time' not in k.lower()}
                data_list.append(clean_row)
        return data_list
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

def migrate():
    # Connect to MongoDB
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]

    # Paths to CSVs - Hardcoded logic for absolute paths based on environment
    reports_file = r'd:\FINSIGHT-brch_main\main\finsight_services\data\raw\cleandpt001.csv'
    assets_file = r'd:\FINSIGHT-brch_main\main\finsight_services\data\raw\assets001.csv'

    print(f"Reading data from:\n {reports_file}\n {assets_file}")
    
    if not os.path.exists(reports_file):
        print("ERROR: Report file not found!")
        return

    reports_data = read_csv_to_list(reports_file)
    assets_data = read_csv_to_list(assets_file)

    if not reports_data and not assets_data:
        print("No data found in CSV files. Aborting.")
        return

    company_doc = {
        "ticker": "ICT",
        "year": 2025,
        "reports": reports_data,
        "assets": assets_data
    }

    # Clear existing collection (WARNING: This deletes current data)
    print("Clearing existing companies collection...")
    collection.delete_many({})

    # Insert new structured document
    print("Inserting new ICT company document...")
    result = collection.insert_one(company_doc)

    print(f"Migration successful. Inserted ID: {result.inserted_id}")
    
    # Verify by checking count directly
    count = collection.count_documents({})
    print(f"\n[FINAL CHECK] Total documents in collection: {count}")
    
    if count == 1:
        print("SUCCESS: Data flattened into exactly 1 document.")
    else:
        print(f"WARNING: Unexpected document count: {count}")

    client.close()

if __name__ == "__main__":
    migrate()
