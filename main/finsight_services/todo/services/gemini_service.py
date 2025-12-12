"""
Gemini AI Service for Financial Analysis Recommendations
Uses Google Gemini API to generate investment recommendations
"""
import os
import time
import google.generativeai as genai
from typing import Dict, Any

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')


def configure_gemini():
    """Configure Gemini API with the API key"""
    api_key = GEMINI_API_KEY or os.getenv('GEMINI_API_KEY', '')
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    genai.configure(api_key=api_key)


def generate_comparison_recommendation(comparison_data: Dict[str, Any]) -> str:
    """
    Generate AI-powered investment recommendation based on comparison data
    
    Args:
        comparison_data: Dictionary containing comparison results from compare_companies
        
    Returns:
        Investment recommendation string
    """
    try:
        configure_gemini()
        
        # Extract key metrics for the prompt
        meta = comparison_data.get('meta', {})
        company1 = meta.get('company1', 'Company 1')
        company2 = meta.get('company2', 'Company 2')
        
        analysis = comparison_data.get('analysis', {})
        details = comparison_data.get('details', [])
        
        # Build metrics summary
        metrics_summary = ""
        for company_data in details:
            ticker = company_data.get('ticker', '')
            metrics = company_data.get('metrics', {})
            
            prof = metrics.get('profitability', {})
            liq = metrics.get('liquidity', {})
            eff = metrics.get('efficiency', {})
            growth = metrics.get('growth', {})
            
            metrics_summary += f"""
            {ticker}:
            - Gross Margin: {prof.get('grossMargin', 0)}%
            - Net Margin: {prof.get('netMargin', 0)}%
            - ROA: {prof.get('roa', 0)}%
            - ROE: {prof.get('roe', 0)}%
            - Current Ratio: {liq.get('currentRatio', 0)}
            - Quick Ratio: {liq.get('quickRatio', 0)}
            - Asset Turnover: {eff.get('assetTurnover', 0)}
            - Revenue Growth: {growth.get('revenueGrowth', 0)}%
            - Profit Growth: {growth.get('profitGrowth', 0)}%
            """
        
        # Create prompt
        prompt = f"""
        You are a financial analyst expert. Analyze and compare the 2 companies below, 
        then provide an investment recommendation.
        
        Comparison Data:
        {metrics_summary}
        
        Analysis Results:
        - Company with better profitability: {analysis.get('profitability_winner', '')}
        - Company with better liquidity: {analysis.get('liquidity_winner', '')}
        - Company with better efficiency: {analysis.get('efficiency_winner', '')}
        - Company with better growth: {analysis.get('growth_winner', '')}
        
        Requirements:
        1. Analyze strengths/weaknesses of each company
        2. Compare investment risks
        3. Provide recommendation: Which company to invest in and why
        4. Keep response concise, maximum 200 words
        """
        
        # Call Gemini API - no retry, return fallback on any error
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        print(f"Gemini API error: {e}")
        # Return fallback recommendation immediately
        return generate_fallback_recommendation(comparison_data)


def generate_fallback_recommendation(comparison_data: Dict[str, Any]) -> str:
    """
    Generate a basic recommendation when Gemini API is not available
    """
    try:
        analysis = comparison_data.get('analysis', {})
        meta = comparison_data.get('meta', {})
        
        profitability_winner = analysis.get('profitability_winner', '')
        liquidity_winner = analysis.get('liquidity_winner', '')
        efficiency_winner = analysis.get('efficiency_winner', '')
        growth_winner = analysis.get('growth_winner', '')
        
        # Count wins
        winners = [profitability_winner, liquidity_winner, efficiency_winner, growth_winner]
        company1 = meta.get('company1', '')
        company2 = meta.get('company2', '')
        
        c1_wins = winners.count(company1)
        c2_wins = winners.count(company2)
        
        if c1_wins > c2_wins:
            recommended = company1
            reason = f"wins in {c1_wins} out of 4 categories"
        elif c2_wins > c1_wins:
            recommended = company2
            reason = f"wins in {c2_wins} out of 4 categories"
        else:
            recommended = profitability_winner
            reason = "has better profitability (tie-breaker)"
        
        return f"""**Investment Recommendation (Auto-generated)**

Based on the financial analysis:
- **Profitability Winner**: {profitability_winner}
- **Liquidity Winner**: {liquidity_winner}
- **Efficiency Winner**: {efficiency_winner}
- **Growth Winner**: {growth_winner}

**Recommendation**: Consider investing in **{recommended}** as it {reason}.

*Note: This is an auto-generated recommendation. AI analysis is temporarily unavailable due to rate limits. Please try again later for detailed AI insights.*"""
        
    except Exception as e:
        return f"Unable to generate recommendation: {str(e)}"


async def async_generate_recommendation(comparison_data: Dict[str, Any]) -> str:
    """Async wrapper for generate_comparison_recommendation"""
    return generate_comparison_recommendation(comparison_data)
