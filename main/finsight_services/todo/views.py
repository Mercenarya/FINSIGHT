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
def analysis_api(request):
    try:
        if request.method == 'POST':
            
            df_reports = an.read_data(an.RAW)
            df_assets = an.read_data(an.ASSETS)
   
            if df_reports is None or df_assets is None or isinstance(df_reports, str) or isinstance(df_assets,str):
                return JsonResponse(
                    {
                        'error':'Failed to read data files.',
                        'detail':f"{df_reports} {df_assets}"
                    },
                    status = 500
                )
            # thực hiện phân tích tính toán (Profitability)
            profitability_results = an.extract_finance_profitability(df=df_reports,df2=df_assets)
            # mẫu sử dụng ( lợi nhuận từ kinh doanh )

            single_growth = an.extract_finance_growth()
            

            analysis_data = json.loads(profitability_results)
            return JsonResponse(analysis_data)

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
@require_http_methods(['GET'])
def companies_search(request):
    try:
        query = request.GET.get('query','')
        if not query:
            # nếu không có query nào thì trả về kết quả rỗng
            return JsonResponse([],safe=False)
        
        suggestions = cpn.search_result(query)
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



