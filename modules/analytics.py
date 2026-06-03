import pandas as pd

# 預設參數設定區 (可由主程式覆寫)
DEFAULT_AM_START = 7
DEFAULT_AM_END = 9
DEFAULT_PM_START = 17
DEFAULT_PM_END = 19
DEFAULT_TOP_N = 5

def get_peak_hourly_traffic(df: pd.DataFrame, start_hour: int, end_hour: int) -> pd.DataFrame:
    """
    任務 1 & 2：篩選特定時段，並利用 .groupby() 計算各站進出站總人潮
    """
    # 篩選時段
    peak_df = df[(df['時段'] >= start_hour) & (df['時段'] <= end_hour)]
    
    # 分組加總
    grouped_df = peak_df.groupby('標準車站')[['進站人次', '出站人次']].sum().reset_index()
    
    return grouped_df

def get_top_load_stations(df: pd.DataFrame, top_n: int = DEFAULT_TOP_N) -> pd.DataFrame:
    """
    任務 3A：計算人流負荷最大 (進站 + 出站) 的 Top N 車站
    """
    # 這裡的 df 應該先經過 get_peak_hourly_traffic 處理，或是直接傳入全日資料
    df_load = df.copy()
    df_load['總負荷'] = df_load['進站人次'] + df_load['出站人次']
    
    # 多維度排序
    top_stations = df_load.sort_values(by='總負荷', ascending=False).head(top_n)
    
    return top_stations

def get_top_imbalanced_stations(df: pd.DataFrame, top_n: int = DEFAULT_TOP_N) -> pd.DataFrame:
    """
    任務 3B：計算進出站人流最不平衡 ( |進站 - 出站| ) 的 Top N 車站
    """
    df_imbalance = df.copy()
    # 絕對值計算不平衡度
    df_imbalance['不平衡度'] = abs(df_imbalance['進站人次'] - df_imbalance['出站人次'])
    
    # 排序
    top_stations = df_imbalance.sort_values(by='不平衡度', ascending=False).head(top_n)
    
    return top_stations
