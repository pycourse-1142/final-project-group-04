import matplotlib.pyplot as plt
import os
import pandas as pd

# ==========================================
# 解決 Matplotlib 中文顯示變方塊(RuntimeError)痛點
# ==========================================
plt.rcParams['font.family'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False # 確保負號 "-" 能正常顯示

def plot_top_load(df_load, title_name="早尖峰人流負荷 Top 5 核心車站"):
    """ 圖一 & 圖二：繪製人流負荷最大排行（橫條圖） """
    print(f"【Plotter】正在繪製: {title_name}...")
    plt.figure(figsize=(9, 5))
    plt.barh(df_load['標準車站'], df_load['總負荷'], color='salmon')
    plt.title(title_name, fontsize=14, fontweight='bold')
    plt.xlabel('總人次 (進站 + 出站)')
    plt.ylabel('車站名稱')
    plt.gca().invert_yaxis()
    
    os.makedirs('results', exist_ok=True)
    plt.savefig(f"results/{title_name}.png", bbox_inches='tight')
    plt.close()

def plot_top_imbalance(df_imbalance, title_name="進出站人流最不平衡 Top 5 核心車站"):
    """ 繪製進出站人流最不平衡排行（橫條圖） """
    print(f"【Plotter】正在繪製: {title_name}...")
    plt.figure(figsize=(9, 5))
    plt.barh(df_imbalance['標準車站'], df_imbalance['不平衡度'], color='orange')
    plt.title(title_name, fontsize=14, fontweight='bold')
    plt.xlabel('不平衡度 ( |進站 - 出站| )')
    plt.ylabel('車站名稱')
    plt.gca().invert_yaxis()
    
    os.makedirs('results', exist_ok=True)
    plt.savefig(f"results/{title_name}.png", bbox_inches='tight')
    plt.close()

def plot_hourly_line(df_line, station_name="台北車站"):
    """ 圖三：樞紐車站 24 小時進出站人流變化折線圖 """
    print(f"【Plotter】正在繪製圖三：{station_name} 24小時人流折線圖...")
    plt.figure(figsize=(10, 5))
    plt.plot(df_line['時段'], df_line['進站人次'], marker='o', label='進站人次', color='blue')
    plt.plot(df_line['時段'], df_line['出站人次'], marker='s', label='出站人次', color='red')
    
    plt.title(f'{station_name} 24 小時進出站人流變化折線圖', fontsize=14, fontweight='bold')
    plt.xlabel('時段 (小時)')
    plt.ylabel('人次')
    plt.xticks(range(0, 24))
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    
    os.makedirs('results', exist_ok=True)
    plt.savefig(f"results/{station_name}_24h_flux.png", bbox_inches='tight')
    plt.close()
    print(f"👉 圖三已儲存至: results/{station_name}_24h_flux.png")

def plot_balance_scatter(df_scatter):
    """ 圖四：全車站進出站平衡度散佈圖 """
    print("【Plotter】正在繪製圖四：全車站進出站平衡度散佈圖...")
    plt.figure(figsize=(8, 8))
    plt.scatter(df_scatter['進站人次'], df_scatter['出站人次'], alpha=0.7, color='purple', edgecolors='k')
    
    # 畫一條 Y=X 的對角基準線
    max_val = max(df_scatter['進站人次'].max(), df_scatter['出站人次'].max())
    plt.plot([0, max_val], [0, max_val], 'r--', label='進出平衡基準線')
    
    plt.title('全車站進出站平衡度散佈圖', fontsize=14, fontweight='bold')
    plt.xlabel('總進站人次')
    plt.ylabel('總出站人次')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    
    os.makedirs('results', exist_ok=True)
    plt.savefig("results/stations_balance_scatter.png", bbox_inches='tight')
    plt.close()
    print("👉 圖四已儲存至: results/stations_balance_scatter.png")