import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
root = os.path.join(current_dir, '..')
sys.path.append(root)

# build_dir = os.path.join(current_dir,'ml_pipeline','caculation','build')
# sys.path.append(build_dir)


from ml_pipeline.calculation.build import evaluate_module


ev = evaluate_module.Evaluate()
print(ev)
print(dir(ev))

print("Kết quả: ",ev.gross_margin_result(100000,100,1000))