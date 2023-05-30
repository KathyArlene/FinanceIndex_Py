import tushare as ts

ts.set_token('349ca319dbbeccf6f67d150f1c68deff9d74261c7c3689071abfd41d')  # 将'your_token'替换为你的tushare获取的token

pro = ts.pro_api()

# 获取沪深A股列表
data = pro.stock_basic(exchange='', list_status='L', fields='ts_code')

# 打印所有股票代码
for index, row in data.iterrows():
    print(row['ts_code'])
