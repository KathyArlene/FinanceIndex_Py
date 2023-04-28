import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

# 读取训练数据和测试数据
train_data = pd.read_csv(r'C:\Quant2\DataProcessing\train_data.csv')
test_data = pd.read_csv(r'C:\Quant2\DataProcessing\test_data.csv')
# 处理训练数据和测试数据中的缺失值
train_data.fillna(method='ffill', inplace=True)
train_data.fillna(method='bfill', inplace=True)

test_data.fillna(method='ffill', inplace=True)
test_data.fillna(method='bfill', inplace=True)

# 定义要预测的目标变量（例如收盘价）
target_column = 'sp500_data_csi500_close'

# 选择训练数据和测试数据的特征列（这里我们选择除了“date”和目标变量之外的所有列）
feature_columns = [col for col in train_data.columns if col not in ['date', target_column]]

# 划分训练集和验证集
X_train, X_val, y_train, y_val = train_test_split(train_data[feature_columns], train_data[target_column], test_size=0.2, random_state=42)

# 训练随机森林回归模型
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 验证模型在验证集上的性能
val_predictions = model.predict(X_val)
mse = mean_squared_error(y_val, val_predictions)
print(f'Validation MSE: {mse}')

# 使用训练好的模型预测测试数据
test_predictions = model.predict(test_data[feature_columns])

# 保存预测结果到一个新的 DataFrame
test_data['predictions'] = test_predictions
print(test_data[['date', target_column, 'predictions']].head())

# 可以将预测结果保存到一个新的 CSV 文件
test_data.to_csv('test_data_with_predictions.csv', index=False)
