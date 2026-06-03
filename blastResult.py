import pandas as pd
import matplotlib.pyplot as plt

def load_data(file_path):
    """
    讀取捷運運量 CSV 資料 (使用相對路徑)
    """
    try:
        # 根據講義規範，必須處理髒資料或空行
        df = pd.read_csv(file_path)
        print("運量資料讀取成功！")
        return df
    except Exception as e:
        print(f"讀取資料發生錯誤: {e}")
        return None

if __name__ == "__main__":
    print("--- 捷運核心車站人潮擁擠度分析系統 ---")
    
    # 講義規範：禁止使用絕對路徑(C:\...)，要用相對路徑
    # 之後你們把捷運的 CSV 檔案下載下來後，要放在 data 資料夾裡
    data_path = "data/mtr_flow.csv" 
    
    # 測試讀取功能
    # data = load_data(data_path)