import pymysql
from datetime import datetime

# 连接到 MySQL 数据库
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="Zyyjjdl6543201",
    database="sp500_history"
)

cursor = connection.cursor()

# 为 2022 年设置起始和结束日期
start_date = datetime(2022, 1, 1)
end_date = datetime(2022, 12, 31)

# 查询数据库中是否有 2022 年的数据
query = f"""
SELECT COUNT(*)
FROM sp500_data_nikkei225
WHERE date BETWEEN '{start_date.date()}' AND '{end_date.date()}';
"""

cursor.execute(query)
num_rows = cursor.fetchone()[0]

# 输出结果
if num_rows > 0:
    print(f"在数据库中找到了 {num_rows} 行 2022 年的数据。")
else:
    print("在数据库中未找到 2022 年的数据。")

# 关闭数据库连接
cursor.close()
connection.close()
