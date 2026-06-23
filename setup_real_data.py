# 匯入內建的 os 套件，處理資料夾與檔案路徑
import os

# 匯入 pandas 套件，用於資料表處理與輸出 CSV，縮寫為 pd
import pandas as pd

# 匯入 numpy 套件，這是一個強大的科學運算庫，這裡主要借用它的「亂數產生器」來模擬人潮，縮寫為 np
import numpy as np


# ==========================================
# 1. 產生模擬真實捷運人流的 CSV 資料檔
# ==========================================

# 檢查當前目錄下有沒有 'data' 這個資料夾，沒有的話就自動建立一個
# exist_ok=True 代表如果資料夾已經存在，程式不會報錯崩潰，會默默略過
os.makedirs('data', exist_ok=True)

# 組合出我們要把假資料存進去的目標路徑：data/taipei_metro_traffic.csv
csv_path = os.path.join('data', 'taipei_metro_traffic.csv')

# 印出提示訊息，讓使用者知道程式開始做事了
print("⏳ 正在產生台北捷運真實欄位結構數據 (包含 24 小時人流分佈)...")

# 設定一個清單，包含我們想模擬的 8 個台北捷運核心樞紐車站
stations = ['台北車站', '市政府', '西門', '忠孝復興', '板橋', '淡水', '中山', '松江南京']

# list(range(24)) 會產生一個從 0 到 23 的整數清單，代表一天的 24 小時
hours = list(range(24))

# 建立一個空的清單 rows，等一下用來收集每一筆生成的資料列
rows = []

# 設定 numpy 亂數的「種子 (Seed)」。
# 只要設定了固定的數字 (例如 42)，每次執行這支程式產生的亂數都會一模一樣，方便測試與重現結果
np.random.seed(42)


# 開始雙層迴圈：對「每一個車站」的「每一個小時」進行運算
for station in stations:
    for hour in hours:
        
        # 根據時間軸，模擬通勤「雙峰現象」(早尖峰與晚尖峰) 的人流基數
        if 7 <= hour <= 9:  # 早尖峰時段 (早上 7 點到 9 點)
            
            # 使用 np.random.randint(下限, 上限) 產生隨機整數
            # 模擬進站：如果不是市政府站，進站人數設很高(4000~8000)；市政府站早上主要是出站上班，所以進站人數設低一點(2000~4000)
            base_in = np.random.randint(4000, 8000) if station != '市政府' else np.random.randint(2000, 4000)
            
            # 模擬出站：特定商業/辦公大站(北車、市府、忠孝)早上出站人潮爆滿(5000~9000)，其他站普通(1500~3000)
            base_out = np.random.randint(5000, 9000) if station in ['台北車站', '市政府', '忠孝復興'] else np.random.randint(1500, 3000)
            
        elif 17 <= hour <= 19:  # 晚尖峰時段 (下午 5 點到 7 點，下班時間)
            
            # 晚尖峰邏輯剛好反過來，辦公大站(市府、北車)進站準備回家的人爆滿(6000~10000)，其他站普通
            base_in = np.random.randint(6000, 10000) if station in ['市政府', '台北車站'] else np.random.randint(2000, 4500)
            
            # 大家回到各自的居住地，所以所有站的出站人數都滿高的(4000~8000)
            base_out = np.random.randint(4000, 8000)
            
        else:  # 離峰時段與深夜
            
            # hour >= 6 代表白天離峰(6點後)，給予基礎人流(200~1500)；否則就是凌晨 0~5 點，人流趨近於 0 (0~5人)
            base_in = np.random.randint(200, 1500) if hour >= 6 else np.random.randint(0, 5)
            base_out = np.random.randint(200, 1500) if hour >= 6 else np.random.randint(0, 5)
            
        # 將剛剛算好這一個小時的資料，包裝成一個「字典 (Dictionary)」，並加入 rows 清單中
        rows.append({
            '日期': '2026-06-10', # 假日期
            '時段': hour,
            '進站車站': station,
            '出站車站': station,  # 這裡為求方便，假設進出站算在同一個維度，便於後續聚合運算
            '進站人數': base_in,
            '出站人數': base_out
        })

# 迴圈結束後，將塞滿幾百筆字典資料的 rows 清單，轉換成 pandas 的 DataFrame 表格
df = pd.DataFrame(rows)

# 將表格輸出成實體的 CSV 檔案
# index=False：不要把表格最左邊的 0,1,2,3 索引號碼存進去
# encoding='utf-8-sig'：針對微軟 Excel 優化的萬用中文編碼，防止 Windows 開啟 CSV 時中文變亂碼
df.to_csv(csv_path, index=False, encoding='utf-8-sig')

# 印出 CSV 產生成功提示
print(f"✅ 成功在 {csv_path} 生成北捷真實結構數據檔！")


# ==========================================
# 2. 自動改寫最外層的主程式 (main.py)
# ==========================================

# 建立一個超級巨大的「多行字串 (用三個雙引號包起來)」，把整份新的 Python 程式碼當成純文字存入變數 main_code
# 這段文字的內容，就是一個會去讀取我們的 CSV、進行 groupby 資料分組聚合、然後畫圖的新版 main.py！
main_code = """import os
import pandas as pd
from modules.plotter import generate_all_plots

def main():
    csv_path = os.path.join('data', 'taipei_metro_traffic.csv')
    
    # 防禦性設計：如果找不到 CSV 就報錯並退出
    if not os.path.exists(csv_path):
        print(f"❌ 找不到資料檔：{csv_path}，請先執行 setup_real_data.py！")
        return
        
    print("🚀 成功讀取真實資料來源 [taipei_metro_traffic.csv]，開始進行資料清洗與聚合分析...")
    
    # 讀取剛剛產出的 CSV
    df = pd.read_csv(csv_path)
    
    # 1. 24小時流量 (以台北車站為例)，並轉成列表清單
    main_station_df = df[df['進站車站'] == '台北車站'].sort_values('時段')
    hourly_data = {
        'hours': main_station_df['時段'].tolist(),
        'in_flow': main_station_df['進站人數'].tolist(),
        'out_flow': main_station_df['出站人數'].tolist()
    }
    
    # 2. 算出各站早尖峰總流量 (進站+出站) 排行榜
    am_df = df[(df['時段'] >= 7) & (df['時段'] <= 9)]
    # 使用 groupby 和 agg 把進出站人數加總，並把車站從 index 變回欄位
    am_station = am_df.groupby('進站車站').agg({'進站人數':'sum', '出站人數':'sum'}).reset_index()
    # 新增欄位 'total_load' 等於進站加出站
    am_station['total_load'] = am_station['進站人數'] + am_station['出站人數']
    # 降冪排序，抓前 5 名
    am_top5 = am_station.sort_values('total_load', ascending=False).head(5)
    
    am_peaks = {
        'stations': am_top5['進站車站'].tolist(),
        'loads': am_top5['total_load'].tolist()
    }
