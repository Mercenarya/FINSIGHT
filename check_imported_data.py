
from pymongo import MongoClient

def check_db():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['dataset']
    collection = db['companies']
    
    total = collection.count_documents({})
    print(f"Total Companies in DB: {total}")
    
    docs = collection.find({}).sort("ticker", 1)
    
    print(f"Total Companies: {total}")
    print("List of Tickers found in DB:")
    for doc in docs:
        print(f"- {doc.get('ticker', 'NO_TICKER')} (ID: {doc.get('_id')})")

if __name__ == "__main__":
    check_db()
