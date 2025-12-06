"""
Main runner for Ichimoku Backtest Pipeline.
Pulls data from database, applies Ichimoku strategy, and produces results.
"""

import argparse
from ichimoku_backtest import (
    run_backtest_from_database,
    run_all_pairs_backtest,
    optimize_strategy
)
from ichimoku import plot_signals_ichimoku, plot_ichimoku_cloud
from database import load_from_database
from config import CURRENCY_PAIRS, DATABASE_PATH


def main():
    parser = argparse.ArgumentParser(
        description="Run Ichimoku Cloud trading strategy backtest"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # --- Single backtest command ---
    single_parser = subparsers.add_parser(
        "backtest",
        help="Run backtest on a single currency pair"
    )
    single_parser.add_argument(
        "--pair",
        type=str,
        default="EUR_USD_daily",
        help="Table name in database (e.g., EUR_USD_daily, GBP_USD_daily)"
    )
    single_parser.add_argument(
        "--cash",
        type=float,
        default=1_000_000,
        help="Initial account cash"
    )
    single_parser.add_argument(
        "--plot",
        action="store_true",
        help="Show Plotly interactive chart"
    )
    
    # --- Multi-pair backtest command ---
    multi_parser = subparsers.add_parser(
        "multi",
        help="Run backtest on all currency pairs"
    )
    multi_parser.add_argument(
        "--plot",
        action="store_true",
        help="Show charts for each pair"
    )
    
    # --- Optimize command ---
    opt_parser = subparsers.add_parser(
        "optimize",
        help="Optimize strategy parameters"
    )
    opt_parser.add_argument(
        "--pair",
        type=str,
        default="EUR_USD_daily",
        help="Table name to optimize"
    )
    opt_parser.add_argument(
        "--metric",
        type=str,
        default="Return [%]",
        help="Metric to maximize"
    )
    
    # --- Plot signals command ---
    plot_parser = subparsers.add_parser(
        "plot-signals",
        help="Plot signals and Ichimoku cloud"
    )
    plot_parser.add_argument(
        "--pair",
        type=str,
        default="EUR_USD_daily",
        help="Table name to plot"
    )
    plot_parser.add_argument(
        "--start",
        type=int,
        default=100,
        help="Start row index"
    )
    plot_parser.add_argument(
        "--end",
        type=int,
        default=200,
        help="End row index"
    )
    
    # --- Plot cloud command ---
    cloud_parser = subparsers.add_parser(
        "plot-cloud",
        help="Plot full Ichimoku cloud analysis"
    )
    cloud_parser.add_argument(
        "--pair",
        type=str,
        default="EUR_USD_daily",
        help="Table name to plot"
    )
    
    args = parser.parse_args()
    
    # --- Execute commands ---
    if args.command == "backtest":
        print(f"\n{'='*70}")
        print("Running Ichimoku Backtest (Single Pair)")
        print(f"{'='*70}\n")
        
        stats, df, bt = run_backtest_from_database(
            args.pair,
            cash=args.cash,
            show_plot=args.plot
        )
    
    elif args.command == "multi":
        print(f"\n{'='*70}")
        print("Running Ichimoku Backtest (Multi-Pair)")
        print(f"{'='*70}\n")
        
        summary = run_all_pairs_backtest(show_plot=args.plot)
        
        print(f"\n{'='*70}")
        print("Summary saved. Run with --plot to visualize individual pairs.")
        print(f"{'='*70}\n")
    
    elif args.command == "optimize":
        print(f"\n{'='*70}")
        print("Optimizing Ichimoku Strategy Parameters")
        print(f"{'='*70}\n")
        
        stats, heatmap = optimize_strategy(
            args.pair,
            maximize=args.metric
        )
    
    elif args.command == "plot-signals":
        print(f"\n{'='*70}")
        print("Plotting Trading Signals")
        print(f"{'='*70}\n")
        
        from ichimoku import fetch_data_from_database, add_ichimoku, add_ema_signal, create_ichimoku_signal
        from config import ICHIMOKU_TENKAN, ICHIMOKU_KIJUN, ICHIMOKU_SENKOU_B
        
        df = fetch_data_from_database(args.pair)
        df = add_ichimoku(df, tenkan=ICHIMOKU_TENKAN, kijun=ICHIMOKU_KIJUN, senkou_b=ICHIMOKU_SENKOU_B)
        df = add_ema_signal(df)
        df = create_ichimoku_signal(df)
        
        fig = plot_signals_ichimoku(
            df,
            start_idx=args.start,
            end_idx=args.end,
            title=f"{args.pair} — Trading Signals"
        )
        
        print("✅ Chart displayed")
    
    elif args.command == "plot-cloud":
        print(f"\n{'='*70}")
        print("Plotting Ichimoku Cloud Analysis")
        print(f"{'='*70}\n")
        
        from ichimoku import fetch_data_from_database, add_ichimoku
        from config import ICHIMOKU_TENKAN, ICHIMOKU_KIJUN, ICHIMOKU_SENKOU_B
        
        df = fetch_data_from_database(args.pair)
        df = add_ichimoku(df, tenkan=ICHIMOKU_TENKAN, kijun=ICHIMOKU_KIJUN, senkou_b=ICHIMOKU_SENKOU_B)
        
        fig = plot_ichimoku_cloud(df, title=f"{args.pair} — Ichimoku Cloud Analysis")
        
        print("✅ Chart displayed")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
