'''
The data uses Types_Of_Activity_RAW_FILE.xlsx, this is from Sports England 
Active lives Data Table, found here: https://www.sportengland.org/research-and-data/data/active-lives/active-lives-data-tables
This has data for all sports in the UK, using the Nov 2023-2024 data table.

The data is cleaned and check for any missing values and duplicates, and making sure all 
data sounds plausible. 
A dictionary is created to filter for 6 sports including Climbing. 

The plot produced is a horizontal bar chart, highlighting the percentage change of the 
the sport from 2015. Showing key growth of climbing against other sports.

'''

import pandas as pd
import matplotlib.pyplot as plt



####################################################################################
# Load Data
####################################################################################

raw = pd.read_excel('TYPES_OF_ACTIVITY_RAW_FILE.xlsx',
    sheet_name='Table 6b Activities Trends',  # <-- changed sheet
    header=None
)

TARGET_SPORTS = {
    'Climbing and bouldering': 'Climbing & Bouldering',
    'Football':                'Football',
    'Swimming':                'Swimming',
    'Tennis':                  'Tennis',
    'Badminton':               'Badminton',
    'Running, athletics or multi-sports': 'Running',
    
}

POP_COLS = [2, 6, 10, 14, 18, 22, 26, 30, 34]
YEARS    = ['2015-16','2016-17','2017-18','2018-19',
            '2019-20','2020-21','2021-22','2022-23','2023-24']

records = []
for _, row in raw.iterrows():
    if str(row[0]).strip() in TARGET_SPORTS:
        entry = {'activity': TARGET_SPORTS[str(row[0]).strip()]}
        for year, col in zip(YEARS, POP_COLS):
            entry[year] = pd.to_numeric(row[col], errors='coerce') / 1_000_000
        records.append(entry)

df = pd.DataFrame(records)

# Keep only 2015, 2020, 2024  <-- only change to plot 1a

df_plot = df[['activity','2015-16','2019-20','2023-24']].rename(columns={
    '2015-16': '2015', '2019-20': '2020', '2023-24': '2024'
})
df_plot = df_plot.sort_values('2024', ascending=False).reset_index(drop=True)



####################################################################################
# DATA QUALITY CHECKS
####################################################################################

print("--- DATA QUALITY REPORT ---")

# No missing values

print(f"Missing values:      {df[YEARS].isnull().sum().sum() or '0'}")
 
# Values are plausible (millions — should be between 0 and 15)

too_low  = (df[YEARS] < 0).any().any()
too_high = (df[YEARS] > 15).any().any()
print(f"Values in range:     {'WARNING' if too_low or too_high else 'All between 0-15M'}")
 
 
# COVID year should show drops across most sports

covid_drops = (df['2020-21'] < df['2019-20']).sum()
print(f"COVID sanity check:  {covid_drops}/{len(df)} sports dropped in 2020-2021")
print(f"Duplicate sports:    {df['activity'].duplicated().sum() or '0'}") 


 
####################################################################################
# Plot_sports_Bar_Chart
####################################################################################

df['pct_change'] = ((df['2023-24'] - df['2015-16']) / df['2015-16'] * 100).round(1)
df_sorted = df.sort_values('pct_change')
colours = ['#2A9D8F' if x >= 0 else '#E63946'
           for x in df_sorted['pct_change']]
df_sorted.plot(x='activity', y='pct_change', kind='barh', figsize=(9, 6),
               legend=False,color=colours, zorder=3)

plt.grid(axis='x', linestyle='--', color='grey', alpha=0.4)
plt.title('% Change in Participation Since 2015-16')
plt.xlabel('% Change')
plt.axvline(0, color='black', linewidth=0.8)
plt.tight_layout()
plt.savefig('Plots/Sports_Plot_1b_2015.png', dpi=150)
