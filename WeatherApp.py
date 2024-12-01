import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from datetime import datetime, timedelta
import random

def generate_mock_weather_data(city):
    base_date = datetime.now()
    dates = [base_date + timedelta(hours=i * 3) for i in range(8)]

    city_base_temps = {
        "London": 10,
        "India": 15,
        "Canada": 20,
        "Paris": 12,
        "Germany": 18,
    }

    data = []
    base_temp = city_base_temps.get(city, 15)

    for date in dates:
        temp_variation = random.uniform(-3, 3)
        data.append({
            "datetime": date,
            "temperature": round(base_temp + temp_variation, 1),
            "feels_like": round(base_temp + temp_variation - 1, 1),
            "humidity": round(random.uniform(50, 80), 1),
            "wind_speed": round(random.uniform(2, 10), 1),
            "description": random.choice(["Partly Cloudy", "Cloudy", "Sunny", "Light Rain", "Overcast", "Clear Sky"]),
        })

    return pd.DataFrame(data)

def create_visualizations(df):
    st.subheader("📊 Temperature Trends")
    fig_temp = px.line(
        df, x="datetime", y="temperature",
        title="Temperature Forecast",
        labels={"temperature": "Temperature (°C)", "datetime": "Date and Time"}
    )
    fig_temp.add_trace(
        go.Scatter(
            x=df["datetime"], y=df["feels_like"],
            mode="lines", name="Feels Like",
            line=dict(dash="dot", color="orange")
        )
    )
    fig_temp.update_layout(hovermode="x unified")
    st.plotly_chart(fig_temp, use_container_width=True)

    st.subheader("🌡 Temperature vs Humidity")
    fig_humidity = px.scatter(
        df, x="temperature", y="humidity",
        color="description",
        title="Correlation Between Temperature and Humidity",
        labels={"temperature": "Temperature (°C)", "humidity": "Humidity (%)"}
    )
    st.plotly_chart(fig_humidity, use_container_width=True)

    st.subheader("💨 Wind Speed Analysis")
    fig_wind = px.bar(
        df, x="datetime", y="wind_speed",
        color="description",
        title="Wind Speed Over Time",
        labels={"wind_speed": "Wind Speed (m/s)", "datetime": "Date and Time"}
    )
    st.plotly_chart(fig_wind, use_container_width=True)

def display_hourly_breakdown(df):
    st.subheader("⏱ Hourly Weather Breakdown")
    cols = st.columns(len(df))
    for i, row in df.iterrows():
        with cols[i]:
            st.markdown(
                f"""
                <div style="border: 1px solid #ccc; padding: 10px; border-radius: 5px; text-align: center; background-color: #f9f9f9;">
                    <h4>{row['datetime'].strftime('%I %p')}</h4>
                    <p><b>Temp:</b> {row['temperature']}°C</p>
                    <p><b>Feels Like:</b> {row['feels_like']}°C</p>
                    <p><b>Humidity:</b> {row['humidity']}%</p>
                    <p><b>Wind:</b> {row['wind_speed']} m/s</p>
                    <p><b>Condition:</b> {row['description']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

def main():
    st.set_page_config(
        page_title="Enhanced Weather Dashboard",
        page_icon="🌦",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown("<h1 style='text-align: center;'>🌍 Weather Dashboard</h1>", unsafe_allow_html=True)

    st.sidebar.title("Weather Preferences")
    
    uv_sensitivity = st.sidebar.select_slider(
        "UV Protection Recommendation", 
        options=["Low", "Medium", "High"], 
        value="Medium"
    )
    st.sidebar.markdown("---")
    
    if uv_sensitivity == "Low":
        st.sidebar.info("✅ Minimal sun protection needed. SPF 15 is sufficient.")
    elif uv_sensitivity == "Medium":
        st.sidebar.info("⚠️ Use SPF 30+. Seek shade during peak hours.")
    else:
        st.sidebar.info("🛡️ High UV sensitivity. Use SPF 50+, wear protective clothing.")

    st.sidebar.markdown("---")
    st.sidebar.info("This app is showcasing advanced weather visualizations using mock data.")

    cities = ["London", "India", "Canada", "Paris", "Germany"]
    selected_city = st.selectbox("Select City for Weather Simulation", cities)

    if st.button("Generate Weather Data"):
        try:
            df = generate_mock_weather_data(selected_city)

            st.subheader(f"🌟 Key Insights for {selected_city}")
            col1, col2, col3 = st.columns(3)
            col1.metric("Avg Temperature", f"{df['temperature'].mean():.1f}°C")
            col2.metric("Max Wind Speed", f"{df['wind_speed'].max():.1f} m/s")
            col3.metric("Dominant Condition", df["description"].mode()[0])

            create_visualizations(df)

            display_hourly_breakdown(df)

            with st.expander("📋 View Full Weather Data Table"):
                st.dataframe(df)

        except Exception as e:
            st.error("An error occurred while generating weather data.")
            st.exception(e)

if __name__ == "__main__":
    main()
