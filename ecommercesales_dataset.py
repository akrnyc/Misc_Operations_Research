import pandas as pd
import random
import barnum
from faker import Faker
fake = Faker()

##generate product df
data1 = pd.read_csv('/Users/alex/Downloads/ecommerce_sales_dataset/pl_march_2021.csv', 
            usecols=['Sku', 'Style Id', 'Catalog', 'Category']
            ).rename(dict(zip(['Sku', 'Style Id', 'Catalog', 'Category'], 
                              ['sku', 'style_id', 'catalog', 'category'])), 
                              axis=1) #union base

data2 = pd.read_csv('/Users/alex/Downloads/ecommerce_sales_dataset/may_2022.csv', 
            usecols=['Sku', 'Style Id', 'Catalog', 'Category']
            ).rename(dict(zip(['Sku', 'Style Id', 'Catalog', 'Category'], 
                              ['sku', 'style_id', 'catalog', 'category'])), 
                              axis=1) #union base

data3 = pd.read_csv('/Users/alex/Downloads/ecommerce_sales_dataset/sales_report.csv',
            usecols=['SKU Code', 'Design No.', 'Category',]
            ).rename(dict(zip(['SKU Code', 'Design No.', 'Category',], 
                              ['sku', 'style_id', 'category',])), 
                              axis=1).dropna()  #union base

products = pd.concat([data1, data2, data3], 
          axis=0, 
          ignore_index=True).drop_duplicates(subset='sku') #base product df

catalogue = ['Moments', 'Summer', 'Breezy', 'Gemstones', 'Festival']
products['catalog'] = pd.Series(random.choices(catalogue, 
                                               weights=[0.20, 0.40, 0.10, 0.10, 0.20], 
                                               k=len(products)), 
                                               index=products.index)

dicat = {
    'KURTA': 'jeans',
    'KURTA SET': 'suit',
    'SET': 'matching_set',
    'TOP': 'top',
    'Kurta': 'skirt',
    'DRESS': 'dress',
    'Kurta Set': 'shorts',
    'BLOUSE': 'blouse',
    'NIGHT WEAR': 'lingerie',
    'TUNIC': 'loungewear',
    'SAREE': 'jackets',
    'AN : LEGGINGS': 'leggings',
    'PALAZZO': 'palazzo',
    'PANT': 'pants',
    'Nill': 'sunglasses',
    'Tops': 'knit_tops',
    'CROP TOP': 'cropped_tops',
    'SHARARA': 'coats',
    'LEHENGA CHOLI': 'socks',
    'Gown': 'gown',
    'KURTI': 'activewear',
    'SKIRT': 'leather_goods',
    'BOTTOM': 'trousers',
    'CARDIGAN': 'cardigans',
    'JUMPSUIT': 'jumpsuit',
    'CROP TOP WITH PLAZZO': 'cropped_set'
}
products['category'] = products['category'].map(dicat)

products['msrp'] = [round(random.normalvariate(120, 37), 1) for i in range(products.shape[0])]
products['amazon_price'] = [round(random.normalvariate(90, 37), 1) for i in range(products.shape[0])]

#generate order-sales df
sales = pd.read_csv('/Users/alex/Downloads/ecommerce_sales_dataset/amazon_sale_report.csv',
                           usecols=['Order ID', 'Date', 'Status', 'Fulfilment', 'Sales Channel ',
                            'ship-service-level', 'SKU', 'Courier Status', 'Qty', 'B2B', 'fulfilled-by']).rename(
                                dict(
                                    zip(['Order ID', 'Date', 'Status', 'Fulfilment', 'Sales Channel ',
                                    'ship-service-level', 'SKU', 'Courier Status', 'Qty', 'B2B', 'fulfilled-by'],
                                    ['order_id', 'order_date', 'status', 'fulfilment', 'sales_channel', 'service_level',
                                    'sku', 'courier_status', 'quantity', 'b2b', 'fulfilled_by'])), axis=1)

# sales[sales['SKU'].isin(products.sku.values.tolist())] #validation
sales['sales_channel'] = sales['sales_channel'].map({'Amazon.in': 'Amazon', 'Non-Amazon': 'Other'})
sales['order_date'] = pd.to_datetime(sales.order_date)

#generate customers df
addresses = [barnum.create_city_state_zip() for x in range(2000)]

customers_us = pd.DataFrame({'id': random.sample(range(1000, 8000), 2000),
                             'first_name': [fake.first_name() for x in range(2000)],
                             'last_name': [fake.last_name() for x in range(2000)],
                             'street': [fake.address().split('\n')[0] for x in range(2000)],
                             'city': [x[1] for x in addresses],
                             'state': [x[2] for x in addresses],
                             'zipcode': [int(x[0]) for x in addresses],
                             'country': 'US'
                             })

customers_int = pd.DataFrame({'id': random.sample(range(8001, 9999), 1000),
                             'first_name': [fake.first_name() for x in range(1000)],
                             'last_name': [fake.last_name() for x in range(1000)],
                             'street': [fake.street_address().split('\n')[0] for x in range(1000)],
                             'city': [fake.city() for x in range(1000)],
                             'state': [fake.city() for x in range(1000)],
                             'zipcode': [fake.postcode() for x in range(1000)],
                             'country': [fake.country_code() for x in range(1000) if x != 'US']
                             })

customers = pd.concat([customers_us, customers_int],
                      axis=0,
                      ignore_index=True)

sales['customer_id'] = [random.choice(customers.id.unique().tolist()) for x in range(sales.shape[0])]

#generate marketing df
# catalogue, campaign, utm_source, utm_medium, impressions, spend
marketing = products[['catalog', 'style_id']].drop_duplicates(subset=['catalog', 'style_id']).copy(deep=True)
campaigns = ['new_member', 'lead', 'springbreak', 'resort']
marketing['campaign'] = pd.Series(random.choices(campaigns, 
                                                weights=[0.30, 0.40, 0.20, 0.10], 
                                                k=len(marketing)), 
                                                index=marketing.index)
utm_sources = ['facebook', 'amazon', 'instagram', 'billboard', 'subway', 'referral']
marketing['utm_source'] = pd.Series(random.choices(utm_sources, 
                                                weights=[0.10, 0.5, 0.20, 0.080, 0.020, 0.10], 
                                                k=len(marketing)), 
                                                index=marketing.index)
diutm={
    'facebook': 'digital',
    'amazon': 'digital',
    'instagram': 'digital',
    'billboard': 'print',
    'subway': 'print',
    'referral': 'human'
}
marketing['utm_medium'] = marketing['utm_source'].map(diutm)
dispend = {
    'digital': 0.02,
    'print': 0.1,
    'human': 0.00
}
marketing['unit_spend'] =  marketing['utm_medium'].map(dispend)
marketing['impressions'] = [int(round(random.normalvariate(100, 37), 0)) for x in range(marketing.shape[0])]

with pd.ExcelWriter('/Users/alex/Downloads/ecommercesales.xlsx', engine='openpyxl') as writer:
    customers.to_excel(writer, sheet_name='customers')
    marketing.to_excel(writer, sheet_name='marketing')
    products.to_excel(writer, sheet_name='products')
    sales.to_excel(writer, sheet_name='sales')

