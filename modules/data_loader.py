# 匯入 pandas 套件，用於資料處理，並縮寫為 pd
import pandas as pd

# 匯入內建的 regular expression (正規表示式) 套件，用於複雜的字串比對、搜尋與替換
import re

# 匯入內建的 os (Operating System) 套件，用於與作業系統互動，像是檢查檔案路徑、讀取資料夾等
import os

# 定義一個名為 load_and_clean_data 的函式
# 設定參數 file_path 的預設值為 "data/metro_data.csv" (代表如果在呼叫函式時沒給路徑，就會預設去讀這個位址)
def load_and_clean_data(file_path="data/metro_data.csv"):
    """
    Parser 模組：負責以相對路徑讀取捷運 CSV 資料，並進行基本字串清洗與防禦。
    """
    
    # ==========================================
    # 1. 注意事項規範：檢查檔案是否存在，防止路徑錯誤導致 Crash
    # ==========================================
    
    # 使用 os.path.exists() 檢查指定的 file_path 到底存不存在。加上 'not' 代表「如果檔案不存在」
    if not os.path.exists(file_path):
        # 如果真的找不到檔案，主動拋出一個 FileNotFoundError 錯誤，並中斷程式。
        # 這樣做比讓 pandas 讀不到檔案崩潰還要好，因為我們可以自訂明確的錯誤訊息提示開發者
        raise FileNotFoundError(f"找不到資料檔案，請確認檔案是否放在相對路徑: {file_path}")
        
    # 在終端機印出提示，讓使用者知道程式目前跑到哪裡
    print("正在讀取捷運原始資料...")
    
    # 檔案確認存在後，使用 pandas 的 read_csv 將檔案讀取進來，並存成 DataFrame 物件，命名為 df
    df = pd.read_csv(file_path)
    
    # ==========================================
    # 2. 數據自我測試：型別污染處理，確保人數欄位(Sum)都是數字，髒數據轉為 NaN 再補 0
    # ==========================================
    
    # 防禦性寫法：先檢查 'Sum' 這個欄位有沒有在資料表 (df.columns) 裡面，有才進行處理
    if 'Sum' in df.columns:
        # 這一行做了三件事 (Method Chaining 串聯寫法)：
        # (1) pd.to_numeric(..., errors='coerce')：強制將 'Sum' 欄位轉為數字。
        #     如果遇到無法轉換的髒字串 (例如中文字或亂碼)，errors='coerce' 會強迫它變成 NaN (缺失值)。
        # (2) .fillna(0)：把剛才變成 NaN 或是原本就空白的格子，全部填補為 0 (沒有人次)。
        # (3) .astype(int)：把整個欄位的資料型態統一轉換為整數 (integer)。
        # 最後將結果覆寫回 df['Sum']
        df['Sum'] = pd.to_numeric(df['Sum'], errors='coerce').fillna(0).astype(int)
    
    # ==========================================
    # 3. 次要問題實作：利用正規表示式剝離車站代號 (例如把 "BL15 忠孝復興" 變成 "忠孝復興")
    # ==========================================
    
    # 在大函式裡面定義一個小函式 (這叫做 Closure 或 Nested Function)，專門用來處理單筆站名
    def remove_station_code(station_name):
        # 檢查傳入的站名是不是 NaN (缺失值)，如果是，就回傳空字串，避免接下來的字串處理報錯
        if pd.isna(station_name):
            return ""
        
        # 精修版：精準匹配 1-2 個大寫英文字母（如 BL 或 R），後面接 2 位數字與空格
        # 使用 re.sub(pattern, replacement, string) 來替換字串：
        # r'...'：前面的 r 代表 Raw String，避免跳脫字元的干擾。
        # ^：代表必須從字串的「最開頭」開始比對。
        # [A-Z]{1,2}：尋找 1 到 2 個連續的大寫英文字母 (例如 R, BL, BR)。
        # \d{2}：緊接著尋找剛好 2 個數字 (例如 15, 05)。
        # \s+：緊接著尋找 1 個或多個空白字元 (Space)。
        # ''：把上面比對到的整串東西 (例如 "BL15 ")，替換成空字串 (也就是直接刪除)。
        # str(station_name)：確保傳入的東西一定是字串型態。
        clean_name = re.sub(r'^[A-Z]{1,2}\d{2}\s+', '', str(station_name))
        
        # .strip() 可以切除字串最前面與最後面多餘的空白，確保乾淨後再回傳
        return clean_name.strip()  
    
    # 印出進度提示
    print("正在進行車站名稱字串清洗(剝離代號)...")
    
    # 檢查有沒有 'Entrance' (進站) 這個欄位
    if 'Entrance' in df.columns:
        # 使用 .apply() 將我們上面寫好的 remove_station_code 函式，套用到 'Entrance' 欄位的「每一格」
        # 並將清洗好的乾淨站名覆寫回原本的欄位
        df['Entrance'] = df['Entrance'].apply(remove_station_code)
        
    # 同理，檢查並清洗 'Exit' (出站) 欄位
    if 'Exit' in df.columns:
        df['Exit'] = df['Exit'].apply(remove_station_code)
        
    # 印出完成提示
    print("資料初步清洗完成！")
    
    # 把清洗好的 DataFrame 回傳出去給呼叫的人
    return df

# ==========================================
# 本地測試區
# ==========================================
# 這是 Python 慣用寫法：代表「如果這隻程式是被直接執行 (而不是被其他檔案 import 當作模組使用)」，
# 才會執行下面這段測試程式碼
if __name__ == "__main__":
    # 使用 try-except 區塊捕捉可能發生的錯誤
    try:
        # 呼叫上面寫好的清洗函式 (因為沒給參數，所以會用預設路徑)，將結果存入 test_df
        test_df = load_and_clean_data()
        
        # 印出分隔線與提示
        print("\n--- 清洗後的前五列資料預覽 ---")
        
        # .head() 預設會印出 DataFrame 的前五筆資料，方便我們快速預覽清洗結果
        print(test_df.head())
        
    # 如果在 try 區塊裡面發生任何例外錯誤 (例如找不到檔案)，就會跳進這裡
    # 並把錯誤物件命名為 e
    except Exception as e:
        # 印出錯誤訊息 (使用 f-string 把變數 e 塞進字串中)
        print(f"執行出錯了: {e}")
