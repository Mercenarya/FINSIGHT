
import os
from pymongo import MongoClient

# Cấu hình MongoDB
MONGO_URI = 'mongodb://localhost:27017/'
MONGO_DB = 'dataset'
MONGO_COLLECTION = 'companies'

def merge_existing_docs_to_one():
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]

    # 1. Lấy tất cả document hiện tại
    all_docs = list(collection.find({}))
    count = len(all_docs)
    
    if count <= 1:
        print(f"Collection chỉ có {count} document. Không cần gộp.")
        return

    print(f"Tìm thấy {count} documents rời rạc. Đang tiến hành gộp...")

    # 2. Phân loại dữ liệu (Giả sử dựa trên cấu trúc để chia vào reports/assets nếu cần)
    # Ở đây tôi sẽ gộp chung vào 1 array 'raw_data' nếu không phân biệt được, 
    # HOẶC giữ nguyên logic chia assets/reports nếu dữ liệu có đặc điểm nhận dạng.
    
    # Tuy nhiên, vì code trước đã gộp chuẩn rồi, nên script này 
    # giả định trường hợp dữ liệu bị tản mát (flat structure).
    
    merged_reports = []
    merged_assets = []
    
    for doc in all_docs:
        # Loại bỏ _id để không bị duplicate key khi lưu lại
        doc.pop('_id', None)
        
        # Logic phân loại đơn giản (Ví dụ dựa vào tên chỉ tiêu)
        title = doc.get('Title', '')
        if 'TÀI SẢN' in title or 'NGUỒN VỐN' in title:
            merged_assets.append(doc)
        else:
            merged_reports.append(doc)

    # 3. Tạo document tổng hợp
    main_doc = {
        "ticker": "ICT", # Gán mã mặc định là ICT
        "reports": merged_reports,
        "assets": merged_assets
    }

    # 4. Xóa dữ liệu cũ và Insert document mới
    collection.delete_many({})
    result = collection.insert_one(main_doc)

    print(f"Đã gộp thành công vào 1 document duy nhất!")
    print(f"New ID: {result.inserted_id}")
    print(f"- Reports: {len(merged_reports)} dòng")
    print(f"- Assets: {len(merged_assets)} dòng")
    
    client.close()

if __name__ == "__main__":
    merge_existing_docs_to_one()
