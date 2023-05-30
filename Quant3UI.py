import tkinter as tk
from tkinter import scrolledtext
import subprocess

# 创建主窗口
root = tk.Tk()

# 设置窗口标题
root.title('Quant3')

# 设置主窗口大小为800x600
root.geometry("800x600")

# 创建一个回调函数来处理按钮点击事件
def on_button_click():
    # 创建一个新的Tkinter窗口
    new_window = tk.Toplevel(root)

    # 设置新窗口的标题
    new_window.title('股票代码')

    # 设置新窗口的大小
    new_window.geometry("600x400")

    # 创建一个ScrolledText
    scrolly = scrolledtext.ScrolledText(new_window)

    # 运行StockCodes.py并获取输出
    result = subprocess.run(['python', 'StockCodes.py'], stdout=subprocess.PIPE)

    # 在ScrolledText中显示输出
    scrolly.insert(tk.INSERT, result.stdout.decode('utf-8'))
    scrolly.pack()

# 创建一个按钮，点击时运行on_button_click函数
button = tk.Button(root, text="股票代码查询", command=on_button_click)
button.pack()

# 启动消息循环
root.mainloop()
