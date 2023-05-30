import akshare as ak
import pandas as pd
import os
import time
import datetime
import calendar

# 获取上一个工作日的日期
current_date = datetime.datetime.now()
while current_date.weekday() == calendar.SATURDAY or current_date.weekday() == calendar.SUNDAY:
    current_date -= datetime.timedelta(days=1)
last_workday = current_date.strftime('%Y-%m-%d')

# 获取沪深A股股票列表
stock_list = ak.stock_zh_a_spot_em()

# 剔除以300, 688, 和 8开头的股票
stock_list = stock_list[~stock_list['代码'].str.startswith(('300', '688', '8'))]

# 创建一个新的目录来存储CSV文件
if not os.path.exists('stock_data_Akshare'):
    os.makedirs('stock_data_Akshare')

# 设置一个固定的开始日期
start_date = '2000-01-01'

# 为每只股票获取历史数据
for index, row in stock_list.iterrows():
    print(f"Fetching data for stock: {row['代码']}")

    # 获取历史数据
    try:
        stock_df = ak.stock_zh_a_hist(symbol=row['代码'], start_date=start_date, end_date=last_workday)
        if stock_df.empty:
            print(f"No data fetched for stock: {row['代码']}")
            continue
        else:
            print(f"Data fetched for stock: {row['代码']}")
    except Exception as e:
        print(f"Error fetching data for stock: {row['代码']}, error: {str(e)}")
        continue

    # 将数据保存为CSV文件
    csv_file = f'stock_data_Akshare/{row["代码"]}.csv'
    try:
        stock_df.to_csv(csv_file, index=False)
        print(f"Data for stock {row['代码']} has been written to {csv_file}")
    except Exception as e:
        print(f"Error writing to {csv_file}: {str(e)}")

    # 每次请求之后休眠1秒
    time.sleep(1)
