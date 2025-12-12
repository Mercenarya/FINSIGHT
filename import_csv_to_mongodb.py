"""
Import CSV files to MongoDB
Imports financial data from CSV files to MongoDB for the comparison API
"""
import os
import pandas as pd
from pymongo import MongoClient

# Configuration
CSV_DIR = r"C:\Users\Shiro\Downloads\data\data\processed"
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "dataset"
MONGO_COLLECTION = "companies"

def import_csv_to_mongodb():
    """Import all CSV files to MongoDB"""
    
    # Connect to MongoDB
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]
    
    # Clear existing data (optional)
    collection.drop()
    print(f"✅ Cleared collection: {MONGO_COLLECTION}")
    
    # Get all CSV files
    csv_files = [f for f in os.listdir(CSV_DIR) if f.endswith('_finance.csv')]
    print(f"📁 Found {len(csv_files)} CSV files")
    
    imported_count = 0
    
    for csv_file in csv_files:
        ticker = csv_file.replace('_finance.csv', '')
        file_path = os.path.join(CSV_DIR, csv_file)
        
        try:
            # Read CSV
            df = pd.read_csv(file_path)
            
            # Convert to list of dicts (each row becomes an item)
            reports = []
            for _, row in df.iterrows():
                item = {
                    'title': row['Title'],
                    'First_quarter': str(row.get('Quarter 1', '')),
                    'Second_quarter': str(row.get('Quarter 2', '')),
                    'Third_quarter': str(row.get('Quarter 3', '')),
                    'Fourth_quarter': str(row.get('Quarter 4', ''))
                }
                reports.append(item)
            
            # Create document for this company
            document = {
                'ticker': ticker,
                'reports': reports,
                'assets': reports  # Using same data for assets (adjust if you have separate asset files)
            }
            
            # Insert to MongoDB
            collection.insert_one(document)
            imported_count += 1
            print(f"  ✅ Imported: {ticker} ({len(reports)} rows)")
            
        except Exception as e:
            print(f"  ❌ Error importing {ticker}: {e}")
    
    print(f"\n🎉 Import completed! {imported_count}/{len(csv_files)} companies imported.")
    print(f"   Database: {MONGO_DB}")
    print(f"   Collection: {MONGO_COLLECTION}")
    
    # Verify
    count = collection.count_documents({})
    tickers = collection.distinct('ticker')
    print(f"\n📊 Verification:")
    print(f"   Total documents: {count}")
    print(f"   Tickers: {tickers}")
    
    client.close()

if __name__ == "__main__":
    import_csv_to_mongodb()
