import pandas as pd
import numpy as np

def compute_lockdown_impact (df):

    # Calculates Pre-Lockdown vs. During Lockdown rate metrics for each state.

    pre_lockdown = (
        df [df ["Date"] < "2020-03-24"]
        .groupby ("State")["Unemployment_Rate"]
        .mean ()
    )
    during_lockdown = (
        df [df ["Is_Lockdown"]]
        .groupby ("State")["Unemployment_Rate"]
        .mean ()
    )

    impact_df = pd.DataFrame (
        {
            "Pre_Lockdown_Avg (%)": pre_lockdown,
            "Lockdown_Peak_Avg (%)": during_lockdown,
        }
    ).dropna ()

    impact_df ["Absolute_Increase (%)"] = (
        impact_df ["Lockdown_Peak_Avg (%)"] - impact_df ["Pre_Lockdown_Avg (%)"]
    )
    impact_df ["Percentage_Spike (%)"] = (
        impact_df ["Absolute_Increase (%)"] / impact_df ["Pre_Lockdown_Avg (%)"]
    ) * 100

    return impact_df.sort_values (by = "Absolute_Increase (%)",ascending = False)

def compute_moving_averages (df,window = 3):

    # Computes moving averages to smooth out monthly volatility in time series data.

    df_sorted = df.sort_values (by = "Date").copy ()
    df_sorted ["MA_Unemployment"] = (
        df_sorted.groupby ("State")["Unemployment_Rate"]
        .transform (lambda x: x.rolling (window = window,min_periods = 1).mean ())
    )
    return df_sorted

def generate_executive_summary (df_geo,df_area):

    # Generates dynamic textual executive summary metrics and observations.

    # Peak state identification

    max_rate_row = df_geo.loc [df_geo ["Unemployment_Rate"].idxmax ()]
    peak_state = max_rate_row ["State"]
    peak_rate = max_rate_row ["Unemployment_Rate"]
    peak_date = max_rate_row ["Date"].strftime ("%B %Y")

    # Overall pre vs lockdown comparison

    pre_avg = df_geo [df_geo ["Date"] < "2020-03-24"]["Unemployment_Rate"].mean ()
    lockdown_avg = df_geo [df_geo ["Is_Lockdown"]]["Unemployment_Rate"].mean ()
    overall_spike = (lockdown_avg-pre_avg)

    # Sectoral comparison

    rural_avg = df_area [df_area ["Area"] == "Rural"]["Unemployment_Rate"].mean ()
    urban_avg = df_area [df_area ["Area"] == "Urban"]["Unemployment_Rate"].mean ()

    summary_text = {
        "peak_state": peak_state,
        "peak_rate": f"{peak_rate:.2f} %",
        "peak_date": peak_date,
        "pre_avg": f"{pre_avg:.2f} %",
        "lockdown_avg": f"{lockdown_avg:.2f} %",
        "spike": f"+{overall_spike:.2f} %",
        "rural_avg": f"{rural_avg:.2f} %",
        "urban_avg": f"{urban_avg:.2f} %",
        "higher_sector": "Urban" if urban_avg > rural_avg else "Rural",
    }
    return summary_text