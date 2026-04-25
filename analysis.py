#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 18:07:00 2026

@author: timothysmith
"""
import pandas as pd
from fredapi import Fred
import os
from dotenv import load_dotenv

load_dotenv()

fred = Fred(api_key=os.getenv("FRED_API_KEY"))


def analytical_data():
    
    #Series of raw data and Joining
    cpi=fred.search("Consumer Price Index For Urban Consumers in USA")

    #Series of CPI over time
    cpi=fred.get_series("CPIAUCSL")
    median_income=fred.get_series("MEHOINUSA672N")

    #Convert Series to Data Frame
    cpi = cpi.to_frame(name = "cpi")
    median_income = median_income.to_frame(name ="median_income")

    #New Column that converts year from index
    cpi.index = pd.to_datetime(cpi.index)
    cpi = cpi[cpi.index <= "2024-01-01"]

    
    cpi = cpi.copy()
    median_income = median_income.copy()
    
    #New Column that gets year from the index
    median_income.index = pd.to_datetime(median_income.index)
    
    #CPi( Consumer Price Index)
    #Extract Dates from Monthly CPI: 1984 - 2024 By Year
    #Resample and Calculate the Cpi based on the index 
    #Resampling CPi into an annual datframe to to extract the cpi value for each December
    cpi_annual= cpi.resample("YE").last()
    #Only show dates between this range to match Median Income Dataframe
    cpi_annual = cpi_annual.loc["1984":"2024"]
    #Setting the CPi Annual index into year
    cpi_annual.index = cpi_annual.index.year
    median_income.index = median_income.index.year
    
    
    cpi.index = pd.to_datetime(cpi.index)
    cpi_dec = cpi[cpi.index.month == 12].copy()
    cpi_dec.index = cpi_dec.index.year
    cpi_dec.index.name = "Year"
    
    
    cpi_annual.loc[2024]
    
    #Convert Income index into years
    annual = pd.merge(cpi_dec, median_income, left_index= True , right_index = True,
                      how = "inner")
    
    annual.loc[2024, "cpi"] = cpi_annual.loc[2024, "cpi"]
    annual.loc[2024, "median_income"] = median_income.loc[2024, "median_income"]
    
    annual["Year"] = annual.index
    
    
    #Base CPI calculation 
    base_cpi = annual.iloc[-1]["cpi"]
   
    #Adjusted Income to represent the buying power power over time 
    annual["Adjusted Income"] = annual["median_income"] * (base_cpi/annual["cpi"])
    
    #Percentage Changes throughout the years
    pct = pd.DataFrame()
    pct["real_growth"] = (annual["Adjusted Income"].pct_change() * 100).round(2)
    pct["real_growth"] = pct["real_growth"].fillna(0) 
    
    #Joining both dataframes based on Index
    annual = annual.join(pct)
    
    #KEY PERIODS
    annual.groupby(annual["Year"] //10)["real_growth"].mean()
    
   

    
    return annual


def recession_flagging(df):
    df = df.copy()

    df.index = pd.to_datetime(df.index.astype(str), format="%Y")

    df["recession"] = (
        (df.index.year >= 2007) &
        (df.index.year <= 2009)
    )

    if len(df) == 0:
        raise ValueError("Invalid, Try again")

    return df


annual = analytical_data()
annual = recession_flagging(annual)


        
    
    
    
    
    
