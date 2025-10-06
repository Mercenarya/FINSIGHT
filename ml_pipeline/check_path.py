import sys
import os
import pybind11


current_dir = os.path.dirname(os.path.abspath(__file__))
root = os.path.join(current_dir, '..')
sys.path.append(root)

from ml_pipeline.calculation.build import evaluate_module


ev = evaluate_module.Profitability()
print(ev)
print(dir(ev))
print(pybind11.get_include())
print("Gross profit margin : ",
    round(ev.gross_margin_result(27245717878312.0,2818409788534.0,1000000000),2
),"%")