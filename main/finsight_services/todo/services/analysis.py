import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn
import json
from sklearn.preprocessing import StandardScaler



CURRENT = os.path.dirname(os.path.realpath(__file__))
ROOT = os.path.abspath(os.path.join(CURRENT,'..'))
# MODULE_DIR là thư mục chứa file .pyd đã được đổi tên

RAW_DIR = os.path.abspath(os.path.join(CURRENT,'..','..','..','..'))
RAW = os.path.join(RAW_DIR,'data','raw','cleandpt001.csv')
ASSETS = os.path.join(RAW_DIR,'data','raw','assets001.csv')
LIBS = os.path.join(ROOT, 'libs') 
os.add_dll_directory('D:/Msys2/ucrt64/bin')

print(CURRENT)
print(ROOT)
print(LIBS)
print(RAW)
print(ASSETS)
# Thêm đường dẫn thư mục vào sys.path
sys.path.append(LIBS)

# Sử dụng cú pháp import trực tiếp
from libs import evaluate_module_update as ev 





'''
Mục tính mức độ lơi nhuận tài chính
'''


# chuẩn hóa cụm
def normalization(data):
    try:
        '''
        Thực hiện quá trình chuẩn hóa 
        theo từng cụm
        '''
        std = StandardScaler()
        nml_data = std.fit_transform(data)
        return nml_data
    except Exception as error:
        return f"Normalization errors : {error}"




# đọc dữ liệu
def read_data(filename:str):
    try:
        if os.path.exists(filename):
            df = pd.read_csv(filename)
            df['Quarter 1'] = df['Quarter 1'].str.replace(',','')
            df['Quarter 2'] = df['Quarter 2'].str.replace(',','')
            df['Quarter 3'] = df['Quarter 3'].str.replace(',','')
            df['Quarter 4'] = df['Quarter 4'].str.replace(',','')
            df = df.replace(np.nan,0)
            return df
        else: 
            print("Dataset is not exists")
            return None

    except OSError as oserr:
        return f"OS errors : {oserr}"
    except Exception as error:
        return f"General Error of data reader {error}"

# lấy thông tin tăng trưởng
def extract_finance_growth(prev_quarter,current_quarter,years):
    try:
        growth = ev.Growth()
        
        current_quarter = int(current_quarter)
        prev_quarter = int(prev_quarter)
        # lấy chỉ số tăng trưởng đơn
        single_growth_rate = growth.single_growth_rate(current_quarter,prev_quarter)

        # lấy chỉ số tăng trưởng kép theo năm
        cagr_growth_rate = growth.cagr_growth_rate(current_quarter,prev_quarter,years)

        # không thể tính toán chỉ số tăng trưởng khi giá trị của mốc trước là 0
        if prev_quarter == 0:
            print("Previous quarter cannot be none")
            return
        if prev_quarter <= 0 or current_quarter <=0 or years <= 0:
            cagr_growth_rate = 'N/A'



        analysis_template = {
            'Year':years,
            'single growth rate':single_growth_rate,
            'compound annual growth rate':cagr_growth_rate
        }
        return analysis_template

    except Exception as error:
        return f"Extract finance growth problems set : {error}"

# lọc các nội dung tài chính từ Báo Cáo
def extract_finance_profitability(df,df2):
    # tính lợi nhuận gộp
    # REVENUE = 27245717878312 # Doanh thu thuần

    # COGS = 2818409788534    # Giá vốn hàng bán
    # GROSS_PROFIT = REVENUE - COGS # Lợi nhuận gộp (GP)
    
    try:
        pft = ev.Profitability()
        revenue = df.iloc[2]['Quarter 1']

        # lợi nhuận gộp, doanh thu thuần (cho gross margin)
        gross_profit = df.iloc[4]['Quarter 1']
        

        # lợi nhuận từ hoạt động kinh doanh (cho operating profit margin)
        business_net_profit = df.iloc[11]['Quarter 1']

        # lợi nhuận sau thuế thu nhập, lợi nhuận kế toán trước thuế 
        # Net profit margin , ROA Ratio (cần lợi nhuận sau thuế thu nhập)
        after_income_profit = df.iloc[18]['Quarter 1']
        print("Profit after tax: ",after_income_profit)
        tta = df2.iloc[62]['Quarter 1'] # tương đương tổng tài sản

        # vốn chủ sở hữu
        equity = df2.iloc[93]['Quarter 1']
        print("Equity : ",equity)

        # lợi nhuận sau thuế công ty mẹ (ROE Profit)
        hqt_income_profit = df.iloc[19]['Quarter 1']

        # lãi cơ bản trên cổ phiếu
        basis_share_holder = df.iloc[21]['Quarter 1']

        '''
        triển khai các phép phân tích tài chính từ pyd gồm:
        - gross margin
        - ROA Ratios
        - Net profit margin
        - ROE Profit
        - EPS ratios
        '''
        #biểu thị giá trị sử dụng
        gross_margin = pft.gross_margin(int(gross_profit),int(revenue))
        operating_margin = pft.opm_margin(int(business_net_profit),int(revenue))
        roa_ratio = pft.roa_ratio(int(tta),int(after_income_profit))
        roe_ratio = pft.roe_profit(int(equity),int(after_income_profit))
        # eps_ratios = pft.eps_ratio

        # biểu thị giá trị minh họa 
        roa_percent = f"{roa_ratio:.7f} %"
        roe_percent = f"{roe_ratio:.7f} %"


        analysis_template = {
            "Gross marrgin":round(gross_margin,2),
            "Operating profit margin":round(operating_margin,2),
            "ROA Ratio value":round(roa_ratio,7) ,
            "ROA Percent": roa_percent,
            "ROE Profit":roe_ratio,
            "ROE Percent":roe_percent
        }
        return json.dumps(analysis_template)



    except Exception as error :
        return f"Extract params errors : {error}"





# chuyển đổi dữ liệu bảo cáo đã được phân tích vào dữ liệu đặc thù riêng
def convert_reports(template,filename):
    try:
        
        title = [
            'Gross margin',
            'Operating profit margin',
            'ROA ratio'
        ]
        # chuyển đổi dữ liệu
        df = pd.DataFrame(title,template)
        df.to_csv(filename)
        return df
    except Exception as error:
        return f"Reports general errors : {error}"
    



# if __name__ == "__main__":

#     df = read_data(RAW)
#     df2 = read_data(ASSETS)
#     print(df)
#     print("="*100)
#     tta = df2.iloc[62]['Title'] + " : "+df2.iloc[62]['Quarter 1']
#     print(tta)
#     print(extract_finance_profitability(df,df2))