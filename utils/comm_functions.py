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
    message = input("Enter data title: ")
    try:
        
        with open(filename, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        
        
            for obj in json_data:
                if message in obj.get("title"):
                    print(obj)
            else:
                print("This data is invalid")
        # return json_data
                    
        
        
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


PATH = get_path(RAW)
JSN = get_path(JSP)

print(json_data('data/json/prototype01.json'))