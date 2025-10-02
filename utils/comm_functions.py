import os
import sys
import pandas as pd
import json

current_dir = os.path.dirname(os.path.abspath(__file__))
root = os.path.join(current_dir, '..')
sys.path.append(root)

from config import JSP,RAW,PRC


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

    try:
        if os.path.exists(path):
            return True
        else:
            return False
        
    except OSError as error:
        return f"OSERROR : {error}"

# chuyển dữ liệu vào csv
def save_to_csv(filename:str,df,directory='data/raw'):
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

def looping_json(data:dict):
    pass


# chuyển dữ liệu json
def save_to_json(filename:str,data:dict,directory='data/json'):
    '''
    Args:
        - filename : prototype01.json
        - data : dictionary data
        - directory : data/json
    '''
    try:
        
        with open(filename, "a+", encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=True)
    except Exception as error:
        return "JSON hooking : ",error


PATH = get_path(RAW)