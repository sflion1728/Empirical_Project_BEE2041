'''
The file uses data from Google_Trends_Over_Time.csv and from ActiveLivesDataExport_Regions_RAW_FILE.xlsx
the data is cleaned and validated,values are converted to 1000's. The Active Lives data has North East 
dropped due to insufficent data. Checks are done for missing values and data ranges.

An advance modelling technique is used which is a regression Model. This imports
packages: sklearn and scipy to create a line of best fit. The 'bouldering' keyword from
google trends is used as the x-axis, and the climbing participation is the y-axis. This created a scatter
plot for each year.  A fitted regression line is plotted on the scatter plot

A summary statistics table is produced, showing key stats about the regression model 
and allow for interpretation.

'''

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from scipy import stats
import statsmodels.api as sm
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
import os 
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

 
 
 
#################################################################
# Load Google Trends & Regions data
#################################################################

trends = pd.read_csv("../Data/Google_Trends_Over_Time.csv")
trends["date"] = pd.to_datetime(trends["date"])
trends["year"] = trends["date"].dt.year
 
print(" --- GOOGLE TRENDS RAW --- ")
print(f"Shape: {trends.shape}")
print(f"Columns: {trends.columns.tolist()}")
print(f"Date range: {trends['date'].min()} → {trends['date'].max()}")
print('')
print(f"Missing values:\n{trends.isnull().sum()}")

 
# Check bouldering column 

assert 'Bouldering' in trends.columns, "ERROR: 'Bouldering' column missing"
assert pd.api.types.is_numeric_dtype(trends['Bouldering']), "ERROR: Bouldering is not numeric" 
# Annual average
annual_trends = trends.groupby('year')['Bouldering'].mean().reset_index()
annual_trends.columns = ['year', 'search_interest']
annual_trends = annual_trends[annual_trends['year'] <= 2023]
 
# Regions data

year_map = {
    '2015-16': 2015, '2016-17': 2016, '2017-18': 2017,
    '2018-19': 2018, '2019-20': 2019, '2020-21': 2020,
    '2021-22': 2021, '2022-23': 2022, '2023-24': 2023,
}
 
sport = pd.read_excel('../Data/ActiveLivesDataExport_Regions_RAW_FILE.xlsx', skiprows=3, header=0, index_col=0)
sport.columns = list(year_map.keys())
 
print("--- SPORT ENGLAND RAW ---")
print(f"Shape: {sport.shape}")
print(f"Regions: {sport.index.tolist()}")




########################################################################
# CLEANING & VALIDATION
########################################################################

print("--- DATA QUALITY REPORT ---")

# Google Trends

print(f"Trends missing values:  {trends.isnull().sum().sum() or '0'}")
print(f"Trends date range:      {trends['date'].min().date()} to {trends['date'].max().date()}")
print(f"Trends values 0-100:    {'WARNING' if (trends[['Climbing','Bouldering','La Sportiva','Scarpa']] > 100).any().any() else 'Yes'}")

# Active Lives

print(f"Sport missing values:   {sport.isnull().sum().sum() or '0'}")
print(f"Regions remaining:      {sport.shape[0]}")
print(f"COVID sanity check:     {(sport['2020-21'] < sport['2019-20']).sum()}/8 regions dropped in 2020-21")
print('')


# Clean

sport = sport.replace({',': '', '-': None}, regex=True).infer_objects(copy=False)
sport = sport.apply(pd.to_numeric, errors='coerce')
 
# Check for missing values

missing = sport.isnull().sum()
print("Missing values per year after cleaning:")
print(missing[missing > 0] if missing.any() else "  None")
 
# Drop North East 

sport = sport.drop(index='North East Region', errors='ignore')
print(f"Remaining regions: {sport.shape[0]}")
 
# Sum to England total

england_total = sport.sum(axis=0).reset_index()
england_total.columns = ['survey_year', 'participants']
england_total['year'] = england_total['survey_year'].map(year_map)
england_total['participants'] = england_total['participants'] / 1000
 
 
 
#######################################################################
# MERGE & VALIDATE
#######################################################################

merged = england_total.merge(annual_trends, on='year')
 
print(f" --- MERGED DATASET --- ")
print(f"shape:{merged.shape}")

# Check the merge quality

assert len(merged) == len(annual_trends), \
    f"WARNING: Merge lost rows — expected {len(annual_trends)}, got {len(merged)}"

 
# Check for NaN

assert merged[['search_interest', 'participants']].isnull().sum().sum() == 0, \
    "WARNING: NaN values in merged dataset"
print(f"No missing values")
 
 
 
########################################################################
# REGRESSION
########################################################################

X      = merged[['search_interest']].values
y      = merged['participants'].values
reg    = LinearRegression().fit(X, y)
y_pred = reg.predict(X)
r2     = r2_score(y, y_pred)
slope  = reg.coef_[0]
_, _, _, p_value, std_err = stats.linregress(
    merged['search_interest'], merged['participants']
)


# Results from the regression
 
print(f" --- REGRESSION RESULTS --- ")
print(f"R²:       {r2:.4f}")
print(f"Slope:    {slope:.4f}")
print(f"P-value:  {p_value:.4f}")



'''

PLOTS, 7a(regression line, plotting the participants in each year and fitting a regression line) 
7b(a regression table, showing the R-sqaured, P-value and Slope)

'''

 
###################################################################################
# PLOT 7a — Scatter + Regression Line
###################################################################################

colours = ['#E63946' if yr in [2020] else '#2A9D8F'
           for yr in merged['year']]
 
fig, ax = plt.subplots(figsize=(7, 5))
fig.patch.set_facecolor('#f7f4ef')   # ← outer background
ax.set_facecolor('#f7f4ef') 
ax.scatter(merged['search_interest'], merged['participants'],
           color=colours, s=80, zorder=5)
 
x_line = np.linspace(merged['search_interest'].min(),
                     merged['search_interest'].max(), 100)
ax.plot(x_line, reg.predict(x_line.reshape(-1, 1)),
        color='#457B9D', linewidth=2, linestyle='--',
        label=f'Regression line (R²={r2:.2f})')
 
for _, row in merged.iterrows():
    ax.annotate(str(int(row['year'])),
                (row['search_interest'], row['participants']),
                textcoords='offset points', xytext=(5, 4), fontsize=8)
 
ax.set_xlabel("Google Trends Search Interest ('Bouldering' UK)", fontsize=10)
ax.set_ylabel('Climbing Participants (thousands)', fontsize=10)
ax.set_title('Does Hype Predict Participation?', fontsize=13, fontweight='bold')
ax.legend(fontsize=9)
ax.spines[['top', 'right']].set_visible(False)
plt.tight_layout()
plt.savefig('../Plots/Regression_scatter.png', dpi=150)


 
##################################################################################
# PLOT 7b — Statistics Table
##################################################################################

# OLS 

X_ols = sm.add_constant(merged['search_interest'])
model = sm.OLS(merged['participants'], X_ols).fit()

slope   = model.params['search_interest']
pval    = model.pvalues['search_interest']
ci_low  = model.conf_int().loc['search_interest', 0]
ci_high = model.conf_int().loc['search_interest', 1]

# Table, including relevent statistics 

table_data = [
    ['R²',                  f'{model.rsquared:.4f}'],
    ['Adj. R²',             f'{model.rsquared_adj:.4f}'],
    ['Coefficient (Slope)', f'{slope:.2f}'],
    ['P-Value',             f'{pval:.4f}'],
    ['95% Conf. Interval',  f'[{ci_low:.2f}, {ci_high:.2f}]'],
    ['Observations',        f'{int(model.nobs)}'],
]


# Creating the table 

fig, ax = plt.subplots(figsize=(6, 3))
fig.patch.set_facecolor('#f7f4ef')   # ← outer background
ax.set_facecolor('#f7f4ef') 
ax.axis('off')

tbl = ax.table(cellText=table_data,
               colLabels=['Statistic', 'Value'],
               cellLoc='left', loc='center')
tbl.auto_set_font_size(False)
tbl.set_fontsize(9)
tbl.scale(1, 1.8)

# Loop through each column and assign a colour

for col_idx in range(2):
    tbl[(0, col_idx)].set_facecolor('#264653')
    tbl[(0, col_idx)].set_text_props(color='white', fontweight='bold')

# Loop through each row assign colour and make bold
for row_idx in range(1, len(table_data) + 1):
    for col_idx in range(2):
        if row_idx % 2 == 0:
            tbl[(row_idx, col_idx)].set_facecolor("#E7E7E5")
        if col_idx == 1:
            tbl[(row_idx, col_idx)].set_text_props(fontweight='bold', color='#2A9D8F')

ax.set_title('OLS Regression Results', fontsize=12, fontweight='bold', pad=12)
plt.gcf().set_facecolor('#f7f4ef')   # ← outer background
plt.gca().set_facecolor('#f7f4ef')
plt.tight_layout()
plt.savefig('../Plots/Regression_Chart_table.png', dpi=150)


