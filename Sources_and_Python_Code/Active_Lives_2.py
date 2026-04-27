'''
This code uses the raw file ActiveLivesDataExport_Regions_RAW_FILE.xlsx from the 
Active Lives Website found here: https://activelives.sportengland.org/

The data is loaded and cleaned, check for data quality and removing any null values/
missing data. The data is filtered for regions. 

The Heatmap plot is produced, creating a table that shows the growing rate of climbing
across regions,using 2015-2016 as a Base Index = 100 it has been filtered to show the 
true effect from phasing out of COVID. A percentage effect shown in the plot is the 
difference between the 2015-2016 year compared to the 2023-2024 year.
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)


 
###########################################################################
# LOAD DATA
###########################################################################

df = pd.read_excel('ActiveLivesDataExport_Regions_RAW_FILE.xlsx', skiprows=3)
df.columns = ['Region'] + list(df.columns[1:])
df['Region'] = df['Region'].str.strip('"').str.strip()
 
year_cols = [col for col in df.columns if col != 'Region']
 
for col in year_cols:
    df[col] = pd.to_numeric(df[col].replace('-', np.nan), errors='coerce')
 
print(f"Shape: {df.shape}\n")


 
###########################################################################
# DATA QUALITY CHECKS
###########################################################################

print(" --- DATA QUALITY REPORT --- ")

 
# NaN values

print('NaN values:' + str(df.isnull().sum().sum()))
 
# Missing values 

missing_mask = df[year_cols].isna()
if missing_mask.any().any():
    print(f"Missing values found:")
    for region in df['Region']:
        row = df[df['Region'] == region][year_cols].iloc[0]
        missing_years = row[row.isna()].index.tolist()
        if missing_years:
            print(f"    {region}: {missing_years}")

else:
    print(f"Missing values:0")
    
 
# Duplicate regions

dupes = df['Region'].duplicated().sum()
print(f"Duplicate regions:    {str(dupes) + 'found' if dupes else '0'}")
 
# All regions present

expected_regions = [
    'East Midlands Region', 'East Region', 'London Region',
    'North East Region', 'North West Region', 'South East Region',
    'South West Region', 'West Midlands Region', 'Yorkshire Region'
]
missing_regions = [r for r in expected_regions if r not in df['Region'].values]
print(f"Missing regions:      {str(missing_regions) if missing_regions else '0'}")
 
# No region shows zero across ALL years

all_zero = (df[year_cols].fillna(0) == 0).all(axis=1)
print(f"Regions all zeros:    {'WARNING: ' + str(df[all_zero]['Region'].tolist()) if all_zero.any() else '0'}")

print('Any negative values: ' + str(( df[col] < 0).any().any())) 



 
########################################################################
# PLOT FILTERING
########################################################################

# Drop North East — too many missing years to index reliably

df = df.drop(index=df[df['Region'] == 'North East Region'].index)
df = df.set_index('Region')
df.index = df.index.str.replace(' Region', '')
 
# Select key years and rebase to index 100

selected = ['Nov 15-16', 'Nov 20-21', 'Nov 21-22', 'Nov 22-23', 'Nov 23-24']
labels   = ['2015-16', '2020-21',
            '2021-22', '2022-23', '2023-24']
 
df = df[selected]
df_idx = df.div(df['Nov 15-16'], axis=0) * 100
 
assert (df_idx['Nov 15-16'] == 100).all()
 
df_idx = df_idx.sort_values('Nov 23-24', ascending=True)
growth = (df_idx['Nov 23-24'] - 100).round(0).astype(int)
 
print(f"--- OVERALL GROWTH FROM BASELINE ---")
for region, g in growth.sort_values(ascending=False).items():
    print(f"  {region:20s}: {'▲' if g > 0 else '▼'} {g}%")
    
    
 
####################################################################
# PLOT - Heatmap
####################################################################

plt.figure(figsize=(13, 6))
plt.imshow(df_idx.values, cmap='YlGn', aspect='auto', vmin=50, vmax=220)
 
 
# loop through each row and column and add numbers in each cell

for i in range(len(df_idx.index)):
    for j in range(len(selected)):
        val = df_idx.values[i, j]
        if not np.isnan(val):
            colour = 'white' if val > 160 else 'black'
            plt.text(j, i, f'{val:.0f}', ha='center', va='center',
                     fontsize=10, color=colour, fontweight='bold')
 
plt.axvline(0.5, color='white', linewidth=3)
plt.axvline(1.5, color='white', linewidth=3)
plt.axvline(0.5, color='#E63946', linewidth=2, linestyle='--', alpha=0.8)
plt.axvline(1.5, color='#E63946', linewidth=2, linestyle='--', alpha=0.8)
 
 
# add growth arrows on RHS of Heatmap

for i, (region, g) in enumerate(growth.items()):
    symbol = '▲' if g > 0 else '▼'
    colour = '#2A9D8F' if g > 0 else '#E63946'
    plt.text(len(selected) + 0.1, i, f'{symbol} {g}%',
             ha='center', va='center', fontsize=10,
             color=colour, fontweight='bold')
 
plt.text(0.0, -0.6, 'Baseline',               ha='center', fontsize=9, color='#457B9D', fontweight='bold')
plt.text(1.0, -0.6, 'COVID',                  ha='center', fontsize=9, color='#E63946', fontweight='bold')
plt.text(len(selected) + 0.1, -0.6, 'Total Change: 2015 to 2024 ',
         ha='center', fontsize=8, color='#333333', fontweight='bold')
 
plt.xticks(range(len(selected)), labels, fontsize=9)
plt.yticks(range(len(df_idx.index)), df_idx.index, fontsize=11)
plt.xlim(-0.5, len(selected) + 0.75)
plt.colorbar(label='Participation Index (Base 2015-16 = 100)', shrink=0.75)
plt.title('Regional Climbing Participation Heatmap: (Using 2015 as Baseline = 100)\n',
          fontsize=12, fontweight='bold', pad=25)
 
plt.tight_layout()
plt.savefig('Plots/Heatmap_Regions.png', dpi=150, bbox_inches='tight', facecolor='#FAFAFA')