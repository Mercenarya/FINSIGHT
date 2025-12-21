from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .services import analysis as an
from .services import companies_search as cpn
from .services import ultimate as ulti
from .services import prediction as predict
from .services import comparison_service as cmp
from .services import prediction_ai_generate as gen
from django.template import loader
from django.views.decorators.csrf import csrf_exempt #skip csrf của react để tương tác API
from django.views.decorators.http import require_http_methods
from asgiref.sync import sync_to_async
import json
# import asyncio
import os
import sys

# Create your views here.
def clients(request):

    return render(request, 'index.html')


# tạo api của phân tích tài chính
@csrf_exempt # Rất quan trọng cho API
@require_http_methods(['GET','POST'])
async def analysis_api(request):
    try:
        
        # http://127.0.0.1:8001/api/analysis/?company=VIC&year=2025&period=4&metrics=cash_ratio,quick_ratio,current_ratio
        if request.method == 'GET':
            
            df_reports = await an.read_data(an.RAW)
            df_assets = await an.read_data(an.ASSETS)


            if df_reports is None or df_assets is None or isinstance(df_reports, str) or isinstance(df_assets,str):
                return JsonResponse(
                    {
                        'error':'Failed to read data files.',
                        'detail':f"{df_reports} {df_assets}"
                    },
                    status = 500
                )


            company = request.GET.get('company','')
            year = request.GET.get('year','')
            quarter = request.GET.get('period','')
            metrics = request.GET.get('metrics','')

        
            # kết quả phân tích (dict result chính cho đối số hiển thị và dữ liệu biểu đồ)
            analysis_result = {}

            # danh sách các quarter
            quarter = ['Quarter 1', 'Quarter 2', 'Quarter 3','Quarter 4']

            # đồng thời, lấy dữ liệu khi fetch về cho biểu đồ
            chart_data = []
            quarter_num = 1

            if quarter == 'Quarter 1':
                quarter_num = 1
            if quarter == 'Quarter 2':
                quarter_num = 2
            if quarter == 'Quarter 3':
                quarter_num = 3
            if quarter == 'Quarter 4':
                quarter_num = 4

            await ulti.run_procedure_ultimate(
                result=company,
                metrics=metrics,
                year=int(year),
                quarter=int(quarter_num),
                prev_quarter='Quarter 2',
                current_quarter='Quarter 4',
                major=0
            )



            # lấy dữ liệu theo 4 quý
            for q in quarter:
                
                quarter_data = {
                    'quarter':q
                }

                '''
                Hiển thị các mục nội dung tính toán
                đã được chọn và phân tích
                '''
                # profitability
                try:
                    prof = await an.extract_finance_profitability(
                        df=df_reports,
                        df2=df_assets,
                        quarter=q
                    )

                    if isinstance(prof, dict):
                        quarter_data.update(prof)

                except: pass
                
                # liquidity
                try:
                    liq = await an.extract_finance_liquidity(
                        df=df_assets,
                        quarter=q
                    )
                    if isinstance(liq, dict):
                        quarter_data.update(liq)

                except: pass

                chart_data.append(quarter_data)

            # thêm dữ liệu của chart vào dict result chính
            analysis_result['chart_data'] = chart_data
            
            # thực hiện phân tích các quarter được chọn
            

            pft = await an.extract_finance_profitability(
                df=df_reports,
                df2=df_assets,
                quarter=quarter
            )
            if isinstance(pft, dict):
                analysis_result['profitability'] = pft

            lq = await an.extract_finance_liquidity(
                df=df_assets,
                quarter=quarter,

            )

            if isinstance(lq, dict):
                analysis_result['liquidity'] = lq

            analysis_result['request_info'] = {
                'company': company,
                'year':year,
                'quarter':quarter,
                'metrics':metrics
            }

            if not company or not year or not quarter or not metrics:
                return JsonResponse(
                    {
                        "error":'Missing parameters: result, metrics , quarter or timeline'
                    },
                    status=400
                )
            
            if isinstance(analysis_result, str):
                analysis_result = json.loads(analysis_result)
            
            return JsonResponse(analysis_result,safe=False)

        if request.method == 'POST':
            try:
                pass
            except Exception as error:
                return JsonResponse(
                    {
                        'Analysis error':"An unexpected error occured during analysis",
                        'Detail':f"{error}"
                    },
                    status = 500
                )

        # return redirect("http://127.0.0.1:8080/user/analysis")
    except Exception as error:
        return JsonResponse(
            {
                'Analysis error':"An unexpected error occured during analysis",
                'Detail':f"{error}"
            },
            status = 500
        )
    except ImportError as errorstatus:
        return JsonResponse(
            {
                'Import Error':'Modules not found',
                'Detail':f"{errorstatus}"
            },
            status = 500
        )





# tìm kiếm doanh nghiệp, công ti
@csrf_exempt # Rất quan trọng cho API
@require_http_methods(['GET'])
async def companies_search(request):
    try:
        query = request.GET.get('company')
        if not query:
            # nếu không có query nào thì trả về kết quả rỗng
            return JsonResponse([],safe=False)

        suggestions = await cpn.search_result(query)
        if isinstance(suggestions,str):
            result = json.loads(suggestions)
        else:
            result = suggestions

        return JsonResponse(result, safe=False)

    except Exception as error:
        return JsonResponse(
            {
                'error':'An unexpected error occured during loading result',
                'Detail':f'{error}'
            },
            status = 500
        )


# dự đoán các giá trị doanh nghiệp

# dự đoán các giá trị doanh nghiệp

@csrf_exempt
@require_http_methods(['GET'])
async def prediction_api(request):
    try:

        company = request.GET.get('company', '')
        year = request.GET.get('year', '')
        quarter = request.GET.get('period', 'Quarter 4')
        metrics_str = request.GET.get('metrics', '')
        
        # Chuyển đổi period thành số (ví dụ: 'Quarter 4' -> 4)
        quarter_num = int(quarter) if quarter.isdigit() else 4

        # Chạy Procedure để chuẩn bị dữ liệu Q1 -> Q4
        await ulti.run_procedure_ultimate(
            result=company,
            metrics=metrics_str,
            year=int(year),
            quarter=quarter_num,
            prev_quarter='Quarter 2',
            current_quarter='Quarter 4',
            major=0
        )

        # Lấy dữ liệu thực tế (Historical Data)
        df_assets = await an.read_data(an.ASSETS)
        
        chart_data = []
        
        # Build mảng dữ liệu lịch sử - gọi extract_finance_liquidity cho TỪNG quarter
        for q in ['Quarter 1', 'Quarter 2', 'Quarter 3', 'Quarter 4']:
            try:
                q_values = await an.extract_finance_liquidity(df=df_assets, quarter=q)
                if isinstance(q_values, dict) and q_values:
                    chart_data.append({
                        "quarter": q,
                        "cash_ratio": round(float(q_values.get("cash ratio", 0)),2),
                        "quick_ratio": round(float(q_values.get("quick ratio", 0)),2),
                        "current_ratio": round(float(q_values.get("current ratio", 0)),2),
                        "isForecast": False
                    })
                else:
                    # Fallback nếu không có dữ liệu
                    chart_data.append({
                        "quarter": q,
                        "cash_ratio": 0,
                        "quick_ratio": 0,
                        "current_ratio": 0,
                        "isForecast": False
                    })
            except Exception as e:
                print(f"Error extracting liquidity for {q}: {e}")
                chart_data.append({
                    "quarter": q,
                    "cash_ratio": 0,
                    "quick_ratio": 0,
                    "current_ratio": 0,
                    "isForecast": False
                })

        #Lấy dữ liệu dự báo cho Q5 (Prediction)
        liquidity_predict = await predict.total_prediction(quarter=f"Quarter {quarter_num}")

        if isinstance(liquidity_predict, dict):
            # total_prediction trả về: {"prediction": [{"cash_ratio": ...}, {"current_ratio": ..., "quick_ratio": ...}]}
            predictions = liquidity_predict.get("prediction", [])
            
            # Lấy giá trị từ mảng predictions
            cash_ratio_val = 0
            quick_ratio_val = 0
            current_ratio_val = 0
            
            if len(predictions) >= 1 and isinstance(predictions[0], dict):
                cash_ratio_val = predictions[0].get("cash_ratio", 0)
            
            if len(predictions) >= 2 and isinstance(predictions[1], dict):
                quick_ratio_val = predictions[1].get("quick_ratio", 0)
                current_ratio_val = predictions[1].get("current_ratio", 0)
            
            chart_data.append({
                "quarter": "Quarter 5",
                "cash_ratio": round(float(cash_ratio_val),2),
                "quick_ratio": round(float(quick_ratio_val),2),
                "current_ratio": round(float(current_ratio_val),2),
                "isForecast": True
            })

            
        # kết quả đánh giá và nhận xét từ AI
        generative = gen.AgentGenerative(
            float(predictions[0].get("cash_ratio", 0)), 
            float(predictions[1].get("quick_ratio", 0)),
            float(predictions[1].get("current_ratio", 0))
        )

        predict_data = generative._result()
        gen_text = await gen.genereative(predict_data,chart_data)
        print(chart_data)
        print(gen_text)
        # Trả về cho Frontend
        return JsonResponse({
            "chart_data": chart_data,
            "ai_insight": f"{gen_text}"
        }, safe=False)

    except Exception as error:
        return JsonResponse({'error': str(error)}, status=500)



# @csrf_exempt
# @require_http_methods(['GET'])
# async def prediction_api(request):
#     try:
#         if request.method == 'GET':
            
#             # lấy dữ liệu được cập nhật về 
#             df_reports = await an.read_data(an.RAW)
#             df_assets = await an.read_data(an.ASSETS)

#             # kiểm tra và xác nhận dữ liệu được lấy về
#             if df_reports is None or df_assets is None or isinstance(df_reports, str) or isinstance(df_assets,str):
#                 return JsonResponse(
#                     {
#                         'error':'Failed to read data files.',
#                         'detail':f"{df_reports} {df_assets}"
#                     },
#                     status = 500
#                 )


#             company = request.GET.get('company','')
#             year = request.GET.get('year','')
#             quarter = request.GET.get('period','')
#             metrics = request.GET.get('metrics','')

#             df_reports = await an.read_data(an.RAW)
#             df_assets = await an.read_data(an.ASSETS)

#             if df_reports is None or df_assets is None or isinstance(df_reports, str) or isinstance(df_assets,str):
#                 return JsonResponse(
#                     {
#                         'error':'Failed to read data files.',
#                         'detail':f"{df_reports} {df_assets}"
#                     },
#                     status = 500
#                 )
            
#             # kết quả phân tích 
#             predict_analysis = {}
#             predict_target = {}

#             # danh sách các quarters để lấy giá trị hiện tại và dự báo
#             quarters = ['Quarter 1','Quarter 2','Quarter 3','Quarter 4','Quarter 5']

#             # previous quarter

#             prev_quarter = [x for x in range(len(quarters)-1)]

#             # dữ liệu biểu đồ cột
#             chart_data = []

#             quarter_num = 1

#             if quarter == 'Quarter 1':
#                 quarter_num = 1
#             if quarter == 'Quarter 2':
#                 quarter_num = 2
#             if quarter == 'Quarter 3':
#                 quarter_num = 3
#             if quarter == 'Quarter 4':
#                 quarter_num = 4
            

#             await ulti.run_procedure_ultimate(
#                 result=company,
#                 metrics=metrics,
#                 year=int(year),
#                 quarter=int(quarter_num),
#                 prev_quarter='Quarter 2',
#                 current_quarter='Quarter 4',
#                 major=0
#             )

#             # lấy dữ liệu cho
#             for q in prev_quarter:
#                 quarters_data = {
#                     'quarter': q
#                 }

#                 try:
#                     lq = await predict.total_prediction(quarter='Quarter 4')
#                     # Nếu như dữ liệu được trả về là dictionary
#                     if isinstance(lq,dict):
#                         quarters_data.update(
#                             {
#                                 'Quarter 5':lq
#                             }
#                         )


#                 except: pass
#                 chart_data.append(quarters_data)

#             predict_analysis['chart_data'] = chart_data
            
#             # Liquidity cho quarter được chọn
#             liquidity_results = await an.extract_finance_liquidity(
#                 df=df_assets,
#                 quarter=prev_quarter,
                
#             )
#             liquidity_predict = await predict.total_prediction(quarter=quarter)
#             if isinstance(liquidity_predict, dict):
#                 chart_data.append({
#                     "quarter": "Q5 (Predict)",
#                     "cash_ratio": liquidity_predict.get("cash ratio", 0),
#                     "quick_ratio": liquidity_predict.get("quick ratio", 0),
#                     "current_ratio": liquidity_predict.get("current ratio", 0),
#                     "isForecast": True 
#                 })

#             if isinstance(liquidity_results, dict):
#                 predict_analysis['liquidity'] = liquidity_results
            

#             # Thêm thông tin request vào response
#             predict_analysis['request_info'] = {
#                 'company': company,
#                 'year': year,
#                 'quarter': quarter,
#                 'metrics': metrics
#             }

#             # quý được dự báo
#             predict_target['request_info'] = {
#                 'company': company,
#                 'year': year,
#                 'quarter': quarter,
#                 'metrics': metrics,
#                 'prediction':liquidity_predict
#             }
#             response_data = {
#                 'chart_data':chart_data
#             }

#             return JsonResponse(response_data, safe=False)
#     except Exception as error:
#         return JsonResponse(
#            {
#                 'error':'An unexpected error occured during prediction',
#                 'Detail':f'{error}'
#            },
#            status = 500
#         )
    
# So sánh hai công ty
@csrf_exempt
@require_http_methods(['POST', 'GET'])
async def compare_companies_api(request):
    """
    API endpoint to compare two companies
    
    POST Request Body (JSON):
    {
        "ticker1": "VIC",
        "ticker2": "VNM",
        "quarter": "Third_quarter"  // Optional, defaults to Third_quarter
    }
    
    GET Request Parameters:
    ?ticker1=VIC&ticker2=VNM&quarter=Third_quarter
    
    Response:
    {
        "meta": {
            "quarter": "Third_quarter",
            "company1": "VIC",
            "company2": "VNM"
        },
        "analysis": {
            "profitability_winner": "VIC",
            "liquidity_winner": "VNM",
            "efficiency_winner": "VIC"
        },
        "details": [...]
    }
    """
    try:
        # Handle both POST and GET requests
        if request.method == 'POST':
            try:
                body = json.loads(request.body.decode('utf-8'))
                ticker1 = body.get('ticker1', '')
                ticker2 = body.get('ticker2', '')
                quarter = body.get('quarter', 'Third_quarter')
            except json.JSONDecodeError:
                return JsonResponse(
                    {
                        'error': 'Invalid JSON format',
                        'detail': 'Request body must be valid JSON'
                    },
                    status=400
                )
        else:  # GET request
            ticker1 = request.GET.get('ticker1', '')
            ticker2 = request.GET.get('ticker2', '')
            quarter = request.GET.get('quarter', 'Third_quarter')
        
        # Validate parameters
        if not ticker1 or not ticker2:
            return JsonResponse(
                {
                    'error': 'Missing required parameters',
                    'detail': 'Both ticker1 and ticker2 are required',
                    'example': {
                        'ticker1': 'VIC',
                        'ticker2': 'VNM',
                        'quarter': 'Third_quarter'
                    }
                },
                status=400
            )
        
        # Call comparison service
        comparison_result = await cmp.async_compare_companies(
            ticker1=ticker1.upper(),
            ticker2=ticker2.upper(),
            quarter=quarter
        )
        
        # Check for errors in result
        if 'error' in comparison_result:
            return JsonResponse(
                comparison_result,
                status=404
            )
        
        return JsonResponse(comparison_result, safe=False)
    
    except Exception as error:
        return JsonResponse(
            {
                'error': 'An unexpected error occurred during comparison',
                'detail': str(error)
            },
            status=500
        )


@csrf_exempt
@require_http_methods(['GET'])
async def companies_list_api(request):
    """
    API endpoint to fetch all available company tickers from MongoDB
    
    GET /api/v1/companies/
    
    Returns:
        JSON response with list of company tickers
    """
    try:
        from pymongo import MongoClient
        import os
        
        MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
        MONGO_DB = os.getenv('MONGO_DB', 'dataset')
        MONGO_COLLECTION = os.getenv('MONGO_COLLECTION', 'companies')
        
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB]
        collection = db[MONGO_COLLECTION]
        
        # Get all unique tickers
        tickers = collection.distinct('ticker')
        client.close()
        
        # Filter search query if provided
        search = request.GET.get('search', '').upper()
        if search:
            tickers = [t for t in tickers if search in t.upper()]
        
        return JsonResponse({
            'companies': sorted(tickers),
            'count': len(tickers)
        })
    
    except Exception as error:
        return JsonResponse(
            {
                'error': 'Failed to fetch companies list',
                'detail': str(error)
            },
            status=500
        )


@csrf_exempt
@require_http_methods(['GET'])
async def dashboard_data_api(request):
    """
    API endpoint to fetch dashboard data with company metrics
    
    GET /api/v1/dashboard/
    
    Returns:
        JSON response with company metrics for dashboard table
    """
    try:
        from pymongo import MongoClient
        import os
        
        MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
        MONGO_DB = os.getenv('MONGO_DB', 'dataset')
        MONGO_COLLECTION = os.getenv('MONGO_COLLECTION', 'companies')
        
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB]
        collection = db[MONGO_COLLECTION]
        
        # Get quarter parameter (default to Third_quarter)
        quarter = request.GET.get('quarter', 'Third_quarter')
        
        # Fetch all companies
        companies = list(collection.find())
        client.close()
        
        # Process each company data
        dashboard_data = []
        
        for company in companies:
            ticker = company.get('ticker', 'Unknown')
            reports = company.get('reports', [])
            assets = company.get('assets', [])
            
            # Helper function to get value from data array
            def get_value(data_array, keyword, quarter_key):
                import math
                if not data_array:
                    return 0
                for item in data_array:
                    if 'title' in item and keyword.lower() in item['title'].lower():
                        val = item.get(quarter_key, 0)
                        if val is None or val == '':
                            return 0
                        if isinstance(val, str):
                            try:
                                return float(val.replace(',', '').strip()) if val.strip() else 0
                            except:
                                return 0
                        try:
                            result = float(val)
                            return 0 if math.isnan(result) else result
                        except:
                            return 0
                return 0
            
            # Extract metrics
            revenue = get_value(reports, "1. Doanh thu bán hàng", quarter)
            net_profit = get_value(reports, "18. Lợi nhuận sau thuế", quarter)
            total_assets = get_value(assets, "TỔNG CỘNG TÀI SẢN", quarter)
            equity = get_value(assets, "D. VỐN CHỦ SỞ HỮU", quarter)
            total_liabilities = get_value(assets, "C- NỢ PHẢI TRẢ", quarter)
            
            # Calculate ratios with NaN protection
            import math
            roi = round((net_profit / total_assets * 100), 2) if total_assets > 0 else 0
            debt_ratio = round((total_liabilities / total_assets), 2) if total_assets > 0 else 0
            growth = round((net_profit / revenue * 100), 2) if revenue > 0 else 0
            
            # Ensure no NaN values
            roi = 0 if math.isnan(roi) else roi
            debt_ratio = 0 if math.isnan(debt_ratio) else debt_ratio
            growth = 0 if math.isnan(growth) else growth
            
            # Format large numbers
            def format_number(num):
                import math
                if num is None or (isinstance(num, float) and math.isnan(num)):
                    return "0"
                if num >= 1000000000:
                    return f"{num/1000000000:.1f}B"
                elif num >= 1000000:
                    return f"{num/1000000:.0f}M"
                elif num >= 1000:
                    return f"{num/1000:.0f}K"
                return str(int(num)) if num >= 0 else "0"
            
            dashboard_data.append({
                'company': ticker,
                'industry': 'Finance',  # Default - can be extended with industry data
                'revenue': format_number(revenue),
                'netProfit': format_number(net_profit),
                'roi': f"{roi}%",
                'debtRatio': debt_ratio,
                'growth': growth
            })
        
        # Sort by revenue (highest first)
        dashboard_data.sort(key=lambda x: float(x['revenue'].replace('B', '000').replace('M', '').replace('K', '')) if x['revenue'] else 0, reverse=True)
        
        return JsonResponse({
            'data': dashboard_data[:10],  # Return top 10
            'quarter': quarter,
            'count': len(dashboard_data)
        })
    
    except Exception as error:
        return JsonResponse(
            {
                'error': 'Failed to fetch dashboard data',
                'detail': str(error)
            },
            status=500
        )