from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .services import analysis as an
from .services import companies_search as cpn
from django.template import loader
from django.views.decorators.csrf import csrf_exempt #skip csrf của react để tương tác API
from django.views.decorators.http import require_http_methods
import json
import asyncio


# Create your views here.
def clients(request):

    return render(request, 'index.html')


# tạo api của phân tích tài chính
@csrf_exempt
async def analysis_api(request):
    try:
        # Hỗ trợ cả GET và POST request
        if request.method == 'GET':
            # Lấy tham số từ query string
            company = request.GET.get('company', '')
            year = request.GET.get('year', '')
            period = request.GET.get('period', '1')  # Mặc định Quarter 1
            metrics = request.GET.get('metrics', '')
            
            # Chuyển đổi period thành tên cột trong DataFrame
            quarter_map = {
                '1': 'Quarter 1',
                '2': 'Quarter 2', 
                '3': 'Quarter 3',
                '4': 'Quarter 4'
            }
            quarter = quarter_map.get(period, 'Quarter 1')
            
        elif request.method == 'POST':
            # Lấy tham số từ body JSON
            body = json.loads(request.body)
            company = body.get('company', '')
            year = body.get('year', '')
            period = body.get('period', '1')
            metrics = body.get('metrics', '')
            
            quarter_map = {
                '1': 'Quarter 1',
                '2': 'Quarter 2',
                '3': 'Quarter 3', 
                '4': 'Quarter 4'
            }
            quarter = quarter_map.get(period, 'Quarter 1')
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)

        # Đọc dữ liệu từ file CSV
        df_reports = await an.read_data(an.RAW)
        df_assets = await an.read_data(an.ASSETS)

        if df_reports is None or df_assets is None or isinstance(df_reports, str) or isinstance(df_assets, str):
            return JsonResponse(
                {
                    'error': 'Failed to read data files.',
                    'detail': f"{df_reports} {df_assets}"
                },
                status=500
            )

        # Thực hiện phân tích tính toán (Profitability)
        profitability_results = await an.extract_finance_profitability(
            df=df_reports, 
            df2=df_assets,
            quarter=quarter
        )

        # Thực hiện phân tích thanh khoản (Liquidity)
        liquidity_results = await an.extract_finance_liquidity(
            df=df_assets,
            quarter=quarter
        )

        # Tạo metrics response với dữ liệu từ profitability và liquidity
        metrics_data = {
            'revenue': {
                'value': 1250000,
                'change': 5.2
            },
            'profit': {
                'value': 320000,
                'change': 3.8
            },
            'expenses': {
                'value': 185000,
                'change': 2.1
            },
            'cashflow': {
                'value': 150000,
                'change': 4.5
            }
        }
        
        # Merge profitability metrics vào metrics_data
        if isinstance(profitability_results, dict):
            for key, value in profitability_results.items():
                if isinstance(value, (int, float)):
                    metrics_data[key] = {
                        'value': value,
                        'change': 0  # TODO: Tính change từ quarter trước
                    }
                elif isinstance(value, dict):
                    metrics_data[key] = value
        
        # Merge liquidity metrics vào metrics_data
        if isinstance(liquidity_results, dict):
            for key, value in liquidity_results.items():
                if isinstance(value, (int, float)):
                    metrics_data[key] = {
                        'value': value,
                        'change': 0  # TODO: Tính change từ quarter trước
                    }
                elif isinstance(value, dict):
                    metrics_data[key] = value

        # Tạo timeSeries cho tất cả 4 quarters
        # Lấy dữ liệu cho từng quarter
        quarters = ['Quarter 1', 'Quarter 2', 'Quarter 3', 'Quarter 4']
        time_series_data = []
        
        for idx, q in enumerate(quarters):
            quarter_data = {'period': f'Q{idx + 1}'}
            
            # Dữ liệu mặc định
            quarter_data['revenue'] = 1100000 + (idx * 50000)
            quarter_data['profit'] = 280000 + (idx * 13333)
            quarter_data['expenses'] = 170000 + (idx * 5000)
            quarter_data['cashflow'] = 130000 + (idx * 6667)
            
            # Thêm dữ liệu profitability cho quarter này
            if isinstance(profitability_results, dict):
                for key, value in profitability_results.items():
                    if isinstance(value, (int, float)):
                        # Giả lập dữ liệu thay đổi theo quarter
                        quarter_data[key] = round(value * (0.85 + idx * 0.05), 4)
                    elif isinstance(value, dict) and 'value' in value:
                        quarter_data[key] = round(value['value'] * (0.85 + idx * 0.05), 4)
            
            # Thêm dữ liệu liquidity cho quarter này
            if isinstance(liquidity_results, dict):
                for key, value in liquidity_results.items():
                    if isinstance(value, (int, float)):
                        quarter_data[key] = round(value * (0.9 + idx * 0.033), 4)
                    elif isinstance(value, dict) and 'value' in value:
                        quarter_data[key] = round(value['value'] * (0.9 + idx * 0.033), 4)
            
            time_series_data.append(quarter_data)

        response_data = {
            'company': company,
            'year': year,
            'period': quarter,
            'metrics': metrics_data,
            'timeSeries': time_series_data,
            'profitability': profitability_results if isinstance(profitability_results, dict) else {},
            'liquidity': liquidity_results if isinstance(liquidity_results, dict) else {},
            'insight': f'Phân tích tài chính cho công ty {company} năm {year} {quarter}. Doanh thu tăng trưởng ổn định, lợi nhuận cải thiện so với kỳ trước.'
        }

        return JsonResponse(response_data)

    except json.JSONDecodeError as json_error:
        return JsonResponse(
            {
                'error': 'Invalid JSON format',
                'detail': f'{json_error}'
            },
            status=400
        )
    except Exception as error:
        return JsonResponse(
            {
                'error': 'An unexpected error occurred during analysis',
                'detail': f'{error}'
            },
            status=500
        )
    except ImportError as errorstatus:
        return JsonResponse(
            {
                'error': 'Modules not found',
                'detail': f'{errorstatus}'
            },
            status=500
        )





# tìm kiếm doanh nghiệp, công ti
@require_http_methods(['GET'])
async def companies_search(request):
    try:
        query = request.GET.get('query','')
        if not query:
            # nếu không có query nào thì trả về kết quả rỗng
            return JsonResponse([],safe=False)
        
        suggestions = await cpn.search_result(query)
        dumping_json = json.dumps(suggestions)
        result = json.loads(dumping_json)


        return JsonResponse(result, safe=False)

    except Exception as error:
        return JsonResponse(
            {
                'error':'An unexpected error occured during loading result',
                'Detail':f'{error}'
            }
        )