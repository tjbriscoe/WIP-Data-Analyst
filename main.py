#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 18:11:29 2026

@author: timothysmith
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from visualization import visualization, visualization_interactive
from fetch_data import fetch_data_fred
from analysis import analytical_data
from fredapi import Fred
import time



load_dotenv()
time.sleep(1)
fred = Fred(api_key= os.getenv("FRED_API_KEY"))

def load_config():
    api_key = os.getenv("FRED_API_KEY")
    if not api_key:
        raise ValueError("API couldn't be found")
    return api_key


def main():
    env_path = Path(__file__).resolve().parent / "API_KEY" / ".env"
    load_dotenv(env_path)

    print("Fetching Data...")
    api_key = load_config()

    cpi, median_income = fetch_data_fred(api_key)

    if cpi is None or median_income is None:
        raise ValueError("Failed to fetch data from FRED")
        
    df = analytical_data()
    
    visualization(df)
    visualization_interactive(df)


if __name__ == "__main__":
    main()

    
