import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the air quality dataset
df = pd.read_csv('air_quality.csv')  # Adjust filename as needed

# Check for missing values and handle them
df = df.dropna()

# Example 1: Line plot for pollutant variation by hour
plt.figure(figsize=(10,6))
sns.lineplot(data=df, x='hour', y='PM2.5', label='PM2.5')
sns.lineplot(data=df, x='hour', y='NO2', label='NO2')
plt.title('Pollutant Levels Throughout the Day')
plt.xlabel('Hour of Day')
plt.ylabel('Pollutant Concentration (µg/m³)')
plt.legend()
plt.show()

# Example 2: Scatter plot for correlation between temperature and PM2.5
plt.figure(figsize=(8,6))
sns.scatterplot(data=df, x='temperature', y='PM2.5', hue='humidity')
plt.title('Temperature vs PM2.5 with Humidity')
plt.xlabel('Temperature (°C)')
plt.ylabel('PM2.5 Concentration (µg/m³)')
plt.show()

# Example 3: Heatmap for correlation between variables
correlation_matrix = df[['PM2.5', 'NO2', 'temperature', 'humidity']].corr()
plt.figure(figsize=(8,6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Between Pollutants and Weather Conditions')
plt.show()
