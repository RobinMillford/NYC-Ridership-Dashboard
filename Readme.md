# 🚇 NYC Subway Ridership Analysis Dashboard

An interactive web dashboard built with Streamlit to analyze and visualize **live, hourly ridership data** from the New York City MTA subway system.

This application connects directly to the NYC Open Data portal, allowing users to **dynamically select date ranges between 2020 and 2024**. It provides a deep dive into transit patterns, station performance, and rider behavior through a comprehensive and user-friendly interface.

## 🚀 Live Demo

**This dashboard is deployed on Streamlit Community Cloud.**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://nyc-ridership-dashboard.streamlit.app/)

---

## 📊 Power BI Version

A version of this dashboard was also created in **Microsoft Power BI** to demonstrate the same analysis using a different business intelligence tool. You can find the `.pbix` file in this repository.

![Power BI Dashboard - Page 1](https://raw.githubusercontent.com/RobinMillford/NYC-Ridership-Dashboard/main/Page%201.png)
![Power BI Dashboard - Page 2](https://raw.githubusercontent.com/RobinMillford/NYC-Ridership-Dashboard/main/Page%202.png)

---

## ✨ Features

This dashboard offers a multi-faceted and fully interactive view of the MTA dataset:

- **📅 Dynamic Date Range Selector:** Users can select any start and end date to analyze specific periods, from a single day to multiple years.
- **🌐 Live Data Connection:** Fetches up-to-date data directly from the official Socrata API, ensuring the analysis is always current.
- **boroughs:** All charts and metrics dynamically update based on the selected borough from the sidebar filter.
- 📈 **High-Level Overview:**
  - At-a-glance KPIs: Total Ridership, Busiest Day, Busiest Station, Total Transfers.
  - A donut chart showing the proportion of ridership across boroughs.
  - A box plot visualizing the distribution of hourly ridership values.
- 🚉 **Station-Level Analysis:**
  - Bar charts for the Top 10 busiest stations and Top 10 transfer hubs.
  - An interactive map displaying station locations with ridership volume represented by bubble size and color.
- 💳 **Rider Behavior Analysis:**
  - An area chart tracking the adoption of OMNY vs. MetroCard over time.
  - A heatmap visualizing the typical weekly ridership patterns by hour and day.
- 🔬 **Comparative & Hierarchical Insights:**
  - A scatter plot analyzing the relationship between station ridership and transfers.
  - A sunburst chart and a treemap breaking down ridership by fare class and station hierarchy.

---

## 💾 Data Source

The data is fetched live from the **MTA Subway Hourly Ridership** dataset on the [NYC Open Data portal](https://data.ny.gov/) via the Socrata API. The dataset contains hourly records from turnstiles across the NYC subway system for the period of 2020-2024.

---

## 🛠️ Technology Stack

- **Language:** Python
- **Web Framework / Dashboarding:** Streamlit, Power BI
- **Data Manipulation:** Pandas, NumPy
- **Visualization:** Plotly Express
- **API Client:** Sodapy

---

## ⚙️ Setup and Local Installation

To run this dashboard on your local machine, please follow these steps:

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/RobinMillford/NYC-Ridership-Dashboard.git
    cd NYC-Ridership-Dashboard
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your API Token:**
    This app requires a free Socrata App Token to access the data.

    - Create a new folder in your project directory named `.streamlit`.
    - Inside the `.streamlit` folder, create a new file named `secrets.toml`.
    - Add your token to this file as shown below:
      ```toml
      [socrata]
      app_token = "YOUR_APP_TOKEN_HERE"
      ```

5.  **Run the Streamlit app:**
    `bash
    streamlit run app.py
    `
    The application should now be running and accessible in your web browser.
