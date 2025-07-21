import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- Page Configuration ---
st.set_page_config(
    page_title="NYC Ridership Dashboard",
    page_icon="🚇",
    layout="wide"
)

# --- Data Loading and Processing ---
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    # FIX 1: Add the date format for faster parsing
    df['transit_timestamp'] = pd.to_datetime(df['transit_timestamp'], format='%m/%d/%Y %I:%M:%S %p')
    return df

# --- Data Aggregation for Summaries ---
@st.cache_data
def create_station_summary(df):
    station_summary = df.groupby(['station_complex', 'borough']).agg(
        total_ridership=('ridership', 'sum'),
        total_transfers=('transfers', 'sum'),
        latitude=('latitude', 'mean'),
        longitude=('longitude', 'mean')
    ).reset_index()
    return station_summary

# Load the data
try:
    df = load_data('MTA_Subway_Hourly_Ridership__2020-2024_20250721.csv')
    station_summary = create_station_summary(df)
except FileNotFoundError:
    st.error("Error: The specified data file was not found.")
    st.info("Please make sure the CSV file is in the same directory as your Streamlit app.")
    st.stop()

# --- Sidebar ---
st.sidebar.header("Filter Options")
borough_list = ['Overall'] + df['borough'].unique().tolist()
selected_borough = st.sidebar.selectbox("Select a Borough:", borough_list)

# --- Filter data based on selection ---
if selected_borough == 'Overall':
    main_df = df
    station_df = station_summary
    title_suffix = "in NYC"
    zoom_level = 9.5
else:
    main_df = df[df['borough'] == selected_borough]
    station_df = station_summary[station_summary['borough'] == selected_borough]
    title_suffix = f"in {selected_borough}"
    zoom_level = 11

# --- Main Panel ---
st.title("🚇 NYC Subway Ridership Dashboard")
st.markdown("""
- **This dashboard provides an interactive exploration of New York City's subway system, using hourly MTA turnstile data from 2020 to 2024.** 
- **Analyze ridership trends over time, compare station performance, and uncover insights into rider behavior.**

**Use the Filter Options in the sidebar to begin your analysis.**
""")

# --- Section 1: Time Series Chart ---
st.header("Hourly Ridership Trends")
line_data_to_plot = main_df.groupby('transit_timestamp')['ridership'].sum().reset_index()
fig_line = px.line(
    line_data_to_plot, x='transit_timestamp', y='ridership',
    title=f"Hourly Subway Ridership {title_suffix}", template="plotly_white",
    labels={'ridership': 'Total Ridership', 'transit_timestamp': 'Date & Time'},
    color_discrete_sequence=['#636EFA']
)
fig_line.update_layout(hovermode="x unified")
fig_line.update_xaxes(rangeslider_visible=True)
st.plotly_chart(fig_line, use_container_width=True)


# --- Section 2: High-Level Overview ---
st.markdown("---")
st.header("High-Level Overview")
col9, col10, col11 = st.columns(3)

with col9:
    st.subheader(f"Ridership by Borough")
    if selected_borough == 'Overall':
        borough_ridership = station_df.groupby('borough')['total_ridership'].sum().reset_index()
        fig_pie = px.pie(
            borough_ridership,
            names='borough',
            values='total_ridership',
            template='plotly_white',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Antique,
            title=f"Ridership Share by Borough"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.subheader(f"Top 5 Station Share {title_suffix}")
        top_stations_in_borough = station_df.nlargest(5, 'total_ridership')
        fig_pie = px.pie(
            top_stations_in_borough,
            names='station_complex',
            values='total_ridership',
            template='plotly_white',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Antique,
            title=f"Top 5 Stations in {selected_borough}"
        )
        st.plotly_chart(fig_pie, use_container_width=True)


with col10:
    st.subheader(f"Hourly Ridership Distribution {title_suffix}")
    fig_box = px.box(
        main_df,
        x='borough',
        y='ridership',
        template='plotly_white',
        title="Ridership Spread by Borough",
        color='borough',
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig_box.update_traces(boxpoints=False)
    st.plotly_chart(fig_box, use_container_width=True)

with col11:
    st.subheader(f"Key Metrics {title_suffix}")
    total_ridership_metric = main_df['ridership'].sum()
    avg_ridership_metric = main_df['ridership'].mean()
    
    st.metric("Total Ridership", f"{total_ridership_metric:,.0f}")
    st.metric("Avg. Ridership / Hour", f"{avg_ridership_metric:,.2f}")
    
    if not line_data_to_plot.empty:
        busiest_day_data = line_data_to_plot.loc[line_data_to_plot['ridership'].idxmax()]
        busiest_day = pd.to_datetime(busiest_day_data['transit_timestamp']).strftime('%b %d, %Y')
        busiest_day_riders = busiest_day_data['ridership']
        st.metric("Busiest Day", busiest_day, f"{busiest_day_riders:,.0f} riders")

    if not station_df.empty:
        busiest_station_data = station_df.loc[station_df['total_ridership'].idxmax()]
        busiest_station_name = busiest_station_data['station_complex']
        busiest_station_riders = busiest_station_data['total_ridership']
        st.metric("Busiest Station", busiest_station_name, f"{busiest_station_riders:,.0f} riders")

        total_transfers_metric = station_df['total_transfers'].sum()
        st.metric("Total Transfers", f"{total_transfers_metric:,.0f}")


# --- Section 3: Station Analysis ---
st.markdown("---")
st.header("Station-Level Analysis")
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Top 10 Busiest Stations {title_suffix}")
    top_10_stations = station_df.nlargest(10, 'total_ridership')
    fig_bar = px.bar(
        top_10_stations.sort_values("total_ridership"),
        x="total_ridership", y="station_complex", orientation='h', template="plotly_white",
        labels={'total_ridership': 'Total Ridership', 'station_complex': 'Station'},
        color_discrete_sequence=['#00CC96']
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.subheader(f"Ridership Volume Map {title_suffix}")
    # FIX 2: Use scatter_map and map_style instead of scatter_mapbox and mapbox_style
    fig_map = px.scatter_map(
        station_df, lat="latitude", lon="longitude", hover_name="station_complex",
        size="total_ridership", color="total_ridership",
        color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=zoom_level
    )
    fig_map.update_layout(map_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig_map, use_container_width=True)

# --- Section 4: Behavior Analysis ---
st.markdown("---")
st.header("Rider Behavior Analysis")
col3, col4 = st.columns(2)

with col3:
    st.subheader(f"Payment Method Trends {title_suffix}")
    payment_trends = main_df.groupby([main_df['transit_timestamp'].dt.date, 'payment_method'])['ridership'].sum().reset_index()
    fig_area = px.area(
        payment_trends, x='transit_timestamp', y='ridership', color='payment_method',
        template='plotly_white', title='Ridership by Payment Method',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig_area, use_container_width=True)

with col4:
    st.subheader(f"Typical Weekly Ridership Pattern {title_suffix}")
    hourly_df_to_plot = main_df.copy()
    hourly_df_to_plot['hour'] = hourly_df_to_plot['transit_timestamp'].dt.hour
    hourly_df_to_plot['day_of_week'] = hourly_df_to_plot['transit_timestamp'].dt.day_name()
    heatmap_data = hourly_df_to_plot.groupby(['day_of_week', 'hour'])['ridership'].mean().reset_index()
    heatmap_pivot = heatmap_data.pivot(index='hour', columns='day_of_week', values='ridership')
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    heatmap_pivot = heatmap_pivot.reindex(columns=day_order)
    fig_heatmap = px.imshow(
        heatmap_pivot, labels=dict(x="Day of Week", y="Hour of Day", color="Avg Ridership"),
        template='plotly_white', title='Average Ridership by Hour and Day',
        color_continuous_scale="Teal"
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

# --- Section 5: Fare and Transfer Insights ---
st.markdown("---")
st.header("Fare and Transfer Insights")
col5, col6 = st.columns(2)

with col5:
    st.subheader(f"Fare Class Breakdown {title_suffix}")
    fare_data = main_df.groupby(['payment_method', 'fare_class_category'])['ridership'].sum().reset_index()
    fig_treemap = px.treemap(
        fare_data,
        path=[px.Constant("All Fares"), 'payment_method', 'fare_class_category'],
        values='ridership', template='plotly_white', title='Ridership Distribution by Fare Type',
        color_continuous_scale=px.colors.sequential.GnBu
    )
    st.plotly_chart(fig_treemap, use_container_width=True)

with col6:
    st.subheader(f"Top 10 Transfer Hubs {title_suffix}")
    top_10_transfers = station_df.nlargest(10, 'total_transfers')
    fig_bar_transfers = px.bar(
        top_10_transfers.sort_values("total_transfers"),
        x="total_transfers", y="station_complex", orientation='h', template="plotly_white",
        labels={'total_transfers': 'Total Transfers', 'station_complex': 'Station'},
        color_discrete_sequence=['#EF553B']
    )
    st.plotly_chart(fig_bar_transfers, use_container_width=True)

# --- Section 6: System-Wide Comparative Analysis ---
st.markdown("---")
st.header("System-Wide Comparative Analysis")
col7, col8 = st.columns(2)

with col7:
    st.subheader("Ridership vs. Transfers Analysis")
    fig_scatter = px.scatter(
        station_df, x="total_ridership", y="total_transfers", color="borough",
        hover_name="station_complex", size="total_ridership", template="plotly_white",
        title="Station Profile: Ridership vs. Transfers",
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with col8:
    st.subheader("Hierarchical Ridership Breakdown")
    fig_sunburst = px.sunburst(
        station_df, path=['borough', 'station_complex'], values='total_ridership',
        template='plotly_white', title='Ridership Proportion by Borough and Station',
        color='total_ridership', color_continuous_scale=px.colors.sequential.Plasma
    )
    st.plotly_chart(fig_sunburst, use_container_width=True)


# --- Expander for Raw Data ---
with st.expander("📋 Show Raw Dataset Sample"):
    st.dataframe(df.head(1000))

st.markdown(
    """
    <hr>
    <div style='text-align: center;'>
        <p style='font-size: 1.2em; font-family: "Arial", sans-serif;'>
            © 2025 All rights reserved by <a href='https://github.com/RobinMillford' target='_blank'><img src='https://img.icons8.com/?size=100&id=LoL4bFzqmAa0&format=png&color=000000' height='30' style='vertical-align: middle;'></a>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)