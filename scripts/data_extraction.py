import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import os
from config import STOCK_SYMBOLS, PERIOD, INTERVAL

class StockDataExtractor:
    def __init__(self):
        self.data_dir = 'data/raw'
        os.makedirs(self.data_dir, exist_ok=True)
    
    def fetch_stock_data(self, symbol):
        """Fetch stock data for a single symbol"""
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(period=PERIOD, interval=INTERVAL)
            
            if data.empty:
                print(f"No data found for {symbol}")
                return None
                
            # Add symbol column
            data['Symbol'] = symbol
            data.reset_index(inplace=True)
            
            return data
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return None
    
    def fetch_all_stocks(self):
        """Fetch data for all stocks in all sectors"""
        all_data = []
        
        for sector, symbols in STOCK_SYMBOLS.items():
            print(f"Fetching data for {sector} sector...")
            
            for symbol in symbols:
                print(f"  Fetching {symbol}...")
                data = self.fetch_stock_data(symbol)
                
                if data is not None:
                    data['Sector'] = sector
                    all_data.append(data)
        
        if all_data:
            combined_data = pd.concat(all_data, ignore_index=True)
            
            # Save raw data
            filename = f"{self.data_dir}/stock_data_{datetime.now().strftime('%Y%m%d')}.csv"
            combined_data.to_csv(filename, index=False)
            print(f"Data saved to {filename}")
            
            return combined_data
        
        return None

# Usage
if __name__ == "__main__":
    extractor = StockDataExtractor()
    data = extractor.fetch_all_stocks()