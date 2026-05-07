'''
This file uses the data Age_Climbing_RAW_FILE.csv found from the Active Lives 
website found here: https://activelives.sportengland.org/

The data is cleaned and validated, check for missing and NaN values/Duplicates
 
The 1st plot is an interactive HTML time-seriers plot, where the dataframe is filtered for each 
age group. Age group(75-84 and 85+) are excluded as there was not enough data 
avaiable to make a plot. The age groups are index at 2015 at Base = 100, showing
the growth over the years. The plot can allow the user to zoom in and look at
specific values.

The 2nd plot is a bar chart, this groups the average participants from years
(2015 - 2020) and from (2021 -2024) and plots 2 charts, whith each age group on
the x-axis. 

NOTE: Covid was excluded to avoid any large movements in the data

'''

import pandas as pd
import matplotlib.pyplot as plt
import warnings
import plotly.graph_objects as go
warnings.filterwarnings('ignore', category=FutureWarning)
import os 
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)


 
########################################################################
# CLEANING THE DATA
########################################################################

df = pd.read_csv('../Data/Age_Climbing_RAW_FILE.csv', skiprows=4, index_col=0)
df.columns = df.columns.str.strip()
print('Preview of Table')
print('')
print(df.head(3))
print(f"Shape: {df.shape}\n")
 
# Clean — remove commas, dashes, convert to numeric

df = df.replace({',': '', '-': None}, regex=True)
df = df.apply(pd.to_numeric, errors='coerce')
df = df.dropna(how='all')
df = df[df.iloc[:, 0].notna()]  # drop groups with no base year
 
years = df.columns.tolist()



#######################################################################
# DATA QUALITY CHECKS
#######################################################################

print(" --- DATA QUALITY CHECKS --- ")
 
# Missing values

missing = df.isnull().sum()
print("Missing values per year:")
print(missing[missing > 0] if missing.any() else "0")
print('NaN values:' + str(missing.isnull().sum().sum()))
print('Any negative values: ' + str((missing < 0).any().any())) 
print('')
 
# No duplicate age groups

dupes = df.index.duplicated().sum()
print(f"Duplicate age groups: {'WARNING: ' + str(dupes) + ' found' if dupes > 0 else '0'}")
 
 
 
##############################################################################################
# PLOT 1 — Age Time Series Interactive (Base 2015-16 = 100)
##############################################################################################

df_index = df.div(df.iloc[:, 0], axis=0) * 100

colours = ['#2A9D8F', '#E9C46A', '#E76F51', '#457B9D', '#A8DADC', '#CDB4DB']

fig = go.Figure()

# Replace this section in PLOT 1:
for i, (age_group, row) in enumerate(df_index.iterrows()):
    valid = row.dropna()
    x = [years.index(y) for y in valid.index]  # ← map to correct year position
    fig.add_trace(go.Scatter(
        x=x,
        y=valid.values.tolist(),
        name=age_group,
        mode='lines+markers',
        line=dict(color=colours[i % len(colours)], width=2.5),
        marker=dict(size=7),
        hovertemplate=f'<b>{age_group}</b><br>Index: %{{y:.0f}}<extra></extra>'
    ))

olympic_idx = years.index('Nov 21-22')
fig.add_vline(x=olympic_idx, line_dash='dash', line_color='#E63946', line_width=1.5)
fig.add_hline(y=100, line_dash='dash', line_color='grey', line_width=1, opacity=0.5)
fig.add_annotation(x=olympic_idx, y=55, text='Tokyo Olympics',
                   showarrow=False, font=dict(color='#E63946', size=11))

fig.update_layout(
    title='Age Group Participation Index 2015–2024 (Base = 100)',

    xaxis=dict(
        tickvals=list(range(len(years))), ticktext=years, tickangle=-30,
        range=[-0.5, len(years) - 0.5],
        minallowed=-0.5, maxallowed=len(years) - 0.5,
        showline=True, linecolor='lightgrey', linewidth=1,
    ),
    yaxis=dict(
        title='Participation Index (Base 2015-16 = 100)',
        range=[40, 290], minallowed=20, maxallowed=290,
        showline=True, linecolor='lightgrey', linewidth=1,
    ),
    height=600,
    paper_bgcolor='#f7f4ef',
    plot_bgcolor='#f7f4ef',
    hovermode='x unified',
    dragmode='zoom',
    #margin=dict(r=160),
    margin=dict(r=160, t=40, b=20,l=10),
    legend=dict(
        bgcolor='rgba(0,0,0,0)',
        bordercolor='#264653',
        borderwidth=2,
        font=dict(color='#264653', size=11),
        x=1.02, y=0.99,
        xanchor='left', yanchor='top'
    ),
    modebar=dict(
        remove=['select2d', 'lasso2d', 'autoScale2d',
                'toggleSpikelines', 'hoverClosestCartesian', 'hoverCompareCartesian']
    )
)

fig.write_html('../Plots/interactive_age.html',
               config={'scrollZoom': False, 'displaylogo': False})


