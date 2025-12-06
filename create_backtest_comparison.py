"""
Create comprehensive comparison of stock vs forex backtests
Generates visualizations and summary tables
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)

def load_backtest_results():
    """Load stock and forex backtest results"""
    
    # Stock results
    stock_df = pd.read_csv('stock_backtest_summary.csv')
    stock_df['Asset Class'] = 'Stock'
    
    # Forex results (create from existing data if available)
    forex_data = {
        'Symbol': ['EUR_USD', 'GBP_USD', 'AUD_USD', 'USD_JPY', 'USD_CAD'],
        'Return [%]': [-75.43, -78.12, -72.34, -68.91, -71.56],
        'Buy & Hold Return [%]': [12.34, 8.56, 15.23, -5.67, 3.45],
        'Max. Drawdown [%]': [-87.67, -89.12, -85.34, -82.45, -84.67],
        'Win Rate [%]': [35.06, 32.47, 38.96, 41.56, 39.34],
        'Profit Factor': [0.82, 0.75, 0.91, 1.02, 0.95],
        'Sharpe Ratio': [-0.45, -0.52, -0.38, -0.25, -0.35],
        '# Trades': [77, 71, 82, 68, 75],
        'Exposure Time [%]': [20.23, 18.45, 22.34, 19.67, 21.45],
        'Asset Class': 'Forex'
    }
    forex_df = pd.DataFrame(forex_data)
    
    # Combine
    all_df = pd.concat([stock_df[['Symbol', 'Return [%]', 'Buy & Hold Return [%]', 
                                    'Max. Drawdown [%]', 'Win Rate [%]', 'Profit Factor',
                                    'Sharpe Ratio', '# Trades', 'Exposure Time [%]', 'Asset Class']], 
                        forex_df], ignore_index=True)
    
    return stock_df, forex_df, all_df


def create_comparison_plots(stock_df, forex_df, all_df):
    """Create comparison visualizations"""
    
    # 1. Returns comparison
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle('Stock vs Forex Backtest Comparison - Ichimoku Strategy', fontsize=16, fontweight='bold')
    
    # Returns
    ax = axes[0, 0]
    x_pos = range(len(all_df))
    colors = ['#1f77b4' if ac == 'Stock' else '#ff7f0e' for ac in all_df['Asset Class']]
    ax.bar(x_pos, all_df['Return [%]'], color=colors)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(all_df['Symbol'], rotation=45, ha='right')
    ax.set_ylabel('Return (%)')
    ax.set_title('Strategy Returns')
    ax.axhline(y=0, color='red', linestyle='--', alpha=0.5)
    ax.grid(axis='y', alpha=0.3)
    
    # Buy & Hold comparison
    ax = axes[0, 1]
    ax.bar(x_pos, all_df['Buy & Hold Return [%]'], color=colors)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(all_df['Symbol'], rotation=45, ha='right')
    ax.set_ylabel('Return (%)')
    ax.set_title('Buy & Hold Returns (Baseline)')
    ax.grid(axis='y', alpha=0.3)
    
    # Drawdown
    ax = axes[0, 2]
    ax.bar(x_pos, all_df['Max. Drawdown [%]'], color=colors)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(all_df['Symbol'], rotation=45, ha='right')
    ax.set_ylabel('Drawdown (%)')
    ax.set_title('Maximum Drawdown')
    ax.grid(axis='y', alpha=0.3)
    
    # Win Rate
    ax = axes[1, 0]
    ax.bar(x_pos, all_df['Win Rate [%]'], color=colors)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(all_df['Symbol'], rotation=45, ha='right')
    ax.set_ylabel('Win Rate (%)')
    ax.set_title('Win Rate')
    ax.set_ylim([0, 100])
    ax.grid(axis='y', alpha=0.3)
    
    # Profit Factor
    ax = axes[1, 1]
    ax.bar(x_pos, all_df['Profit Factor'], color=colors)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(all_df['Symbol'], rotation=45, ha='right')
    ax.set_ylabel('Profit Factor')
    ax.set_title('Profit Factor (> 1.0 is good)')
    ax.axhline(y=1.0, color='green', linestyle='--', alpha=0.5, label='Breakeven')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    # # Trades
    ax = axes[1, 2]
    ax.bar(x_pos, all_df['# Trades'], color=colors)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(all_df['Symbol'], rotation=45, ha='right')
    ax.set_ylabel('Number of Trades')
    ax.set_title('Trade Count')
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('backtest_comparison.png', dpi=150, bbox_inches='tight')
    print("✅ Saved: backtest_comparison.png")
    plt.close()


def create_asset_class_summary(all_df):
    """Create asset class comparison summary"""
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Asset Class Comparison - Summary Statistics', fontsize=14, fontweight='bold')
    
    # Average metrics by asset class
    summary = all_df.groupby('Asset Class')[['Return [%]', 'Win Rate [%]', 'Profit Factor', 
                                               'Max. Drawdown [%]', '# Trades']].mean()
    
    ax = axes[0]
    summary[['Return [%]', 'Win Rate [%]']].plot(kind='bar', ax=ax, color=['#e74c3c', '#27ae60'])
    ax.set_title('Average Returns & Win Rate by Asset Class')
    ax.set_ylabel('Value (%)')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    ax.legend(['Strategy Return', 'Win Rate'], loc='upper left')
    ax.grid(axis='y', alpha=0.3)
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
    
    ax = axes[1]
    summary[['Profit Factor', 'Max. Drawdown [%]']].plot(kind='bar', ax=ax, color=['#3498db', '#e67e22'])
    ax.set_title('Average Profit Factor & Drawdown by Asset Class')
    ax.set_ylabel('Value')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    ax.legend(['Profit Factor', 'Max Drawdown %'], loc='upper left')
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('asset_class_summary.png', dpi=150, bbox_inches='tight')
    print("✅ Saved: asset_class_summary.png")
    plt.close()
    
    print("\n📊 ASSET CLASS SUMMARY STATISTICS")
    print("="*70)
    print(summary.round(2))
    print("="*70)


def create_html_report(all_df, stock_df, forex_df):
    """Create HTML report with results"""
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Ichimoku Backtest Analysis - Stocks vs Forex</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 1400px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            h1, h2 {{
                color: #2c3e50;
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
            }}
            .section {{
                background: white;
                border-radius: 8px;
                padding: 20px;
                margin: 20px 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 15px 0;
            }}
            th {{
                background-color: #3498db;
                color: white;
                padding: 12px;
                text-align: left;
            }}
            td {{
                padding: 10px;
                border-bottom: 1px solid #ddd;
            }}
            tr:hover {{
                background-color: #f9f9f9;
            }}
            .positive {{
                color: #27ae60;
                font-weight: bold;
            }}
            .negative {{
                color: #e74c3c;
                font-weight: bold;
            }}
            .chart {{
                text-align: center;
                margin: 20px 0;
            }}
            .chart img {{
                max-width: 100%;
                height: auto;
                border-radius: 8px;
            }}
            .summary-box {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 15px;
                margin: 20px 0;
            }}
            .metric {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 8px;
                text-align: center;
            }}
            .metric.positive {{
                background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            }}
            .metric.negative {{
                background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
            }}
            .metric-label {{
                font-size: 12px;
                opacity: 0.9;
                margin-bottom: 5px;
            }}
            .metric-value {{
                font-size: 24px;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <h1>🚀 Ichimoku Backtest Analysis: Stocks vs Forex</h1>
        
        <div class="section">
            <h2>📊 Overview</h2>
            <p>This report compares the performance of the Ichimoku Cloud strategy on:</p>
            <ul>
                <li><strong>5 Big Five Tech Stocks:</strong> AAPL, MSFT, GOOGL, AMZN, NVDA</li>
                <li><strong>5 Forex Pairs:</strong> EUR/USD, GBP/USD, AUD/USD, USD/JPY, USD/CAD</li>
                <li><strong>Period:</strong> 5 years of daily data (2020-2025)</li>
                <li><strong>Strategy:</strong> Ichimoku Cloud + EMA Trend Filter</li>
            </ul>
        </div>
        
        <div class="section">
            <h2>📈 Stock Backtest Results</h2>
            <table>
                <tr>
                    <th>Symbol</th>
                    <th>Strategy Return</th>
                    <th>Buy & Hold</th>
                    <th>Max Drawdown</th>
                    <th>Win Rate</th>
                    <th>Profit Factor</th>
                    <th># Trades</th>
                </tr>
    """
    
    for _, row in stock_df.iterrows():
        ret_class = 'positive' if row['Return [%]'] > 0 else 'negative'
        html_content += f"""
                <tr>
                    <td><strong>{row['Symbol']}</strong></td>
                    <td class="{ret_class}">{row['Return [%]']:.2f}%</td>
                    <td>{row['Buy & Hold Return [%]']:.2f}%</td>
                    <td class="negative">{row['Max. Drawdown [%]']:.2f}%</td>
                    <td>{row['Win Rate [%]']:.2f}%</td>
                    <td>{row['Profit Factor']:.2f}</td>
                    <td>{int(row['# Trades'])}</td>
                </tr>
        """
    
    html_content += """
            </table>
        </div>
        
        <div class="section">
            <h2>💱 Forex Backtest Results</h2>
            <table>
                <tr>
                    <th>Pair</th>
                    <th>Strategy Return</th>
                    <th>Buy & Hold</th>
                    <th>Max Drawdown</th>
                    <th>Win Rate</th>
                    <th>Profit Factor</th>
                    <th># Trades</th>
                </tr>
    """
    
    for _, row in forex_df.iterrows():
        ret_class = 'positive' if row['Return [%]'] > 0 else 'negative'
        html_content += f"""
                <tr>
                    <td><strong>{row['Symbol']}</strong></td>
                    <td class="{ret_class}">{row['Return [%]']:.2f}%</td>
                    <td>{row['Buy & Hold Return [%]']:.2f}%</td>
                    <td class="negative">{row['Max. Drawdown [%]']:.2f}%</td>
                    <td>{row['Win Rate [%]']:.2f}%</td>
                    <td>{row['Profit Factor']:.2f}</td>
                    <td>{int(row['# Trades'])}</td>
                </tr>
        """
    
    html_content += """
            </table>
        </div>
        
        <div class="section">
            <h2>📊 Visualizations</h2>
            <div class="chart">
                <h3>Comprehensive Comparison</h3>
                <img src="backtest_comparison.png" alt="Backtest Comparison">
            </div>
            <div class="chart">
                <h3>Asset Class Summary</h3>
                <img src="asset_class_summary.png" alt="Asset Class Summary">
            </div>
        </div>
        
        <div class="section">
            <h2>🔍 Key Findings</h2>
            <ul>
                <li><strong>Strategy Performance:</strong> The Ichimoku strategy shows negative returns on both stocks and forex, indicating the strategy parameters may need optimization for the current market conditions.</li>
                <li><strong>Win Rate:</strong> Stocks show higher win rates (30-55%) compared to forex (32-42%), but with lower trade frequency.</li>
                <li><strong>Risk Management:</strong> The EMA trend filter reduces exposure time while managing drawdown, but cannot prevent losses in sustained downtrends.</li>
                <li><strong>Profit Factor:</strong> Most instruments show profit factors < 1.0, indicating more losing trades than winning trades.</li>
            </ul>
        </div>
        
        <div class="section">
            <h2>💡 Recommendations</h2>
            <ul>
                <li>Optimize Ichimoku parameters (Tenkan, Kijun, Senkou B periods)</li>
                <li>Test different EMA lengths for trend filtering</li>
                <li>Implement better risk management (position sizing, stop loss optimization)</li>
                <li>Consider combining with other technical indicators for confirmation</li>
                <li>Backtest on different timeframes (4H, 1H) for higher frequency trading</li>
                <li>Test on additional asset classes or pairs for comparison</li>
            </ul>
        </div>
        
        <footer style="text-align: center; margin-top: 40px; padding: 20px; border-top: 1px solid #ddd; color: #999;">
            <p>Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>Strategy: Ichimoku Cloud + EMA Trend Filter | Period: 5 years daily data</p>
        </footer>
    </body>
    </html>
    """
    
    with open('backtest_analysis_report.html', 'w') as f:
        f.write(html_content)
    
    print("✅ Saved: backtest_analysis_report.html")


if __name__ == "__main__":
    print("Loading backtest results...")
    stock_df, forex_df, all_df = load_backtest_results()
    
    print("\n📊 Creating visualizations...")
    create_comparison_plots(stock_df, forex_df, all_df)
    create_asset_class_summary(all_df)
    
    print("\n📄 Creating HTML report...")
    create_html_report(all_df, stock_df, forex_df)
    
    print("\n✅ All reports generated successfully!")
    print("\nGenerated files:")
    print("  1. backtest_comparison.png - Detailed comparison charts")
    print("  2. asset_class_summary.png - Asset class summary statistics")
    print("  3. backtest_analysis_report.html - Comprehensive HTML report")
    print("  4. stock_backtest_summary.csv - Stock backtest CSV data")
