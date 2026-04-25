#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 17:13:02 2026

@author: timothysmith
"""

from fredapi import Fred
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
import os 

#Fetching Data from fred website 
def fetch_data_fred(fred_key):
    fred = Fred(api_key = fred_key)
    
    cpi=fred.get_series("CPIAUCSL").to_frame(name="cpi")
    
    cpi.index = pd.to_datetime(cpi.index)
    cpi = cpi[cpi.index >="1984-01-01"]
    
    median_income=fred.get_series("MEHOINUSA672N").to_frame(name = "median_income")
    median_income.index = pd.to_datetime(median_income.index)
    
    
    return cpi, median_income


if __name__ == "__main__":
    fred_key = os.getenv("FRED_API_KEY")
    
    if fred_key is None:
        raise ValueError (
            "API Key Couldn't Be Found"
            
            )
    cpi, median_income = fetch_data_fred(fred_key)
    print(cpi.head())
    
    
        
    


