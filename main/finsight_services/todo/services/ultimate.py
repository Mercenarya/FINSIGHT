import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import asyncio
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common import keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from .companies_search import search_result
from .analysis import extract_finance_growth,extract_finance_liquidity,extract_finance_profitability
from .analysis import read_data,RAW,ASSETS

from .finance_execute import run_procedure_collect
import json





# cập nhật vào thư mục json đặc thù
async def updating_json_anylis(data,filename:str):
    try:
        with open(filename) as file:
            json.dump(
                data, file, 
                indent=4, ensure_ascii=False
            )
        print('Json updated')
    except Exception as dce:
        print("Error occured during updating json",dce)
        return {}
    


# đồng bộ quá trình lấy dữ liệu của 4 chuyên mục
async def get_analysis(df,df2,**kwargs):
    
    try:

        growth = await extract_finance_growth(
            df=df2,
            prev_quarter=kwargs['quarter_prev'],
            current_quarter=kwargs['quarter_current'],
            years=kwargs["years"],
            major=kwargs["major"]
        )
 
        profitability = await extract_finance_profitability(
            df=df,
            df2=df2,
            quarter=kwargs["quarter_selection"]
        )

        liquidity = await extract_finance_liquidity(
            df2,
            kwargs['quarter_selection']
        )
        
        return {
            "Growth":growth,
            "Profitability":profitability,
            "Liquidity":liquidity,
            # "Efficiency":efficiency
        }
        
    except Exception as error:
        print("An error occured during analytics ",error)
        return {}
    
# chạy đồng bộ tất cả các chức năng trên
async def run_procedure_ultimate(result,year,quarter):
    options = Options()
    service = Service(ChromeDriverManager().install())
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=service,options=options)
    # từ khóa - mã công ty 
    # result = "VIC"
    await search_result(result)
    print("Starting collect data ... ")
    # asyncio.sleep(3)
    await run_procedure_collect(result=result,driver=driver,year=year,quarter=quarter)
    print("Starting analytic ...")
    # asyncio.sleep(3)
    df = await read_data(RAW)
    df2 = await read_data(ASSETS)
    print(df)
    print(df2)

    template = {
        "quarter_selection":'Quarter 3',
        "quarter_prev":'Quarter 2',
        "quarter_current":'Quarter 3',
        "major":0,
        "years":year
    }
    result = await get_analysis(df=df,df2=df2,**template)
    # await updating_json(result,ANALYSISJS)
    print(result)
    # driver.quit()
    return result


# if __name__ == "__main__":
    
#     asyncio.run(run_procedure())