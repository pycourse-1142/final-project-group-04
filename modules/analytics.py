# 匯入 pandas 套件，這是一個 Python 中用於資料清理與分析的強大工具，並將其縮寫為 pd，方便後續在程式中呼叫
import pandas as pd

# ==========================================
# 預設參數設定區 (可由主程式覆寫)
# 這裡定義了全域變數 (常數)，用來設定一些預設值，避免把數字直接寫死在程式碼中 (Hardcode)
# ==========================================

# 設定早上尖峰時段的起始時間為 7 點
DEFAULT_AM_START = 7
# 設定早上尖峰時段的結束時間為 9 點
DEFAULT_AM_END = 9

# 設定下午尖峰時段的起始時間為 17 點 (下午 5 點)
DEFAULT_PM_START = 17
# 設定下午尖峰時段的結束時間為 19 點 (下午 7 點)
DEFAULT_PM_END = 19

# 設定預設要取出的「前 N 名」數量，這裡預設為取前 5 名
DEFAULT_TOP_N = 5


# 定義函式 get_peak_hourly_traffic
# 接收三個參數：包含資料的表格 df (型態為 pd.DataFrame)、起始時段 start_hour (整數) 與結束時段 end_hour (整數)
# 「-> pd.DataFrame」是型別提示 (Type Hint)，告訴開發者這個函式最後會回傳一個 pandas DataFrame
def get_peak_hourly_traffic(df: pd.DataFrame, start_hour: int, end_hour: int) -> pd.DataFrame:
    """
    篩選特定時段，並利用 .groupby() 計算各站進出站總人潮
    """
    
    # 篩選時段
    # df['時段'] >= start_hour：找出時段大於等於起始時間的資料
    # df['時段'] <= end_hour：找出時段小於等於結束時間的資料
    # 將兩者用 '&' (且) 連接，代表必須同時滿足這兩個條件。
    # 接著把符合條件的資料從原本的 df 中篩選出來，存成一個新的變數 peak_df
    peak_df = df[(df['時段'] >= start_hour) & (df['時段'] <= end_hour)]
    
    # 分組加總
    # 1. peak_df.groupby('標準車站')：把資料依照 '標準車站' 這個欄位進行分組 (同一個車站的資料會被歸類在同一組)
    # 2. [['進站人次', '出站人次']]：告訴程式我們分組後，只關心這兩個欄位的數值
    # 3. .sum()：將同一組 (同車站) 的資料相加起來，算出總進站與總出站人次
    # 4. .reset_index()：groupby 之後 '標準車站' 會變成資料的索引 (Index)，用這個方法可以把它還原成一般的資料欄位
    # 將最終結果存成變數 grouped_df
    grouped_df = peak_df.groupby('標準車站')[['進站人次', '出站人次']].sum().reset_index()
    
    # 將計算並整理好的結果回傳出去
    return grouped_df


# 定義函式 get_top_load_stations
# 接收兩個參數：表格 df 與 top_n (若呼叫時沒給 top_n，則預設使用上面的常數 DEFAULT_TOP_N，也就是 5)
# 此函式同樣會回傳一個 pandas DataFrame
def get_top_load_stations(df: pd.DataFrame, top_n: int = DEFAULT_TOP_N) -> pd.DataFrame:
    """
    計算人流負荷最大 (進站 + 出站) 的 Top N 車站
    """
    
    # 這裡的 df 應該先經過 get_peak_hourly_traffic 處理，或是直接傳入全日資料
    # 使用 .copy() 完整複製一份傳入的 dataframe
    # 這是為了避免我們接下來新增欄位的操作，去改動 (污染) 到原本傳進來的原始 df 資料
    df_load = df.copy()
    
    # 在複製出來的表格 df_load 中，建立一個新的欄位叫做 '總負荷'
    # 它的數值來源是將該列的 '進站人次' 加上 '出站人次'
    df_load['總負荷'] = df_load['進站人次'] + df_load['出站人次']
    
    # 多維度排序
    # 1. df_load.sort_values(by='總負荷', ascending=False)：依照剛剛算出來的 '總負荷' 欄位進行排序。
    #    ascending=False 代表使用「降冪排序」(數字最大的排在最上面)
    # 2. .head(top_n)：只取排序結果的「最前面 N 筆」資料 (也就是前 N 名的意思)
    # 把這個排行榜結果存入 top_stations 變數中
    top_stations = df_load.sort_values(by='總負荷', ascending=False).head(top_n)
    
    # 回傳負荷量最大的前 N 名車站資料
    return top_stations


# 定義函式 get_top_imbalanced_stations
# 同樣接收 df 與 top_n，用來找出進出站人流落差最大的車站
def get_top_imbalanced_stations(df: pd.DataFrame, top_n: int = DEFAULT_TOP_N) -> pd.DataFrame:
    """
    計算進出站人流最不平衡 ( |進站 - 出站| ) 的 Top N 車站
    """
    
    # 一樣使用 .copy() 先複製一份資料，避免改動到原始的 dataframe
    df_imbalance = df.copy()
    
    # 絕對值計算不平衡度
    # 建立一個新欄位叫做 '不平衡度'
    # 計算方式是將 '進站人次' 減去 '出站人次'。
    # 外層包一個內建函式 abs()，意思是「取絕對值」。因為我們只在乎落差有多大，不在乎是進站多還是出站多 (確保算出來都是正數)
    df_imbalance['不平衡度'] = abs(df_imbalance['進站人次'] - df_imbalance['出站人次'])
    
    # 排序
    # df_imbalance.sort_values(by='不平衡度', ascending=False)：依照 '不平衡度' 進行降冪排序 (落差越大的排越前面)
    # .head(top_n)：只抓取排行榜最前面的 N 筆資料
    top_stations = df_imbalance.sort_values(by='不平衡度', ascending=False).head(top_n)
    
    # 回傳進出站人潮最不平衡的前 N 名車站資料
    return top_stations
