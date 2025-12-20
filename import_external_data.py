
import os
import csv
import glob
from pymongo import MongoClient

# MongoDB Config
MONGO_URI = 'mongodb://localhost:27017/'
MONGO_DB = 'dataset'
MONGO_COLLECTION = 'companies'

# Source Directory
SOURCE_DIR = r"C:\Users\Shiro\Downloads\New folder (3)\data\processed"

def classify_row(title):
    """
    Heuristic to classify a row as belonging to 'assets' (Balance Sheet) 
    or 'reports' (Income Statement).
    """
    title_upper = title.upper()
    
    # Keywords often found in Balance Sheet
    assets_keywords = [
        "TÀI SẢN", "NGUỒN VỐN", "NỢ PHẢI TRẢ", "VỐN CHỦ SỞ HỮU",
        "TIỀN VÀ CÁC KHOẢN TƯƠNG ĐƯƠNG", "HÀNG TỒN KHO", "PHẢI THU",
        "TÀI SẢN CỐ ĐỊNH", "BẤT ĐỘNG SẢN ĐẦU TƯ"
    ]
    
    # Check if any asset keyword matches
    for kw in assets_keywords:
        if kw in title_upper:
            return 'assets'
            
    # Default to reports (Income Statement) if ambiguous, 
    # but let's try to be specific for reports too if needed.
    # Usually Income statement starts with "Doanh thu..."
    
    # However, Balance Sheet items are usually structured with Roman numerals or A, B, C...
    # Let's try a simpler approach: 
    # If the file is mixed, usually Assets come after Reports or vice versa.
    # But for now, let's treat specific Balance Sheet sections as assets.
    
    return 'reports'

def import_data():
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]
    
    # Find all finance csv files
    csv_pattern = os.path.join(SOURCE_DIR, "*_finance.csv")
    files = glob.glob(csv_pattern)
    
    print(f"Found {len(files)} files to process in {SOURCE_DIR}")
    
    for file_path in files:
        filename = os.path.basename(file_path)
        # Extract ticker (e.g. PLP_finance.csv -> PLP)
        ticker = filename.split('_')[0].upper()
        
        # Skip ICT if we want to preserve the manual one (though this script is smarter)
        # The user said "ko đụng j thằng ICT", so we skip ICT.
        if ticker == 'ICT':
            print(f"Skipping ICT (user requested to preserve existing)...")
            continue
            
        print(f"Processing {ticker} from {filename}...")
        
        reports_data = []
        assets_data = []
        
        try:
            # Use utf-8-sig to handle BOM if present
            with open(file_path, mode='r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                
                # Normalize headers: strip spaces
                if reader.fieldnames:
                    reader.fieldnames = [x.strip() for x in reader.fieldnames]
                
                for row in reader:
                    # Clean keys/values
                    clean_row = {k.strip(): v.strip() for k, v in row.items() if k}
                    
                    # Try to find Title column (Title, title, Chi tieu, etc.)
                    title = clean_row.get('Title', clean_row.get('title', ''))
                    
                    # If Title is empty, maybe it's the first column?
                    if not title and list(clean_row.values()):
                         title = list(clean_row.values())[0] # Fallback to first value
                         # Update dictionary to consistenly use 'Title' key if we want to save valid data
                         # But let's just use it for classification for now.

                    if not title:
                        continue # Skip empty rows

                    # LOGIC Classification improved
                    title_upper = title.upper().strip()
                    
                    # LOGIC Classification improved
                    title_upper = title.upper().strip()
                    is_asset = False
                    
                    # 1. Assets/Capital often start with A-, B-, C-, D- or Roman Numerals
                    # Reports usually start with Arabic numerals 1. 2. 3. ...
                    
                    if title_upper.startswith("A-") or title_upper.startswith("B-") or title_upper.startswith("C-") or title_upper.startswith("D-"):
                        is_asset = True
                    elif title_upper.startswith("I.") or title_upper.startswith("II.") or title_upper.startswith("III.") or title_upper.startswith("IV.") or title_upper.startswith("V."):
                        is_asset = True
                    # Headers
                    elif "TÀI SẢN" in title_upper or "NGUỒN VỐN" in title_upper or "NỢ PHẢI TRẢ" in title_upper:
                         # Unless it's "Tổng cộng tài sản" which is a sum line, still asset
                         is_asset = True
                    
                    # Specific exclusion: "Doanh thu", "Lợi nhuận" (except unallocated profit), "Chi phí" usually Reports
                    # But exclude "Chi phí xây dựng dở dang" (Asset) or "Chi phí trả trước" (Asset)
                    if not is_asset:
                        # Fallback: if it starts with a number "1. ", "10. " -> Likely Report
                        # BUT "1. Tiền" is Asset.
                        # So let's use keywords strongly.
                        
                        asset_keywords = ["TIỀN", "HÀNG TỒN KHO", "PHẢI THU", "TRẢ TRƯỚC", "THUẾ GTGT", "ĐẦU TƯ TÀI CHÍNH", "TÀI SẢN", "XDCB", "KÝ QUỸ"]
                        if any(k in title_upper for k in asset_keywords):
                             # Double check it's not "Doanh thu hoạt động tài chính" (Report)
                             if "DOANH THU" not in title_upper:
                                 is_asset = True

                    if is_asset:
                        assets_data.append(clean_row)
                    else:
                        reports_data.append(clean_row)
                        
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            continue
            
        # Construct Document
        # Determine year. Assuming 2025 as requested for all.
        company_doc = {
            "ticker": ticker,
            "year": 2025,
            "reports": reports_data,
            "assets": assets_data
        }
        
        # Upsert: Replace if exists, Insert if new
        collection.replace_one(
            {"ticker": ticker},
            company_doc,
            upsert=True
        )
        print(f"Imported {ticker}: {len(reports_data)} reports rows, {len(assets_data)} assets rows.")

    print("\nImport finished.")
    
    # Verification
    total = collection.count_documents({})
    print(f"Total entries in DB: {total}")
    
    client.close()

if __name__ == "__main__":
    import_data()
