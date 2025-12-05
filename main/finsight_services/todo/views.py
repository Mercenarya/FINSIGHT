from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .services import analysis as an
from .services import companies_search as cpn
from .services import ultimate as ulti
from django.template import loader
from django.views.decorators.csrf import csrf_exempt #skip csrf của react để tương tác API
from django.views.decorators.http import require_http_methods
import json
import asyncio
import os
import sys

# Create your views here.
def clients(request):

    return render(request, 'index.html')


# tạo api của phân tích tài chính
@require_http_methods(['GET'])
async def analysis_api(request):
    try:
        

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
            # thực hiện phân tích tính toán 
            query = request.GET.get('query','')
            year = 2025
            quarter = 4
            if not query:
                return JsonResponse(
                    [],safe=False
                )
            result = await ulti.run_procedure_ultimate(query,year=year,quarter=quarter)
            
            # kiểm tra kết quả và điều kiện đầu ra:
            if isinstance(result, str):
                result = json.loads(result)
            
            return JsonResponse(result,safe=False)

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