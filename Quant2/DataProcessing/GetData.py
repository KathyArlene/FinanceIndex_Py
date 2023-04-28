import os
import subprocess

# 指定文件夹路径
folder_path = r'C:\Quant2\Indexs'

# 获取文件夹中所有的.py文件
files = [f for f in os.listdir(folder_path) if f.endswith('.py')]

# 遍历每个文件，并使用subprocess模块运行它们
for f in files:
    # 拼接文件的完整路径
    file_path = os.path.join(folder_path, f)
    print(f'Running {file_path}...')
    subprocess.run(['python', file_path])
