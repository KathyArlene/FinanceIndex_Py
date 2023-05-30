import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
from pandas.plotting import register_matplotlib_converters
import os
import math
import tkinter as tk
from PIL import Image, ImageTk

# 注册matplotlib转换器以处理pandas时间戳
register_matplotlib_converters()


def satisfy_condition(df):
    recent_data = df.iloc[-6:]

    # Condition 1: Rise for first 2 days and fall for the next 4 days
    rise_days1 = recent_data.iloc[0:2]
    fall_days1 = recent_data.iloc[2:]
    condition1 = (rise_days1['close'].iloc[-1] / rise_days1['close'].iloc[0] - 1) > 0.10 and (fall_days1['close'].iloc[-1] / fall_days1['close'].iloc[0] - 1) < -0.06

    # Condition 2: Rise for first 3 days and fall for the next 3 days
    rise_days2 = recent_data.iloc[0:3]
    fall_days2 = recent_data.iloc[3:]
    condition2 = (rise_days2['close'].iloc[-1] / rise_days2['close'].iloc[0] - 1) > 0.10 and (fall_days2['close'].iloc[-1] / fall_days2['close'].iloc[0] - 1) < -0.06


    return condition1 or condition2


files = os.listdir('stock_data')
satisfy_stocks = {}
for file in files:
    df = pd.read_csv(f'stock_data/{file}')
    df['trade_date'] = pd.to_datetime(df['trade_date'])
    df.set_index('trade_date', inplace=True)
    df = df[['open', 'high', 'low', 'close', 'vol']].astype(float)
    df.rename(columns={'vol': 'volume'}, inplace=True)
    if len(df) < 6:
        continue
    if satisfy_condition(df):
        satisfy_stocks[file[:-4]] = df

if len(satisfy_stocks) == 0:
    print("No stocks satisfy the condition.")
    exit()

stocks_per_page = 6
num_pages = math.ceil(len(satisfy_stocks) / stocks_per_page)

root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()


def draw_plot(page):
    start = (page - 1) * stocks_per_page
    end = page * stocks_per_page
    current_stocks = list(satisfy_stocks.items())[start:end]
    fig, axes = plt.subplots(nrows=math.ceil(len(current_stocks) / 2), ncols=2,
                             figsize=(screen_width / 120, screen_height / 120), squeeze=False)
    axes = axes.flatten()
    for ax in axes[len(current_stocks):]:
        fig.delaxes(ax)
    for idx, (code, stock_df) in enumerate(current_stocks):
        ax = axes[idx]
        stock_df = stock_df[-15:]  # 只保留最近15个交易日的数据
        mpf.plot(stock_df, type='candle', mav=(5, 10, 20), ax=ax, show_nontrading=False, tight_layout=True, xrotation=0)
        ax.set_title(f'Stock Code: {code}')

    plt.savefig('temp_plot.png')
    plt.close()


def on_slider_change(val):
    page = int(val)
    draw_plot(page)
    img = ImageTk.PhotoImage(Image.open('temp_plot.png'))
    panel.configure(image=img)
    panel.image = img


slider = tk.Scale(root, from_=1, to=num_pages, orient='horizontal', command=on_slider_change)
slider.pack()
draw_plot(1)
img = ImageTk.PhotoImage(Image.open('temp_plot.png'))
panel = tk.Label(root, image=img)
panel.pack(side="bottom", fill="both", expand="yes")
root.mainloop()
