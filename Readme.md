# 🚇 NYC Subway Ridership Analysis Dashboard

An interactive web dashboard built with Streamlit to analyze and visualize hourly ridership data from the New York City MTA subway system.

This application provides a deep dive into transit patterns from December 2024, allowing users to explore trends, station performance, and rider behavior through a dynamic and user-friendly interface.

## 🚀 Live Demo

**This dashboard is deployed on Streamlit Community Cloud.**

[Streamlit Dashboard](https://nyc-ridership-dashboard.streamlit.app/)

**Also I made this Dashboard on Power bi too**

![Alt Text](https://github.com/RobinMillford/NYC-Ridership-Dashboard/blob/main/Page%201.png)

![Alt Text](https://github.com/RobinMillford/NYC-Ridership-Dashboard/blob/main/Page%202.png)

**Clone this repo to get the pbix file or power bi file**
## ✨ Features

This dashboard offers a multi-faceted view of the MTA dataset, including:

- **📈 Hourly Ridership Trends:** An interactive time-series chart showing ridership over time, filterable by borough.
- **📊 High-Level Overview:** At-a-glance KPIs for Total Ridership, Busiest Day, Busiest Station, and a proportional breakdown of ridership by borough.
- **🚉 Station-Level Analysis:**
  - Bar charts for the Top 10 busiest stations and Top 10 transfer hubs.
  - An interactive map displaying station locations with ridership volume represented by bubble size and color.
- **💳 Rider Behavior Analysis:**
  - An area chart tracking the adoption of OMNY vs. MetroCard over time.
  - A heatmap visualizing the typical weekly ridership patterns by hour and day.
- **🔬 Comparative & Hierarchical Insights:**
  - A scatter plot analyzing the relationship between station ridership and transfers.
  - A sunburst chart and a treemap breaking down ridership by fare class and station hierarchy.

## 💾 Data Source

The data used in this project is the **MTA Turnstile Data**, which contains hourly records of entries and exits from turnstiles across the NYC subway system. The dataset used for this dashboard covers the period from December 2024.

[Source](https://data.ny.gov/)

## 🛠️ Technology Stack

- **Language:** Python
- **Dashboarding:** Streamlit
- **Data Manipulation:** Pandas, NumPy
- **Visualization:** Plotly Express

## ⚙️ Setup and Local Installation

To run this dashboard on your local machine, please follow these steps:

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
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
    _(Ensure you have a `requirements.txt` file in your repository. If not, create one by running `pip freeze > requirements.txt` in your activated virtual environment after installing the necessary packages.)_

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit app:**

    ```bash
    streamlit run app.py
    ```

The application should now be running and accessible in your web browser.
