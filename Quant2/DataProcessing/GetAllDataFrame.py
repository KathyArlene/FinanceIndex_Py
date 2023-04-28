import pymysql
import pandas as pd

def read_table_from_database(database, table):
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="Zyyjjdl6543201",
        database=database
    )

    query = f"SELECT * FROM {table}"
    data = pd.read_sql(query, connection)
    connection.close()
    return data

def add_moving_averages(df, close_col, window_sizes):
    for window_size in window_sizes:
        ma_col_name = f"ma{window_size}"
        df[ma_col_name] = df[close_col].rolling(window=window_size).mean()
    return df

# 数据库和股指表名
database_name = "sp500_history"
table_names = ['sp500_data', 'sp500_data_csi1000', 'sp500_data_csi500', 'sp500_data_dax30', 'sp500_data_dji',
               'sp500_data_ftse100', 'sp500_data_hs300', 'sp500_data_nasdaq', 'sp500_data_nikkei225',
               'sp500_data_sse50']

# 要计算的移动平均窗口大小
window_sizes = [5, 10, 20, 60]

# 遍历表名列表，逐个读取股指数据并添加移动平均
for table_name in table_names:
    table_data = read_table_from_database(database_name, table_name)
    table_data = add_moving_averages(table_data, 'close', window_sizes)
    table_data.to_csv(f"{table_name}.csv", index=False)
