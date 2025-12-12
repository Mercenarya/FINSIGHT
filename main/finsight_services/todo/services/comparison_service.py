"""
Comparison Service for Financial Analysis
Handles company comparison logic and MongoDB integration
"""
import os
import sys
from pymongo import MongoClient
from typing import Dict, List, Optional, Tuple, Any

# MongoDB Configuration
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
MONGO_DB = os.getenv('MONGO_DB', 'dataset')
MONGO_COLLECTION = os.getenv('MONGO_COLLECTION', 'companies')


# Utility Functions
def parse_money(value) -> float:
    """
    Parse monetary value from string or number
    Handles comma-separated values and empty strings
    """
    if not value or value == "":
        return 0.0
    if isinstance(value, str):
        return float(value.replace(',', '').strip())
    return float(value)


def safe_div(numerator: float, denominator: float) -> float:
    """
    Safe division to avoid division by zero
    Returns 0 if denominator is 0
    """
    if denominator == 0:
        return 0.0
    return numerator / denominator


def get_value_by_title(data_array: List[Dict], keyword: str, quarter_key: str) -> float:
    """
    Extract value from JSON array based on title keyword
    
    Args:
        data_array: Array of financial data items
        keyword: Keyword to search in title field
        quarter_key: Quarter field name (e.g., 'Third_quarter')
    
    Returns:
        Parsed monetary value or 0 if not found
    """
    if not data_array or not isinstance(data_array, list):
        return 0.0
    
    for item in data_array:
        if 'title' in item and keyword.lower() in item['title'].lower():
            return parse_money(item.get(quarter_key, 0))
    
    return 0.0


def map_quarter_format(quarter: str) -> Tuple[str, str]:
    """
    Map between different quarter formats
    
    Args:
        quarter: Quarter in either format ('Quarter 3' or 'Third_quarter')
    
    Returns:
        Tuple of (standard_format, mongodb_format)
        standard_format: 'Quarter 3'
        mongodb_format: 'Third_quarter'
    """
    quarter_mapping = {
        'Quarter 1': 'First_quarter',
        'Quarter 2': 'Second_quarter',
        'Quarter 3': 'Third_quarter',
        'Quarter 4': 'Fourth_quarter',
        'First_quarter': 'Quarter 1',
        'Second_quarter': 'Quarter 2',
        'Third_quarter': 'Quarter 3',
        'Fourth_quarter': 'Quarter 4',
    }
    
    if quarter in quarter_mapping:
        if 'Quarter' in quarter and quarter[0].isdigit() == False:
            # It's mongodb format (e.g., 'Third_quarter')
            return quarter_mapping[quarter], quarter
        else:
            # It's standard format (e.g., 'Quarter 3')
            return quarter, quarter_mapping[quarter]
    
    # Default to Quarter 3 if not found
    return 'Quarter 3', 'Third_quarter'


def fetch_companies_data(ticker1: str, ticker2: str) -> List[Dict]:
    """
    Fetch company data from MongoDB
    
    Args:
        ticker1: First company ticker symbol
        ticker2: Second company ticker symbol
    
    Returns:
        List of company data dictionaries
    """
    try:
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB]
        collection = db[MONGO_COLLECTION]
        
        # Query for both companies
        query = {
            "ticker": {
                "$in": [ticker1, ticker2]
            }
        }
        
        results = list(collection.find(query))
        client.close()
        
        return results
    
    except Exception as error:
        print(f"MongoDB fetch error: {error}")
        return []


def calculate_growth_metrics(company_data: Dict) -> Dict:
    """
    Calculate growth metrics across quarters
    
    Args:
        company_data: Company data from MongoDB with reports and assets
    
    Returns:
        Dictionary containing growth metrics and future prediction
    """
    reports = company_data.get('reports', [])
    assets = company_data.get('assets', [])
    
    quarters = ['First_quarter', 'Second_quarter', 'Third_quarter', 'Fourth_quarter']
    
    # Get revenue and net income for each quarter
    revenues = []
    net_incomes = []
    
    for q in quarters:
        rev = get_value_by_title(reports, "1. Doanh thu bán hàng", q)
        net = get_value_by_title(reports, "18. Lợi nhuận sau thuế", q)
        if rev > 0:
            revenues.append(rev)
        if net > 0:
            net_incomes.append(net)
    
    # Calculate growth rates
    revenue_growth = 0.0
    profit_growth = 0.0
    
    if len(revenues) >= 2:
        # Quarter-over-quarter growth
        revenue_growth = safe_div(revenues[-1] - revenues[-2], revenues[-2]) * 100
    
    if len(net_incomes) >= 2:
        profit_growth = safe_div(net_incomes[-1] - net_incomes[-2], net_incomes[-2]) * 100
    
    # Calculate CAGR (Compound Annual Growth Rate) if we have enough data
    cagr = 0.0
    if len(revenues) >= 4 and revenues[0] > 0:
        # Using first and last quarter data
        cagr = ((revenues[-1] / revenues[0]) ** (1/4) - 1) * 100
    
    # Predict future profit percentage based on trends
    predicted_profit_pct = 0.0
    confidence = "Low"
    
    if len(net_incomes) >= 2:
        # Simple linear trend projection
        avg_growth = profit_growth
        
        # Adjust prediction based on multiple factors
        if profit_growth > 0 and revenue_growth > 0:
            predicted_profit_pct = min(profit_growth * 0.8, 50)  # Conservative estimate
            confidence = "Medium"
        
        if profit_growth > 10 and revenue_growth > 10:
            predicted_profit_pct = min(profit_growth * 0.9, 60)
            confidence = "High"
        
        if profit_growth < 0:
            predicted_profit_pct = max(profit_growth * 1.2, -30)
            confidence = "High Risk"
    
    return {
        'revenueGrowth': round(revenue_growth, 2),
        'profitGrowth': round(profit_growth, 2),
        'cagr': round(cagr, 2),
        'prediction': {
            'nextQuarterProfitGrowth': round(predicted_profit_pct, 2),
            'confidence': confidence,
            'analysis': generate_growth_analysis(revenue_growth, profit_growth, predicted_profit_pct)
        }
    }


def generate_growth_analysis(revenue_growth: float, profit_growth: float, prediction: float) -> str:
    """Generate human-readable analysis of growth metrics"""
    
    if profit_growth > 20:
        trend = "Strong growth"
    elif profit_growth > 10:
        trend = "Good growth"
    elif profit_growth > 0:
        trend = "Slight growth"
    elif profit_growth > -10:
        trend = "Slight decline"
    else:
        trend = "Sharp decline"
    
    if prediction > 15:
        outlook = "Positive outlook, consider investing"
    elif prediction > 5:
        outlook = "Stable outlook"
    elif prediction > -5:
        outlook = "Needs further monitoring"
    else:
        outlook = "High risk, be cautious"
    
    return f"{trend}. {outlook}."


def calculate_company_metrics(company_data: Dict, quarter: str) -> Dict:
    """
    Calculate all financial metrics for a single company
    
    Args:
        company_data: Company data from MongoDB
        quarter: Quarter key in mongodb format (e.g., 'Third_quarter')
    
    Returns:
        Dictionary containing all calculated metrics
    """
    reports = company_data.get('reports', [])
    assets = company_data.get('assets', [])
    ticker = company_data.get('ticker', 'Unknown')
    
    # Extract raw data
    revenue = get_value_by_title(reports, "1. Doanh thu bán hàng", quarter)
    gross_profit = get_value_by_title(reports, "5. Lợi nhuận gộp", quarter)
    net_income = get_value_by_title(reports, "18. Lợi nhuận sau thuế", quarter)
    cost_of_goods_sold = get_value_by_title(reports, "4. Giá vốn hàng bán", quarter)
    
    total_assets = get_value_by_title(assets, "TỔNG CỘNG TÀI SẢN", quarter)
    current_assets = get_value_by_title(assets, "A- TÀI SẢN NGẮN HẠN", quarter)
    current_liabilities = get_value_by_title(assets, "I. Nợ ngắn hạn", quarter)
    inventory = get_value_by_title(assets, "IV. Hàng tồn kho", quarter)
    cash = get_value_by_title(assets, "I. Tiền và các khoản tương đương tiền", quarter)
    receivables = get_value_by_title(assets, "III. Các khoản phải thu ngắn hạn", quarter)
    equity = get_value_by_title(assets, "D. VỐN CHỦ SỞ HỮU", quarter)
    
    # Calculate Profitability Metrics
    gross_margin = safe_div(gross_profit, revenue) * 100
    net_margin = safe_div(net_income, revenue) * 100
    roa = safe_div(net_income, total_assets) * 100
    roe = safe_div(net_income, equity) * 100
    
    # Calculate Liquidity Metrics
    current_ratio = safe_div(current_assets, current_liabilities)
    quick_ratio = safe_div(current_assets - inventory, current_liabilities)
    cash_ratio = safe_div(cash, current_liabilities)
    
    # Calculate Efficiency Metrics
    asset_turnover = safe_div(revenue, total_assets)
    inventory_turnover = safe_div(cost_of_goods_sold, inventory)
    receivables_turnover = safe_div(revenue, receivables)
    
    return {
        'ticker': ticker,
        'metrics': {
            'profitability': {
                'grossMargin': round(gross_margin, 2),
                'netMargin': round(net_margin, 2),
                'roa': round(roa, 2),
                'roe': round(roe, 2)
            },
            'liquidity': {
                'currentRatio': round(current_ratio, 2),
                'quickRatio': round(quick_ratio, 2),
                'cashRatio': round(cash_ratio, 2)
            },
            'efficiency': {
                'assetTurnover': round(asset_turnover, 2),
                'inventoryTurnover': round(inventory_turnover, 2),
                'receivablesTurnover': round(receivables_turnover, 2)
            },
            'raw': {
                'revenue': revenue,
                'netIncome': net_income,
                'totalAssets': total_assets
            }
        }
    }


def compare_companies(ticker1: str, ticker2: str, quarter: str = 'Third_quarter') -> Dict:
    """
    Compare two companies across all financial metrics
    
    Args:
        ticker1: First company ticker
        ticker2: Second company ticker
        quarter: Quarter to analyze (mongodb format)
    
    Returns:
        Comparison results with winners and detailed metrics
    """
    # Fetch data from MongoDB
    companies_data = fetch_companies_data(ticker1, ticker2)
    
    if len(companies_data) < 2:
        return {
            'error': 'Could not find data for both companies',
            'data_found': len(companies_data),
            'tickers_requested': [ticker1, ticker2]
        }
    
    # Calculate metrics for both companies
    results = []
    growth_data = []
    
    for company_data in companies_data:
        metrics = calculate_company_metrics(company_data, quarter)
        growth = calculate_growth_metrics(company_data)
        metrics['metrics']['growth'] = growth
        results.append(metrics)
        growth_data.append({
            'ticker': metrics['ticker'],
            'growth': growth
        })
    
    # Ensure we have exactly 2 companies
    if len(results) != 2:
        return {
            'error': 'Invalid number of companies',
            'data_found': results
        }
    
    c1 = results[0]
    c2 = results[1]
    
    # Determine winners
    profitability_winner = c1['ticker'] if c1['metrics']['profitability']['netMargin'] > c2['metrics']['profitability']['netMargin'] else c2['ticker']
    liquidity_winner = c1['ticker'] if c1['metrics']['liquidity']['currentRatio'] > c2['metrics']['liquidity']['currentRatio'] else c2['ticker']
    efficiency_winner = c1['ticker'] if c1['metrics']['efficiency']['assetTurnover'] > c2['metrics']['efficiency']['assetTurnover'] else c2['ticker']
    
    # Growth winner based on profit growth
    growth_winner = c1['ticker'] if c1['metrics']['growth']['profitGrowth'] > c2['metrics']['growth']['profitGrowth'] else c2['ticker']
    
    # Future prediction winner
    c1_prediction = c1['metrics']['growth']['prediction']['nextQuarterProfitGrowth']
    c2_prediction = c2['metrics']['growth']['prediction']['nextQuarterProfitGrowth']
    future_profit_winner = c1['ticker'] if c1_prediction > c2_prediction else c2['ticker']
    
    # Build comparison response
    comparison = {
        'meta': {
            'quarter': quarter,
            'company1': c1['ticker'],
            'company2': c2['ticker']
        },
        'analysis': {
            'profitability_winner': profitability_winner,
            'liquidity_winner': liquidity_winner,
            'efficiency_winner': efficiency_winner,
            'growth_winner': growth_winner,
            'future_profit_winner': future_profit_winner
        },
        'chart_data': {
            'profitability': [
                {'metric': 'Gross Margin (%)', c1['ticker']: c1['metrics']['profitability']['grossMargin'], c2['ticker']: c2['metrics']['profitability']['grossMargin']},
                {'metric': 'Net Margin (%)', c1['ticker']: c1['metrics']['profitability']['netMargin'], c2['ticker']: c2['metrics']['profitability']['netMargin']},
                {'metric': 'ROA (%)', c1['ticker']: c1['metrics']['profitability']['roa'], c2['ticker']: c2['metrics']['profitability']['roa']},
                {'metric': 'ROE (%)', c1['ticker']: c1['metrics']['profitability']['roe'], c2['ticker']: c2['metrics']['profitability']['roe']},
            ],
            'liquidity': [
                {'metric': 'Current Ratio', c1['ticker']: c1['metrics']['liquidity']['currentRatio'], c2['ticker']: c2['metrics']['liquidity']['currentRatio']},
                {'metric': 'Quick Ratio', c1['ticker']: c1['metrics']['liquidity']['quickRatio'], c2['ticker']: c2['metrics']['liquidity']['quickRatio']},
                {'metric': 'Cash Ratio', c1['ticker']: c1['metrics']['liquidity']['cashRatio'], c2['ticker']: c2['metrics']['liquidity']['cashRatio']},
            ],
            'efficiency': [
                {'metric': 'Asset Turnover', c1['ticker']: c1['metrics']['efficiency']['assetTurnover'], c2['ticker']: c2['metrics']['efficiency']['assetTurnover']},
                {'metric': 'Inventory Turnover', c1['ticker']: c1['metrics']['efficiency']['inventoryTurnover'], c2['ticker']: c2['metrics']['efficiency']['inventoryTurnover']},
                {'metric': 'Receivables Turnover', c1['ticker']: c1['metrics']['efficiency']['receivablesTurnover'], c2['ticker']: c2['metrics']['efficiency']['receivablesTurnover']},
            ],
            'growth': [
                {'metric': 'Revenue Growth (%)', c1['ticker']: c1['metrics']['growth']['revenueGrowth'], c2['ticker']: c2['metrics']['growth']['revenueGrowth']},
                {'metric': 'Profit Growth (%)', c1['ticker']: c1['metrics']['growth']['profitGrowth'], c2['ticker']: c2['metrics']['growth']['profitGrowth']},
                {'metric': 'CAGR (%)', c1['ticker']: c1['metrics']['growth']['cagr'], c2['ticker']: c2['metrics']['growth']['cagr']},
            ],
        },
        'prediction': {
            c1['ticker']: {
                'predictedGrowth': c1_prediction,
                'confidence': c1['metrics']['growth']['prediction']['confidence'],
                'analysis': c1['metrics']['growth']['prediction']['analysis']
            },
            c2['ticker']: {
                'predictedGrowth': c2_prediction,
                'confidence': c2['metrics']['growth']['prediction']['confidence'],
                'analysis': c2['metrics']['growth']['prediction']['analysis']
            },
            'recommendation': f"Based on predictions, {future_profit_winner} has better profit growth prospects.",
            'disclaimer': "Note: Predictions are based on historical trends and do not guarantee future results."
        },
        'details': results
    }
    
    # Generate AI recommendation using Gemini
    try:
        from .gemini_service import generate_comparison_recommendation
        ai_recommendation = generate_comparison_recommendation(comparison)
        comparison['ai_recommendation'] = ai_recommendation
    except Exception as e:
        print(f"Gemini AI error: {e}")
        comparison['ai_recommendation'] = f"Unable to generate AI recommendation: {str(e)}"
    
    return comparison


async def async_compare_companies(ticker1: str, ticker2: str, quarter: str = 'Third_quarter') -> Dict:
    """
    Async wrapper for compare_companies to work with Django async views
    """
    return compare_companies(ticker1, ticker2, quarter)
