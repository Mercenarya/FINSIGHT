import os
import time
import google.generativeai as genai  # Use old SDK - tested working
# import google.genai as genai
from typing import Dict, Any

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyAtRP8pwpPoKDptESlwjVXreCw9dY9b1kU')


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
        growth_winner = analysis.get('growth_winner', '')
        
        # Count wins - only 2 categories: profitability and growth
        winners = [profitability_winner, growth_winner]
        company1 = meta.get('company1', '')
        company2 = meta.get('company2', '')
        
        c1_wins = winners.count(company1)
        c2_wins = winners.count(company2)
        
        if c1_wins > c2_wins:
            recommended = company1
            reason = f"wins in {c1_wins} out of 2 categories"
        elif c2_wins > c1_wins:
            recommended = company2
            reason = f"wins in {c2_wins} out of 2 categories"
        else:
            recommended = profitability_winner
            reason = "has better profitability (tie-breaker)"
        
        return f"""**Investment Recommendation (Auto-generated)**

Based on the financial analysis:
- Best Profitability: {profitability_winner}
- Best Growth: {growth_winner}

Recommendation: Consider investing in {recommended} as it {reason}.

*Note: This is an auto-generated recommendation. AI analysis is temporarily unavailable due to rate limits. Please try again later for detailed AI insights.*"""
        
    except Exception as e:
        return f"Unable to generate recommendation: {str(e)}"


async def async_generate_recommendation(comparison_data: Dict[str, Any]) -> str:
    """Async wrapper for generate_comparison_recommendation"""
    return generate_comparison_recommendation(comparison_data)


def generate_analysis_insight(analysis_data: Dict[str, Any], company: str = '') -> str:
    """
    Generate AI-powered insight for single company analysis
    
    Args:
        analysis_data: Dictionary containing analysis results (profitability, liquidity, chart_data)
        company: Company name/ticker
        
    Returns:
        AI-generated insight string about the company's financial health
    """
    try:
        configure_gemini()
        
        # Extract key metrics
        profitability = analysis_data.get('profitability', {})
        liquidity = analysis_data.get('liquidity', {})
        chart_data = analysis_data.get('chart_data', [])
        
        # Build metrics summary
        metrics_summary = f"""
        Công ty: {company}
        
        Chỉ số lợi nhuận (Profitability):
        - Biên lợi nhuận gộp (Gross Margin): {profitability.get('Gross marrgin', 'N/A')}%
        - Biên lợi nhuận hoạt động (Operating Profit Margin): {profitability.get('Operating profit margin', 'N/A')}%
        - Tỷ suất sinh lời trên tài sản (ROA): {profitability.get('ROA Ratio value', 'N/A')}
        - Tỷ suất sinh lời trên vốn chủ sở hữu (ROE): {profitability.get('ROE Profit', 'N/A')}
        
        Chỉ số thanh khoản (Liquidity):
        - Tỷ số tiền mặt (Cash Ratio): {liquidity.get('cash ratio', 'N/A')}
        - Tỷ số thanh toán nhanh (Quick Ratio): {liquidity.get('quick ratio', 'N/A')}
        - Tỷ số thanh toán hiện hành (Current Ratio): {liquidity.get('current ratio', 'N/A')}
        """
        
        # Add quarterly trend if available
        if chart_data and len(chart_data) > 0:
            metrics_summary += "\n        Dữ liệu theo quý:\n"
            for q_data in chart_data[-4:]:  # Last 4 quarters
                quarter = q_data.get('quarter', q_data.get('Quarter', ''))
                cash_r = q_data.get('cash ratio', q_data.get('cash_ratio', 'N/A'))
                quick_r = q_data.get('quick ratio', q_data.get('quick_ratio', 'N/A'))
                current_r = q_data.get('current ratio', q_data.get('current_ratio', 'N/A'))
                metrics_summary += f"        - {quarter}: Cash={cash_r}, Quick={quick_r}, Current={current_r}\n"
        
        # Create prompt
        prompt = f"""
        Bạn là chuyên gia phân tích tài chính. Phân tích dữ liệu tài chính của công ty dưới đây
        và đưa ra nhận xét về tình hình tài chính.
        
        {metrics_summary}
        
        Yêu cầu:
        1. Đánh giá khả năng sinh lời của công ty
        2. Đánh giá khả năng thanh khoản và ổn định tài chính
        3. Xác định các xu hướng đáng lo ngại hoặc tích cực
        4. Đưa ra khuyến nghị ngắn gọn
        5. Trả lời tối đa 150 từ
        6. Sử dụng ngôn ngữ đơn giản, dễ hiểu cho nhà đầu tư
        7. Trả lời bằng tiếng Việt
        """
        
        # Call Gemini API with retry logic for quota limits
        max_retries = 2
        for attempt in range(max_retries):
            try:
                print(f"[Gemini] Attempt {attempt + 1}/{max_retries} for {company}")
                model = genai.GenerativeModel('gemini-2.0-flash')
                response = model.generate_content(prompt)
                print(f"[Gemini] SUCCESS for {company}")
                return response.text
            except Exception as api_error:
                error_str = str(api_error)
                print(f"[Gemini] API error on attempt {attempt + 1}: {error_str}")
                if 'quota' in error_str.lower() or 'rate' in error_str.lower() or 'retry' in error_str.lower():
                    if attempt < max_retries - 1:
                        print(f"[Gemini] Quota limit hit, waiting 45 seconds before retry...")
                        time.sleep(45)
                    else:
                        raise
                else:
                    raise
        
    except Exception as e:
        print(f"[Gemini] Analysis API error: {e}")
        # Return fallback insight
        return generate_fallback_analysis_insight(analysis_data, company)


def generate_fallback_analysis_insight(analysis_data: Dict[str, Any], company: str = '') -> str:
    """
    Generate a basic insight when Gemini API is not available
    """
    try:
        profitability = analysis_data.get('profitability', {})
        liquidity = analysis_data.get('liquidity', {})
        
        gross_margin = profitability.get('Gross marrgin', 0)
        roa = profitability.get('ROA Ratio value', 0)
        current_ratio = liquidity.get('current ratio', 0)
        
        insights = []
        
        # Analyze profitability
        if isinstance(gross_margin, (int, float)):
            if gross_margin > 30:
                insights.append(f"Biên lợi nhuận gộp {gross_margin:.1f}% cho thấy khả năng sinh lời tốt")
            elif gross_margin > 15:
                insights.append(f"Biên lợi nhuận gộp {gross_margin:.1f}% ở mức trung bình")
            else:
                insights.append(f"Biên lợi nhuận gộp {gross_margin:.1f}% cần được cải thiện")
        
        # Analyze liquidity
        if isinstance(current_ratio, (int, float)):
            if current_ratio > 2:
                insights.append("Chỉ số thanh khoản tốt, công ty có khả năng thanh toán nợ ngắn hạn")
            elif current_ratio > 1:
                insights.append("Khả năng thanh khoản ổn định")
            else:
                insights.append("Cần chú ý đến khả năng thanh khoản")
        
        if insights:
            return f"**Phân tích tài chính {company}:**\n\n" + "\n".join([f"• {i}" for i in insights]) + "\n\n*Lưu ý: Đây là phân tích tự động. Vui lòng thử lại sau để có nhận xét AI chi tiết hơn.*"
        else:
            return "Không đủ dữ liệu để phân tích. Vui lòng chọn các chỉ số và chạy phân tích."
            
    except Exception as e:
        return f"Không thể tạo nhận xét: {str(e)}"

