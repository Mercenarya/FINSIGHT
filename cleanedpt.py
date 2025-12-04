import pandas as pd
import os

RAW_FILE = r"D:\nckh\FINSIGHT-brch_2\data\raw\cleanedpt001.csv"
OUTPUT_FILE = r"D:\nckh\FINSIGHT-brch_2\data\processed\normalized_output.csv"

def normalize_csv(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Không tìm thấy file: {input_file}")
        return
    if os.path.getsize(input_file) == 0:
        print(f"File {input_file} rỗng, không có dữ liệu để xử lý!")
        return
    df = pd.read_csv(input_file, encoding="utf-8-sig", header=None)
    col_names = ["item", "col1", "col2", "col3", "col4"][:df.shape[1]]
    df.columns = col_names
    numeric_df = df[df.columns[1:]]  # bỏ cột đầu tiên (item)
    for c in numeric_df.columns:
        numeric_df[c] = pd.to_numeric(
            numeric_df[c].astype(str).str.replace(",", "", regex=False),
            errors="coerce"
        )
        
    numeric_df = numeric_df.dropna(how="any")
    for c in numeric_df.columns:
        mean = numeric_df[c].mean()
        std = numeric_df[c].std()
        if std != 0 and not pd.isna(std):
            numeric_df[c] = (numeric_df[c] - mean) / std
    numeric_df = numeric_df.reset_index(drop=True)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    numeric_df.to_csv(output_file, index=False, encoding="utf-8-sig")

    print(f"Đã loại bỏ chữ (item), chỉ giữ số liệu chuẩn hoá Z-score! File lưu tại: {output_file}")

if __name__ == "__main__":
    normalize_csv(RAW_FILE, OUTPUT_FILE)
