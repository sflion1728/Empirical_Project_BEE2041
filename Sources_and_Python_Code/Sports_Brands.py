'''
This file uses the Google_Trends_Over_Time.csv

The data is converted into a datetime, to be turned into a numerical value. The data 
is cleaned and checked making sure there is no duplicates and data is plausible

The plot is a line graph for 'La Sportiva' and 'Scarpa'  showing their trend in 
the searches. A trend line is prodice for each line, showing how many points
the trends are moving on average per year. A Tokyo Olymics line is added to show
if there was any Hype affect on the keywords

'''

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_csv('Google_Trends_Over_Time.csv')
df['date'] = pd.to_datetime(df['date'])
df['date_num'] = (df['date'] - df['date'].min()).dt.days



######################################################################### 
# DATA QUALITY CHECKS
#########################################################################

print(" --- DATA QUALITY REPORT --- ")
 
# No missing values

print(f"Missing values: {df.isnull().sum().sum() or ' 0'}")
 
# Expected columns present

expected_cols = ['date', 'Climbing', 'Bouldering', 'La Sportiva', 'Scarpa']
missing_cols  = [c for c in expected_cols if c not in df.columns]
print(f"Expected columns: {'⚠ Missing: ' + str(missing_cols) if missing_cols else 'All present'}")
 
# Date range is correct

print(f"Date range: {df['date'].min().date()} → {df['date'].max().date()}")
 
# No duplicate dates

dupes = df['date'].duplicated().sum()
print(f"Duplicate dates: {str(dupes) + ' found' if dupes else ' 0'}")
 
# Expected number of monthly rows (2015-2026 ≈ 133 months)

print(f"Row count: {len(df)}")



#########################################################################
# Plot - Bar Chart
######################################################################### 

fig, ax = plt.subplots(figsize=(12, 6))

colours = {
    'La Sportiva': '#2A9D8F',
    'Scarpa':      '#E63946',
}

for column, colour in colours.items():
    # Bold raw line
    ax.plot(df['date'], df[column], color=colour, linewidth=2, label=column)
    
    # Light grey dotted trend line
    z = np.polyfit(df['date_num'], df[column], 1)
    p = np.poly1d(z)
    ax.plot(df['date'], p(df['date_num']), color='black', linewidth=1.5, alpha = 0.4,
            linestyle='--', label=f'{column} trend (+{z[0]*365:.1f} pts/yr)')

# Event Line Markers

ax.axvline(pd.Timestamp('2021-08-01'), color='grey', linewidth=1.2,
           linestyle='--', alpha=0.7)
ax.text(pd.Timestamp('2021-08-01'), 95, 'Tokyo\nOlympics', fontsize=8,
        color='grey', ha='center')

ax.axvline(pd.Timestamp('2024-08-01'), color='grey', linewidth=1.2,
           linestyle='--', alpha=0.7)
ax.text(pd.Timestamp('2024-08-01'), 95, 'Paris\nOlympics', fontsize=8,
        color='grey', ha='center')

ax.set_title('La Sportiva & Scarpa Search Interest Over Time',
             fontsize=13, fontweight='bold')
ax.set_xlabel('Year')
ax.set_ylabel('Search Interest (0-100)')
ax.legend(fontsize=9)
ax.spines[['top', 'right']].set_visible(False)
plt.tight_layout()
plt.savefig('Plots/plot_brands.png', dpi=150)