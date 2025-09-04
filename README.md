#  Stock Price Trend Dashboard


##  Overview

This project creates a comprehensive stock market dashboard that provides:
- **Real-time stock price tracking** across multiple sectors
- **Technical analysis** with 10+ indicators (SMA, RSI, MACD, Bollinger Bands)
- **Interactive visualizations** with sector drilldown capabilities
- **Automated data pipeline** for daily updates
- **Power BI integration** for professional dashboards

![Dashboard Preview](https://via.placeholder.com/800x400/1f1f1f/ffffff?text=Dashboard+Preview+%28Add+your+screenshot+here%29)

##  Key Features

###  Market Analysis
- **Multi-sector coverage**: Technology, Finance, Healthcare, Energy, Consumer
- **OHLCV data**: Complete price and volume information
- **Performance metrics**: Daily/YTD returns, volatility analysis
- **Trend indicators**: Moving averages (20, 50, 200 day)

###  Technical Indicators
- **Momentum**: RSI, MACD with signal lines
- **Volatility**: Bollinger Bands, rolling volatility
- **Trend**: Simple Moving Averages, price channels
- **Custom metrics**: Sector performance, correlation analysis

###  Interactive Dashboard
- **Sector drilldown**: From market → sector → individual stocks
- **Time series analysis**: Daily/weekly/monthly views
- **KPI cards**: Quick performance snapshots
- **Heatmaps**: Sector and stock performance visualization

##  Quick Start

### Prerequisites
- Python 3.8 or higher
- Power BI Desktop
- Internet connection (for data fetching)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/stock-dashboard.git
   cd stock-dashboard
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the data pipeline**
   ```bash
   python scripts/main.py
   ```

5. **Open Power BI Dashboard**
   - Launch Power BI Desktop
   - Open `power_bi/dashboard.pbix`
   - Refresh data connections

##  Project Structure

```
stock-dashboard/
├──  data/
│   ├──  raw/                     # Raw CSV files from APIs
│   ├──  processed/               # Cleaned and processed data
│   └──  power_bi/               # Power BI ready datasets
├──  scripts/
│   ├──  data_extraction.py       # Yahoo Finance API integration
│   ├──  data_processing.py       # Technical indicators & cleaning
│   ├──  config.py               # Configuration settings
│   └──  main.py                 # Main execution pipeline
├──  power_bi/
│   ├──  dashboard.pbix          # Power BI dashboard file
│   └──  measures.dax            # Custom DAX measures
├──  docs/                       # Documentation and guides
├──  requirements.txt            # Python dependencies
├──  README.md                   # Project documentation
└──  .gitignore                  # Git ignore rules
```

##  Configuration

### Stock Symbols
Edit `scripts/config.py` to customize tracked stocks:

```python
STOCK_SYMBOLS = {
    'Technology': ['AAPL', 'MSFT', 'GOOGL', 'META', 'NVDA'],
    'Finance': ['JPM', 'BAC', 'WFC', 'GS', 'MS'],
    # Add more sectors and symbols
}
```

### Technical Indicators
Adjust indicator parameters:

```python
SMA_PERIODS = [20, 50, 200]        # Moving average periods
VOLATILITY_WINDOW = 30             # Volatility calculation window
PERIOD = '1y'                      # Data fetch period
INTERVAL = '1d'                    # Data interval (1d, 1wk, 1mo)
```

##  Dashboard Components

### 1. Market Overview Page
- **KPI Cards**: Market summary, top/worst performers
- **Sector Treemap**: Visual sector performance comparison
- **Time Series**: Historical price movements with filters
- **Performance Table**: Sortable stock performance metrics

### 2. Technical Analysis Page
- **OHLC Charts**: Candlestick charts with volume
- **Indicator Overlays**: Moving averages, Bollinger Bands
- **Oscillators**: RSI, MACD in separate panels
- **Stock Selector**: Interactive stock and timeframe selection

### 3. Sector Comparison Page
- **Drilldown Hierarchy**: Market → Sector → Company
- **Correlation Matrix**: Stock relationship heatmap
- **Relative Performance**: Normalized price comparison
- **Volatility Analysis**: Risk assessment by sector

##  Automation & Scheduling

### Daily Data Updates

**Windows Task Scheduler:**
```batch
# Create update_data.bat
@echo off
cd /d "C:\path\to\stock-dashboard"
call venv\Scripts\activate
python scripts/main.py
```

**Linux/macOS Cron:**
```bash
# Add to crontab (runs daily at 9 AM)
0 9 * * * /path/to/stock-dashboard/venv/bin/python /path/to/stock-dashboard/scripts/main.py
```

### Power BI Auto-Refresh
1. Publish dashboard to Power BI Service
2. Configure **scheduled refresh** in dataset settings
3. Set up **Power BI Gateway** for on-premises data

##  Customization

### Adding New Indicators
```python
# In data_processing.py
def calculate_custom_indicator(df):
    # Example: Williams %R
    df['Williams_R'] = ta.momentum.WilliamsRIndicator(
        high=df['High'], 
        low=df['Low'], 
        close=df['Close']
    ).williams_r()
    return df
```

### Custom DAX Measures
```dax
// Sector Market Cap (add to measures.dax)
Sector Market Cap = 
SUMX(
    FILTER(stock_summary, stock_summary[Sector] = SELECTEDVALUE(stock_summary[Sector])),
    stock_summary[Latest_Price] * stock_summary[Shares_Outstanding]
)
```

##  Acknowledgments

- **Yahoo Finance** for providing free financial data
- **Power BI Community** for dashboard inspiration
- **TA-Lib** for technical analysis indicators
- **Pandas** for data manipulation capabilities

</div>
