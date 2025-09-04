from data_extraction import StockDataExtractor
from data_processing import StockDataProcessor
from datetime import datetime
import os

def main():
    """Main execution function"""
    print("=== Stock Dashboard Data Pipeline ===")
    print(f"Started at: {datetime.now()}")
    
    # Step 1: Extract data
    print("\n1. Extracting stock data...")
    extractor = StockDataExtractor()
    raw_data = extractor.fetch_all_stocks()
    
    if raw_data is None:
        print("Failed to extract data. Exiting.")
        return
    
    # Step 2: Process data
    print("\n2. Processing data and calculating indicators...")
    processor = StockDataProcessor()
    
    # Get the latest raw data file
    raw_files = [f for f in os.listdir('data/raw') if f.endswith('.csv')]
    if not raw_files:
        print("No raw data files found. Exiting.")
        return
    
    latest_raw_file = f"data/raw/{sorted(raw_files)[-1]}"
    processed_data, summary_data = processor.process_data(latest_raw_file)
    
    print(f"\n✅ Pipeline completed successfully!")
    print(f"Total stocks processed: {len(processed_data['Symbol'].unique())}")
    print(f"Date range: {processed_data['Date'].min()} to {processed_data['Date'].max()}")
    
    # Display summary statistics
    print("\n📊 Summary by Sector:")
    sector_summary = summary_data.groupby('Sector').agg({
        'Daily_Change_Pct': 'mean',
        'YTD_Return_Pct': 'mean',
        'Current_Volatility': 'mean'
    }).round(2)
    print(sector_summary)

if __name__ == "__main__":
    main()