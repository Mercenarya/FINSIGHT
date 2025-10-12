import sys
import os
import pybind11
import importlib.util

current_dir = os.path.dirname(os.path.abspath(__file__))
root = os.path.join(current_dir, '..')
sys.path.append(root)




from ml_pipeline.calculation.build import evaluate_module

ev = evaluate_module.Profitability()
av = evaluate_module.Liquidity()
ef = evaluate_module.Efficiency()

print(ev)
print(dir(ev))
print(pybind11.get_include())
print("Gross profit margin : ",
    round(ev.gross_margin_result(27245717878312.0,2818409788534.0,1000000000),2
),"%")


print("Gross profit margin : ",
    round(av.current_ratio(20000,28180.0),2
),"%")

print("Turnover assets : ", round(ef.asset_turnover(2000000000.0,1000000000.0),2))