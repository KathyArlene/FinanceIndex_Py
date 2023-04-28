import baostock as bs
import pandas as pd
import pymysql
import datetime

# 登录baostock系统
lg = bs.login()

# 下载上证50指数的历史数据
ticker = "sh.000016"
start_date = "1900-01-01"
end_date = datetime.datetime.now().strftime("%Y-%m-%d")

fields = "date,code,open,high,low,close,volume,amount,adjustflag"
rs = bs.query_history_k_data_plus(ticker, fields, start_date, end_date, frequency="w")

# 将数据保存到 DataFrame 中
data_list = []
while (rs.error_code == "0") and rs.next():
    data_list.append(rs.get_row_data())
data = pd.DataFrame(data_list, columns=rs.fields)
data["date"] = pd.to_datetime(data["date"])

# 计算涨跌幅
data["涨跌幅"] = data["close"].astype(float).pct_change()
data["最高价"] = data["high"].astype(float)
data["最低价"] = data["low"].astype(float)
data["最终收盘价"] = data["close"].astype(float)

# 仅保留需要的列
data = data[["date", "涨跌幅", "最高价", "最低价", "最终收盘价"]]

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
CREATE TABLE IF NOT EXISTS sp500_data_sse50 (
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
for index, row in data.iterrows():
    date = row["date"].date()
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
    INSERT INTO sp500_data_sse50 (date, pct_change, high, low, close)
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

print("上证50指数的历史数据已成功保存到 MySQL 数据库。")

# 登出baostock系统
bs.logout()
