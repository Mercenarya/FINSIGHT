"""
Dataset Service for saving Analysis and Forecasting results to MongoDB
Saves data to dataset.dataset collection
"""
import os
from datetime import datetime
from pymongo import MongoClient
from typing import Dict, Any, Optional

# MongoDB Configuration
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
MONGO_DB = os.getenv('MONGO_DB', 'dataset')
DATASET_COLLECTION = 'dataset'  # Collection name: dataset.dataset


def get_mongo_client():
    """Get MongoDB client connection"""
    return MongoClient(MONGO_URI)


def save_analysis_result(
    company: str,
    year: str,
    quarter: str,
    metrics: str,
    analysis_data: Dict[str, Any],
    ai_insight: str = ''
) -> Optional[str]:
    """
    Save analysis result to MongoDB dataset.dataset collection
    
    Args:
        company: Company ticker (e.g., 'VIC')
        year: Analysis year (e.g., '2025')
        quarter: Quarter analyzed (e.g., 'Quarter 4')
        metrics: Metrics used (e.g., 'cash_ratio,quick_ratio')
        analysis_data: Full analysis result data
        ai_insight: AI generated insight text
        
    Returns:
        Inserted document ID as string, or None if failed
    """
    try:
        client = get_mongo_client()
        db = client[MONGO_DB]
        collection = db[DATASET_COLLECTION]
        
        document = {
            'type': 'analysis',
            'company': company.upper(),
            'year': year,
            'quarter': quarter,
            'metrics': metrics,
            'created_at': datetime.utcnow(),
            'data': {
                'profitability': analysis_data.get('profitability', {}),
                'liquidity': analysis_data.get('liquidity', {}),
                'chart_data': analysis_data.get('chart_data', [])
            },
            'ai_insight': ai_insight
        }
        
        result = collection.insert_one(document)
        client.close()
        
        print(f"[Dataset] Saved analysis result for {company} - ID: {result.inserted_id}")
        return str(result.inserted_id)
        
    except Exception as e:
        print(f"[Dataset] Error saving analysis result: {e}")
        return None


def save_forecasting_result(
    company: str,
    year: str,
    quarter: str,
    metrics: str,
    chart_data: list,
    ai_insight: str = ''
) -> Optional[str]:
    """
    Save forecasting/prediction result to MongoDB dataset.dataset collection
    
    Args:
        company: Company ticker (e.g., 'VIC')
        year: Forecast year (e.g., '2025')
        quarter: Quarter forecasted (e.g., '4')
        metrics: Metrics used (e.g., 'cash_ratio,quick_ratio')
        chart_data: Chart data including historical and predicted values
        ai_insight: AI generated insight text
        
    Returns:
        Inserted document ID as string, or None if failed
    """
    try:
        client = get_mongo_client()
        db = client[MONGO_DB]
        collection = db[DATASET_COLLECTION]
        
        # Separate historical and forecast data
        historical_data = [d for d in chart_data if not d.get('isForecast', False)]
        forecast_data = [d for d in chart_data if d.get('isForecast', False)]
        
        document = {
            'type': 'forecasting',
            'company': company.upper(),
            'year': year,
            'quarter': f'Quarter {quarter}' if quarter.isdigit() else quarter,
            'metrics': metrics,
            'created_at': datetime.utcnow(),
            'data': {
                'historical': historical_data,
                'forecast': forecast_data,
                'chart_data': chart_data
            },
            'ai_insight': ai_insight
        }
        
        result = collection.insert_one(document)
        client.close()
        
        print(f"[Dataset] Saved forecasting result for {company} - ID: {result.inserted_id}")
        return str(result.inserted_id)
        
    except Exception as e:
        print(f"[Dataset] Error saving forecasting result: {e}")
        return None


def get_analysis_history(
    company: str = None,
    result_type: str = None,
    limit: int = 10
) -> list:
    """
    Get history of analysis/forecasting results from database
    
    Args:
        company: Filter by company ticker (optional)
        result_type: Filter by type 'analysis' or 'forecasting' (optional)
        limit: Maximum number of results to return
        
    Returns:
        List of saved results, sorted by created_at descending
    """
    try:
        client = get_mongo_client()
        db = client[MONGO_DB]
        collection = db[DATASET_COLLECTION]
        
        query = {}
        if company:
            query['company'] = company.upper()
        if result_type:
            query['type'] = result_type
        
        results = list(
            collection.find(query)
            .sort('created_at', -1)
            .limit(limit)
        )
        
        client.close()
        
        # Convert ObjectId to string for JSON serialization
        for result in results:
            result['_id'] = str(result['_id'])
            if 'created_at' in result:
                result['created_at'] = result['created_at'].isoformat()
        
        return results
        
    except Exception as e:
        print(f"[Dataset] Error fetching history: {e}")
        return []
