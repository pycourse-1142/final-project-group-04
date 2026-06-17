import os
import pandas as pd
# 導入你寫好的模組
from modules.analytics import (
    get_peak_hourly_traffic, 
    get_top_load_stations, 
    get_top_imbalanced_stations
)
from modules.plotter import generate_all_plots

def main():
    csv_path = os.path.join('data', 'taipei_metro_traffic.csv')
    
    if not os.path.exists(csv_path):
        print(f"❌ 找不到資料檔...")
        return
        
    print("🚀 成功讀取資料，呼叫 Analytics 模組進行核心運算...")
    df = pd.read_csv(csv_path)
    
    # 1. 準備 24 小時資料 (透過 analytics 模組獲取)
    main_station_df = df[df['進站車站'] == '台北車站'].sort_values('時段')
    hourly_data = {
        'hours': main_station_df['時段'].tolist(),
        'in_flow': main_station_df['進站人數'].tolist(),
        'out_flow': main_station_df['出站人數'].tolist()
    }
    
    # 2. 呼叫 analytics 模組進行複雜的聚合運算
    # 這裡的邏輯被封裝在模組中，main 看起來清爽多了！
    am_top5 = get_top_load_stations(df[(df['時段'] >= 7) & (df['時段'] <= 9)])
    pm_top5 = get_top_imbalanced_stations(df[(df['時段'] >= 17) & (df['時段'] <= 19)])
    
    am_peaks = {
        'stations': am_top5['進站車站'].tolist(),
        'loads': am_top5['total_load'].tolist()
    }
    
    pm_unbalances = {
        'stations': pm_top5['進站車站'].tolist(),
        'imbalances': pm_top5['imbalance'].tolist()
    }
    
    # 3. 散佈圖數據
    all_station = df.groupby('進站車站').agg({'進站人數':'sum', '出站人數':'sum'}).reset_index()
    all_stations_data = {
        'in_flow': all_station['進站人數'].tolist(),
        'out_flow': all_station['出站人數'].tolist()
    }
    
    print("📊 運算完成，正在呼叫繪圖模組...")
    generate_all_plots(am_peaks, pm_unbalances, hourly_data, all_stations_data)
    print("✨ 完成！")

if __name__ == '__main__':
    main()
