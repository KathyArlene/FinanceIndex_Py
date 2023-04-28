import yfinance as yf
import pandas as pd
import pymysql

# 下载德国DAX30指数的历史数据
ticker = "^GDAXI"
start_date = "1900-01-01"
end_date = pd.to_datetime("today")

data = yf.download(ticker, start=start_date, end=end_date)

# 计算每周数据
data_weekly = data.resample("W").agg({"Open": "first", "High": "max", "Low": "min", "Close": "last"})
data_weekly["涨跌幅"] = data_weekly["Close"].pct_change()
data_weekly = data_weekly.reset_index()

# 连接到 MySQL 数据库
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="Zyyjjdl6543201"
)

cursor = connection.cursor()

# 使用之前创建的数据库
use_database_query = """
USE sp500_history;
"""

cursor.execute(use_database_query)
connection.commit()

# 在 MySQL 中创建新表（如果不存在）
create_table_query = """
CREATE TABLE IF NOT EXISTS sp500_data_dax30 (
    date DATE PRIMARY KEY,
    pct_change FLOAT,
    high FLOAT,
    low FLOAT,
    close FLOAT
);
"""

cursor.execute(create_table_query)
connection.commit()

# 将数据插入到 MySQL 数据库中
for index, row in data_weekly.iterrows():
    date = row["Date"].date()
    pct_change = row["涨跌幅"]
    high = row["High"]
    low = row["Low"]
    close = row["Close"]

    # 如果数值列包含 NaN，将其替换为 NULL
    pct_change = "NULL" if pd.isna(pct_change) else pct_change
    high = "NULL" if pd.isna(high) else high
    low = "NULL" if pd.isna(low) else low
    close = "NULL" if pd.isna(close) else close

    insert_query = f"""
    INSERT INTO sp500_data_dax30 (date, pct_change, high, low, close)
    VALUES ('{date}', {pct_change}, {high}, {low}, {close})
    ON DUPLICATE KEY UPDATE
        pct_change = VALUES(pct_change),
        high = VALUES(high),
        low = VALUES(low),
        close = VALUES(close);
    """

    cursor.execute(insert_query)
    connection.commit()

# 关闭数据库连接
cursor.close()
connection.close()

print("德国DAX30指数的历史数据已成功保存到 MySQL 数据库。")
