import pandas as pd
import re
import os

def load_and_clean_data(file_path="data/metro_data.csv"):
    """
    Parser 模組：負責以相對路徑讀取捷運 CSV 資料，並進行基本字串清洗與防禦。
    """
    # 1. 注意事項規範：檢查檔案是否存在，防止路徑錯誤導致 Crash
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"找不到資料檔案，請確認檔案是否放在相對路徑: {file_path}")
        
    print("正在讀取捷運原始資料...")
    # 使用相對路徑讀取資料夾內檔案
    df = pd.read_csv(file_path)
    
    # 2. 數據自我測試：型別污染處理，確保人數欄位(Sum)都是數字，髒數據轉為 NaN 再補 0
    if 'Sum' in df.columns:
        df['Sum'] = pd.to_numeric(df['Sum'], errors='coerce').fillna(0).astype(int)
    
    # 3. 次要問題實作：利用正規表示式剝離車站代號 (例如把 "BL15 忠孝復興" 變成 "忠孝復興")
    def remove_station_code(station_name):
        if pd.isna(station_name):
            return ""
        # 匹配開頭的英數字編號加上空格，並將其替換為空字串
        return re.sub(r'^[A-Z0-9]+\s+', '', str(station_name))
    
    print("正在進行車站名稱字串清洗(剝離代號)...")
    if 'Entrance' in df.columns:
        df['Entrance'] = df['Entrance'].apply(remove_station_code)
    if 'Exit' in df.columns:
        df['Exit'] = df['Exit'].apply(remove_station_code)
        
    print("資料初步清洗完成！")
    return df

# 本地測試區
if __name__ == "__main__":
    try:
        test_df = load_and_clean_data()
        print("\n--- 清洗後的前五列資料預覽 ---")
        print(test_df.head())
    except Exception as e:
        print(f"執行出錯了: {e}")