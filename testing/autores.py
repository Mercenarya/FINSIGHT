from inspect import signature
import os, sys
import unittest
from config import DLL
import threading
from queue import Queue

current_dir = os.path.dirname(os.path.abspath(__file__))
root = os.path.join(current_dir, '..')
sys.path.append(root)

build_dir = os.path.join(current_dir,'caculation','build')
sys.path.append(build_dir)
dll = os.add_dll_directory(DLL)
sys.path.append(dll)

from ml_pipeline.calculation.build import evaluate_module


class Module:
    def __init__(self, objective):
        self.objective = objective

    def get_docs(self):
        docs = self.objective.__doc__
        return docs
        


class StatmentCoverage:
    def __init__(self, module, path):
        self.path = path
        self.module = module

    def read_module(self):
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                data = file.read()
                return data
        except FileNotFoundError as fnf:
            return f"FILE error : {fnf}"
        except Exception as error:
            return f"Error : {error}"
        
    def coverage(self, args:list, queue):
        params = [arg for arg in args]
        result = self.module(*params)
        print(f"THREAD RESULT : {result}")
        queue.put(result)
        return self.module(*params)

    # ghi chú các số liẹu
    def input_records(self,case_title,record,count):
        try:
            
            with open('input_records.txt','a') as file:
                file.write(f"TITLE - {case_title}\n")
                file.write(f"CASE {count} :  {record}"+"\n")
        except FileNotFoundError as fnf:
            return f"FILE not found : {fnf}"
        except Exception as error:
            return f"error : {error}"
        
        
    def create_threads(self):
        params = []
        threads = []
        data = []
        result_queue = Queue()
        count = 0
        
        case_title = input("Case title: ")
        steps = int(input("Enter number of threads: "))
        args = int(input("Number of arguments: "))

        for obj in range(args):
            value = input(f"Arguments {obj+1}: ")
            if '.' in value:
                params.append(float(value))
            else:
                params.append(int(value))

        for step in range(steps):
            
            thread = threading.Thread(target=self.coverage, args=(params,result_queue))
            threads.append(thread)
            thread.start()

        # for value in threads:
        #     count += 1
        #     result = value.join()
        #     record = threading.Thread(target=self.input_records, args=(case_title,str(result),count))
        #     data.append(record)
        #     record.start()
        for th in threads:
            th.join()

        while not result_queue.empty():
            count += 1
            record = result_queue.get()
            self.input_records(case_title, record, count)


   

        

if __name__ == "__main__":

    # Phần chứa nội dung hàm cần ckiểm thử 
    ev = evaluate_module.Profitability()
    av = evaluate_module.Liquidity()
    ef = evaluate_module.Efficiency()
    gt = evaluate_module.Growth()
    mdll = Module(ev.gross_margin_result)

    '''
    Các module cần kiểm thử sẽ được viết tiếp ở bên 
    dưới đây ... 
    
    '''

    # Phần chứa nội dung thông tin và cấu hình 
    print("MODULE DOCS: ")
    rootpath = os.path.join('D:\Finsightdata\ml_pipeline')
    dirpath = os.path.join(rootpath,'calculation')
    path = dirpath + '\\profitability.cpp'
    print("PATH: ", path)
    if os.path.exists(path):
        print("Exists file")
    else:
        print("Not exists")

    # Triển khai và kiểm thử hệ thống
    objective = StatmentCoverage(ev.gross_margin_result, path)
    print(objective.read_module())
    print(objective.create_threads())


    
    # 27245717878312.0
    # 2818409788534.0
    

    

    
    