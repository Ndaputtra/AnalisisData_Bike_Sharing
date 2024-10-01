import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import folium
from streamlit_folium import folium_static
import geopandas as gpd

# Load the Air Quality Dataset
df = pd.read_csv('air_quality.csv')  # Change this with the actual dataset

# Step 1: Data Cleaning
# Handling missing data
df = df.dropna()

# Step 2: RFM Analysis
# We simulate 'Recency', 'Frequency', and 'Monetary' based on air quality readings
df['Date'] = pd.to_datetime(df['Date'])
latest_date = df['Date'].max()

# Recency - number of days since last measurement
df['Recency'] = (latest_date - df['Date']).dt.days

# Frequency - Assume it refers to how frequently air quality measurements are taken
frequency_df = df.groupby('City').size().reset_index(name='Frequency')

# Monetary - We simulate this using some pollutant readings as 'impact costs'
df['Monetary'] = df['PM2.5'] + df['NO2']  # Adjust columns based on the actual dataset

# Visualizing RFM using Bar plots
st.title('RFM Analysis for Air Quality')
fig, ax = plt.subplots(1, 3, figsize=(15, 5))
sns.histplot(df['Recency'], ax=ax[0], kde=True)
ax[0].set_title('Recency Distribution')

sns.histplot(frequency_df['Frequency'], ax=ax[1], kde=True)
ax[1].set_title('Frequency Distribution')

sns.histplot(df['Monetary'], ax=ax[2], kde=True)
ax[2].set_title('Monetary Distribution')

st.pyplot(fig)

# Step 3: Geospatial Analysis
st.title('Geospatial Analysis of Air Quality')

# Use folium for geospatial mapping
m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=6)

# Adding data points to the map
for i, row in df.iterrows():
    folium.CircleMarker(
        location=(row['Latitude'], row['Longitude']),
        radius=5,
        color='red' if row['PM2.5'] > 50 else 'green',
        fill=True,
        fill_color='red' if row['PM2.5'] > 50 else 'green',
        popup=f"PM2.5: {row['PM2.5']} µg/m³"
    ).add_to(m)

# Display the map using Streamlit
folium_static(m)

# Step 4: Clustering without machine learning
# We'll use a simple manual grouping technique based on pollutant levels
def air_quality_category(pm_value):
    if pm_value <= 25:
        return 'Good'
    elif pm_value <= 50:
        return 'Moderate'
    elif pm_value <= 75:
        return 'Unhealthy'
    else:
        return 'Hazardous'

df['Air_Quality_Category'] = df['PM2.5'].apply(air_quality_category)

# Displaying the manual grouping
st.title('Clustering - Manual Grouping of Air Quality')
category_count = df['Air_Quality_Category'].value_counts()
st.bar_chart(category_count)

# Step 5: Streamlit Deployment
st.markdown("""
    ### Streamlit Dashboard
    This dashboard presents an analysis of air quality data using advanced techniques such as RFM analysis, geospatial mapping, and manual clustering of air quality based on PM2.5 levels.
""")

