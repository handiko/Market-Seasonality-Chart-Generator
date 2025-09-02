# Market Seasonality Chart Generator
Generating "Market Seasonality" Chart for Any Market listed on Yahoo Finance.

## Background
For effective analysis and the development of seasonal trading strategies, it is often necessary to have a historical average return for the month. By independently generating this data, we gain a deeper understanding of the underlying mechanics, which allows us to customize the historical period to suit our specific analytical or strategic requirements.

## How The Chart is Calculated
This is a cumulative average return chart. It's calculated by first finding the average daily return for each specific day of the year over the last decade. These daily averages are then accumulated to create the plotted line. That's it! That's simple!

Code : [here](https://github.com/handiko/Market-Seasonality-Chart-Generator/blob/main/JupyterNotebook/Market%20Seasonality.ipynb)

## How to Use
Simply define the ticker symbol (Yahoo Finance ticker consensus), the start-end dates, and the file-saving path:
```python
# Define the forex pair and the date range for the analysis
# Note: 'EURUSD=X' is a common Yahoo Finance ticker for the EUR/USD pair.
TICKER = '^VIX'
START_DATE = '2015-01-01'
END_DATE = '2025-01-01'
SAVE_PATH = f'./{TICKER}_seasonality_chart.png'
```

---
## Examples
### Nasdaq Futures
![](./NQ=F_seasonality_chart.png)


### Gold Contract Futures
![](./GC=F_seasonality_chart.png)


### EURUSD
![](./EURUSD=X_seasonality_chart.png)


### USDJPY
![](./USDJPY=X_seasonality_chart.png)


### Bitcoin
![](./BTC-USD_seasonality_chart.png)


### IDX COMPOSITE Index
![](./^JKSE_seasonality_chart.png)


### US Dollar Index
![](./^NYICDX_seasonality_chart.png)

---

## Related Project
[Monthly Seasonality Trading Strategy Backtest](https://github.com/handiko/Monthly-Seasonality-Trading-Strategy-Backtest/blob/main/README.md)

---

Back to [Index](https://github.com/handiko/handiko/blob/master/README.md)
