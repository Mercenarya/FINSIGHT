"""
MongoDB Connection Test Script
Kiểm tra kết nối MongoDB và cấu trúc dữ liệu
"""
import os
from pymongo import MongoClient
import json

# MongoDB Configuration
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
MONGO_DB = os.getenv('MONGO_DB', 'financial_db')
MONGO_COLLECTION = os.getenv('MONGO_COLLECTION', 'datasets')

def test_mongodb_connection():
    """Test MongoDB connection"""
    print("=" * 60)
    print("Testing MongoDB Connection")
    print("=" * 60)
    
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        
        # Test connection
        client.server_info()
        print("✅ Successfully connected to MongoDB")
        print(f"   URI: {MONGO_URI}")
        
        # List databases
        databases = client.list_database_names()
        print(f"\n📊 Available databases: {databases}")
        
        # Check if our database exists
        if MONGO_DB in databases:
            print(f"✅ Database '{MONGO_DB}' exists")
        else:
            print(f"⚠️  Database '{MONGO_DB}' not found")
            print(f"   Available: {databases}")
        
        return client
    
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return None


def test_collection_structure(client):
    """Test collection structure"""
    print("\n" + "=" * 60)
    print("Testing Collection Structure")
    print("=" * 60)
    
    try:
        db = client[MONGO_DB]
        collection = db[MONGO_COLLECTION]
        
        # Count documents
        count = collection.count_documents({})
        print(f"📈 Total documents in '{MONGO_COLLECTION}': {count}")
        
        if count == 0:
            print("⚠️  Collection is empty!")
            print("\n💡 Sample document structure needed:")
            print(json.dumps({
                "ticker": "VIC",
                "reports": [
                    {
                        "title": "1. Doanh thu bán hàng và cung cấp dịch vụ",
                        "Third_quarter": "1500000"
                    }
                ],
                "assets": [
                    {
                        "title": "TỔNG CỘNG TÀI SẢN",
                        "Third_quarter": "5000000"
                    }
                ]
            }, indent=2, ensure_ascii=False))
            return
        
        # Get sample document
        sample = collection.find_one()
        print(f"\n📄 Sample document structure:")
        print(f"   Ticker: {sample.get('ticker', 'N/A')}")
        print(f"   Has 'reports': {('reports' in sample)}")
        print(f"   Has 'assets': {('assets' in sample)}")
        
        if 'reports' in sample:
            print(f"   Reports count: {len(sample['reports'])}")
            if sample['reports']:
                print(f"   First report title: {sample['reports'][0].get('title', 'N/A')}")
        
        if 'assets' in sample:
            print(f"   Assets count: {len(sample['assets'])}")
            if sample['assets']:
                print(f"   First asset title: {sample['assets'][0].get('title', 'N/A')}")
        
        # List all tickers
        tickers = collection.distinct('ticker')
        print(f"\n🏢 Available tickers ({len(tickers)}):")
        for ticker in tickers[:10]:  # Show first 10
            print(f"   - {ticker}")
        if len(tickers) > 10:
            print(f"   ... and {len(tickers) - 10} more")
        
    except Exception as e:
        print(f"❌ Collection test failed: {e}")


def test_sample_query(client):
    """Test sample query for two companies"""
    print("\n" + "=" * 60)
    print("Testing Sample Query")
    print("=" * 60)
    
    try:
        db = client[MONGO_DB]
        collection = db[MONGO_COLLECTION]
        
        # Get first two tickers
        tickers = collection.distinct('ticker')
        if len(tickers) < 2:
            print("⚠️  Need at least 2 companies in database")
            return
        
        ticker1, ticker2 = tickers[0], tickers[1]
        print(f"🔍 Querying for: {ticker1} and {ticker2}")
        
        query = {
            "ticker": {
                "$in": [ticker1, ticker2]
            }
        }
        
        results = list(collection.find(query))
        print(f"✅ Found {len(results)} companies")
        
        for result in results:
            ticker = result.get('ticker', 'N/A')
            reports_count = len(result.get('reports', []))
            assets_count = len(result.get('assets', []))
            print(f"\n   {ticker}:")
            print(f"   - Reports: {reports_count} items")
            print(f"   - Assets: {assets_count} items")
            
            # Check for required fields
            if 'reports' in result and result['reports']:
                has_revenue = any('doanh thu' in item.get('title', '').lower() 
                                 for item in result['reports'])
                has_profit = any('lợi nhuận' in item.get('title', '').lower() 
                                for item in result['reports'])
                print(f"   - Has revenue data: {has_revenue}")
                print(f"   - Has profit data: {has_profit}")
            
            if 'assets' in result and result['assets']:
                has_total_assets = any('tổng cộng tài sản' in item.get('title', '').lower() 
                                      for item in result['assets'])
                has_current_assets = any('tài sản ngắn hạn' in item.get('title', '').lower() 
                                        for item in result['assets'])
                print(f"   - Has total assets: {has_total_assets}")
                print(f"   - Has current assets: {has_current_assets}")
        
    except Exception as e:
        print(f"❌ Sample query failed: {e}")


def main():
    print("\n🚀 MongoDB Connection Test")
    print("Configuration:")
    print(f"   URI: {MONGO_URI}")
    print(f"   Database: {MONGO_DB}")
    print(f"   Collection: {MONGO_COLLECTION}\n")
    
    # Test connection
    client = test_mongodb_connection()
    
    if client:
        # Test collection
        test_collection_structure(client)
        
        # Test sample query
        test_sample_query(client)
        
        # Close connection
        client.close()
        print("\n" + "=" * 60)
        print("✅ All tests completed!")
        print("=" * 60)
    else:
        print("\n❌ Cannot proceed without MongoDB connection")
        print("\n💡 Troubleshooting:")
        print("   1. Make sure MongoDB is running")
        print("   2. Check MONGO_URI in .env file")
        print("   3. Verify firewall settings")


if __name__ == "__main__":
    main()
