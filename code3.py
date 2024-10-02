import os
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import folium_static

# Streamlit title
st.title("Air Quality Geospatial Analysis")

st.markdown("""
## Auto-load Datasets from Local Folder
This app automatically loads datasets from a specified folder on your local machine.
""")

# Specify the folder path where the datasets are located
folder_path = 'D:\\Penyimpanan Uama\\BANGKIT 2024\\code'  # Replace with your actual folder path

# Initialize an empty list to hold the dataframes
dataframes = []

# List all files in the folder and read CSV files
for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        file_path = os.path.join(folder_path, filename)
        st.write(f"Loading {filename}...")
        df = pd.read_csv(file_path)
        df.fillna(df.median(), inplace=True)  # Impute missing values
        dataframes.append(df)

if dataframes:
    # Combine all dataframes into a single dataframe
    combined_data = pd.concat(dataframes, ignore_index=True)

    # Calculate the average PM2.5 levels for each station
    average_pm25 = combined_data.groupby('station')['PM2.5'].mean().reset_index()

    # Coordinates for the monitoring stations (replace with actual data if available)
    station_coords = {
        'Aotizhongxin': (39.9825, 116.3976),
        'Changping': (40.2171, 116.2334),
        'Dingling': (40.2924, 116.2202),
        'Dongsi': (39.9292, 116.4179),
        'Guanyuan': (39.9290, 116.3387),
        'Gucheng': (39.9144, 116.1842),
        'Huairou': (40.3281, 116.6333),
        'Nongzhanguan': (39.9376, 116.4617)
    }

    # Create a Folium map centered on Beijing
    map_beijing = folium.Map(location=[39.9042, 116.4074], zoom_start=10)

    # Add markers to the map for each station
    for index, row in average_pm25.iterrows():
        if row['station'] in station_coords:
            folium.CircleMarker(
                location=station_coords[row['station']],
                radius=10,
                popup=f"{row['station']}: {row['PM2.5']:.2f} µg/m³",
                color='red',
                fill=True,
                fill_color='red'
            ).add_to(map_beijing)

    # Display the map using Streamlit
    folium_static(map_beijing)
else:
    st.write("No CSV files found in the specified folder.")






