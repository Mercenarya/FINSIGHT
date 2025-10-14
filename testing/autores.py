from inspect import signature
import os, sys
import unittest
from config import DLL
import threading

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
        
    def coverage(self, args:list):
        params = [arg for arg in args]
        result = self.module(*params)
        print(f"THREAD RESULT : {result}")
        return self.module(*params)


        
    def create_threads(self):
        params = []
        threads = []
        
        steps = int(input("Enter number of threads: "))
        args = int(input("Number of arguments: "))

        for obj in range(args):
            value = input(f"Arguments {obj+1}: ")
            if '.' in value:
                params.append(float(value))
            else:
                params.append(int(value))

        for step in range(steps):
            thread = threading.Thread(target=self.coverage, args=(params,))
            threads.append(thread)
            thread.start()

        for th in threads:
            th.join()

        

if __name__ == "__main__":
    ev = evaluate_module.Profitability()
    av = evaluate_module.Liquidity()
    ef = evaluate_module.Efficiency()
    gt = evaluate_module.Growth()
    mdll = Module(ev.gross_margin_result)
    print("MODULE DOCS: ")
    print(mdll.get_docs())
    rootpath = os.path.join('D:\Finsightdata\ml_pipeline')
    dirpath = os.path.join(rootpath,'calculation')
    path = dirpath + '\\profitability.cpp'
    print("PATH: ", path)
    if os.path.exists(path):
        print("Exists file")
    else:
        print("Not exists")

    objective = StatmentCoverage(ev.gross_margin_result, path)
    print(objective.read_module())
    print(objective.create_threads())
    
    # 27245717878312.0
    # 2818409788534.0
    

    

    
    