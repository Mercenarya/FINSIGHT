from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .services import analysis as an
from .services import companies_search as cpn
from .services import ultimate as ulti
from .services import prediction as predict
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