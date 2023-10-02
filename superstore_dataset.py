import pandas as pd
from faker import Faker
fake = Faker()
Faker.seed(47)

data = pd.read_excel('/Users/alex/Downloads/superstoredataset.xlsx')

data.columns
data.shape

customer_names = data['customer_name'].unique().tolist()
customer_id = [fake.ean(length=13) for x in range(len(customer_names))]
customer_di = dict(zip(customer_names, customer_id))
data['customer_id'] = data['customer_name'].map(customer_di)

customers = data[['customer_id', 'customer_name', 'state', 'country', 'market', 'segment']].drop_duplicates(subset='customer_id')

orders = data[['order_id', 'order_date', 'ship_date', 'ship_mode', 'customer_id', 'region', 'product_id', 'quantity', 'shipping_cost', 'order_priority']]

products = data[['product_id', 'category', 'sub_category', 'product_name', 'product_style', 'unit_price']].drop_duplicates(subset='product_id')

sales = data[['product_id', 'sales', 'expenses', 'year']].rename(columns={'sales':'revenue'})
sales['revenue'] = sales['revenue'].astype(float)
sales['expenses'] = sales['expenses']*0.74
sales

with pd.ExcelWriter('/Users/alex/Downloads/superstoredatapull.xlsx', engine='openpyxl') as writer:
    customers.to_excel(writer, sheet_name='customers')
    orders.to_excel(writer, sheet_name='orders')
    products.to_excel(writer, sheet_name='products')
    sales.to_excel(writer, sheet_name='sales')
