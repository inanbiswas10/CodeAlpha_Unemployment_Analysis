import sys
import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Ensure project root directory is added to python path

sys.path.append (os.path.abspath (os.path.join (os.path.dirname (__file__),"..")))
from src.data_loader import load_area_data,load_geo_data
from src.analytics import (compute_lockdown_impact,compute_moving_averages,generate_executive_summary,)

# Streamlit application layout configuration

st.set_page_config (
    page_title = "National Unemployment Analytics Platform",
    page_icon = "⚡",
    layout = "wide",
    initial_sidebar_state = "expanded",
)

# Polished CSS styling for clean spacing, card padding and professional dark UI

st.markdown (
    """
    <style>
    /* Main page container margins */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }
    
    /* Executive Metric Card Design */
    .metric-card {
        background: #161B22;
        border: 1px solid #30363D;
        border-radius: 10px;
        padding: 16px 18px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.25);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        border-color: #238636;
        transform: translateY(-2px);
    }
    .metric-title {
        color: #8B949E;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 6px;
    }
    .metric-value {
        color: #00D26A;
        font-size: 26px;
        font-weight: 800;
    }
    
    /* Navigation Tabs Spacing */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        margin-top: 10px;
        margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 44px;
        padding: 0px 22px;
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 8px;
        color: #C9D1D9;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #238636 !important;
        border-color: #238636 !important;
        color: #FFFFFF !important;
    }
    </style>
""",
    unsafe_allow_html = True,
)

@st.cache_data

def load_all_data ():

    # Cached loader function for optimized dashboard performance.

    area_path = os.path.join ("data","Unemployment in India.csv")
    geo_path = os.path.join ("data","Unemployment_Rate_upto_11_2020.csv")
    df_area = load_area_data (area_path)
    df_geo = load_geo_data (geo_path)
    return df_area,df_geo

df_area,df_geo = load_all_data()

# Header Section

st.title ("📈 National Unemployment & COVID-19 Impact Analytics Platform")
st.caption ("An industry grade analytics platform responsible for inspecting the employment trends, regional impacts as well as the COVID-19 shocks across the different states of India")
st.divider ()

# Global Filters Sidebar

st.sidebar.header ("🕹️ Dashboard Control Panel")
selected_dataset = st.sidebar.radio (
    "Data Source Mode",
    options = ["Geospatial & Zone Analytics","Sectoral Breakdown (Rural vs Urban)"],)

st.sidebar.markdown ("---")
st.sidebar.subheader ("📥 Data Export Engine")

# Convert current view dataframe to CSV string for download

csv_data = (
    df_geo.to_csv (index = False)
    if selected_dataset == "Geospatial & Zone Analytics"
    else df_area.to_csv (index = False)
)
st.sidebar.download_button (
    label = "Export Current Dataset (CSV)",
    data = csv_data,
    file_name = f"{selected_dataset.replace (' ','_').lower ()}_export.csv",
    mime = "text/csv",
    use_container_width = True,)

if selected_dataset == "Geospatial & Zone Analytics":
    df_selected = df_geo.copy ()
    states = ["All States"] + sorted (list(df_selected ["State"].unique ()))
    selected_state = st.sidebar.selectbox ("Filter State Focus",options = states)

    if selected_state != "All States":
        df_selected = df_selected [df_selected ["State"] == selected_state]

    # KPI Top Bar with comfortable gap spacing

    kpi1,kpi2,kpi3,kpi4,kpi5 = st.columns (5,gap = "medium")

    kpi1.markdown (f'<div class="metric-card"><div class="metric-title">Mean Rate</div><div class="metric-value">{df_selected ["Unemployment_Rate"].mean ():.2f} %</div></div>',unsafe_allow_html = True)
    kpi2.markdown (f'<div class="metric-card"><div class="metric-title">Peak Rate</div><div class="metric-value">{df_selected ["Unemployment_Rate"].max ():.2f} %</div></div>',unsafe_allow_html = True)
    kpi3.markdown (f'<div class="metric-card"><div class="metric-title">Average Workforce</div><div class="metric-value">{df_selected ["Employed"].mean ()/1e6:.2f} M</div></div>',unsafe_allow_html = True)
    kpi4.markdown (f'<div class="metric-card"><div class="metric-title">Lockdown Average</div><div class="metric-value">{df_selected [df_selected ["Is_Lockdown"]]["Unemployment_Rate"].mean ():.2f} %</div></div>',unsafe_allow_html = True)
    kpi5.markdown (f'<div class="metric-card"><div class="metric-title">Participation Rate</div><div class="metric-value">{df_selected ["Labour_Participation_Rate"].mean ():.2f} %</div></div>',unsafe_allow_html = True)

    st.write ("")
    st.write ("")

    tab1,tab2,tab3,tab4,tab5  = st.tabs (
        [
            "📉 Temporal Trajectory & Map Analysis",
            "🏛️ Macro Zonal Analysis",
            "🔍 Multi State Comparison Section",
            "⚡ Impact Matrix & Forecast Analysis",
            "📋 Executive Briefing Section"
        ]
    )

    with tab1:
        col_left,col_right = st.columns ([1.1,0.9],gap = "large")
        
        with col_left:
            st.subheader ("Monthly Unemployment Trajectory")
            fig_line = px.line (
                df_selected,
                x = "Date",
                y = "Unemployment_Rate",
                color = "State" if selected_state == "All States" else None,
                markers = True,
                template = "plotly_dark",
                height = 430,
            )
            fig_line.add_vrect (
                x0 = "2020-03-24",
                x1 = "2020-05-31",
                fillcolor = "#FF4B4B",
                opacity = 0.2,
                line_width = 0,
                annotation_text = "Strict Lockdown Period",
                annotation_position = "top left",
            )
            fig_line.update_layout (
                margin = dict(l = 15,r = 15,t = 35,b = 25),
                legend = dict(orientation = "h",y = -0.25),
            )
            st.plotly_chart (fig_line,width = "stretch")

        with col_right:
            st.subheader ("Unemployment Severity Map For The Different States Of India")
            geo_summary = (
                df_geo.groupby (["State","Latitude","Longitude"])[
                    ["Unemployment_Rate","Employed","Labour_Participation_Rate"]
                ]
                .mean ()
                .reset_index ()
            )

            fig_map = px.scatter_map (
                geo_summary,
                lat = "Latitude",
                lon = "Longitude",
                size = "Unemployment_Rate",
                color = "Unemployment_Rate",
                hover_name = "State",
                hover_data = {
                    "Unemployment_Rate": ":.2f %",
                    "Labour_Participation_Rate": ":.2f %",
                    "Latitude": False,
                    "Longitude": False,
                },
                color_continuous_scale = "Reds",
                size_max = 30,
                zoom = 3.4,
                center = {"lat": 22.5937,"lon": 78.9629},
                map_style = "carto-darkmatter",
                template = "plotly_dark",
                height = 430,
            )
            fig_map.update_layout (
                margin = dict(l = 10,r = 10,t = 35,b = 10)
            )
            st.plotly_chart (fig_map,width = "stretch")

    with tab2:
        c1,c2 = st.columns (2,gap = "large")
        with c1:
            st.subheader ("Regional Rate Distribution Analysis")
            fig_box = px.box (
                df_geo,
                x = "Zone",
                y = "Unemployment_Rate",
                color = "Zone",
                points = "all",
                template = "plotly_dark",
                height = 400,
            )
            fig_box.update_layout (margin = dict(l = 15,r = 15,t = 35,b = 15),showlegend = False)
            st.plotly_chart (fig_box,width = "stretch")

        with c2:
            st.subheader ("Zone Wise Labour Force Participation Analysis")
            fig_zone_lpr = px.bar (
                df_geo.groupby ("Zone")["Labour_Participation_Rate"].mean ().reset_index (),
                x = "Zone",
                y = "Labour_Participation_Rate",
                color = "Zone",
                template = "plotly_dark",
                height = 400,
            )
            fig_zone_lpr.update_layout (margin = dict(l = 15,r = 15,t = 35,b = 15),showlegend = False)
            st.plotly_chart (fig_zone_lpr,width = "stretch")

    with tab3:
        st.subheader ("State Wise Comparative Engine")
        selected_states = st.multiselect (
            "Select States to Compare",
            options = sorted (list (df_geo ["State"].unique ())),
            default = ["Maharashtra","Tamil Nadu","Delhi","Haryana"],
        )
        st.write ("")
        if selected_states:
            comp_df = df_geo [df_geo ["State"].isin (selected_states)]
            c1,c2 = st.columns ([1.1,0.9],gap = "large")
            with c1:
                fig_comp = px.bar (
                    comp_df,
                    x = "Month_Name",
                    y = "Unemployment_Rate",
                    color = "State",
                    barmode = "group",
                    template = "plotly_dark",
                    height = 390,
                )
                fig_comp.update_layout (margin = dict(l = 15,r = 15,t = 35,b = 15))
                st.plotly_chart (fig_comp,width = "stretch")
            with c2:
                fig_scatter = px.scatter (
                    comp_df,
                    x = "Labour_Participation_Rate",
                    y = "Unemployment_Rate",
                    color = "State",
                    size = "Employed",
                    template = "plotly_dark",
                    height = 390,
                )
                fig_scatter.update_layout (margin = dict(l = 15,r = 15,t = 35,b = 15))
                st.plotly_chart (fig_scatter,width = "stretch")

    with tab4:
        st.subheader ("State Lockdown Vulnerability Rankings")
        impact_df = compute_lockdown_impact (df_geo)
        
        c1,c2 = st.columns ([1.1,0.9],gap = "large")
        with c1:
            st.dataframe (
                impact_df.style.background_gradient (
                    cmap = "Reds",subset = ["Absolute_Increase (%)","Percentage_Spike (%)"]
                ).format ("{:.2f}"),
                height = 380,
                width = "stretch",
            )
        with c2:
            st.subheader ("3-Month Moving Average Trend Analysis")
            df_smoothed = compute_moving_averages (df_selected,window=3)
            fig_smooth = px.line (
                df_smoothed,
                x = "Date",
                y = ["Unemployment_Rate","MA_Unemployment"],
                template = "plotly_dark",
                height = 340,
            )
            fig_smooth.update_layout (margin = dict(l = 10,r = 10,t = 20,b = 10))
            st.plotly_chart (fig_smooth,width = "stretch")

    with tab5:
        st.subheader ("📋 Automated Executive Economic Summary")
        summary = generate_executive_summary (df_geo,df_area)

        col_a,col_b = st.columns (2,gap = "large")

        with col_a:
            st.markdown (
                f"""
            ### 🚨 Critical COVID-19 Impact Highlights
            * **Historical Peak Unemployment:** **{summary ['peak_state']}** recorded the highest unemployment rate of **{summary ['peak_rate']}** in **{summary ['peak_date']}**.
            * **National Lockdown Shock:** National average unemployment jumped from **{summary ['pre_avg']}** (Pre-Lockdown) to **{summary ['lockdown_avg']}** during strict lockdown, reflecting an overall surge of **{summary ['spike']}**.
            * **Sectoral Vulnerability:** The **{summary ['higher_sector']}** sector experienced higher overall unemployment during the observation period (**Urban: {summary ['urban_avg']}** vs **Rural: {summary ['rural_avg']}**).
            """
            )

        with col_b:
            st.markdown (
                """
            ### 💡 Strategic Policy Recommendations
            * **Targeted Regional Aid:** Allocate emergency labor relief funds to top vulnerable states identified in the Impact Matrix.
            * **Urban Job Guarantee Programs:** Expand employment support programs in urban areas to mitigate systemic shocks during economic disruptions.
            * **Real-Time Surveillance:** Implement monthly automated data monitoring pipelines to track early signs of labour market distress.
            """
            )

else:
    df_selected = df_area.copy ()
    
    kpi1,kpi2,kpi3 = st.columns (3,gap = "large")
    kpi1.markdown (f'<div class="metric-card"><div class="metric-title">Overall Unemployment Rate</div><div class="metric-value">{df_selected ["Unemployment_Rate"].mean ():.2f} %</div></div>',unsafe_allow_html = True)
    kpi2.markdown (f'<div class="metric-card"><div class="metric-title">Rural Mean Rate</div><div class="metric-value">{df_selected [df_selected ["Area"] == "Rural"]["Unemployment_Rate"].mean ():.2f} %</div></div>',unsafe_allow_html = True)
    kpi3.markdown (f'<div class="metric-card"><div class="metric-title">Urban Mean Rate</div><div class="metric-value">{df_selected [df_selected ["Area"] == "Urban"]["Unemployment_Rate"].mean ():.2f} %</div></div>',unsafe_allow_html = True)

    st.write ("")
    st.write ("")

    c1,c2 = st.columns ([1.1,0.9],gap = "large")
    with c1:
        st.subheader ("Rural vs Urban Unemployment Over Time")
        fig_sector = px.line (
            df_selected,
            x = "Date",
            y = "Unemployment_Rate",
            color = "Area",
            line_group = "State",
            hover_name = "State",
            template = "plotly_dark",
            height = 410,
        )
        fig_sector.update_layout (margin = dict(l = 15,r = 15,t = 35,b = 15))
        st.plotly_chart (fig_sector,width = "stretch")

    with c2:
        st.subheader ("Top 10 Lockdown Impacted States")
        lockdown_df = df_selected [df_selected ["Is_Lockdown"]]
        top_states = (
            lockdown_df.groupby ("State")["Unemployment_Rate"]
            .mean ()
            .nlargest (10)
            .reset_index ()
        )
        fig_bar = px.bar (
            top_states,
            x = "Unemployment_Rate",
            y = "State",
            orientation = "h",
            color = "Unemployment_Rate",
            color_continuous_scale = "Reds",
            template = "plotly_dark",
            height = 410,
        )
        fig_bar.update_layout (
            yaxis = {"categoryorder": "total ascending"},
            margin = dict(l = 15,r = 15,t = 35,b = 15),
            showlegend = False,
        )
        st.plotly_chart (fig_bar,width = "stretch")