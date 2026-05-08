# **The Rise of Climbing**
### BEE2041 Empirical Project

*GitHub Pages Link:* **[The Rise of Climbing](https://sflion1728.github.io/Empirical_Project_BEE2041/)**


## Table of Contents
- [About](#about)
- [Project Structure](#project-structure)
- [Installation Requirements](#installation-requirements)
- [How to Run](#how-to-run)
- [Outputs](#outputs)
- [Advanced modelling technique](#advanced-modelling-technique)
- [Data Sources & References](#data-sources--references)

---

## About
This project will look to analyse the boom in climbing, looking at different factors and digging deeper to see what has caused a rise in popularity of the sport. 

Using data sources listed in the  [Data Sources](#data-sources) section, we will use python to analyse and produce some insightful outputs that will be analysed 
in detail on the GitHub Pages site.





---
## Project Structure

```
Empirical_Project/
├── README.md
├── index.html                          ← website homepage
├── style.css                           ← website styling
├── main.js                             ← website interactivity
└── Sources_and_Python_Code/
    ├── Data/                           ← all raw data files
    ├── Plots/                          ← all generated plots
    ├── Code/
    │   ├── Google_Trends.py            ← data collection (run first)
    │   ├── Sport_Compare_Bar_Chart.py  ← sports comparison chart
    │   ├── Gym_Location.py             ← gym area chart
    │   ├── Sports_Brands.py            ← brands line chart
    │   ├── Age.py                      ← age interactive chart
    │   ├── Active_Lives_2.py           ← regional heatmap
    │   └── Regression.py               ← regression analysis
```
 The blog will use the files  `index.html` `style.css` `main.js` to create and render the website live
 
 The raw data will live in `Data/`, the output produce will live in `Plots/`


---

## Installation Requirements

### System

- `python` version used: 3.10.12

### Python Packages 

In order for the python code to run, make sure all packages listed below are installed. the code below will install them.


```bash

pip install pandas==2.3.3 matplotlib==3.10.8 numpy==2.2.6 scikit-learn==1.7.2 scipy==1.15.3 pytrends==4.9.2 openpyxl==3.1.5 plotly==6.7.0 statsmodels==0.14.6 urllib3==1.26.15

```

They are also listed below with exact versions

| Package | Version |
|---| ---|
| `pandas` | 2.3.3 |
| `matplotlib` | 3.10.8 |
| `numpy` | 2.2.6 |
| `scikit-learn` | 1.7.2 |
| `scipy` | 1.15.3 |
| `pytrends` | 4.9.2 |
| `openpyxl` | 3.1.5 |
| `plotly` | 6.7.0 |
| `statsmodels` | 0.14.6 |
| `urllib3` | 1.26.15 |

Note: `urllib3` must be version `1.26.15` — newer versions may conflict with `pytrends`

---
## How to Run

### Step 1: Clone the repository
```bash
git clone https://github.com/sflion1728/Empirical_Project_BEE2041.git
cd Empirical_Project_BEE2041
```

### Step 2: Install all python packages necessary

```bash
pip install pandas==2.3.3 matplotlib==3.10.8 numpy==2.2.6 scikit-learn==1.7.2 scipy==1.15.3 pytrends==4.9.2 openpyxl==3.1.5 plotly==6.7.0 statsmodels==0.14.6 urllib3==1.26.15
```

### Step 3: Run Python code in order:

```bash
# 1
python3 Sources_and_Python_Code/Code/Google_Trends.py
```
**NOTE: Run the `Google_Trends.py` file first. There may be a 404 error and you may get timed out, if you do get timed out, then wait 15-20 mins to try again/or change your IP address. The `csv` file produced from this code is included in the folder in case it does not run.**



You may run these .py files listed below in whatever order you wish.
```bash
# 2 

python3 Sources_and_Python_Code/Code/Sport_Compare_Bar_Chart.py
 
python3 Sources_and_Python_Code/Code/Gym_Location.py

python3 Sources_and_Python_Code/Code/Sports_Brands.py
    
python3 Sources_and_Python_Code/Code/Age.py

python3 Sources_and_Python_Code/Code/Active_Lives_2.py
    
python3 Sources_and_Python_Code/Code/Regression.py
```

Running these files will produce all outputs in `Plots` and a `Google_Trends_Over_Time.csv` in the `Data`

### Step 4: Check blog page
The website is available on online as GitHub Pages, copy and paste the webite here in your browser
```bash
https://sflion1728.github.io/Empirical_Project_BEE2041/
```


Alternative there are options below to open the website


**Option 1: Open the index.html directly**

1. Find `index.html` in your file explorer
2. Double click it
3. Opens directly in your default browser

**Option 2: Open directly on VS Code**
1. Open VS Code
2. Install **Live Server** extension
3. Right click `index.html`
4. Click **Open with Live Server**

---
## Outputs

These outputs are stored in `Empirical Project/Sources_and_Python_Code/Plots` folder. A decription of them is down below:

| Chart | File | Description |
|---|---|---|
| 1 | `Area_Chart.png` | UK gym openings 1995–2025 |
| 2 | `Sports_Plot_2015.png` | % change in participation since 2015 |
| 3 | `interactive_age.html` | Participation index by age group (Base = 100) |
| 4 | `Heatmap_Regions.png` | Regional participation index 2015–2024 |
| 5 | `plot_brands.png` | La Sportiva & Scarpa Google Trends |
| 6 | `Regression_scatter.png` | Google Trends vs participation |
| 7 | `Regression_Chart_table.png` | OLS regression statistics |

This is the order the chart are shown in the GitHub Pages site.

---
## Advanced modelling technique

### OLS Regression

The advance modelling technique used will be a simple regression. 

* `Participation in climbing` as the Dependent variable
* `Google searches('bouldering')` as the Independent variable

This model will look to explain if a causal relationship between Google trend searchs between bouldering and climbing participants existed. 

---
## Data Sources & References

### Datasets
| Files | Source | Method |
|---|---|---|
| `ActiveLivesDataExport_Regions_RAW_FILE.xlsx` | [sportengland.org](https://activelives.sportengland.org/) | downloaded |
| `Age_Climbing_RAW_FILE.csv` | [sportengland.org](https://activelives.sportengland.org/) | downloaded |
| `Google_Trends_Over_Time.csv` | [trends.google.com](https://trends.google.com) | pytrends API |
| `Gym_Location_RAW_FILE.xlsx` | Individual gym websites | Manually compiled |
|`TYPES_OF_ACTIVITY_RAW_FILE.xlsx`|  [sportengland.org](https://www.sportengland.org/research-and-data/data/active-lives/active-lives-data-tables) | downloaded


**NOTE: `Gym_Location_RAW_FILE.xlsx` has a list of all climbing gyms and their sources in the excel file**
###

### References (Used in site) 
* Ball, E. (2026, February 15). Indoor climbing becoming “mainstream” sport, says Shrewsbury gym. BBC News. https://www.bbc.co.uk/news/articles/c309pnpj5m9o
* Roberts, G. (2025, January 10). Why does everyone suddenly want to rock climb? - The Oxford Blue. The Oxford Blue; OxBlue. https://theoxfordblue.co.uk/why-does-everyone-suddenly-want-to-rock-climb/
