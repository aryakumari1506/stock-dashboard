import pandas as pd
import numpy as np
import ta
from config import SMA_PERIODS, VOLATILITY_WINDOW
import os

class StockDataProcessor:
    def __init__(self):
        self.processed_dir = 'data/processed'
        self.power_bi_dir = 'data/power_bi'
        os.makedirs(self.processed_dir, exist_ok=True)
        os.makedirs(self.power_bi_dir, exist_ok=True)
    
    def calculate_technical_indicators(self, df):
        """Calculate technical indicators for stock data"""
        df = df.copy()
        
        # Group by symbol to calculate indicators separately
        result_dfs = []
        
        for symbol in df['Symbol'].unique():
            symbol_data = df[df['Symbol'] == symbol].copy()
            symbol_data = symbol_data.sort_values('Date')
            
            # Simple Moving Averages
            for period in SMA_PERIODS:
                symbol_data[f'SMA_{period}'] = symbol_data['Close'].rolling(window=period).mean()
            
            # Daily Returns
            symbol_data['Daily_Return'] = symbol_data['Close'].pct_change()
            
            # Volatility (rolling standard deviation of returns)
            symbol_data['Volatility'] = symbol_data['Daily_Return'].rolling(window=VOLATILITY_WINDOW).std()
            
            # Price change from previous day
            symbol_data['Price_Change'] = symbol_data['Close'].diff()
            symbol_data['Price_Change_Pct'] = symbol_data['Price_Change'] / symbol_data['Close'].shift(1) * 100
            
            # RSI (Relative Strength Index)
            symbol_data['RSI'] = ta.momentum.RSIIndicator(symbol_data['Close']).rsi()
            
            # MACD
            macd = ta.trend.MACD(symbol_data['Close'])
            symbol_data['MACD'] = macd.macd()
            symbol_data['MACD_Signal'] = macd.macd_signal()
            
            # Bollinger Bands
            bb = ta.volatility.BollingerBands(symbol_data['Close'])
            symbol_data['BB_Upper'] = bb.bollinger_hband()
            symbol_data['BB_Lower'] = bb.bollinger_lband()
            symbol_data['BB_Middle'] = bb.bollinger_mavg()
            
            result_dfs.append(symbol_data)
        
        return pd.concat(result_dfs, ignore_index=True)
    
    def create_summary_metrics(self, df):
        """Create summary metrics for Power BI"""
        summary_data = []
        
        for symbol in df['Symbol'].unique():
            symbol_data = df[df['Symbol'] == symbol]
            latest_data = symbol_data.iloc[-1]
            
            # Calculate metrics
            latest_price = latest_data['Close']
            prev_price = symbol_data.iloc[-2]['Close'] if len(symbol_data) > 1 else latest_price
            
            # YTD performance
            first_price = symbol_data.iloc[0]['Close']
            ytd_return = ((latest_price - first_price) / first_price) * 100
            
            # Recent volatility
            recent_volatility = symbol_data['Volatility'].iloc[-1] if not pd.isna(symbol_data['Volatility'].iloc[-1]) else 0
            
            summary_data.append({
                'Symbol': symbol,
                'Sector': latest_data['Sector'],
                'Latest_Price': latest_price,
                'Previous_Price': prev_price,
                'Daily_Change': latest_price - prev_price,
                'Daily_Change_Pct': ((latest_price - prev_price) / prev_price) * 100,
                'YTD_Return_Pct': ytd_return,
                'Current_Volatility': recent_volatility,
                'Latest_Volume': latest_data['Volume'],
                'Date': latest_data['Date']
            })
        
        return pd.DataFrame(summary_data)
    
    def process_data(self, input_file):
        """Main processing function"""
        print("Loading raw data...")
        df = pd.read_csv(input_file)
        df['Date'] = pd.to_datetime(df['Date'])
        
        print("Calculating technical indicators...")
        processed_df = self.calculate_technical_indicators(df)
        
        print("Creating summary metrics...")
        summary_df = self.create_summary_metrics(processed_df)
        
        # Save processed data
        processed_file = f"{self.processed_dir}/processed_stock_data.csv"
        summary_file = f"{self.power_bi_dir}/stock_summary.csv"
        power_bi_file = f"{self.power_bi_dir}/stock_data_full.csv"
        
        processed_df.to_csv(processed_file, index=False)
        summary_df.to_csv(summary_file, index=False)
        processed_df.to_csv(power_bi_file, index=False)
        
        print(f"Processed data saved to:")
        print(f"  - {processed_file}")
        print(f"  - {summary_file}")
        print(f"  - {power_bi_file}")
        
        return processed_df, summary_df

# Usage
if __name__ == "__main__":
    processor = StockDataProcessor()
    # Assuming you have a raw data file
    latest_file = "data/raw/stock_data_20240903.csv"  # Update with actual filename
    processed_data, summary_data = processor.process_data(latest_file)