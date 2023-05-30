import os
import pandas as pd

# 获取所有的股票文件
stock_files = os.listdir('stock_data')

# 对每个股票文件进行处理
for file_name in stock_files:
    # 读取股票数据
    stock_data = pd.read_csv(os.path.join('stock_data', file_name))

    # 检查每一列是否有缺失值
    for column in stock_data.columns:
        # 如果这一列有缺失值
        if stock_data[column].isnull().any():
            print(f'Stock {file_name} has missing values in column {column}.')
