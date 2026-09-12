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