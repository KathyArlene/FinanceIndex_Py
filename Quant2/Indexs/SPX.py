import yfinance as yf
import pandas as pd
import pymysql
import datetime
# 下载标普500的历史数据
ticker = "^GSPC"
end_date = datetime.datetime.now().strftime("%Y-%m-%d")
data = yf.download(ticker, start="1900-01-01", end=end_date)

# 重采样为每周数据，并计算涨跌幅、最高价、最低价和最终收盘价
data_weekly = data.resample("W").agg({
    "Open": "first",
    "High": "max",
    "Low": "min",
    "Close": "last",
    "Volume": "sum",
    "Adj Close": "last"
})

data_weekly["涨跌幅"] = data_weekly["Adj Close"].pct_change()
data_weekly["最高价"] = data_weekly["High"]
data_weekly["最低价"] = data_weekly["Low"]
data_weekly["最终收盘价"] = data_weekly["Close"]

# 仅保留需要的列
data_weekly = data_weekly[["涨跌幅", "最高价", "最低价", "最终收盘价"]]

# 连接到 MySQL 数据库
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="Zyyjjdl6543201"
)

cursor = connection.cursor()

# 在 MySQL 中创建新数据库（如果不存在）
create_database_query = """
CREATE DATABASE IF NOT EXISTS sp500_history;
"""

cursor.execute(create_database_query)
connection.commit()

# 使用新创建的数据库
use_database_query = """
USE sp500_history;
"""

cursor.execute(use_database_query)
connection.commit()

# 在 MySQL 中创建新表（如果不存在）
create_table_query = """
CREATE TABLE IF NOT EXISTS sp500_data (
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
    date = index.date()
    pct_change = row["涨跌幅"]
    high = row["最高价"]
    low = row["最低价"]
    close = row["最终收盘价"]

    # 如果数值列包含 NaN，将其替换为 NULL
    pct_change = "NULL" if pd.isna(pct_change) else pct_change
    high = "NULL" if pd.isna(high) else high
    low = "NULL" if pd.isna(low) else low
    close = "NULL" if pd.isna(close) else close

    insert_query = f"""
    INSERT INTO sp500_data (date, pct_change, high, low, close)
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

print("数据已成功保存到 MySQL 数据库。")

