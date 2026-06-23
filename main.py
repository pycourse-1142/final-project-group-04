# 匯入作業系統互動套件，用來處理跨平台的檔案路徑與檢查檔案是否存在
import os

# 匯入 pandas 套件，用於讀取與操作關聯式資料，縮寫為 pd
import pandas as pd

# ==========================================
# 導入你寫好的自訂模組 (模組化設計的核心)
# 從 modules 資料夾底下的 analytics.py 檔案中，匯入我們寫好的三個核心運算函式
# ==========================================
from modules.analytics import (
    get_peak_hourly_traffic, 
    get_top_load_stations, 
    get_top_imbalanced_stations
)

# 從 modules 資料夾底下的 plotter.py 檔案中，匯入統整好的繪圖函式
from modules.plotter import generate_all_plots


# 定義主程式函式 main()
# 將執行邏輯包裝在一個函式裡是個好習慣，可以避免變數污染到全域環境
def main():
    
    # 建立檔案相對路徑
    # 使用 os.path.join 是一個非常安全的寫法，它會根據使用者的作業系統 (Windows 是 '\', Mac/Linux 是 '/') 
    # 自動組合出正確的路徑，例如 "data/taipei_metro_traffic.csv" 或 "data\taipei_metro_traffic.csv"
    csv_path = os.path.join('data', 'taipei_metro_traffic.csv')
    
    # 防禦性設計：檢查這個組好的路徑底下，是不是真的有檔案？
    if not os.path.exists(csv_path):
        # 如果找不到，印出錯誤提示
        print(f"❌ 找不到資料檔...")
        # 找不到檔案就沒必要往下跑了，直接 return 結束這個 main() 函式 (Early Exit)
        return
        
    # 如果順利通過上面的檢查，印出成功提示
    print("🚀 成功讀取資料，呼叫 Analytics 模組進行核心運算...")
    
    # 將 CSV 讀取成 pandas DataFrame，存入變數 df 中
    df = pd.read_csv(csv_path)
    
    
    # ==========================================
    # 1. 準備 24 小時資料 (針對台北車站)
    # ==========================================
    
    # 篩選並排序資料
    # df[df['進站車站'] == '台北車站']：把進站車站是「台北車站」的列全部抓出來
    # .sort_values('時段')：將抓出來的資料依照「時段」欄位從小到大排序 (確保時間是 0 到 23 連續的)
    main_station_df = df[df['進站車站'] == '台北車站'].sort_values('時段')
    
    # 將整理好的表格資料，轉換成 Python 基礎的「字典 (Dictionary)」格式
    # 這麼做通常是為了方便把純數據傳遞給繪圖模組，降低對 DataFrame 結構的依賴
    hourly_data = {
        # .tolist() 的功能是把 pandas 欄位 (Series) 轉換成純 Python 的列表 (List)
        'hours': main_station_df['時段'].tolist(),      # 存放 0~23 小時的清單
        'in_flow': main_station_df['進站人數'].tolist(), # 存放各小時進站人數的清單
        'out_flow': main_station_df['出站人數'].tolist() # 存放各小時出站人數的清單
    }
    
    
    # ==========================================
    # 2. 呼叫 analytics 模組進行複雜的聚合運算
    # ==========================================
    
    # 這裡的邏輯被封裝在模組中，主程式看起來就清爽多了！
    # 直接在呼叫函式時，把篩選好時段 (7~9點) 的 DataFrame 當作參數傳進去，算出早尖峰最擠的前 5 名
    am_top5 = get_top_load_stations(df[(df['時段'] >= 7) & (df['時段'] <= 9)])
    
    # 同理，篩選出下午時段 (17~19點) 的資料傳進去，算出晚尖峰進出站落差最大的前 5 名
    pm_top5 = get_top_imbalanced_stations(df[(df['時段'] >= 17) & (df['時段'] <= 19)])
    
    # 把算好的「早尖峰最高負荷」結果也轉成字典
    am_peaks = {
        'stations': am_top5['進站車站'].tolist(), # 車站名稱清單
        'loads': am_top5['total_load'].tolist()   # 總負荷(進+出)清單。註：這裡假設你在 analytics 模組把欄位命名為了 total_load
    }
    
    # 把算好的「晚尖峰最不平衡」結果轉成字典
    pm_unbalances = {
        'stations': pm_top5['進站車站'].tolist(),    # 車站名稱清單
        'imbalances': pm_top5['imbalance'].tolist()  # 不平衡度清單。註：假設欄位命名為 imbalance
    }
    
    
    # ==========================================
    # 3. 散佈圖數據 (計算全部車站全日的總進出站)
    # ==========================================
    
    # 使用 .groupby() 與 .agg() 同時聚合多個欄位
    # .groupby('進站車站')：依照車站名稱分組
    # .agg({'進站人數':'sum', '出站人數':'sum'})：針對不同欄位指定不同的運算，這裡是把進站跟出站都做 'sum' (加總)
    # .reset_index()：把車站名稱從分組索引還原成一般欄位
    all_station = df.groupby('進站車站').agg({'進站人數':'sum', '出站人數':'sum'}).reset_index()
    
    # 再次將結果打包成字典，準備餵給繪圖模組
    all_stations_data = {
        'in_flow': all_station['進站人數'].tolist(),  # 全日總進站清單
        'out_flow': all_station['出站人數'].tolist() # 全日總出站清單
    }
    
    
    # ==========================================
    # 最終階段：匯出所有圖表
    # ==========================================
    print("📊 運算完成，正在呼叫繪圖模組...")
    
    # 將前面辛苦準備好的 4 包字典資料，一口氣丟給 plotter 模組裡的 generate_all_plots 函式去畫圖
    generate_all_plots(am_peaks, pm_unbalances, hourly_data, all_stations_data)
    
    print("✨ 完成！")


# ==========================================
# 程式進入點 (Entry Point)
# ==========================================
# 如果這個 .py 檔案是被直接執行 (例如在終端機打 python main.py)，__name__ 就會等於 '__main__'
# 這樣寫可以確保：如果別人把這隻檔案當成模組 import 進其他程式時，裡面的 main() 不會莫名其妙自動跑起來
if __name__ == '__main__':
    main()
