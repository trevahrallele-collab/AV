"""
Stock Data Fetcher
Fetches daily stock data for multiple tickers from yfinance and stores in SQLite database.
Includes Big Five tech stocks: AAPL, MSFT, GOOGL, AMZN, NVDA
"""

import yfinance as yf
import pandas as pd
import time
from sqlalchemy import create_engine
from config import STOCK_SYMBOLS, STOCKS_DB_PATH


def fetch_stock_data_yfinance(symbol: str, period: str = "5y") -> pd.DataFrame:
    """
    Fetch daily stock data from yfinance.
    
    Args:
        symbol: Stock ticker symbol (e.g., 'AAPL')
        period: Data period ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
    
    Returns:
        DataFrame with OHLCV data
    """
    print(f"📥 Fetching {symbol} data for {period}...")
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period)
        
        # Rename columns to lowercase for consistency
        df.columns = df.columns.str.lower()
        
        # Ensure we have the needed columns
        if 'close' in df.columns:
            print(f"   ✅ Loaded {len(df)} rows for {symbol}")
            return df
        else:
            print(f"   ❌ Missing 'close' column for {symbol}")
            return None
            
    except Exception as e:
        print(f"   ❌ Error fetching {symbol}: {str(e)}")
        return None


def save_stock_to_database(symbol: str, df: pd.DataFrame, db_path: str = STOCKS_DB_PATH) -> None:
    """
    Save stock data to SQLite database.
    
    Args:
        symbol: Stock ticker symbol
        df: DataFrame with stock data
        db_path: SQLite database path
    """
    try:
        engine = create_engine(db_path)
        table_name = f"{symbol}_daily"
        df.to_sql(table_name, engine, if_exists='replace', index=True, index_label='date')
        print(f"   💾 {table_name} saved to {db_path}")
    except Exception as e:
        print(f"   ❌ Error saving {symbol}: {str(e)}")


def fetch_and_store_all_stocks(symbols: list = None, period: str = "5y") -> dict:
    """
    Fetch and store all stock data.
    
    Args:
        symbols: List of stock tickers to fetch (default: STOCK_SYMBOLS from config)
        period: Data period to fetch
    
    Returns:
        Dictionary with fetch results
    """
    if symbols is None:
        symbols = STOCK_SYMBOLS
    
    results = {}
    
    print("\n" + "="*70)
    print("🚀 STOCK DATA FETCHER - Big Five Tech Stocks")
    print("="*70)
    
    for i, symbol in enumerate(symbols, 1):
        print(f"\n[{i}/{len(symbols)}] Processing {symbol}...")
        
        # Fetch data
        df = fetch_stock_data_yfinance(symbol, period)
        
        if df is not None and len(df) > 0:
            # Save to database
            save_stock_to_database(symbol, df)
            results[symbol] = {
                'status': 'success',
                'rows': len(df),
                'start_date': df.index[0],
                'end_date': df.index[-1]
            }
        else:
            results[symbol] = {
                'status': 'failed',
                'error': 'No data returned'
            }
        
        # Small delay to avoid rate limiting
        if i < len(symbols):
            time.sleep(1)
    
    # Print summary
    print("\n" + "="*70)
    print("📊 FETCH SUMMARY")
    print("="*70)
    
    successful = sum(1 for r in results.values() if r['status'] == 'success')
    failed = len(results) - successful
    
    for symbol, result in results.items():
        status_icon = "✅" if result['status'] == 'success' else "❌"
        if result['status'] == 'success':
            print(f"{status_icon} {symbol}: {result['rows']} rows ({result['start_date'].date()} to {result['end_date'].date()})")
        else:
            print(f"{status_icon} {symbol}: {result.get('error', 'Unknown error')}")
    
    print("\n" + "-"*70)
    print(f"✅ Successful: {successful}/{len(symbols)}")
    print(f"❌ Failed: {failed}/{len(symbols)}")
    print("="*70 + "\n")
    
    return results


def list_stock_tables(db_path: str = STOCKS_DB_PATH) -> list:
    """
    List all stock tables in the database.
    
    Args:
        db_path: SQLite database path
    
    Returns:
        List of table names
    """
    try:
        engine = create_engine(db_path)
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        return tables
    except Exception as e:
        print(f"Error listing tables: {str(e)}")
        return []


def get_stock_data(symbol: str, db_path: str = STOCKS_DB_PATH) -> pd.DataFrame:
    """
    Load stock data from database.
    
    Args:
        symbol: Stock ticker symbol
        db_path: SQLite database path
    
    Returns:
        DataFrame with stock data
    """
    try:
        engine = create_engine(db_path)
        table_name = f"{symbol}_daily"
        query = f"SELECT * FROM '{table_name}'"
        df = pd.read_sql(query, engine, index_col='date', parse_dates=['date'])
        return df
    except Exception as e:
        print(f"Error loading {symbol}: {str(e)}")
        return None


def get_database_stats(db_path: str = STOCKS_DB_PATH) -> dict:
    """
    Get statistics about the stock database.
    
    Args:
        db_path: SQLite database path
    
    Returns:
        Dictionary with database statistics
    """
    tables = list_stock_tables(db_path)
    stats = {
        'total_tables': len(tables),
        'tables': {}
    }
    
    for table in tables:
        df = get_stock_data(table.replace('_daily', ''))
        if df is not None:
            stats['tables'][table] = {
                'rows': len(df),
                'columns': list(df.columns),
                'date_range': f"{df.index[0].date()} to {df.index[-1].date()}"
            }
    
    return stats


if __name__ == "__main__":
    # Fetch and store all Big Five stocks
    results = fetch_and_store_all_stocks(STOCK_SYMBOLS)
    
    # Display database info
    print("\n📊 DATABASE INFO")
    print("="*70)
    stats = get_database_stats()
    print(f"Total tables: {stats['total_tables']}")
    print(f"Database path: {STOCKS_DB_PATH}")
    print("\nTables created:")
    for table_name, table_stats in stats['tables'].items():
        print(f"  • {table_name}: {table_stats['rows']} rows ({table_stats['date_range']})")
    print("="*70)
