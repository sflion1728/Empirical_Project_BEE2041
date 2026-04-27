# **The Rise of Climbing: Hype vs Reality?**
### BEE2041 Empirical Projec

This project will look to do ....
The project will use data and answer the question: 'Did the Olympic Hype around boulding have a sustained boom across climbing, or was it a short-term boom? 



**GITHUB PAGES LINK** INSERT LINK TO WEBSITE

## Project Structure
 
```
Empirical_Project/
├── README.md
├── requirements.txt
└── Sources_and_Python_Code/
    ├── Plots/                          ← all generated plots
    ├── Google_Trends.py                ← data collection (run first)
    ├── Sport_Compare_Bar_Chart.py      ← plot 1
    ├── Gym_Location.py                 ← plot 2
    ├── Sports_Brands.py                ← plot 3
    ├── Age.py                          ← plots 4 & 5
    ├── Active_Lives_2.py               ← regional heatmap
    └── Regression.py                   ← regression analysis
```
 
The raw date will live in the same folder as the python files inside `Sources_and_Python_Code`

**NOTE: Run the `Google_Trends.py` file first. There may be a 404 error and you may get timed out, if you do get timed out, then wait 15-20 mins to try again/or change your IP address. The `csv` file is included in the folder in case it does not run**






## INSTALLATION REQUIREMENTS

In order for the python code to run, make sure all packages listed below are installed. the code below will install them.


```bash

pip install pandas==2.3.3 matplotlib==3.10.8 numpy==2.2.6 scikit-learn==1.7.2 scipy==1.15.3 pytrends==4.9.2 openpyxl==3.1.5 plotly==6.7.0 statsmodels==0.14.6

```
| Package | Version |
|---| ---|
| `python` | 3.10.12 |
| `pandas` | 2.3.3 |
| `matplotlib` | 3.10.8 |
| `numpy` | 2.2.6 |
| `scikit-learn` | 1.7.2 |
| `scipy` | 1.15.3 |
| `pytrends` | 4.9.2 |
| `openpyxl` | 3.1.5 |
| `plotly` | 6.7.0 |
| `statsmodels` | 0.14.6 |

## RUNNING INSTRUCTION

- ### Step 1: 

- ### Step 2:

- ### Step 3:



## OUTPUTS

These outputs are stored in `Empirical Project\Plots` folder. A decription of them is down below:

| Plot | Description | Key Finding | File |
|---|---|---|---|
| Sport Comparison | % change in participation since 2015 | Climbing is the only sport to grow (+50%) | `xxxx.png`
| Gym Infrastructure | Cumulative UK gym openings 1995–2025 | Bouldering-only gyms dominate post-2021 | `xxxx.png`
| Brand Search Interest | La Sportiva & Scarpa Google Trends | Both brands growing +4–5 pts/yr | `xxxx.png`
| Age Index | Participation index by age group (Base=100) | 55-64s grew fastest — not young people | `xxxx.html`
| Regional Heatmap | Regional participation index 2015–2024 | Yorkshire grew 108% — the biggest winner | `xxxx.png`
| Regression | Google Trends vs participation | Hype explains 38% of participation (R²=0.38) | `xxxx.png`
| OLS Table | Full regression statistics | P=0.079 — relationship exists but not conclusive | `xxxx.png`


## ADVANCE MODELLING TECHNIQUE
### OLS

add something about the data here

## Resources/References

### Data Sources

| Dataset | Source | Method |
|---|---|---|
| Sport England Active Lives | [sportengland.org](https://activelives.sportengland.org/) | Manual download |
| Google Trends | [trends.google.com](https://trends.google.com) | pytrends API |
| UK Gym Locations | Individual gym websites | Manually compiled |

* Ref 1: what you put on the website
* Ref 2
