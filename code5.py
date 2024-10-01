import pandas as pd
import matplotlib.pyplot as plt

# Load datasets
customers = pd.read_csv('D:/Penyimpanan Uama/BANGKIT 2024/code/E-Commerce Public Dataset/customers_dataset.csv')
orders = pd.read_csv('D:/Penyimpanan Uama/BANGKIT 2024/code/E-Commerce Public Dataset/orders_dataset.csv')
order_items = pd.read_csv('D:/Penyimpanan Uama/BANGKIT 2024/code/E-Commerce Public Dataset/order_items_dataset.csv')
products = pd.read_csv('D:/Penyimpanan Uama/BANGKIT 2024/code/E-Commerce Public Dataset/products_dataset.csv')
product_categories = pd.read_csv('D:/Penyimpanan Uama/BANGKIT 2024/code/E-Commerce Public Dataset/product_category_name_translation.csv')

# Data Cleaning and Preparation
# Merge product category names into the products dataframe
products = products.merge(product_categories, on='product_category_name', how='left')

# Merge relevant dataframes for analysis
data = orders.merge(order_items, on='order_id').merge(products, on='product_id').merge(customers, on='customer_id')

# Convert dates to datetime format
data['order_purchase_timestamp'] = pd.to_datetime(data['order_purchase_timestamp'])
data['order_approved_at'] = pd.to_datetime(data['order_approved_at'])

# Drop rows with missing values
data.dropna(subset=['order_approved_at', 'product_category_name_english'], inplace=True)

# Creating a new column for analysis by month and year
data['month_year'] = data['order_purchase_timestamp'].dt.to_period('M')

# 1. Sales Trend Analysis
sales_trends = data.groupby(['month_year', 'product_category_name_english'])['price'].sum().unstack().fillna(0)

# Plotting the sales trends by category
plt.figure(figsize=(14, 7))
sales_trends.plot(kind='bar', stacked=True)
plt.title('Monthly Sales Trends by Product Category')
plt.xlabel('Month-Year')
plt.ylabel('Total Sales in USD')
plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 2. Customer Demographic Segmentation
demographics = data.groupby(['customer_state'])['price'].sum().sort_values(ascending=False)

# Pie chart for customer demographic segmentation
plt.figure(figsize=(10, 8))
demographics.plot(kind='pie', autopct='%1.1f%%')
plt.title('Customer Sales Distribution by State')
plt.ylabel('')  # Remove the y-label as it's unnecessary for pie charts
plt.tight_layout()
plt.show()
