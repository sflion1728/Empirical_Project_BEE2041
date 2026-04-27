'''
NOTE: DO NOT RUN MANY TIMES IN A ROW, GOOGLE HAS A RATE LIMIT ON 
HOW MANY TIMES THIS CAN BE RUN. IF THERE IS AN ERROR, WAIT 10-15 
MINS/OR CHANGE YOUR IP ADDRESS AND RUN AGAIN
NOTE: Code may run longer then usual. If it does not run the csv 
file is in the folder


This file collects data from Google trends using pytrends libary. 
The data collected has been about trend searches of popular climbing 
words. The data is collected individually using a loop, each keyword is 
fetched indvidually, so each word has it's own 0-100 scale. The data is 
then concatenated a datframe and saved as csv file called: 
Google_Trends_Over_Time22.csv

Analysis of this in in code: Sports_Brands.py, Regression.py

'''

import pandas as pd 
from pytrends.request import TrendReq
import time

pd.set_option('future.no_silent_downcasting', True)

#Connect to Google Trends

pytrends = TrendReq(tz=0, timeout=(10, 50), retries=3, backoff_factor=0.5)

#Keywords to find in Google trends

Key_Words = ['Climbing','Bouldering', 'La Sportiva' , 'Scarpa']


#itereate through Google Trends

Trends_df = pd.DataFrame()
for i in Key_Words: 
    pytrends.build_payload([i], timeframe='2015-01-01 2026-04-01', geo = 'GB')

    individual_word = pytrends.interest_over_time()
    
    
    if not individual_word.empty:
    
        if 'isPartial' in individual_word.columns:
            individual_word = individual_word.drop(columns= ['isPartial'])
        
        if Trends_df.empty:
            Trends_df = individual_word
        else:
            Trends_df = pd.concat([Trends_df,individual_word] , axis=1)
    
    time.sleep(10)
    

#Save csv file 
    
Trends_df.to_csv('Google_Trends_Over_Time.csv')  


    
