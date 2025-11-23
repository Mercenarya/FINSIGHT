from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from . import analysis as an
# from analysis import normalization,read_data,extract_finance_profitability
import json


# Create your views here.
def clients(request):

    return render(request, 'index.html')


def analysis(request):
    try:
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