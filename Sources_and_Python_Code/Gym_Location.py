'''
This file uses data from Gym_Location_RAW_FILE.xlsx, the data was manually collected 
since web-scraping was not allowed for websites that do contain location
of climbing gyms/opening date. The data was stored in a excel file

The data was cleaned and validated, checking for NaN/Missing values.

The data was filtered for bouldering and gym that offer 'both' which 
is bouldering and roped climbing. The plot produces is an area chart. Showing the cummulative growth and showing 
how the climbing gym openings have progressed over time

'''

import pandas as pd
import matplotlib.pyplot as plt
 
gyms = pd.read_excel('Gym_Locations_RAW_FILE.xlsx')



##############################################################################
# DATA VALIDATION
##############################################################################

print('Missing values:\n', gyms.isnull().sum())
print('Year range:', gyms['opening_year'].min(), '–', gyms['opening_year'].max())
print('Gym types:', gyms['type'].unique())
print('Total gyms:', len(gyms))
print('Duplicate names:', gyms['name'].duplicated().sum())
print('NaN values: ' + str(gyms.isnull().sum().sum())) 
 
 
##############################################################################
# FILTER DATA
##############################################################################

all_years = range(1995, 2026)
 
bouldering = gyms[gyms['type'] == 'bouldering'].groupby('opening_year').size().reindex(all_years, fill_value=0).cumsum()
both       = gyms[gyms['type'] == 'both'].groupby('opening_year').size().reindex(all_years, fill_value=0).cumsum()
 
years = list(all_years)
 
 
 
#############################################################################
# PLOT - Area Chart
#############################################################################

plt.figure(figsize=(13, 7))
plt.fill_between(years, 0, both,                 alpha=0.6, color='#E9C46A', label='Both (Roped + Bouldering)')
plt.fill_between(years, both, both + bouldering, alpha=0.6, color='#2A9D8F', label='Bouldering Only')
 
plt.plot(years, both,              color='#E9C46A', linewidth=1.5)
plt.plot(years, both + bouldering, color='#2A9D8F', linewidth=1.5)

 
#Mark the Tokyo Olymics

plt.axvline(2021, color='#E63946', linewidth=1.5, linestyle='--', alpha=0.7)
plt.text(2021.2, 40, 'Tokyo\nOlympics\n(Climbing debut)', fontsize=8, color='#E63946')
 
plt.title('The Rise of UK Climbing Gyms', fontsize=13, fontweight='bold')
plt.xlabel('Year', fontsize=10)
plt.ylabel('Total Cumulative Gyms Opened', fontsize=10)
plt.ylim(0, None)
plt.legend(fontsize=9, loc='upper left')
plt.tight_layout()

#Save figure in folder

plt.savefig('Plots/Area_Chart.png', dpi=150)