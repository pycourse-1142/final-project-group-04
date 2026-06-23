# 匯入 matplotlib 的 pyplot 模組，這是 Python 最核心的繪圖庫，並縮寫為 plt 方便呼叫
import matplotlib.pyplot as plt

# 匯入內建的 os 套件，用來檢查或建立儲存圖片的資料夾
import os

# 匯入 pandas 套件，用於處理傳入的 DataFrame 資料型態，並縮寫為 pd
import pandas as pd

# ==========================================
# 解決 Matplotlib 中文顯示變方塊(RuntimeError)痛點
# ==========================================
# Matplotlib 預設不支援中文，如果不設定字型，中文字會變成一堆無意義的「方塊 (□)」
# 這裡將繪圖的預設字型設定為「微軟正黑體 (Microsoft JhengHei)」
plt.rcParams['font.family'] = ['Microsoft JhengHei'] 

# 解決設定中文新字型後，圖表中的負號 "-" 會變成亂碼或無法顯示的問題
# 設定為 False 可以確保負號能以正常的符號渲染出來
plt.rcParams['axes.unicode_minus'] = False 


# 定義函式 plot_top_load：繪製人流負荷量最大的前 N 名車站
# 接收兩個參數：df_load (包含車站與負荷量資料) 與 title_name (圖表標題，有預設值)
def plot_top_load(df_load, title_name="早尖峰人流負荷 Top 5 核心車站"):
    """ 圖一 & 圖二：繪製人流負荷最大排行（橫條圖） """
    
    # 在終端機印出目前的繪圖進度，方便追蹤程式執行到哪裡
    print(f"【Plotter】正在繪製: {title_name}...")
    
    # 初始化一個新的圖表視窗，並設定畫布大小為寬 9 英吋、高 5 英吋
    plt.figure(figsize=(9, 5))
    
    # 繪製「水平條形圖 (Horizontal Bar Chart)」
    # y=df_load['標準車站']：縱軸為車站名稱
    # width=df_load['總負荷']：橫軸的長度為總負荷人數
    # color='salmon'：將條形圖的顏色設定為鮭魚紅 (salmon)
    plt.barh(df_load['標準車站'], df_load['總負荷'], color='salmon')
    
    # 設定圖表的標題名稱，並調整字型大小為 14、字體加粗 (bold)
    plt.title(title_name, fontsize=14, fontweight='bold')
    
    # 設定橫座標 (X軸) 的標籤名稱
    plt.xlabel('總人次 (進站 + 出站)')
    
    # 設定縱座標 (Y軸) 的標籤名稱
    plt.ylabel('車站名稱')
    
    # plt.gca() 代表「取得當前的座標軸 (Get Current Axes)」
    # .invert_yaxis() 的功能是「上下反轉 Y 軸」。
    # 因為條形圖預設會把第一筆資料畫在最下面，反轉後才能讓第一名（最多人）保持在最上面
    plt.gca().invert_yaxis()
    
    # 使用 os.makedirs 建立一個名為 'results' 的資料夾。
    # exist_ok=True 代表「如果資料夾已經存在，就忽略不用重複建立」，防止程式噴錯
    os.makedirs('results', exist_ok=True)
    
    # 將繪製好的圖表儲存為 PNG 圖片，路徑在 results 資料夾底下，檔名就是標題名稱
    # bbox_inches='tight' 是一個非常重要的設定，它會自動計算並裁剪掉圖表四周多餘的留白，
    # 同時確保邊緣的文字（如車站名稱）不會因為太長而被切掉
    plt.savefig(f"results/{title_name}.png", bbox_inches='tight')
    
    # 關閉目前的圖表視窗，釋放記憶體。
    # 如果不關閉，接下來畫下一張圖時，兩張圖的資料可能會重疊在同一個畫布上
    plt.close()


# 定義函式 plot_top_imbalance：繪製進出站最不平衡（落差最大）的車站排行
# 邏輯與上一個函式幾乎完全相同，只是傳入的資料和欄位不同
def plot_top_imbalance(df_imbalance, title_name="進出站人流最不平衡 Top 5 核心車站"):
    """ 繪製進出站人流最不平衡排行（橫條圖） """
    
    # 印出進度提示
    print(f"【Plotter】正在繪製: {title_name}...")
    
    # 開啟新圖表，設定大小為 9x5 英吋
    plt.figure(figsize=(9, 5))
    
    # 繪製水平條形圖，橫軸數值改為 '不平衡度'，顏色換成橘色 (orange)
    plt.barh(df_imbalance['標準車站'], df_imbalance['不平衡度'], color='orange')
    
    # 設定標題（字型 14、加粗）
    plt.title(title_name, fontsize=14, fontweight='bold')
    
    # 設定 X 軸與 Y 軸的標籤
    plt.xlabel('不平衡度 ( |進站 - 出站| )')
    plt.ylabel('車站名稱')
    
    # 反轉 Y 軸，讓最不平衡（落差最大）的第一名車站排在最上方
    plt.gca().invert_yaxis()
    
    # 確保儲存資料夾存在
    os.makedirs('results', exist_ok=True)
    
    # 儲存圖片，並自動校正文字邊界
    plt.savefig(f"results/{title_name}.png", bbox_inches='tight')
    
    # 關閉圖表釋放記憶體
    plt.close()


# 定義函式 plot_hourly_line：繪製特定車站 24 小時的進出站人流趨勢
# 接收 df_line (時間序列資料) 與 station_name (車站名稱，預設為台北車站)
def plot_hourly_line(df_line, station_name="台北車站"):
    """ 圖三：樞紐車站 24 小時進出站人流變化折線圖 """
    
    # 印出進度提示
    print(f"【Plotter】正在繪製圖三：{station_name} 24小時人流折線圖...")
    
    # 開啟一個較寬的圖表視窗（寬 10 英吋、高 5 英吋），因為 24 小時的橫軸需要較多空間展示
    plt.figure(figsize=(10, 5))
    
    # 繪製第一條折線：進站人次趨勢
    # x=時段, y=進站人次
    # marker='o'：在每個數據點上加上「圓形」標記
    # label='進站人次'：設定這條線的名稱，後續會顯示在圖例 (Legend) 中
    # color='blue'：線條顏色設定為藍色
    plt.plot(df_line['時段'], df_line['進站人次'], marker='o', label='進站人次', color='blue')
    
    # 繪製第二條折線：出站人次趨勢，畫在同一個畫布上
    # marker='s'：在每個數據點上加上「方形 (Square)」標記，方便與進站做視覺區隔
    # label='出站人次'：設定圖例名稱
    # color='red'：線條顏色設定為紅色
    plt.plot(df_line['時段'], df_line['出站人次'], marker='s', label='出站人次', color='red')
    
    # 設定圖表標題（動態代入車站名稱，字型 14、加粗）
    plt.title(f'{station_name} 24 小時進出站人流變化折線圖', fontsize=14, fontweight='bold')
    
    # 設定 X 軸與 Y 軸標籤
    plt.xlabel('時段 (小時)')
    plt.ylabel('人次')
    
    # 強制設定 X 軸的刻度
    # range(0, 24) 會產生 0 到 23 的整數，這樣能確保圖表 X 軸會乖乖顯示 0, 1, 2... 一直到 23 點，不會漏掉
    plt.xticks(range(0, 24))
    
    # 開啟圖表的背景網格線
    # True：顯示網格
    # linestyle='--'：網格線使用「虛線」
    # alpha=0.6：透明度設為 0.6 (60%)，讓網格淡淡的就好，不會搶走主要折線的風采
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # 顯示圖例（也就是在右上角或合適位置顯示「藍色圓點=進站人次」、「紅色方塊=出站人次」的對照表）
    plt.legend()
    
    # 檢查並建立 results 資料夾
    os.makedirs('results', exist_ok=True)
    
    # 儲存圖片，檔名包含車站名稱，例如 "results/台北車站_24h_flux.png"
    plt.savefig(f"results/{station_name}_24h_flux.png", bbox_inches='tight')
    
    # 關閉圖表
    plt.close()
    
    # 在終端機印出儲存成功的路徑訊息
    print(f"👉 圖三已儲存至: results/{station_name}_24h_flux.png")


# 定義函式 plot_balance_scatter：繪製所有車站的進出站平衡度散佈圖
# 接收包含所有車站進出總人數的 df_scatter
def plot_balance_scatter(df_scatter):
    """ 圖四：全車站進出站平衡度散佈圖 """
    
    # 印出進度提示
    print("【Plotter】正在繪製圖圖四：全車站進出站平衡度散佈圖...")
    
    # 開啟一個長寬相等的正方形圖表（8x8 英吋）。
    # 因為散佈圖的 X 軸與 Y 軸單位相同（都是人次），正方形最能直觀看出點有沒有偏離對角線
    plt.figure(figsize=(8, 8))
    
    # 繪製「散佈圖 (Scatter Plot)」，每個車站會變成圖上的一個點
    # x=進站人次, y=出站人次
    # alpha=0.7：點的透明度為 70%。這樣當很多車站的點重疊在一起時，顏色會變深，看得出數據的集中度
    # color='purple'：點的填滿顏色為紫色
    # edgecolors='k'：'k' 代表黑色 (Black)，這會幫每個點加上黑色外框，讓點更清晰
    plt.scatter(df_scatter['進站人次'], df_scatter['出站人次'], alpha=0.7, color='purple', edgecolors='k')
    
    # 畫一條 Y=X 的對角基準線（用來判斷誰進出平衡）
    # 1. 找出進站人次和出站人次兩者中的「絕對最大值」
    max_val = max(df_scatter['進站人次'].max(), df_scatter['出站人次'].max())
    
    # 2. 畫線：[0, max_val] 作為 X 範圍，[0, max_val] 作為 Y 範圍
    # 'r--'：'r' 代表紅色 (Red)，'--' 代表虛線 (Dashed)
    # label='進出平衡基準線'：設定這條基準線的圖例名稱
    # 這條線上的點代表「進站人數剛好等於出站人數」，偏離這條線越遠代表越不平衡
    plt.plot([0, max_val], [0, max_val], 'r--', label='進出平衡基準線')
    
    # 設定圖表標題（字型 14、加粗）
    plt.title('全車站進出站平衡度散佈圖', fontsize=14, fontweight='bold')
    
    # 設定 X 軸與 Y 軸標籤
    plt.xlabel('總進站人次')
    plt.ylabel('總出站人次')
    
    # 開啟背景網格（虛線，50% 透明度）
    plt.grid(True, linestyle='--', alpha=0.5)
    
    # 顯示圖例（包含紫色點與紅色虛線的對照說明）
    plt.legend()
    
    # 檢查並建立 results 資料夾
    os.makedirs('results', exist_ok=True)
    
    # 儲存圖片
    plt.savefig("results/stations_balance_scatter.png", bbox_inches='tight')
    
    # 關閉圖表釋放記憶體
    plt.close()
    
    # 印出儲存成功訊息
    print("👉 圖四已儲存至: results/stations_balance_scatter.png")
