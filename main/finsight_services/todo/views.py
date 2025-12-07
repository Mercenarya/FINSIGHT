from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .services import analysis as an
from .services import companies_search as cpn
from .services import ultimate as ulti
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
        

        if request.method == 'GET':
            
            df_reports = await sync_to_async(an.read_data)(an.RAW)
            df_assets = await sync_to_async(an.read_data)(an.ASSETS)


            if df_reports is None or df_assets is None or isinstance(df_reports, str) or isinstance(df_assets,str):
                return JsonResponse(
                    {
                        'error':'Failed to read data files.',
                        'detail':f"{df_reports} {df_assets}"
                    },
                    status = 500
                )
            # thực hiện phân tích tính toán 
            # query = request.GET.get('query','')
            # year = 2025
            # quarter = 4
            # metrics = "Liquidity"

            analysis_selection = ['Liquidity','Profitability','Growth','Efficiency']
            # quarter_selection = ['Quarter 1', 'Quarter 2', 'Quarter 3', 'Quarter 4']

            query = request.GET.get('company')
            year = request.GET.get('year')
            quarter = request.GET.get('period')
            metrics = request.GET.get('metrics')




            if not query or not year or not quarter or not metrics:
                return JsonResponse(
                    {
                        "error":'Missing parameters: result, metrics , quarter or timeline'
                    },
                    status=400
                )
            
            try:
                quarter_value = int(quarter)
            except Exception as error:
                return JsonResponse(
                    {
                        'error':'quarter value must be a valid number'
                    }
                )
           
                
            result = await sync_to_async(ulti.run_procedure_ultimate)(query,metrics=metrics,year=year,quarter=quarter_value)
           
            # kiểm tra kết quả và điều kiện đầu ra:
            if isinstance(result, str):
                result = json.loads(result)
            
            return JsonResponse(result,safe=False)

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

        suggestions = await sync_to_async(cpn.search_result)(query)
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
            }
        )