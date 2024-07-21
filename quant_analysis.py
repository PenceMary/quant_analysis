import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 下载苹果公司（AAPL）的股票数据
data = yf.download('AAPL', start='2020-01-01', end='2023-01-01')

# 计算每日回报率
data['Return'] = data['Adj Close'].pct_change()

# 简单的移动平均线策略
data['SMA_20'] = data['Adj Close'].rolling(window=20).mean()
data['SMA_50'] = data['Adj Close'].rolling(window=50).mean()

# 定义买入和卖出信号
data.loc[20:, 'Signal'] = np.where(data['SMA_20'][20:] > data['SMA_50'][20:], 1, 0)

# 计算策略的持仓
data['Position'] = data['Signal'].diff()

# 计算策略收益
data['Strategy_Return'] = data['Return'] * data['Position'].shift(1)

# 累计收益
data['Cumulative_Return'] = (1 + data['Return']).cumprod()
data['Cumulative_Strategy_Return'] = (1 + data['Strategy_Return']).cumprod()

# 打印信号和持仓
print(data[['Adj Close', 'SMA_20', 'SMA_50', 'Signal', 'Position']].tail())

# 绘制收盘价和移动平均线
plt.figure(figsize=(14, 7))
plt.plot(data['Adj Close'], label='Adj Close')
plt.plot(data['SMA_20'], label='20-Day SMA')
plt.plot(data['SMA_50'], label='50-Day SMA')
plt.legend()
plt.show()

# 绘制累计收益
plt.figure(figsize=(14, 7))
plt.plot(data['Cumulative_Return'], label='Market Return')
plt.plot(data['Cumulative_Strategy_Return'], label='Strategy Return')
plt.legend()
plt.show()