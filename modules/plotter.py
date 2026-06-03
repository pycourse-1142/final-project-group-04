import matplotlib.pyplot as plt
import os
import pandas as pd

# ==========================================
# 解決 Matplotlib 中文顯示變方塊(RuntimeError)痛點
# ==========================================
# Windows 學校電腦通常都有微軟正黑體 (Microsoft JhengHei)
plt.rcParams['font.family'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False # 確保負號 "-" 能正常顯示

def plot_top_load(df_load, title_name="早尖峰人流負荷 Top 5 車站"):
    """
    圖一 & 圖二：繪製人流負荷最大排行（橫條圖）
    """
    print(f"【Plotter】正在繪製: {title_name}...")
    
    plt.figure(figsize=(9, 5))
    # 根據運算模組產出的欄位 '標準車站' 與 '總負荷' 畫圖
    plt.barh(df_load['標準車站'], df_load['總負荷'], color='salmon')
    plt.title(title_name, fontsize=14, fontweight='bold')
    plt.xlabel('總人次 (進站 + 出站)')
    plt.ylabel('車站名稱')
    plt.gca().invert_yaxis() # 讓第一名在最上面
    
    # 建立與確保結果存入 results/ 資料夾
    os.makedirs('results', exist_ok=True)
    file_name = f"results/{title_name}.png"
    plt.savefig(file_name, bbox_inches='tight')
    plt.close()
    print(f"👉 圖片已成功儲存至: {file_name}")

def plot_top_imbalance(df_imbalance, title_name="進出站人流最不平衡 Top 5 車站"):
    """
    繪製進出站人流最不平衡排行（橫條圖）
    """
    print(f"【Plotter】正在繪製: {title_name}...")
    
    plt.figure(figsize=(9, 5))
    plt.barh(df_imbalance['標準車站'], df_imbalance['不平衡度'], color='orange')
    plt.title(title_name, fontsize=14, fontweight='bold')
    plt.xlabel('不平衡度 ( |進站 - 出站| )')
    plt.ylabel('車站名稱')
    plt.gca().invert_yaxis()
    
    os.makedirs('results', exist_ok=True)
    file_name = f"results/{title_name}.png"
    plt.savefig(file_name, bbox_inches='tight')
    plt.close()
    print(f"👉 圖片已成功儲存至: {file_name}")

def plot_hourly_line(df_line):
    """
    圖三：樞紐車站 24 小時進出站人流變化折線圖 (預留整合介面)
    """
    print("【Plotter】圖三折線圖功能已就緒，等待運算模組數據對接...")
    pass

def plot_balance_scatter(df_scatter):
    """
    圖四：全車站進出站平衡度散佈圖 (預留整合介面)
    """
    print("【Plotter】圖四散佈圖功能已就緒，等待運算模組數據對接...")
    pass