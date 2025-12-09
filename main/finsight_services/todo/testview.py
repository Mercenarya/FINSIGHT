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
        if request.method == 'GET':
            # Lấy các tham số từ query string
            company = request.GET.get('company', '')
            year = request.GET.get('year', '')
            quarter = request.GET.get('quarter', 'Quarter 1')  # Mặc định Quarter 1
            metrics_str = request.GET.get('metrics', '')
            metrics = metrics_str.split(',') if metrics_str else []
            
            print(f"Received analysis request: company={company}, year={year}, quarter={quarter}, metrics={metrics}")
            
            # Đọc dữ liệu
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

        
            # Kết quả phân tích
            analysis_results = {}
            
            # Danh sách các quarters
            quarters = ['Quarter 1', 'Quarter 2', 'Quarter 3', 'Quarter 4']
            
            # Lấy dữ liệu cho tất cả 4 quarters để vẽ chart
            chart_data = []
            for q in quarters:
                quarter_data = {'quarter': q}
                
                # Profitability cho quarter này
                try:
                    prof = await an.extract_finance_profitability(
                        df=df_reports, 
                        df2=df_assets, 
                        quarter=q
                    )
                    if isinstance(prof, dict):
                        quarter_data.update(prof)
                except:
                    pass
                
                # Liquidity cho quarter này
                try:
                    liq = await an.extract_finance_liquidity(
                        df=df_assets,
                        quarter=q
                    )
                    if isinstance(liq, dict):
                        quarter_data.update(liq)
                except:
                    pass
                    
                chart_data.append(quarter_data)
            
            analysis_results['chart_data'] = chart_data
            
            # Thực hiện phân tích cho quarter được chọn (để hiển thị chi tiết)
            profitability_results = await an.extract_finance_profitability(
                df=df_reports, 
                df2=df_assets, 
                quarter=quarter
            )
            if isinstance(profitability_results, dict):
                analysis_results['profitability'] = profitability_results
            
            # Liquidity cho quarter được chọn
            liquidity_results = await an.extract_finance_liquidity(
                df=df_assets,
                quarter=quarter
            )
            if isinstance(liquidity_results, dict):
                analysis_results['liquidity'] = liquidity_results
            
            # Thêm thông tin request vào response
            analysis_results['request_info'] = {
                'company': company,
                'year': year,
                'quarter': quarter,
                'metrics': metrics
            }
            
            return JsonResponse(analysis_results)
        
        # Không hỗ trợ các method khác
        return JsonResponse(
            {'error': 'Method not allowed. Use GET.'},
            status=405
        )
        
    except ImportError as errorstatus:
        return JsonResponse(
            {
                'Import Error':'Modules not found',
                'Detail':f"{errorstatus}"
            },
            status = 500
        )
    except Exception as error:
        import traceback
        traceback.print_exc()
        return JsonResponse(
            {
                'Analysis error':"An unexpected error occured during analysis",
                'Detail':f"{error}"
            },
            status = 500
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