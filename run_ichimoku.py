#!/usr/bin/env python3
"""
Quick start script for Ichimoku Cloud trading strategy.
Run this to see a complete example of the integrated pipeline.
"""

import sys
from ichimoku_runner import main

if __name__ == "__main__":
    # Default to multi-pair backtest if no args provided
    if len(sys.argv) == 1:
        sys.argv.extend(["multi"])
    
    main()
