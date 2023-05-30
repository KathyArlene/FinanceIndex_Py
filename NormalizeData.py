import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm

# 原数据存储的目录
data_dir = 'stock_data'

# 标准化后数据存储的目录
normalized_data_dir = 'normalized_stock_data'

# 如果目标目录不存在，则创建
if not os.path.exists(normalized_data_dir):
    os.makedirs(normalized_data_dir)

# 初始化StandardScaler
scaler = StandardScaler()

# 遍历目录中的所有文件
for filename in tqdm(os.listdir(data_dir), desc='Normalizing data:', ncols=70):
    # 构造完整的文件路径
    file_path = os.path.join(data_dir, filename)

    # 读取数据
    data = pd.read_csv(file_path)

    # 提取用于标准化的列
    columns_to_normalize = ['open', 'high', 'low', 'close', 'pre_close', 'change', 'pct_chg', 'vol', 'amount']
    data_to_normalize = data[columns_to_normalize]

    # 对数据进行标准化
    normalized_data = scaler.fit_transform(data_to_normalize)

    # 将标准化后的数据替换原来的数据
    data[columns_to_normalize] = normalized_data

    # 构造新的文件路径
    new_file_path = os.path.join(normalized_data_dir, filename)

    # 将处理过的数据写入新文件
    data.to_csv(new_file_path, index=False)
