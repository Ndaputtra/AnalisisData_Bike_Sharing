import pandas as pd
import matplotlib.pyplot as plt

# Load datasets
customers = pd.read_csv('/mnt/data/customers_dataset.csv')
orders = pd.read_csv('/mnt/data/orders_dataset.csv')
order_items = pd.read_csv('/mnt/data/order_items_dataset.csv')
products = pd.read_csv('/mnt/data/products_dataset.csv')

# Merging datasets for Sales Trend Analysis
merged_sales_data = orders.merge(order_items, on='order_id').merge(products, on='product_id')
merged_sales_data['order_purchase_timestamp'] = pd.to_datetime(merged_sales_data['order_purchase_timestamp'])
merged_sales_data['month_year'] = merged_sales_data['order_purchase_timestamp'].dt.to_period('M')

# Aggregating sales data by month and category
sales_trends = merged_sales_data.groupby(['month_year', 'product_category_name']).agg({'price': 'sum'}).reset_index()

# Pivot the data for visualization
sales_trends_pivot = sales_trends.pivot(index='month_year', columns='product_category_name', values='price').fillna(0)

# Plotting the sales trends
plt.figure(figsize=(14, 7))
for category in sales_trends_pivot.columns:
    plt.plot(sales_trends_pivot.index.astype(str), sales_trends_pivot[category], label=category)
plt.title('Monthly Sales Trends by Product Category')
plt.xlabel('Month-Year')
plt.ylabel('Total Sales in USD')
plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Merging datasets for Customer Demographic Segmentation
demographic_data = orders.merge(customers, on='customer_id')

# Aggregating sales data by customer state
customer_sales_by_state = demographic_data.groupby('customer_state').size().reset_index(name='number_of_orders')

# Pie chart for state distribution
plt.figure(figsize=(10, 8))
plt.pie(customer_sales_by_state['number_of_orders'], labels=customer_sales_by_state['customer_state'], autopct='%1.1f%%')
plt.title('Distribution of Orders by Customer State')
plt.axis('equal')
plt.show()

# Bar chart to compare sales volume
sales_volume_by_state = orders.merge(order_items, on='order_id').merge(customers, on='customer_id')
sales_volume_by_state = sales_volume_by_state.groupby('customer_state').agg({'price': 'sum'}).reset_index()

plt.figure(figsize=(12, 6))
plt.bar(sales_volume_by_state['customer_state'], sales_volume_by_state['price'], color='blue')
plt.title('Sales Volume by Customer State')
plt.xlabel('State')
plt.ylabel('Total Sales in USD')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()
