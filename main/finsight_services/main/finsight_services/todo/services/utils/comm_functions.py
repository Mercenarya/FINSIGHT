import os
import sys
import pandas as pd
import json
# import sklearn
import numpy as np

# from sklearn.preprocessing import StandardScaler


CURRENT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(CURRENT,'..','..','..','..','..')
# MODULE_DIR là thư mục chứa file .pyd đã được đổi tên
sys.path.append(ROOT)


# RAW_DIR = os.path.abspath(os.path.join(ROOT,'..','..','..','..','..'))
# RAW = os.path.join(RAW_DIR,'data','raw','cleandpt001.csv')
# ASSETS = os.path.join(RAW_DIR,'data','raw','assets001.csv')


RAW = os.path.join(ROOT,'data','raw','cleandpt001.csv')
JSR = os.path.join(ROOT,'data','json','reports.json')
ASSETSJS = os.path.join(ROOT,'data','json','assets.json')
ASSETS = os.path.join(ROOT,'data','raw','assets001.csv')
# lấy dữ liệu kết quả sau khi phân tích lưu vào json 
ANALYSISJS = os.path.join(ROOT,'data','json','analysis.json')




def get_path(filename:str):
    try:
        current_dir = os.path.dirname(os.path.realpath(__file__))
        # joined_path = os.path.join(current_dir,filename)
        drive = current_dir[::-10]
        print(drive)
        return filename
    except Exception as error:
        return f"PATH : {error}"


def seed_path(path:str) -> bool:
    '''
    Existed Path review
    args:
    - Path args : string
    '''
    try:
        if os.path.exists(path):
            return True
        else:
            return False
        
    except OSError as error:
        return f"OSERROR : {error}"

# chuyển dữ liệu vào csv
def save_to_csv(filename:str,df):
    try:
        '''
        Args:
        - filename : cleanedpt001.csv
        - df : current imported dataframe
        - directory : data/raw
        '''
        df.to_csv(filename, index=False, encoding='utf-8-sig')

    except Exception as error:
        return f"ERROR to CSV : {error}"

def looping_json(data:list):
    try:
        dict_data = []
        count = 0
        for obj in range(len(data)):
            # nếu phần tử được duyệt là dict
            if isinstance(data[obj], dict):
                dict_data.append(
                    {
                        "title": data[obj].get("title"),
                        "First_quarter": data[obj].get("First"),
                        "Second_quarter":data[obj].get("Second"),
                        "Third_quarter":data[obj].get('Third'),
                        "Fourth_quarter":data[obj].get("Fourth")
                    }
                )
                count += 1
                print(f"sheet {count} appended")
        return dict_data
                
    except json.JSONDecodeError as jsdcerror:
        return f"JSONDecode : {jsdcerror}"
    except Exception as error:
        return f"JSON general : {error}"

#load json data
def json_search(filename:str,search:str):
    message = search
    try:
        data = []
        with open(filename, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            for obj in json_data:
                if message in obj.get("title"):
                    data.append(
                        {
                        
                            "title": obj.get("title"),
                            "First_quarter": obj.get("First_quarter"),
                            "Second_quarter":obj.get("Second_quarter"),
                            "Third_quarter":obj.get('Third_quarter'),
                            "Fourth_quarter":obj.get("Fourth_quarter")
                        
                        }
                
                    )
        return data
        
    except Exception as error:
        return f"JSON data : {error}"

#load json data
def json_data(filename:str):
    
    try:
        
        with open(filename, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        
        return json_data
                    
        
        
    except Exception as error:
        return f"JSON data : {error}"

#load json data
def json_search(filename:str,search:str):
    message = search
    try:
        data = []
        with open(filename, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            for obj in json_data:
                if message in obj.get("title"):
                    data.append(
                        {
                        
                            "title": obj.get("title"),
                            "First_quarter": obj.get("First_quarter"),
                            "Second_quarter":obj.get("Second_quarter"),
                            "Third_quarter":obj.get('Third_quarter'),
                            "Fourth_quarter":obj.get("Fourth_quarter")
                        
                        }
                
                    )
        return data
        
    except Exception as error:
        return f"JSON data : {error}"


# chuyển dữ liệu json
def save_to_json(filename:str,data:list,directory='data/json'):
    '''
    Args:
        - filename : prototype01.json
        - data : dictionary data
        - directory : data/json
    '''
    try:
        # count = 0
        with open(filename, "w", encoding='utf-8') as f:
           
            # for obj in data:
            json.dump(data, f, indent=4, ensure_ascii=False)
            
            print(f"json sheet wrote")


    except Exception as error:
        return "JSON hooking : ",error


# đọc dữ liệu
def release_csv(filename:str):
    try:
        if os.path.exists(filename):
            print(f"filename : {filename} is not exists")
        else:
            df = pd.read_csv(filename)
            
            # thay các dữ liệu NaN ( các giá trị lỗi hoặc rỗng) sang 0
            df['Quarter 1'] = df['Quarter 1'].replace(np.nan,0)
            df['Quarter 2'] = df['Quarter 2'].replace(np.nan,0)
            df['Quarter 3'] = df['Quarter 3'].replace(np.nan,0)
            df['Quarter 4'] = df['Quarter 4'].replace(np.nan,0)

            # thay các giá trị comma (dấu phẩy)
            df = df.replace(',','')

            # kiểm ra ouput sau khi qua xử lí
            print("==="*30)
            print(df)
            print("==="*30)
            data = {
                "Title":df['Title'],
                "Q_1":df['Quarter 1'],
                "Q_2":df['Quarter 2'],
                "Q_3":df['Quarter 3'],
                "Q_4":df['Quarter 4']
            }
            return data
    except OSError as oserr:
        return f"Release CSV OSERRORS : {oserr}"
    except Exception as error:
        return f"Release CSV Errors : {error}"




PATH = get_path(RAW)
JSNRP = get_path(JSR)
JSNAS = get_path(ASSETSJS)
ASSET = get_path(ASSETS)
