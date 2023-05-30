import tushare as ts
import pandas as pd
import concurrent.futures
import time
import os
import shutil
from tqdm import tqdm
from threading import Lock

ts.set_token('')  # 将'your_token'替换为你的tushare获取的token

pro = ts.pro_api()

# 获取所有上市股票代码
stocks = pro.stock_basic(exchange='', list_status='L', fields='ts_code,list_date')

# 过滤股票
stocks = stocks[~stocks['ts_code'].str.startswith(('300', '301', '688', '8', '4'))]

# 创建一个全局的锁和一个全局的滑动窗口
lock = Lock()
window = []

# 获取当前日期
end_date = time.strftime("%Y%m%d")

# 为每个股票获取日交易数据的函数
def get_daily(stock):
    global window
    with lock:
        now = time.time()
        window = [t for t in window if now - t <= 60]  # 移除超过60秒之前的时间戳
        while len(window) >= 499:  # 如果窗口已满，等待直到有空位
            time.sleep(1)
            now = time.time()
            window = [t for t in window if now - t <= 60]
        window.append(now)  # 添加一个新的时间戳到窗口
    _, stock_info = stock

    # 重试机制
    for _ in range(5):  # 最多尝试5次
        try:
            # 使用pro_bar接口直接获取前复权数据
            df = ts.pro_bar(ts_code=stock_info['ts_code'], adj='qfq', start_date=stock_info['list_date'], end_date=end_date)
            if df.empty:
                return
            df.sort_values(by='trade_date', inplace=True)  # 排序数据
            df.to_csv(f"stock_data/{stock_info['ts_code']}.csv", index=False)
            break  # 如果成功，就跳出循环
        except Exception as e:
            print(f"Failed to get data for {stock_info['ts_code']}, retrying. Error: {e}")
            time.sleep(5)  # 等待5秒再尝试

# 删除旧的'stock_data'文件夹，如果存在的话
if os.path.exists('stock_data'):
    shutil.rmtree('stock_data')

# 创建保存数据的目录
os.makedirs('stock_data')

# 创建一个线程池
with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:  # 将线程池的大小设置为30
    # 使用线程池执行每个任务
    list(tqdm(executor.map(get_daily, stocks.iterrows()), total=len(stocks), ncols=70))

# 遍历所有的股票数据文件
for file in tqdm(os.listdir('stock_data'), ncols=70):
    file_path = os.path.join('stock_data', file)
    df = pd.read_csv(file_path)

    # 删除有缺失值的行
    df.dropna(inplace=True)

    # 重新写入文件
    df.to_csv(file_path, index=False)
