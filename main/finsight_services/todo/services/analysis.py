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



CURRENT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(CURRENT)
sys.path.append(ROOT)
# MODULE_DIR là thư mục chứa file .pyd đã được đổi tên

RAW_DIR = os.path.abspath(os.path.join(CURRENT,'..','..','..','..'))
RAW = os.path.join(RAW_DIR,'data','raw','cleandpt001.csv')
ASSETS = os.path.join(RAW_DIR,'data','raw','assets001.csv')

LIBS = os.path.join(ROOT, 'libs') 
MODULE_DIR = os.path.join(ROOT, 'libs') 


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




print(MODULE_DIR)
print(RAW)

# Thêm đường dẫn thư mục vào sys.path
sys.path.append(MODULE_DIR)

# Sử dụng cú pháp import trực tiếp
from libs import evaluate_module_update


ef = evaluate_module_update.Efficiency()
gr = evaluate_module_update.Growth()
lq = evaluate_module_update.Liquidity()



'''
Mục tính mức độ lơi nhuận tài chính
'''



# chuẩn hóa cụm
async def normalization(data):
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
async def read_data(filename:str):

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
async def extract_finance_growth(df,prev_quarter,current_quarter,years,major):
  
    try:
        
        business_net_profit_prev = int(df.iloc[major][prev_quarter])
        business_net_profit_current = int(df.iloc[major][current_quarter])

        growth = evaluate_module_update.Growth()
        
        
        # lấy chỉ số tăng trưởng đơn
        single_growth_rate = growth.single_growth_rate(int(business_net_profit_current),int(business_net_profit_prev))

        # lấy chỉ số tăng trưởng kép theo năm
        cagr_growth_rate = growth.cagr_growth_rate(int(business_net_profit_current),int(business_net_profit_prev),years)

        # không thể tính toán chỉ số tăng trưởng khi giá trị của mốc trước là 0
        if business_net_profit_prev == 0:
            print("Previous quarter cannot be none")
            return
        if business_net_profit_prev <= 0 or business_net_profit_current <=0 or years <= 0:
            cagr_growth_rate = 'N/A'


        print('QUÝ trước : ',business_net_profit_prev)
        print('Quý hiện tại : ',business_net_profit_current)
        analysis_template = {
            
            'Major':df.iloc[major]['Title'],
            'Year':years,
            'single growth rate':single_growth_rate,
            'compound annual growth rate':cagr_growth_rate
        }
        return analysis_template

    except Exception as error:
        return f"Extract finance growth problems set : {error}"







# lọc các nội dung tài chính từ Báo Cáo
async def extract_finance_profitability(df,df2,quarter):

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

        pft = evaluate_module_update.Profitability()
        revenue = df.iloc[2][quarter]

        # lợi nhuận gộp, doanh thu thuần (cho gross margin)
        gross_profit = df.iloc[4][quarter]
        

        # lợi nhuận từ hoạt động kinh doanh (cho operating profit margin)
        business_net_profit = df.iloc[11][quarter]

        # lợi nhuận sau thuế thu nhập, lợi nhuận kế toán trước thuế 
        # Net profit margin , ROA Ratio (cần lợi nhuận sau thuế thu nhập)
        after_income_profit = df.iloc[18][quarter]
        print("Profit after tax: ",after_income_profit)
        tta = df2.iloc[62][quarter] # tương đương tổng tài sản

        # vốn chủ sở hữu
        equity = df2.iloc[93][quarter]
        print("Equity : ",equity)



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



   

        tta = df2.iloc[62]['Title'] + " : "+df2.iloc[62][quarter]
        print(tta)

        analysis_template = {
            "Quarter":quarter,

            "Gross marrgin":round(gross_margin,2),
            "Operating profit margin":round(operating_margin,2),
            "ROA Ratio value":round(roa_ratio,7) ,
            "ROA Percent": roa_percent,
            "ROE Profit":roe_ratio,
            "ROE Percent":roe_percent
        }

        return analysis_template



    except Exception as error :
        return f"Extract params errors : {error}"



# phân tích chỉ số thanh khoản tài chính
async def extract_finance_liquidity(df,quarter):
    try:
        
        # lấy thông tin cho các phép thanh khoản tài chính
        cash = df.iloc[1][quarter] # tiền và các khoản tương đương
        liabilities = df.iloc[65][quarter] # nợ phải trả
        current_assest = df.iloc[0][quarter] # tài sản ngắn hạn
        inventory = df.iloc[17][quarter] # hàng tồn kho



        # chỉ số thanh khoản cash ratio
        cash_ratio = lq.cash_ratio(int(cash),int(liabilities))

        # chỉ số thanh khoản quick ratio
        quick_ratio = lq.quick_ratio(int(current_assest),int(inventory),int(liabilities))

        # chỉ số thanh khoản current ratio
        current_ratio = lq.current_ratio(int(current_assest), int(liabilities))

        # template kết quả
        template = {
            'Quarter':quarter,
            'cash ratio': cash_ratio,
            'quick ratio': quick_ratio,
            'current ratio': current_ratio
        }
        return template



    except Exception as error:
        print("Error occured during extracting liquidity result: ",error)
        return {}

# phân tích và đánh giá mức hiệu quả tài chính 
async def extract_finance_efficiency(df,quarter):
    '''
    // nhóm Efficiency
    using inventory_TOR_sig = double (Efficiency::*)(T,T);
    using dio_stand_sig = double (Efficiency::*)(const int,T);
    using art_turnover_sig = double (Efficiency::*)(T,T);
    using tta_turnover_sig = double (Efficiency::*)(T,T);
    using apt_turnover_sig = double (Efficiency::*)(T,T);
    using dpo_outstanding_sig = double (Efficiency::*)(const int,T);
    '''
    ef = evaluate_module_update.Efficiency()
    try:
        
        # các phân mục hỗ trợ phân tích 
        costgs = int(df[None][quarter])
        avginventory = int(df[None][quarter])
        inventory_turnover = int(df[None][quarter])
        netcreditsale = int(df[None][quarter])
        avgaccountsrcv = int(df[None][quarter])
        netsales = int(df[None][quarter])
        avgttassets = int(df[None][quarter])
        avgaccpay = int(df[None][quarter])
        accpayturnover = int(df[None][quarter])



    except Exception as error:
        print("An error occured during extracting efficiency ", error)
        return {}



# chuyển đổi dữ liệu bảo cáo đã được phân tích vào dữ liệu đặc thù riêng

async def convert_reports(template,filename):

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


# if __name__ == "__main__":
#     quarter = 'Quarter 3'
#     major = 0 #'1. Doanh thu bán hàng và cung cấp dịch vụ'
#     prev = 'Quarter 3'
#     current = 'Quarter 4'

#     df = read_data(RAW)
#     df2 = read_data(ASSETS)
#     print(df)
#     print("="*100)
    
#     print('NỘI DUNG LỢI NHUẬN DOANH NGHIỆP - PROFITABILITY')
#     print(extract_finance_profitability(df,df2,quarter=quarter))
#     print('NỘI DUNG TĂNG TRƯỞNG MỐC - GROWTH')
    
    
    
#     print(extract_finance_growth(df=df,prev_quarter=prev,current_quarter=current,major=major,years=2024))
#     print("NỘI DUNG PHÂN TÍCH CHỈ SỐ THANH KHOẢN TÀI CHÍNH")
#     print(extract_finance_liquidity(df2,quarter=quarter))

